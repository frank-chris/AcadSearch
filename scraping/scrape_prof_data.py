import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import time
import random

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

def extract_prof_info(scholar_id):
    '''
    Function to scrape professor information from Google Scholar url

    Input:
    > scholar_id - scholar id of a professor as str

    Output:
    > a tuple consisting of the scraped information if page is found where first entry of tuple is True/False depending on data is found or not    
    '''
    # example url = 'https://scholar.google.com/citations?user=-mM5PJAAAAAJ&pagesize=100'
    url_base = 'https://scholar.google.com/citations?user='
    url = url_base + scholar_id + '&pagesize=100'
    page = requests.get(url,headers=headers)
    time.sleep(random.randint(1,3))

    # if scholar page does not exist
    if page.status_code == 404:
        return (False, '', '', '', '', '', [], 0, 0, 0, 0, 0, 0, [], '', [], [])    

    try:
        soup = BeautifulSoup(page.content, 'html.parser')  
    except:
        return (False, '', '', '', '', '', [], 0, 0, 0, 0, 0, 0, [], '', [], []) 

    try:           
        right_box = soup.find_all("td", class_ = 'gsc_rsb_std')    
        cit = int(right_box[0].string)
        h_ind = int(right_box[2].string)
        i_ind = int(right_box[4].string)
        cit5 = int(right_box[1].string)
        h_ind5 = int(right_box[3].string)
        i_ind5 = int(right_box[5].string)
    except:
        cit = -1
        h_ind = -1
        i_ind = -1
        cit5 = -1
        h_ind5 = -1
        i_ind5 = -1

    try:    
        inf = soup.find_all("div", class_ = 'gsc_prf_il')
        topics = inf[2].find_all('a')
        topics_list = [topic.text for topic in topics]
        email = (inf[1].text[18:-11])
        affiliation = inf[0].text
    except:
        topics_list = []
        email = ''
        affiliation = ''
    
    try:
        homepage = soup.find_all('a', class_ = 'gsc_prf_ila')[-1]['href']
    except:
        homepage = ''

    try:
        name = soup.find("div", {"id": "gsc_prf_in"}).text
    except:
        name = ''

    try:
        cit_list = [int(cit.text) for cit in soup.find_all('span', class_ = 'gsc_g_al')]
    except:
        cit_list = []
    
    try:
        image_url = soup.find("img", {"id": "gsc_prf_pup-img"})['src']
        if image_url == '/citations/images/avatar_scholar_128.png':
            image_url = 'https://scholar.google.co.in/citations/images/avatar_scholar_128.png'
    except:
        image_url = ''

    try:
        papers_url_list = ['https://scholar.google.co.in' + paper['data-href'] for paper in soup.find_all('a', class_ = 'gsc_a_at')]
        papers_title_list = [paper.contents[0] for paper in soup.find_all('a', class_ = 'gsc_a_at')]
    except:
        papers_url_list = []
        papers_title_list = []
    
    return (True, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)

def write_prof_data_to_csv(professor_file, professor_data_to_write):

    try:
        write = csv.writer(professor_file)
        write.writerow(professor_data_to_write)
    except:
        pass

file_count = 10

for i in range(len(file_count)):
    
    df = pd.read_csv('../data/csrankings-'+str(i)+'.csv')    
    professor_file = open('../data/professor_data-'+str(i)+'.csv', 'a+',newline ='')

    for i in range(0, len(df)):

        scholar_id = df.iloc[i]['scholarid'] 

        if scholar_id == 'NOSCHOLARPAGE':
            continue

        found, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list = extract_prof_info(scholar_id)

        if not found:
            continue

        professor_data_to_write = (scholar_id, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)    
        write_prof_data_to_csv(professor_file, professor_data_to_write)