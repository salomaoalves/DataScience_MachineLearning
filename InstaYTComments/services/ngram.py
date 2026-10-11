import pandas as pd
import numpy as np
import nltk
import spacy # vai fazer a lemmatização
import re
import string
import unidecode
import math
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# load dic in spacy session
#!python -m spacy download pt_core_news_sm # for jupyter
nlp = spacy.load("pt_core_news_sm") # for vscode

# How to load pos_tag in pt-br -- you should have the file POS_tagger_brill.pkl downloaded 
# https://github.com/inoueMashuu/POS-tagger-portuguese-nltk/tree/master/trained_POS_taggers
import joblib
pos_tag_pt = joblib.load(os.path.join(PROJECT_ROOT, 'POS_tagger_brill.pkl'))

# list of stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords_pt = set(stopwords.words('portuguese'))
stopwords_en = set(stopwords.words('english'))

def run(commen, lang):
    '''Delete special characters/accents and tokenize comments in words'''

    new_comen = []
    for text in commen:
        text = unidecode.unidecode(text)
        regex = re.compile('[' + re.escape(string.punctuation) + '\\r\\t\\n]')
        nopunct = regex.sub(" ", str(text))
        doc = nlp(nopunct, disable = ['parser', 'ner'])
        tokinizado = [token.text.lower() for token in doc]
        new_comen.append(tokinizado)
        new_comen.append(' ')
    new_comen = [item for items in new_comen for item in items]

    # get ngram's
    df_unagram = unagram(new_comen, lang)
    df_bigram = bigram(new_comen, lang)
    df_trigram = trigram(new_comen, lang)

    return {'unagram': to_chart(df_unagram, 'unagram'),
            'bigram': to_chart(df_bigram, 'bigram'),
            'trigram': to_chart(df_trigram, 'trigram')}


def to_chart(df, name, max_rows=200):
    '''Return the n-grams in a format that Jinja2 understand (list of dict), sorted by
        frequency, with the bar size (% of the most frequent) used in the chart'''

    df = df.rename(columns={name: 'ngram', f'{name}_frequency': 'frequency'})
    df = df.sort_values(by=['frequency', 'ngram'], ascending=[False, True]).head(max_rows)
    max_freq = df['frequency'].max() if len(df) else 1
    return [{'ngram': n, 'frequency': int(f), 'size': round(100 * f / max_freq, 1)}
            for n, f in zip(df['ngram'], df['frequency'])]


def filter_type_token_bigram(ngram, lang):
    '''Filter ADJ/NN and delete stopwords/spaces in bigrams'''

    if lang=="1":
        stopwords = stopwords_en
    else:
        stopwords = stopwords_pt

    # delete spaces and stopwords
    for word in ngram:
        if word in stopwords or word.isspace():
            return False
        
    # types of tokens accepted
    acceptable_types = ('N', 'NPROP') #adjective, noun
    second_type = ('N', 'NPROP', 'ADJ') #noun
    
    # tags
    tags = pos_tag_pt.tag([str(ngram[0]),str(ngram[1])])

    # filtering
    if tags[0][1] in acceptable_types and tags[1][1] in second_type:
        return True
    else:
        return False

def filter_type_token_trigram(ngram, lang):
    '''Filter ADJ/NN and delete stopwords/spaces in trigrams'''

    if lang=="1":
        stopwords = stopwords_en
    else:
        stopwords = stopwords_pt

    # delete spaces and stopwords
    for word in ngram:
        if word in stopwords or word.isspace():
            return False
        
    # types of tokens accepted
    first_type = ('ADJ', 'N', 'NPROP') #adjective, noun
    second_type = ('ADJ', 'N', 'NPROP') #adjective, noun
    
    # tags
    tags = pos_tag_pt.tag([str(ngram[0]),str(ngram[1]),str(ngram[2])])
    
    # filtering
    if tags[0][1] in first_type and tags[2][1] in second_type:
        return True
    else:
        return False


def unagram(new_comen, lang):
    # delete spaces and stopwords
    if lang=="1":
        new_comen = [w for w in new_comen if not w.isspace() and w not in stopwords_en]
    else:
        new_comen = [w for w in new_comen if not w.isspace() and w not in stopwords_pt]
    

    # create the unagram
    s = pd.Series(new_comen, dtype=str)
    return pd.DataFrame({'unagram': s.value_counts().index,
                         'unagram_frequency': s.value_counts().values})

def bigram(new_comen, lang):
    # reate the bigramas
    buscaBigramas = nltk.collocations.BigramCollocationFinder.from_words(new_comen)

    # frenquency table
    bigram_freq = buscaBigramas.ngram_fd.items()
    FreqTabBigramas = pd.DataFrame(list(bigram_freq), 
                                   columns=['bigram', 'bigram_frequency']
                                  ).sort_values(by='bigram_frequency', ascending=False)
    
    # filter
    bigram_filter = FreqTabBigramas[FreqTabBigramas.bigram.map(lambda x: filter_type_token_bigram(x, lang)).astype(bool)].copy()
    bigram_filter['bigram'] = bigram_filter['bigram'].map(' '.join) # ('trilha', 'sonora') -> 'trilha sonora'
    
    return bigram_filter

def trigram(new_comen, lang):
    # create the trigrams
    buscaTrigramas = nltk.collocations.TrigramCollocationFinder.from_words(new_comen)

    # frenquency table
    trigram_freq = buscaTrigramas.ngram_fd.items()
    FreqTabTrigramas = pd.DataFrame(list(trigram_freq), 
                                    columns=['trigram','trigram_frequency']
                                   ).sort_values(by='trigram_frequency',ascending=False)
    # filter
    trigram_filter = FreqTabTrigramas[FreqTabTrigramas.trigram.map(lambda x: filter_type_token_trigram(x, lang)).astype(bool)].copy()
    trigram_filter['trigram'] = trigram_filter['trigram'].map(' '.join)

    return trigram_filter
