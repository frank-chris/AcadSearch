import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pprint

pp = pprint.PrettyPrinter(indent=4)
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

def extract_paper_info(paper_url):
    '''
    Function to scrape paper information from paper url

    Input:
    > paper_url - url of the paper 

    Output:
    > a tuple consisting of the scraped information if page is found where first entry of tuple is True/False depending on data is found or not        
    '''    

    page = requests.get(paper_url,headers=headers)    

    if page.status_code == 404:
        return (False)

    soup = BeautifulSoup(page.content, 'html.parser') 


    title = soup.find('div', id = 'gsc_vcd_title').text
    original_url = ""
    description = "" 
    publisher = "" 
    conference = "" 
    publication_date = "" 
    authors = "" 
    journal = "" 
    cit_list = []    


    try:
        original_url = soup.find('a', class_ = 'gcd_vcd_title_link')['href']  
    except:
        original_url = ""    

    for div in soup.find_all('div', class_ = 'gs_scl'):
        try:
            field = div.find('div', class_ = 'gsc_vcd_field').text
            value = ''.join(div.find('div', class_ = 'gsc_vcd_value').text)
            if field == 'Authors':
                authors = value
            elif field == 'Description':
                description = value
            elif field == 'Publication date':
                publication_date = value
            elif field == 'Publisher':
                publisher = value
            elif field == 'Conference':
                conference = value
            elif field == 'Journal':
                journal = value
            elif field == 'Total citations':
                cit_list = [ int(span.text) for span in div.find_all('span', class_  = 'gsc_vcd_g_al') ]            
        except:
            continue    
    
    return (True, title, original_url, description, publisher, conference, publication_date, authors, journal, cit_list)


def extract_prof_info(scholar_id):
    '''
    Function to scrape professor information from Google Scholar url

    Input:
    > scholar_id - scholar id of a professor as str

    Output:
    > a tuple consisting of the scraped information if page is found where first entry of tuple is True/False depending on data is found or not    
    '''
    # example url = 'https://scholar.google.com/citations?user=-mM5PJAAAAAJ'
    url_base = 'https://scholar.google.com/citations?user='
    url = url_base + scholar_id
    page = requests.get(url,headers=headers)

    # if scholar page does not exist
    if page.status_code == 404:
        return (False)    

    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)
    right_box = soup.find_all("td", class_ = 'gsc_rsb_std')    
    cit = int(right_box[0].string)
    h_ind = int(right_box[2].string)
    i_ind = int(right_box[4].string)
    cit5 = int(right_box[1].string)
    h_ind5 = int(right_box[3].string)
    i_ind5 = int(right_box[5].string)
    inf = soup.find_all("div", class_ = 'gsc_prf_il')
    topics = inf[2].find_all('a')
    topics_list = [topic.text for topic in topics]
    email = (inf[1].text[18:-11])
    affiliation = inf[0].text
    homepage = soup.find_all('a', class_ = 'gsc_prf_ila')[-1]['href']
    name = soup.find("div", {"id": "gsc_prf_in"}).text
    cit_list = [int(cit.text) for cit in soup.find_all('span', class_ = 'gsc_g_al')]
    image_url = soup.find("img", {"id": "gsc_prf_pup-img"})['src']
    if image_url == '/citations/images/avatar_scholar_128.png':
        image_url = 'https://scholar.google.co.in/citations/images/avatar_scholar_128.png'
    papers_url_list = ['https://scholar.google.co.in' + paper['data-href'] for paper in soup.find_all('a', class_ = 'gsc_a_at')]
    papers_title_list = [paper.contents[0] for paper in soup.find_all('a', class_ = 'gsc_a_at')]

    return (True, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)

df = pd.read_csv('csrankings-0.csv')

professor_info = dict()
papers_info = dict()

for i in range(1):

    scholar_id = df.iloc[i]['scholarid']    

    found, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list = extract_prof_info(scholar_id)

    if not found:
        continue

    professor_info[scholar_id] = (name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)    

    for j in range(max(len(papers_url_list), 5)):

        paper_url = papers_url_list[j]

        paper_found, title, original_url, description, publisher, conference, publication_date, authors, journal, cit_list = extract_paper_info(paper_url)

        if not paper_found:
            continue
        
        if title in papers_info:
            papers_info[title][9].append(scholar_id)        
        else:
            papers_info[title] = (paper_url, original_url, description, publisher, conference, publication_date, authors, journal, cit_list, [scholar_id])


pp.pprint(professor_info)
pp.pprint(papers_info)
