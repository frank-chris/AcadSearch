from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english')) 

def query_parser(query):
    '''
    Function to parse search queries

    Input:
    > query - the query as a str

    Output:
    > parsed_query - a list of words obtained by parsing the query
    '''
    parsed_query = []
    words_list = word_tokenize(query.lower())

    for word in words_list:
        stemmed_word = stemmer.stem(word)
        if stemmed_word not in stop_words:
            parsed_query.append(stemmed_word)

    return parsed_query