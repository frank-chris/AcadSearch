import csv
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

try:
    input_file = pd.read_csv('../../professor_data_combined.csv',header=None)
    output_file = open('research_topic_index.csv','w',newline='',errors="ignore")
    output_writer = csv.writer(output_file)
except:
    print("Error in input and/or output file.")


research_topic_index = dict()
stemmer = PorterStemmer()

def get_words(sentence_list):    
    stemmed_words = []
    for sentence in sentence_list:
        tokenized_words = word_tokenize(sentence.lower())
        for word in tokenized_words:
            stemmed_words.append(stemmer.stem(word))            
    return stemmed_words

def build_index_for_research_topic(topics_list, scholar_id):
    stemmed_words = get_words(topics_list)
    for key in stemmed_words:
        if key in research_topic_index:
            research_topic_index[key].append(scholar_id)
        else:
            research_topic_index[key] = [scholar_id]

def make_list(initial_string):
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def make_list_citations(initial_string):
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []

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

    build_index_for_research_topic(topics_list, scholar_id)        

count = 0
sum_len = 0
for key in research_topic_index:            
    sum_len =  sum_len + len(research_topic_index[key])
    count = count + 1    
    output_writer.writerow((key,research_topic_index[key]))    

print("Average Posting Length = "+str(sum_len/count))