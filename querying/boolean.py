import numpy as np
import json
import sys

index1 = "../data/name_and_affiliation_index_full.json"
with open(index1) as f:
    name_and_affiliation_index = json.load(f)

index2 = "../data/topic_and_paper_index_full.json"
with open(index2) as f:
    topic_and_paper_index = json.load(f)

def merge(list1, list2, req_dist = None):
    '''
    Given the postings lists of two stemmed words, merge them in the following way.
    AND: Only the documents where both the words appear.
    Only the AND merge defined.

    Input:
    > list1 - first list of (documents, postition in document).
    > list2 - second list of (documents, postition in document).
    > req_dist - if this is set, then not only must the documents have the same id, but also their second parameter(their position in the doc) must be req_dist apart.

    Output:
    > docs - returned list of list of (documents, postition in document) according to the merging criteria.
    '''

    ptr1 = 0
    ptr2 = 0
    docs = []


    # Two pointers, increment the pointer that has "fallen behind" the other.
    while ptr1 < len(list1) and ptr2 < len(list2):
        if(list1[ptr1][0] == list2[ptr2][0]):
            # If req_dist is not set, then we do not need to check the second parameter (the position in the document).
            if req_dist == None:
                docs.append(list1[ptr1])
                ptr1 += 1
                ptr2 += 1
            # If req_dist is set, then we need to compare the distance between the positions in the documents with the req_dist.
            else:
                actual_dist = list2[ptr2][1] - list1[ptr1][1]
                if actual_dist == req_dist:
                    docs.append(list1[ptr1])
                    ptr1 += 1
                    ptr2 += 1
                elif actual_dist > req_dist: # This means we need to decrease the actual_dist, or increment the first pointer
                    ptr1 += 1
                elif actual_dist < req_dist: # This means we need to increase the actual_dist, or increment the second pointer
                    ptr2 += 1
        elif list1[ptr1][0] < list2[ptr2][0]:
            ptr1 += 1
        elif list1[ptr1][0] > list2[ptr2][0]:
            ptr2 += 1

    return docs

def boolean_retrieval(parsed_query, use_topic_and_paper_index, AND = True):
    '''
    1) Obtain the postings lists of the words in the phrase.
    2) Sort them in the order of their lengths.
    3) Perform a "merge" for every pair of words in the parsed_query.
    4) Also, in Boolean Retrieval, ignore the values of the key. That is, the second value in each tuple.

    Input:
    > parsed_query - list of words from search query, (with or without stemming).
    > use_topic_and_paper_index - use topic and paper index if true; name and affiliation index if false. 
    > AND - it true, return documents that contain all the words in parsed_query; otherwise return all documents that contain any of the words.

    Output:
    > final_docs - list of all documents obtained as per parameters.
    '''    

    documents_containing_word = dict()

    # Choose the index to be used
    if use_topic_and_paper_index:
        documents_containing_word = topic_and_paper_index
    else:
        documents_containing_word= name_and_affiliation_index

    # We store the postings list of all the words found in the index.
    docs_list = []
    for word in parsed_query:
        if word in documents_containing_word:
            docs_list.append(documents_containing_word[word])
        else:
            docs_list.append([])    

    final_docs = []

    if AND:

        # Find the lengths of the postings_list if AND is used. This is because sort by the lengths is an optimisation for AND. It is not so for OR.
        len_list = [len(docs_with_word) for docs_with_word in docs_list]

        # Handle the case when no match.
        if len(docs_list) == 0:
            return []

        # For efficiency, sort lists by their sizes, then merge.
        sort_by_len = np.argsort(len_list)
        new_docs_list = [None] * len(docs_list)
        for i in range(len(docs_list)):
            new_docs_list[i] = docs_list[sort_by_len[i]]

        # At the ith iteration, store the list of all documents for the first (i + 1) words.
        final_list = new_docs_list[0]
        if len(new_docs_list) != 1:
            for i in range(1, len(new_docs_list)):
                final_list = merge(final_list, new_docs_list[i])
        
        # Return only the documents where these words occur, not the positions.
        for i in range(len(final_list)):
            if i != 0:
                if final_list[i][0] != final_docs[-1]:
                    final_docs.append(final_list[i][0])
            else:
                final_docs.append(final_list[0][0]) 

    
    # OR operation
    else:

        # Couple of dictionaries defined as follows-
        doc_freq = dict() # Doc : Total number of words found in that document. This acts as a tiebreaker between documents having the same "score".
        doc_words = dict() # Doc : Set of all query words that appear in it. The length of this set is the "score" of each document.
        for i, postings_list in zip(range(len(docs_list)), docs_list):
            for doc in postings_list:
                doc_id = doc[0]
                if doc_id not in doc_freq:
                    doc_words[doc_id] = set()
                    doc_freq[doc_id] = 0
                doc_words[doc_id].add(i)
                doc_freq[doc_id] += 1

        # Sort documents in decreasing order of "score" as defined above.
        # If two documents have the same score, then the document which has a higher doc_freq, that is, a higher total number of matches will be returned first.
        for doc_id in doc_freq.keys():
            final_docs.append((doc_id, (len(doc_words[doc_id]), doc_freq[doc_id])))
        final_docs = sorted(final_docs, key = lambda x : x[1], reverse = True)

        # We return only the document ids, however we return them in order.
        for i in range(len(final_docs)):
            final_docs[i] = final_docs[i][0]
            
    return final_docs

