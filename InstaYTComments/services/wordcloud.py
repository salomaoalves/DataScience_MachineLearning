import pandas as pd
import numpy as np
import nltk
import spacy # vai fazer a lemmatização
import re
import os
import string
import unidecode
import random
from os import path
from wordcloud import WordCloud

# load dic in spacy session
#!python -m spacy download pt_core_news_sm # for jupyter
nlp = spacy.load("pt_core_news_sm") # for vscode

# list of stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words('portuguese'))

def run(documents):
    # create the tokens
    token = []
    for text in documents:
        text = unidecode.unidecode(text)
        regex = re.compile('[' + re.escape(string.punctuation) + '\\r\\t\\n]')
        nopunct = regex.sub(" ", str(text))
        doc = nlp(nopunct, disable = ['parser', 'ner'])
        tokinizado = [token.text.lower() for token in doc]
        token.append(tokinizado)

    # put in one list all tokens and delete spaces and stopwords
    token = [item for items in token for item in items]
    token = [w for w in token if not w.isspace() and w not in stopwords]
    token = " ".join(token)

    # creat wordcloud
    wordcloud = WordCloud(width = 800, height = 500, random_state=1, background_color='white', collocations=False).generate(token)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    img_path = f"./static/img/wordcloud{random.randrange(1000)}.png"
    wordcloud.to_file(path.join(d, img_path))

    return img_path