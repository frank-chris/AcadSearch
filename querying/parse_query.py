#import nltk
#nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from spellchecker import SpellChecker
import re

spell = SpellChecker()
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
    words_list = word_tokenize(re.sub(r'[^A-Za-z0-9]', ' ', query.lower()))

    for word in words_list:
        stemmed_word = stemmer.stem(word)
        if stemmed_word not in stop_words:
            parsed_query.append(stemmed_word)

    print(parsed_query)

    return parsed_query

def spell_check(query):
    '''
    Function to correct spelling of a query

    Input:
    > query - the query as a str

    Outputs:
    > corrected_query - spell-corrected query as a str
    > len(misspelled_words) - number of words corrected
    '''
    corrected_query = query.lower()
    words_list = spell.split_words(corrected_query)
    misspelled_words = spell.unknown(words_list)

    for word in misspelled_words:
        corrected_query.replace(word, spell.correction(word))

    return corrected_query, len(misspelled_words)