def phrase_retrieval(parsed_phrase, use_topic_and_paper_index):
    '''
    1) Obtain the postings lists of the words in the phrase
    2) Sort them in the order of their lengths
    3) Perform a merge wherever two documents are the same, and their positions in the given document have the required distance
    3) Perform a "merge" for every pair of words in the parsed_phrase. However this time their positions in the given document have the required distance(as much as in the parsed_phrase).
    In summary, we return all documents where there the parsed_phrase appears exactly in order.

    Input:
    > parsed_phrase - list of words from search phrase.
    > use_topic_and_paper_index - use topic and paper index if true; name and affiliation index if false. 

    Output:
    > final_docs - list of all documents where there the parsed_phrase appears exactly in order.
    '''     

    documents_containing_word = dict()

    if use_topic_and_paper_index:        
        documents_containing_word = topic_and_paper_index
    else:    
        documents_containing_word = name_and_affiliation_index

    # Repeat words in a phrase not handled.
    ctr = 0
    word_pos = dict()
    for word in parsed_phrase:
        word_pos[word] = ctr
        ctr += 1
    
    # We store the postings list of all the words found in the index.
    docs_list = []
    for word in parsed_phrase:        
        if word in documents_containing_word:
            docs_list.append(documents_containing_word[word])
        else:
            docs_list.append([])    
    # Find the lengths of the postings_list of all documents.
    len_list = [len(docs_with_word) for docs_with_word in docs_list]

    # Handle the case when no match.
    if len(docs_list) == 0:
        return []

    # For efficiency, sort lists by their sizes, then merge.
    sort_by_len = np.argsort(len_list)
    new_docs_list = [None] * len(docs_list)
    for i in range(len(docs_list)):
        new_docs_list[i] = docs_list[sort_by_len[i]]

    final_list = new_docs_list[0]
    # At the ith iteration, store the list of all documents for the first (i + 1) words.
    if len(new_docs_list) != 1:
        for i in range(1, len(new_docs_list)):
            distance = sort_by_len[i] - sort_by_len[0]
            final_list = merge(final_list, new_docs_list[i], distance)

    # Return only the documents where these words occur, not the positions.
    final_docs = []
    for i in range(len(final_list)):
        if i != 0:
            if final_list[i][0] != final_docs[-1]:
                final_docs.append(final_list[i][0])
        else:
            final_docs.append(final_list[0][0]) 
            
    return final_docs
