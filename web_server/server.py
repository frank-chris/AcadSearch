from flask import Flask, render_template, request, redirect
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET','POST'])
def search():    
    doc_ids = dict()  
    try:
        search_query = str(request.args['query']) 
    except:
        search_query = ''    
    
    doc_ids = {'0':1000, '1':2000}

    return render_template('index.html',doc_ids=doc_ids)  