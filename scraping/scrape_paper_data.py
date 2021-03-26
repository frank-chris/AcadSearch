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
    time.sleep(random.randint(1,3)) 

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

papers_info = dict()

# below code won't work now, but the function extract_paper_info works properly

for prof in prof:
    for j in range(len(papers_url_list)):

            paper_url = papers_url_list[j]
            title = papers_title_list[j]
            paper_found, original_url, description, publisher, conference, publication_date, authors, journal, cit_list = extract_paper_info(paper_url)

            if not paper_found:
                continue
            
            if title in papers_info:
                papers_info[title][9].append(scholar_id)        
            else:
                papers_info[title] = (paper_url, original_url, description, publisher, conference, publication_date, authors, journal, cit_list, [scholar_id])