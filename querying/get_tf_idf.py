import json
import sys
sys.path.append('../helper_functions/')

with open('../querying/tf_idf_scores_topic_and_paper_full.json') as f:
    tf_idf_score = json.load(f)

def get_tf_idf_list(parsed_query,n=99999999999):
    global tf_idf_score       
    docs_dict = {}        

    for key in tf_idf_score.keys():
        term, doc = key.split('_')
        doc = int(doc)
        if term in parsed_query:
            if doc not in docs_dict:
                docs_dict[doc] = tf_idf_score[key]
            else:
                docs_dict[doc] += tf_idf_score[key]

    docs_list = []
    for doc, score in docs_dict.items():
        docs_list.append([doc, score])

    docs_list.sort(key = lambda x: x[1], reverse=True)

    for i in range(len(docs_list)):
        docs_list[i] = docs_list[i][0]

    return docs_list[:n]