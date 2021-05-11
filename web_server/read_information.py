import numpy as np
import json
import sys
import random
import pandas as pd
import time
sys.path.append('../helper_functions/')
from common_functions import get_file_index_and_prof_index, check_for_nan

def get_parameters(request):
    '''
    Function to extract query, query method and search context(index type)
    from the request

    Input:
    > request - HTTP request
    
    Output:
    > (search_query, query_method, index_type) - a tuple consisting of the
    search query, query method(boolean, phrase or TF-IDF) and index type(name and affiliation
    or topics and paper titles)
    '''
    try:
        search_query = str(request.args['query'])               
    except:
        search_query = ''    # default query is empty

    try:
        query_method = str(request.args['query_method'])  
    except:
        query_method = 'phrase_query' # default method is phrase query

    try:
        index_type = str(request.args['index_type'])  
    except:
        index_type = 'topic_and_paper' # default index to use is topics and papers of professors

    return (search_query, query_method, index_type)

def make_list(initial_string):
    '''
    Function to convert str(list) to list

    Input:
    > initial_string - a list type-casted as str

    Output:
    > list of items from the str-type-casted list
    '''
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def make_list_citations(initial_string):
    '''
    Helper function for creating a python list of citations from the raw HTML string obtained
    from a professor's webpage.
    '''
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []

# number of cleaned files
file_count = 10

# read cleaned CSV files
data_files = [pd.read_csv('../data/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8') for file_index in range(file_count) ]

def read_prof_information(prof_id):   
    '''
    Function to read information of the professor whose
    Global ID is given and return it as a dictionary

    Input:
    > prof_id - Global ID of the professor whose data is to be read and returned

    Output:
    > data_dict_to_return - a dictionary containing all the information of the professor
    whose Global ID was given as prof_id
    '''
    file_index, prof_index = get_file_index_and_prof_index(prof_id)

    data_dict_to_return = dict()    

    data_dict_to_return['scholar_id'] = check_for_nan(data_files[file_index].iloc[prof_index][0])
    data_dict_to_return['name'] = check_for_nan(data_files[file_index].iloc[prof_index][1])
    data_dict_to_return['image_url'] = check_for_nan(data_files[file_index].iloc[prof_index][2])
    data_dict_to_return['affiliation'] = check_for_nan(data_files[file_index].iloc[prof_index][3])
    data_dict_to_return['email'] = check_for_nan(data_files[file_index].iloc[prof_index][4])
    data_dict_to_return['homepage'] = check_for_nan(data_files[file_index].iloc[prof_index][5])
    data_dict_to_return['topics_list'] = make_list(data_files[file_index].iloc[prof_index][6])
    data_dict_to_return['cit'] = int(data_files[file_index].iloc[prof_index][7])
    data_dict_to_return['h_ind'] = int(data_files[file_index].iloc[prof_index][8])
    data_dict_to_return['i_ind'] = int(data_files[file_index].iloc[prof_index][9])
    data_dict_to_return['cit5'] = int(data_files[file_index].iloc[prof_index][10])
    data_dict_to_return['h_ind5'] = int(data_files[file_index].iloc[prof_index][11])
    data_dict_to_return['i_ind5'] = int(data_files[file_index].iloc[prof_index][12])    
    data_dict_to_return['cit_list'] = make_list_citations(data_files[file_index].iloc[prof_index][13])
    data_dict_to_return['image_url'] = check_for_nan(data_files[file_index].iloc[prof_index][14])
    data_dict_to_return['papers_url_list'] = make_list(data_files[file_index].iloc[prof_index][15])
    data_dict_to_return['papers_title_list'] = make_list(data_files[file_index].iloc[prof_index][16])    

    return data_dict_to_return