print("Loading all files...")

import pandas as pd
import numpy as np
import seaborn as sns
from tqdm import tqdm
sns.set()
import time
import random
import sys
sys.path.append('../helper_functions/')
sys.path.append('../querying/')
from common_functions import get_file_index_and_prof_index, get_id, check_for_nan, get_tokenized_words
from get_tf_idf import get_tf_idf_list
from boolean import phrase_retrieval, boolean_retrieval
import matplotlib.pyplot as plt

number_of_professors_to_test = 500
ranks = dict()
ranks['prof-name-boolean-retrieval'] = []
ranks['prof-affiliation-boolean-retrieval'] = []
ranks['prof-name-phrase-retrieval'] = []
ranks['prof-affiliation-phrase-retrieval'] = []
ranks['prof-paper-boolean-retrieval'] = []
ranks['prof-paper-phrase-retrieval'] = []
ranks['prof-paper-tf-idf'] = []

recallrate = dict()
recallrate['prof-name-boolean-retrieval-recall-rate-5'] = 0
recallrate['prof-name-boolean-retrieval-recall-rate-10'] = 0
recallrate['prof-affiliation-boolean-retrieval-recall-rate-5']  = 0
recallrate['prof-affiliation-boolean-retrieval-recall-rate-10']  = 0
recallrate['prof-name-phrase-retrieval-recall-rate-5'] = 0
recallrate['prof-name-phrase-retrieval-recall-rate-10'] = 0
recallrate['prof-affiliation-phrase-retrieval-recall-rate-5'] = 0
recallrate['prof-affiliation-phrase-retrieval-recall-rate-10'] = 0
recallrate['prof-paper-boolean-retrieval-recall-rate-5']  = 0
recallrate['prof-paper-boolean-retrieval-recall-rate-10']  = 0
recallrate['prof-paper-phrase-retrieval-recall-rate-5']  = 0
recallrate['prof-paper-phrase-retrieval-recall-rate-10']  = 0
recallrate['prof-paper-tf-idf-recall-rate-5']  = 0
recallrate['prof-paper-tf-idf-recall-rate-10']  = 0

file_count = 10
data_files = [pd.read_csv('../data/professor_data-'+str(file_index)+'-cleaned.csv',header=None,encoding='utf8') for file_index in range(file_count) ]

def make_list(initial_string):
    return initial_string.lstrip('[\'').rstrip('\']').split('\', \'')

