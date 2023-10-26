import pandas as pd
import numpy as np
import math
import nltk
import spacy
import re
import string
import unidecode

# load dic in spacy session
#!python -m spacy download pt_core_news_sm # for jupyter
nlp = spacy.load("pt_core_news_sm") # for vscode

# list of stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords_pt = set(stopwords.words('portuguese'))
stopwords_en = set(stopwords.words('english'))

def creat_BoW(documents, lang, tf=False):
    bagOfWord = [] # each element is a list of token of each document (stopwords already treated)
    for text in documents:
        text = unidecode.unidecode(text)
        regex = re.compile('[' + re.escape(string.punctuation) + '\\r\\t\\n]')
        nopunct = regex.sub(" ", str(text))
        doc = nlp(nopunct, disable = ['parser', 'ner'])
        tokens = [token.text.lower() for token in doc]
        # delete spaces and stopwords
        if lang=="1":
            tokens = [w for w in tokens if not w.isspace() and w not in stopwords_en]
        else:
            tokens = [w for w in tokens if not w.isspace() and w not in stopwords_pt] 
        bagOfWord.append(tokens)

    if tf:
        return len(bagOfWord[0])
    else:
        return bagOfWord

def run(documents, lang):
    '''Get the TF, DF, IDF and TF-IDF'''
    
    # creat bag of word for each document
    bagOfWord = creat_BoW(documents, lang)

    # list of futures features of the df
    tokens_list, comment_list = [], []
    for bag in range(len(bagOfWord)):
        for t in range(len(bagOfWord[bag])):
            tokens_list.append(bagOfWord[bag][t])
            comment_list.append(documents[bag])

    df = pd.DataFrame({'tokens': tokens_list, 'comment': comment_list})
    values_count = df.value_counts(subset=['tokens','comment'])
    token_list = [t[0] for t in values_count.index]
    comment_list = [t[1] for t in values_count.index]
    token_ind_total = values_count.values
    token_doc_total = [len(c) for c in comment_list]

    # TF
    tf_list = []
    for qtd, d in zip(token_ind_total, comment_list):
        bow_size = creat_BoW([d], lang, True)
        tf_list.append(qtd / bow_size)

    # IDF
    nzao, idf_list = len(documents), []
    for w in token_list:
        df = 0
        for d in bagOfWord:
            if w in d:
                df += 1
        idf_list.append(math.log(nzao/df))

    # TF-IDF
    tf_idf_list = [tf*idf for tf, idf in zip(tf_list,idf_list)]

    return {'Token': token_list, 'Comment': comment_list, 'Numb of that token': token_ind_total,
            'Numb of all tokens': token_doc_total, 'TF':np.round(tf_list,4), 'IDF':np.round(idf_list,4), 
            'TF_IDF':np.round(tf_idf_list,4), 'obs': "Cada comentario/linha é um documento"}