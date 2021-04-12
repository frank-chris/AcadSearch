import csv
import json
import pandas as pd
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import sys
import re
from nltk.corpus import stopwords
sys.path.append('../helper_functions/')
from common_functions import get_id

stop_words = set(stopwords.words('english')) 
full_index = dict()
stemmer = PorterStemmer()

def get_words(sentence_list):      
    words = []
    for sentence in sentence_list:   
        try:                   
            tokenized_words = word_tokenize(re.sub(r'[^A-Za-z0-9]', ' ', sentence.lower()))
            for word in tokenized_words:
                stemmed_word = stemmer.stem(word)            
                if stemmed_word not in stop_words:
                    words.append(stemmed_word)              
        except:
            continue
    return words


def build_index(prof_id, name, affiliation, topics_list, papers_title_list):
    
    search_info_list = [name, affiliation] + topics_list + papers_title_list    
    words = get_words(search_info_list)        
    for position_index, key in zip(range(len(words)), words):
        if key in full_index:            
            full_index[key].append((prof_id, position_index))
        else:
            full_index[key] = [(prof_id, position_index)]

def make_list(initial_string):
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def make_list_citations(initial_string):
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []

file_count = 1

for file_index in range(file_count):    

    try:
        input_file = pd.read_csv('../cleaning/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8')
    except:
        print("Error in opening input file.")
        sys.exit(0)

    number_of_professors = len(input_file)
    
    for prof_index in range(number_of_professors):    

        scholar_id = input_file.iloc[prof_index][0]
        name = input_file.iloc[prof_index][1]
        image_url = input_file.iloc[prof_index][2]
        affiliation = input_file.iloc[prof_index][3]
        email = input_file.iloc[prof_index][4]
        homepage = input_file.iloc[prof_index][5]
        topics_list = make_list(input_file.iloc[prof_index][6])
        cit = int(input_file.iloc[prof_index][7])
        h_ind = int(input_file.iloc[prof_index][8])
        i_ind = int(input_file.iloc[prof_index][9])
        cit5 = int(input_file.iloc[prof_index][10])
        h_ind5 = int(input_file.iloc[prof_index][11])
        i_ind5 = int(input_file.iloc[prof_index][12])    
        cit_list = make_list_citations(input_file.iloc[prof_index][13])
        image_url = input_file.iloc[prof_index][14]
        papers_url_list = make_list(input_file.iloc[prof_index][15])
        papers_title_list = make_list(input_file.iloc[prof_index][16])    
        prof_id = get_id(file_index, prof_index)

        build_index(prof_id, name, affiliation, topics_list, papers_title_list)         

print("Number of keywords - "+str(len(full_index)))

with open('partial_index.json', 'w+',encoding='utf8') as outfile:
    json.dump(full_index, outfile)