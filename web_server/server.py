import time
from processing import read_prof_information
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.debug = True

def get_doc_id_from_tf_idf(query):
    return [i for i in range(10)]

@app.route('/', methods=['GET','POST'])
def search():  
    start_time = time.time()
    prof_data = []
    try:
        search_query = str(request.args['query'])         
    except:
        search_query = ''   

    if search_query == '':
        return render_template('index.html',prof_data=prof_data,time_taken = round(time.time() - start_time, 5), search_query = search_query)  
    
    prof_ids = get_doc_id_from_tf_idf(search_query)

    for prof_id in prof_ids:    
        prof_data.append(read_prof_information(prof_id))

    return render_template('index.html',prof_data=prof_data,time_taken = round(time.time() - start_time, 5), search_query = search_query) 