import json
import sys
sys.path.append('../helper_functions/')

# read TF-IDF scores from JSON file
with open('../data/tf_idf_scores_topic_and_paper_full.json') as f:
    tf_idf_score = json.load(f)

def get_tf_idf_list(parsed_query,n=99999999999):
    '''
    Function to return TF-IDF score based results when given a parsed query as input

    Input:
    > parsed_query - search query parsed using get_tokenized_words()
    > n - number of results to return (default: 99999999999)

    Output:
    > docs_list[:n] - list of global IDs of top n professors based on
    TF-IDF score computed using parsed_query
    '''
    global tf_idf_score       
    docs_dict = {}        

    # Computing TF-IDF scores of all documents(professors) that contain at least 
    # one word/term from the parsed query in it. If a document contains multiple terms
    # from the query, then the scores are added.
    for key in tf_idf_score.keys():
        term, doc = key.split('_')
        doc = int(doc)
        if term in parsed_query:
            if doc not in docs_dict:
                docs_dict[doc] = tf_idf_score[key]
            else:
                docs_dict[doc] += tf_idf_score[key]

    # create list of results containing tuples of form (prof id, score)
    docs_list = []
    for doc, score in docs_dict.items():
        docs_list.append([doc, score])

    # sort in decreasing order of score
    docs_list.sort(key = lambda x: x[1], reverse=True)

    # remove scores from the list
    for i in range(len(docs_list)):
        docs_list[i] = docs_list[i][0]

    # return first n results
    return docs_list[:n]