def find_median(input_list):
    input_list.sort()
    N = len(input_list)    
    if N<=2:
        return input_list[0]
    else:
        return input_list[(N + 1)//2]

def generate_random_professor():
    list_of_prof_count_per_file = list(pd.read_csv('../data/metadata.csv', header=None)[0])
    file_index = random.randint(0, len(list_of_prof_count_per_file)-1)
    prof_index = random.randint(0, list_of_prof_count_per_file[file_index]-1)
    return get_id(file_index, prof_index)

def read_prof_information(prof_id):   
    file_index, prof_index = get_file_index_and_prof_index(prof_id)
    data = dict()       
    data['name'] = check_for_nan(data_files[file_index].iloc[prof_index][1]).strip()    
    data['affiliation'] = check_for_nan(data_files[file_index].iloc[prof_index][3]).strip()        
    data['papers_title_list'] = make_list(data_files[file_index].iloc[prof_index][16])    
    return data

def find_rank_in_list(prof_ids_list, ground_truth_prof_id):    
    index = 0
    for prof_id in prof_ids_list:
        index = index+1
        if prof_id == ground_truth_prof_id:
            return index  
    # if result not found    
    return 9999999   

def find_recall_rate(prof_ids_list, ground_truth_prof_id, recall_rate_number):
    # Return 1 if find in first recall_rate_number (5 or 10) results
    for i in range(min(recall_rate_number, len(prof_ids_list))):
        if prof_ids_list[i] == ground_truth_prof_id:
            return 1
    return 0

def search_with_name_or_affiliation(search_query, query_method):   
    start_time = time.time() 
    parsed_query = get_tokenized_words(search_query,False) # passing 'False' to not remove stop words and not perform stemming
    if query_method=='boolean-retrieval':
        query_result_prof_ids = boolean_retrieval(parsed_query,False)  # passing 'False' to use name and affiliation index
    elif query_method=='phrase-retrieval':
        query_result_prof_ids = phrase_retrieval(parsed_query,False)  # passing 'False' to use name and affiliation index

    time_taken = time.time() - start_time     
    return (query_result_prof_ids, time_taken)  

def search_with_paper_title(search_query, query_method):
    start_time = time.time() 
    parsed_query = get_tokenized_words(search_query,True)
    if query_method=='boolean-retrieval':
        query_result_prof_ids = boolean_retrieval(parsed_query,True)
    elif query_method=='phrase-retrieval':
        query_result_prof_ids = phrase_retrieval(parsed_query,True)
    elif query_method=='tf-idf':
        query_result_prof_ids = get_tf_idf_list(parsed_query)

    time_taken = time.time() - start_time
    return (query_result_prof_ids, time_taken)  



print("Loaded all files. Starting queries..")

count = 0


for i in tqdm(range(number_of_professors_to_test)):

    ground_truth_prof_id = generate_random_professor()
    prof_data = read_prof_information(ground_truth_prof_id)
        
    # If invalid / empty query then continue
    if prof_data['name']=='' or prof_data['affiliation']=='' or len(prof_data['papers_title_list'])==0:
        continue

    count+=1

    # Choose a random paper for the professor
    random_paper_index = random.randint(0, len(prof_data['papers_title_list'])-1)

    # Using name as search query and boolean retrieval as search method    
    search_query = prof_data['name']
    query_method = 'boolean-retrieval'
    (query_result_prof_ids, time_taken) = search_with_name_or_affiliation(search_query, query_method)     
    rank_obtained = find_rank_in_list(query_result_prof_ids, ground_truth_prof_id) 
    recallrate['prof-name-boolean-retrieval-recall-rate-5']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 5)
    recallrate['prof-name-boolean-retrieval-recall-rate-10']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 10)
    ranks['prof-name-boolean-retrieval'].append(rank_obtained)    

    # Using affiliation as search query and boolean retrieval as search method
    search_query = prof_data['affiliation']
    query_method = 'boolean-retrieval'    
    (query_result_prof_ids, time_taken) = search_with_name_or_affiliation(search_query, query_method)     
    rank_obtained = find_rank_in_list(query_result_prof_ids, ground_truth_prof_id) 
    recallrate['prof-affiliation-boolean-retrieval-recall-rate-5']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 5)
    recallrate['prof-affiliation-boolean-retrieval-recall-rate-10']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 10)
    ranks['prof-affiliation-boolean-retrieval'].append(rank_obtained)

    # Using name as search query and phrase retrieval as search method    
    search_query = prof_data['name']
    query_method = 'phrase-retrieval'   
    (query_result_prof_ids, time_taken) = search_with_name_or_affiliation(search_query, query_method)
    rank_obtained = find_rank_in_list(query_result_prof_ids, ground_truth_prof_id)  
    recallrate['prof-name-phrase-retrieval-recall-rate-5']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 5)
    recallrate['prof-name-phrase-retrieval-recall-rate-10']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 10)        
    ranks['prof-name-phrase-retrieval'].append(rank_obtained)

    # Using affiliation as search query and phrase retrieval as search method  
    search_query = prof_data['affiliation']
    query_method = 'phrase-retrieval'     
    (query_result_prof_ids, time_taken) = search_with_name_or_affiliation(search_query, query_method) 
    rank_obtained = find_rank_in_list(query_result_prof_ids, ground_truth_prof_id)  
    recallrate['prof-affiliation-phrase-retrieval-recall-rate-5']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 5)
    recallrate['prof-affiliation-phrase-retrieval-recall-rate-10']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 10)        
    ranks['prof-affiliation-phrase-retrieval'].append(rank_obtained)
    
    # Using paper title as search query and boolean retrieval as search method
    search_query = prof_data['papers_title_list'][random_paper_index]
    query_method = 'boolean-retrieval' 
    (query_result_prof_ids, time_taken) = search_with_paper_title(search_query, query_method)  
    rank_obtained = find_rank_in_list(query_result_prof_ids, ground_truth_prof_id) 
    recallrate['prof-paper-boolean-retrieval-recall-rate-5']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 5)
    recallrate['prof-paper-boolean-retrieval-recall-rate-10']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 10)         
    ranks['prof-paper-boolean-retrieval'].append(rank_obtained)

    # Using paper title as search query and phrase retrieval as search method
    search_query = prof_data['papers_title_list'][random_paper_index]
    query_method = 'phrase-retrieval' 
    (query_result_prof_ids, time_taken) = search_with_paper_title(search_query, query_method)  
    rank_obtained = find_rank_in_list(query_result_prof_ids, ground_truth_prof_id)  
    recallrate['prof-paper-phrase-retrieval-recall-rate-5']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 5)
    recallrate['prof-paper-phrase-retrieval-recall-rate-10']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 10)        
    ranks['prof-paper-phrase-retrieval'].append(rank_obtained)

    # Using paper title as search query and tf-idf as search method
    search_query = prof_data['papers_title_list'][random_paper_index]
    query_method = 'tf-idf' 
    (query_result_prof_ids, time_taken) = search_with_paper_title(search_query, query_method)
    rank_obtained = find_rank_in_list(query_result_prof_ids, ground_truth_prof_id) 
    recallrate['prof-paper-tf-idf-recall-rate-5']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 5)
    recallrate['prof-paper-tf-idf-recall-rate-10']+=find_recall_rate(query_result_prof_ids, ground_truth_prof_id, 10)           
    ranks['prof-paper-tf-idf'].append(rank_obtained)


