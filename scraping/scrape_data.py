import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_paper_info(paper_url):
    '''
    Function to scrape paper information from paper url

    Input:
    > paper_url - url of the paper 

    Output:
    > a tuple consisting of the scraped information if paper is found
    > -1 if the paper is not found
    '''

    print(paper_url)

    page = requests.get(paper_url)

    if page.status_code == 404:
        return -1

    soup = BeautifulSoup(page.content, 'html.parser')
    title_info = soup.find('div', id = 'gsc_vcd_title')

    original_url = None
    description = None
    title = None

    try:
        paper_original_url = title_info['href']
    except:
        paper_original_url = None

    try:
        description = soup.find('div', class_ = 'gsh_csp').text
    except:
        description = None

    return (title, paper_original_url, description)


def extract_prof_info(scholar_id):
    '''
    Function to scrape professor information from Google Scholar url

    Input:
    > scholar_id - scholar id of a professor as str

    Output:
    > a tuple consisting of the scraped information if page is found
    > -1 if the page is not found
    '''
    # example url = 'https://scholar.google.com/citations?user=-mM5PJAAAAAJ'
    url_base = 'https://scholar.google.com/citations?user='
    url = url_base + scholar_id
    page = requests.get(url)

    # if scholar page does not exist
    if page.status_code == 404:
        return -1

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
    cit_list = [cit.text for cit in soup.find_all('span', class_ = 'gsc_g_al')]
    image_url = soup.find("img", {"id": "gsc_prf_pup-img"})['src']
    if image_url == '/citations/images/avatar_scholar_128.png':
        image_url = 'https://scholar.google.co.in/citations/images/avatar_scholar_128.png'
    papers_url_list = ['https://scholar.google.co.in' + paper['data-href'] for paper in soup.find_all('a', class_ = 'gsc_a_at')]
    papers_title_list = [paper.contents for paper in soup.find_all('a', class_ = 'gsc_a_at')]

    return (name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)

df = pd.read_csv('csrankings-0.csv')

professor_info = dict()
papers_info = dict()

for i in range(1):

    scholar_id = df.iloc[i]['scholarid']

    if extract_prof_info(scholar_id) == -1:
        continue

    name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list = extract_prof_info(scholar_id)
    professor_info[scholar_id] = (name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)

    print(professor_info[scholar_id])

    for paper_url in papers_url_list:

        title, paper_original_url, description = extract_paper_info(paper_url)

        print(title, paper_original_url, description)

        if title in papers_info:
            papers_info[title][2].append(scholar_id)
            print("Found paper")
        else:
            papers_info[title] = (paper_original_url, description, [scholar_id])


# print(professor_info)
# print(papers_info)
