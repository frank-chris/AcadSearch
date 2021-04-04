import numpy as np
import json
import sys
query_path = "../querying/"
# Insert query_path at position 1
sys.path.insert(1, query_path)

import parse_query.py

query = input()

parsed_query = parse_query(query)

# Obtain all lists with the required words
# Sort them in the order of their lengths
# Perform a merge wherever two documents are the same
# Also, in Boolean Retrieval, ignore the values of the key, that is, the second value in each tuple

def merge(list1, list2):
    '''
    Given the inverted indexes of two stemmed words, merge them in the following way.
    AND: Only the documents where both the words appear
    Only the AND merge defined.
    '''
    ptr1 = 0
    ptr2 = 0
    docs = []
    while ptr1 < len(list1) and ptr2 < len(list2):
        if(list1[ptr1][0] == list2[ptr2][0]):
            docs.append(list1[ptr1][0])
            ptr1 += 1
            ptr2 += 1
        elif list1[ptr1][0] < list2[ptr2][0]:
            ptr1 += 1
        elif list1[ptr1][0] > list2[ptr2][0]:
            ptr2 += 2
    return sorted(list(set(docs)))

# Open the full file
#json_file = "../indexing/full_index.json"
json_file = "../indexing/partial_index.json"
with open(json_file) as f:
    documents_containing_word = json.load(f)

# The list of all documents corresponding to any word can be found by this
documents_containing_word = json.load(json_file)
words = [word for word in documents_containing_word.keys()]

docs_list = [documents_containing_word[word] for word in parsed_query]
len_list = [len(docs_with_word) for docs_with_word in docs_list]

# For efficiency, sort lists by their sizes, then merge
sort_by_len = np.argsort(len_list)
new_docs_list = [None] * len(docs_list)
for i in range(len(docs_list)):
    new_docs_list[i] = docs_list[sort_by_len[i]]

final_list = new_docs_list[0]
if len(new_docs_list) != 1:
    for i in range(1, len(new_docs_list)):
        final_list = merge(final_list, new_docs_list[i])
print(final_list)
