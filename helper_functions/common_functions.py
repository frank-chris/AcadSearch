import csv
import pandas as pd
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize

stop_words = set(stopwords.words('english')) 
stemmer = PorterStemmer()

M = 5000

def get_tokenized_words(sentence, remove_stop_words_and_perform_stemming):      
    words = []                             
    tokenized_words = word_tokenize(re.sub(r'[^A-Za-z0-9]', ' ', sentence.lower()))
    for word in tokenized_words:
        if not remove_stop_words_and_perform_stemming:
            # Do not perform stemming and not remove stop words, done for name and affiliation index
            words.append(word)
        else:
            stemmed_word = stemmer.stem(word)            
            if stemmed_word not in stop_words:
                words.append(stemmed_word)                      
    return words

def write_prof_data_to_csv(output_file, professor_data_to_write):
    try:
        write = csv.writer(output_file)
        write.writerow(professor_data_to_write)
    except:        
        pass

def check_for_nan(input_string):
    if pd.isna(input_string):
        return ''
    else:
        return input_string

def make_list(initial_string):   

    svg_tag = re.compile(", <svg.*svg>, '")     
    html_tags = re.compile(", <.*>, '") 
    html_tags_inside = re.compile("<.*>.*</.*>")
    splitter = re.compile("[\"'], [\"']")  

    svg_removed =  svg_tag.sub(', \'\', \'',initial_string)
    html_removed = html_tags.sub(', \'', svg_removed)   
    plain_text = html_tags_inside.sub('', html_removed)

    return splitter.split(plain_text.lstrip('[\'').rstrip('\']'))     

def make_list_citations(initial_string):
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []

def get_file_index_and_prof_index(id):
    file_index = id//M
    prof_index = id%M
    return (file_index, prof_index)

def get_id(file_index, prof_index):
    return file_index*M + prof_index