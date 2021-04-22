import time
import sys
sys.path.append('../querying/')
sys.path.append('../helper_functions/')
from common_functions import get_tokenized_words
from read_information import read_prof_information, get_parameters
from get_tf_idf import get_tf_idf_list
from boolean import phrase_retrieval, boolean_retrieval
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def search():  

    start_time = time.time()
    results_found = 0

    prof_data = []   # final data to return

    search_query, query_method, index_type = get_parameters(request)

    if search_query == '':
        return render_template('index.html',prof_data=prof_data,time_taken = round(time.time() - start_time, 5), search_query = search_query, query_method = query_method, index_type = index_type, results_found=results_found)  

    prof_ids = [] # to store professor ids in sorted order returned by querying algorithm and ranking

      

    # choose between different index and different methods
    if index_type == 'name_and_affiliation':
        
        parsed_query = get_tokenized_words(search_query,False)

        if query_method == 'boolean_and':
            prof_ids = boolean_retrieval(parsed_query,False)  # passing 'False' to use name and affiliation index
        else:
            prof_ids = phrase_retrieval(parsed_query,False)    # passing 'False' to use name and affiliation index        
    else:

        parsed_query = get_tokenized_words(search_query,True)    

        if query_method == 'tf_idf':
            prof_ids = get_tf_idf_list(parsed_query)
        elif query_method == 'boolean_and':
            prof_ids = boolean_retrieval(parsed_query,True)   # passing 'True' to use topic and paper index
        else:
            prof_ids = phrase_retrieval(parsed_query,True)  # passing 'True' to use topic and paper index
    
    # given professor ids, read their entire data from files

    results_found = len(prof_ids)

    try:
        prof_ids = prof_ids[:1000]
    except:
        prof_ids = prof_ids[:]

    for prof_id in prof_ids:    
        prof_data.append(read_prof_information(prof_id))

    return render_template('index.html',prof_data=prof_data,time_taken = round(time.time() - start_time, 5), search_query = search_query, query_method = query_method, index_type = index_type, results_found=results_found) 