import numpy as np
import json
import sys
import random
import pandas as pd
import time
sys.path.append('../helper_functions/')
sys.path.append('../querying/')
from common_functions import get_file_index_and_prof_index, check_for_nan

def make_list(initial_string):
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def make_list_citations(initial_string):
    try:
        return list(map(int,initial_string.lstrip('[').rstrip(']').split(', ')))
    except:
        return []

file_count = 10

data_files = [pd.read_csv('../cleaning/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8') for file_index in range(file_count) ]

def read_prof_information(prof_id):   

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