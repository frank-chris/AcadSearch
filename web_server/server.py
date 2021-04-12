import time
from processing import read_prof_information
from tf_idf import get_tf_idf_list
from boolean import phrase_retr, boolean_retrieval
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def search():  

    start_time = time.time()

    prof_data = []   # final data to return

    try:
        search_query = str(request.args['query'])               
    except:
        search_query = ''          

    try:
        query_method = str(request.args['query_method'])  
    except:
        query_method = 'phrase_query' # default method is phrase quer

    if search_query == '':
        return render_template('index.html',prof_data=prof_data,time_taken = round(time.time() - start_time, 5), search_query = search_query, query_method = query_method)  

    prof_ids = [] # to store professor ids in sorted order returned by querying algorithm and ranking

    # choose between different methods
    if query_method == 'tf_idf':
        prof_ids = get_tf_idf_list(search_query)
    elif query_method == 'boolean_and':
        prof_ids = boolean_retrieval(search_query,True)        
    else:
        prof_ids = phrase_retr(search_query)  
    
    # given professor ids, read their entire data from files
    for prof_id in prof_ids:    
        prof_data.append(read_prof_information(prof_id))

    return render_template('index.html',prof_data=prof_data,time_taken = round(time.time() - start_time, 5), search_query = search_query, query_method = query_method) 