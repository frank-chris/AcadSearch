import sys
import csv
import pandas as pd

file_count = 10
redundant_entries = dict()

def write_prof_data_to_csv(output_file, professor_data_to_write):
    try:
        write = csv.writer(output_file)
        write.writerow(professor_data_to_write)
    except:
        pass

for file_index in range(file_count):    

    try:
        input_file = pd.read_csv('../scraping/professor_data-'+str(file_index)+'.csv',header=None,encoding='latin1')
        output_file = open('professor_data-'+str(file_index)+'.csv', 'a+',newline ='')
    except:
        print("Error in opening input/output file.")
        sys.exit(0)

    number_of_professors = len(input_file)

    previous_scholar_id = None
    
    for prof_index in range(number_of_professors):    

        scholar_id = input_file.iloc[prof_index][0]
        name = input_file.iloc[prof_index][1]
        image_url = input_file.iloc[prof_index][2]
        affiliation = input_file.iloc[prof_index][3]
        email = input_file.iloc[prof_index][4]
        homepage = input_file.iloc[prof_index][5]
        topics_list = input_file.iloc[prof_index][6]
        cit = input_file.iloc[prof_index][7]
        h_ind = input_file.iloc[prof_index][8]
        i_ind = input_file.iloc[prof_index][9]
        cit5 = input_file.iloc[prof_index][10]
        h_ind5 = input_file.iloc[prof_index][11]
        i_ind5 = input_file.iloc[prof_index][12] 
        cit_list = input_file.iloc[prof_index][13]
        image_url = input_file.iloc[prof_index][14]
        papers_url_list = input_file.iloc[prof_index][15]
        papers_title_list = input_file.iloc[prof_index][16]

        if scholar_id == previous_scholar_id:
            if file_index not in redundant_entries:
                redundant_entries[file_index] = 1
            else:
                redundant_entries[file_index]+=1
            continue
        else:
            previous_scholar_id = scholar_id
            professor_data_to_write = (scholar_id, name, image_url, affiliation, email, homepage, topics_list, cit, h_ind, i_ind, cit5, h_ind5, i_ind5, cit_list, image_url, papers_url_list, papers_title_list)    
            write_prof_data_to_csv(output_file, professor_data_to_write)

for file_index in redundant_entries:
    print("Removed "+str(redundant_entries[file_index])+" reduntant entries from file "+str(file_index))