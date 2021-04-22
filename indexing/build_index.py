import csv
import json
import pandas as pd
import sys
import re
from tqdm import tqdm 
sys.path.append('../helper_functions/')
from common_functions import get_id, get_tokenized_words,check_for_nan

prof_topic_and_paper_index = dict()
prof_name_and_affiliation_index = dict()

def build_index_helper(prof_id, string1, string2, remove_stop_words_and_perform_stemming, index):    
    string_for_index_building = string1+" "+string2
    words = get_tokenized_words(string_for_index_building,remove_stop_words_and_perform_stemming)        
    for position_index, key in zip(range(len(words)), words):
        if key in index:            
            index[key].append((prof_id, position_index))
        else:
            index[key] = [(prof_id, position_index)]    

def build_index(prof_id, name, affiliation, topics_list, papers_title_list):      
    # Name and Affiliation Index
    build_index_helper(prof_id, name, affiliation, False, prof_name_and_affiliation_index)

    # Topics and Paper Title Index
    topics_string = " ".join(topics_list)
    papers_string = " ".join(papers_title_list)
    build_index_helper(prof_id, topics_string, papers_string, True, prof_topic_and_paper_index)  

def make_list(initial_string):
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def make_list_citations(initial_string):
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []

file_count = 10

for file_index in range(file_count):    

    try:
        input_file = pd.read_csv('../data/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8')
    except:
        print("Error in opening input file.")
        sys.exit(0)

    number_of_professors = len(input_file)
    
    for prof_index in tqdm(range(number_of_professors)):    

        scholar_id = input_file.iloc[prof_index][0]
        name = check_for_nan(input_file.iloc[prof_index][1])
        image_url = check_for_nan(input_file.iloc[prof_index][2])
        affiliation = check_for_nan(input_file.iloc[prof_index][3])
        email = check_for_nan(input_file.iloc[prof_index][4])
        homepage = check_for_nan(input_file.iloc[prof_index][5])
        topics_list = make_list(input_file.iloc[prof_index][6])
        cit = int(input_file.iloc[prof_index][7])
        h_ind = int(input_file.iloc[prof_index][8])
        i_ind = int(input_file.iloc[prof_index][9])
        cit5 = int(input_file.iloc[prof_index][10])
        h_ind5 = int(input_file.iloc[prof_index][11])
        i_ind5 = int(input_file.iloc[prof_index][12])    
        cit_list = make_list_citations(input_file.iloc[prof_index][13])
        image_url = check_for_nan(input_file.iloc[prof_index][14])
        papers_url_list = make_list(input_file.iloc[prof_index][15])
        papers_title_list = make_list(input_file.iloc[prof_index][16])    
        prof_id = get_id(file_index, prof_index)

        build_index(prof_id, name, affiliation, topics_list, papers_title_list) 

    print("File "+str(file_index)+" Completed.")        

print("Number of keywords in name and affiliation index - "+str(len(prof_name_and_affiliation_index)))
print("Number of keywords in topic and paper index - "+str(len(prof_topic_and_paper_index)))

with open('../data/name_and_affiliation_index_full.json', 'w+',encoding='utf8') as outfile:
    json.dump(prof_name_and_affiliation_index, outfile)

with open('../data/topic_and_paper_index_full.json', 'w+',encoding='utf8') as outfile:
    json.dump(prof_topic_and_paper_index, outfile)