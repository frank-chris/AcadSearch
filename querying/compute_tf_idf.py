import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import sys
sys.path.append('../helper_functions/')
from common_functions import get_id

def compute_tf_idf_score():
    with open('../data/topic_and_paper_index_full.json') as f:
        data = json.load(f)
    
    term_list = data.keys()

    csv_sizes = list(pd.read_csv('../data/metadata.csv', header=None)[0])

    id_list = []
    for file_id in range(len(csv_sizes)):
        for prof_id in range(csv_sizes[file_id]):
            id_list.append(get_id(file_id, prof_id))

    scores = {}

    N = len(id_list)

    doc_sizes = {}
    for d in id_list:
        doc_sizes[d] = 0
    df_dict = {}
    for t in term_list:
        df_dict[t] = 0            
    
    for t in data:
        last_seen = -1
        for pair in data[t]:
            doc_sizes[pair[0]] += 1
            if pair[0] != last_seen:
                df_dict[t] += 1
                last_seen = pair[0]

    tf_num_dict = {}
    
    for t in data:
        for pair in data[t]:
            if (t, pair[0]) not in tf_num_dict:
                tf_num_dict[(t, pair[0])] = 1
            else:
                tf_num_dict[(t, pair[0])] += 1

    print('Doc sizes computed. Starting score computation. Len(table) = ', len(tf_num_dict))

    for (t,d) in tqdm(tf_num_dict.keys()):
        tf = tf_num_dict[(t,d)]/(doc_sizes[d]+1)
        idf = np.log(N/df_dict[t]+1)
        scores[str(t)+'_'+str(d)] = tf*idf

    with open("../data/tf_idf_scores_topic_and_paper_full.json", "w+") as fp: 
        json.dump(scores, fp)


compute_tf_idf_score()