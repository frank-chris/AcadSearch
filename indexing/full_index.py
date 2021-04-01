import csv
import json
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import sys
nltk.download('punkt')

try:    
    output_file = open('full_index.csv','w',newline='',errors="ignore",encoding='latin1')
    output_writer = csv.writer(output_file)
except:
    print("Error in opening output file.")
    sys.exit(0)


full_index = dict()
stemmer = PorterStemmer()

def get_words(sentence_list):    
    stemmed_words = []
    for sentence in sentence_list:
        tokenized_words = word_tokenize(sentence.lower())
        for word in tokenized_words:
            stemmed_words.append(stemmer.stem(word))            
    return stemmed_words


def build_index(row, name, affiliation, topics_list, papers_title_list):
    # Should we apply stemming to the name? What about affiliation?
    search_info_list = [name, affiliation] + topics_list + papers_title_list
    stemmed_words = get_words(search_info_list)
    for i, key in zip(range(len(stemmed_words)), stemmed_words):
        if key in full_index:
            full_index[key].append((row, i))
        else:
            full_index[key] = [(row, i)]

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
        input_file = pd.read_csv('../scraping/professor_data-'+str(file_index)+'.csv',header=None,encoding='latin1')
    except:
        print("Error in opening input file.")
        sys.exit(0)

    for i in range(len(input_file)):    

        scholar_id = input_file.iloc[i][0]
        name = input_file.iloc[i][1]
        image_url = input_file.iloc[i][2]
        affiliation = input_file.iloc[i][3]
        email = input_file.iloc[i][4]
        homepage = input_file.iloc[i][5]
        topics_list = make_list(input_file.iloc[i][6])
        cit = int(input_file.iloc[i][7])
        h_ind = int(input_file.iloc[i][8])
        i_ind = int(input_file.iloc[i][9])
        cit5 = int(input_file.iloc[i][10])
        h_ind5 = int(input_file.iloc[i][11])
        i_ind5 = int(input_file.iloc[i][12])    
        cit_list = make_list_citations(input_file.iloc[i][13])
        image_url = input_file.iloc[i][14]
        papers_url_list = make_list(input_file.iloc[i][15])
        papers_title_list = make_list(input_file.iloc[i][16])    

        build_index(i, name, affiliation, topics_list, papers_title_list)        

count = 0
sum_len = 0
for key in full_index:            
    sum_len =  sum_len + len(full_index[key])
    count = count + 1    
    output_writer.writerow((key,full_index[key]))    

print("Average Posting Length = "+str(sum_len/count))

with open('full_index.json', 'w') as outfile:
    json.dump(full_index, outfile)
