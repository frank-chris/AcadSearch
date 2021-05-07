import sys
import csv
import pandas as pd
import re
sys.path.append('../helper_functions/')
from common_functions import *

file_count = 10
redundant_entries = dict()

for file_index in range(file_count):    

    try:
        input_file = pd.read_csv('../data/professor_data-'+str(file_index)+'.csv',header=None,encoding='utf8')
        output_file = open('../data/professor_data-'+str(file_index)+'-cleaned.csv', 'w+',newline ='',encoding='utf8')
    except:
        print("Error in opening input/output file.")
        sys.exit(0)

    number_of_professors = len(input_file)    

    scholar_ids = set()     
    
    for prof_index in range(number_of_professors):            

        # Name and id of the professor
        scholar_id = input_file.iloc[prof_index][0]
        name = check_for_nan(input_file.iloc[prof_index][1])

        # Affiliation, email and homepage of the professor
        affiliation = check_for_nan(input_file.iloc[prof_index][3])
        email = check_for_nan(input_file.iloc[prof_index][4])
        homepage = check_for_nan(input_file.iloc[prof_index][5])

        # List of research topics listed by professor
        topics_list = make_list(input_file.iloc[prof_index][6])

        # Citations, h-index and i10-index of the professor, all time and over the last five years.
        cit = int(input_file.iloc[prof_index][7])
        h_ind = int(input_file.iloc[prof_index][8])
        i_ind = int(input_file.iloc[prof_index][9])
        cit5 = int(input_file.iloc[prof_index][10])
        h_ind5 = int(input_file.iloc[prof_index][11])
        i_ind5 = int(input_file.iloc[prof_index][12])    
        cit_list = make_list_citations(input_file.iloc[prof_index][13])

        # Image URL on the professor's Google Scholar page, if provided.
        image_url = check_for_nan(input_file.iloc[prof_index][14])

        # List of papers co-authored by the professor and their URLs.
        papers_url_list = make_list(input_file.iloc[prof_index][15])
        papers_title_list = make_list(input_file.iloc[prof_index][16])              

        if scholar_id in scholar_ids:            
            if file_index not in redundant_entries:
                redundant_entries[file_index]=1
            else:
                redundant_entries[file_index]+=1            
        else:
            # Check for consistency
            if len(papers_url_list)!=len(papers_title_list):
                continue           
                             
            scholar_ids.add(scholar_id)
            professor_data_to_write = (scholar_id, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)    
            write_prof_data_to_csv(output_file, professor_data_to_write)

for file_index in redundant_entries:
    print("Removed "+str(redundant_entries[file_index])+" reduntant entries from file "+str(file_index))