for key in recallrate:
    recallrate[key]=(recallrate[key]/count)*100


# Plotting the median rank
query_and_method = ['Prof Name, Boolean', 'Prof Name, Phrase', 'Prof Affiliation, Boolean', 'Prof Affiliation, Phrase', 'Prof Paper, Boolean', 'Prof Paper, Phrase', 'Prof Paper, TF-IDF']
ranks_value = [find_median(ranks['prof-name-boolean-retrieval']), find_median(ranks['prof-name-phrase-retrieval']), find_median(ranks['prof-affiliation-boolean-retrieval']), find_median(ranks['prof-affiliation-phrase-retrieval']), find_median(ranks['prof-paper-boolean-retrieval']), find_median(ranks['prof-paper-phrase-retrieval']), find_median(ranks['prof-paper-tf-idf'])]
plt.figure(0)
plt.bar(query_and_method, ranks_value)
plt.xlabel('Median Rank')
plt.title('Median rank evaluation for '+str(number_of_professors_to_test)+' ground truths \n Rank represents the position at which desired result appears in search results')
plt.ylabel('Search Query and Method Used')
plt.xticks(fontsize=6,rotation=10)
for index,data in enumerate(ranks_value):
    plt.text(x=index,y=data+0.5,s=f"{data}",fontdict=dict(fontsize=12))
plt.savefig('median_rank.png', dpi=300)



# Plotting the recall rate
width = 0.25

query_and_method = ['Prof Name, Boolean', 'Prof Name, Phrase', 'Prof Affiliation, Boolean', 'Prof Affiliation, Phrase', 'Prof Paper, Boolean', 'Prof Paper, Phrase', 'Prof Paper, TF-IDF']
recall_rate_5 = [recallrate['prof-name-boolean-retrieval-recall-rate-5'],recallrate['prof-name-phrase-retrieval-recall-rate-5'],recallrate['prof-affiliation-phrase-retrieval-recall-rate-5'],recallrate['prof-affiliation-boolean-retrieval-recall-rate-5'],recallrate['prof-paper-boolean-retrieval-recall-rate-5'],recallrate['prof-paper-phrase-retrieval-recall-rate-5'],recallrate['prof-paper-tf-idf-recall-rate-5']]
recall_rate_10 = [recallrate['prof-name-boolean-retrieval-recall-rate-10'],recallrate['prof-name-phrase-retrieval-recall-rate-10'],recallrate['prof-affiliation-phrase-retrieval-recall-rate-10'],recallrate['prof-affiliation-boolean-retrieval-recall-rate-10'],recallrate['prof-paper-boolean-retrieval-recall-rate-10'],recallrate['prof-paper-phrase-retrieval-recall-rate-10'],recallrate['prof-paper-tf-idf-recall-rate-10']]
x_1 = [2*i for i in range(len(recall_rate_5))]
x_2 = [x + 2*width for x in x_1]
plt.figure(1)
plt.bar(x_1, recall_rate_5, color ='r', width = 0.5, edgecolor ='white', label ='Recall Rate @ 5')
plt.bar(x_2, recall_rate_10, color ='b', width = 0.5, edgecolor ='white', label ='Recall Rate @ 10')
plt.ylabel('Recall Rate')
plt.title('Recall rate evaluation for '+str(number_of_professors_to_test)+' ground truths \n Recall rate (R@X) represents % of time desired results appeared in top X')
plt.xlabel('Search Query and Method Used')
plt.xticks([2*i + width for i in range(len(recall_rate_5))],query_and_method, fontsize=6, rotation=10)
plt.savefig('recall_rate.png', dpi=300)