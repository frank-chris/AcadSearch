import csv
import pandas as pd
import re

M = 5000

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