import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import time
import random



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
        return (False,'', '', '', '', '', '', '', [])

    soup = BeautifulSoup(page.content, 'html.parser') 

    
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
        try:
            original_url = soup.find('a', class_ = 'gsc_vcd_title_link')['href'] 
        except:
            orignial_url = ''

    for div in soup.find_all('div', class_ = 'gs_scl'):
        try:
            field = div.find('div', class_ = 'gsc_vcd_field').text
            value = div.find('div', class_ = 'gsc_vcd_value').text
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
    
    return (True, original_url, description, publisher, conference, publication_date, authors, journal, cit_list)


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
    time.sleep(random.randint(1,3))

    # if scholar page does not exist
    if page.status_code == 404:
        return (False, '', '', '', '', '', [], 0, 0, 0, 0, 0, 0, [], '', [], [])    

    try:
        soup = BeautifulSoup(page.content, 'html.parser')            
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
    except:
        return (False, '', '', '', '', '', [], 0, 0, 0, 0, 0, 0, [], '', [], [])        

    return (True, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)

def write_prof_data_to_csv(professor_file, professor_data_to_write):

    try:
        write = csv.writer(professor_file)
        write.writerow(professor_data_to_write)
    except:
        pass

df = pd.read_csv('csrankings-0.csv')

papers_info = dict()

professor_file = open('professor_data.csv', 'a+',newline ='')

for i in range(0, len(df)):

    scholar_id = df.iloc[i]['scholarid'] 

    if scholar_id == 'NOSCHOLARPAGE':
        continue

    found, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list = extract_prof_info(scholar_id)

    if not found:
        continue

    professor_data_to_write = (scholar_id, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)    
    write_prof_data_to_csv(professor_file, professor_data_to_write)
    

    for j in range(min(len(papers_url_list), 0)):

        paper_url = papers_url_list[j]
        title = papers_title_list[j]
        paper_found, original_url, description, publisher, conference, publication_date, authors, journal, cit_list = extract_paper_info(paper_url)

        if not paper_found:
            continue
        
        if title in papers_info:
            papers_info[title][9].append(scholar_id)        
        else:
            papers_info[title] = (paper_url, original_url, description, publisher, conference, publication_date, authors, journal, cit_list, [scholar_id])