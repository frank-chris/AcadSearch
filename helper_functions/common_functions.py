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
    '''
    Given a sentence, tokenise it.
    Remove stop words (such as "the", "that", etc) and perform stemming(find a simpler word of the form which connects all semantically similar words together; such as science and scientist) if specified.

    Input:
    > sentence - an input sentence
    > remove_stop_words_and_perform_stemming - if true, we perform removal of stop words and stemming

    Output:
    > words - list of tokenised words obtained.
    '''
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
    '''
    Write the data obtained into a csv file.

    Input:
    > output_file - csv file where the data is to be written
    > professor_data_to_write - the actual data that is to be written
    '''

    try:
        write = csv.writer(output_file)
        write.writerow(professor_data_to_write)
    except:        
        pass

def check_for_nan(input_string):
    '''
    Return empty string if NaN found
    '''
    if pd.isna(input_string):
        return ''
    else:
        return input_string

def make_list(initial_string):   
    '''
    Function to remove HTML and SVG tags from raw HTML parsed string.

    Input:
    > initial_string - raw HTML string.

    Output:
    > list of items obtained from the strings after the HTML and SVG tags have been removed.
    '''

    svg_tag = re.compile(", <svg.*svg>, '")     
    html_tags = re.compile(", <.*>, '") 
    html_tags_inside = re.compile("<.*>.*</.*>")
    splitter = re.compile("[\"'], [\"']")  

    svg_removed =  svg_tag.sub(', \'\', \'',initial_string)
    html_removed = html_tags.sub(', \'', svg_removed)   
    plain_text = html_tags_inside.sub('', html_removed)

    return splitter.split(plain_text.lstrip('[\'').rstrip('\']'))     

def make_list_citations(initial_string):
    '''
    Helper function for creating a python list of citations from the raw HTML string obtained from a professor's webpage.
    '''
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []


'''
Since our entire data is contained across multiple csv files, we do not have unique IDs for each of the professors.
We create such a unique ID for the professors using the file number in which they were found, and their position in that file.
The following two functions help us to go back and forth between the two.
'''

def get_file_index_and_prof_index(id):
    '''
    Given the global ID(created by us) of the professor in question, find their actual file number and index in that file.

    Input:
    > id - our global ID assigned to each entry.

    Output:
    A tuple containing the following two things-
    > file_index - the file number(number of the csv) in which this professor's data was given.
    > prof_index - the index of the entry in question in the csv from which it was originally obtained.
    '''

    file_index = id // M
    prof_index = id % M
    return (file_index, prof_index)


def get_id(file_index, prof_index):
    '''
    Input:
    > file_index and prof_index - as described above
    
    Output:
    > id - the global ID, as described above.
    '''

    return file_index * M + prof_index
