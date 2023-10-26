from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
import pandas as pd

def get_data(lang):
    '''Get correct train data'''
    if lang=="1":
        df = pd.read_csv('/home/salomao/Desktop/DSProject/NLP/services/data/train_en.csv')
    else:
        df = pd.read_csv('/home/salomao/Desktop/DSProject/NLP/services/data/train_pt.csv')
    return [[c,s] for c,s in zip(df['Comment'].to_list(),df['Score'].to_list())]

def start_training(data_train, vetorizador):
    '''Train the model'''
    comments = [comment_train[0] for comment_train in data_train]
    scores = [score_train[1] for score_train in data_train]
    comments = vetorizador.fit_transform(comments)
    return BernoulliNB().fit(comments, scores)

def set_format(lista_commen, pred_scores):
    '''Return in format that Jinja2 understand, a list of dict'''
    data = [[c,s] for c,s in zip(lista_commen, pred_scores)]
    return pd.DataFrame(data, columns=['Comment','Score']).to_dict('records')

def run(lista_commen, lang):
    train = get_data(lang)
    vetorizador = CountVectorizer(binary = 'true')
    model = start_training(train, vetorizador)
    pred = model.predict(vetorizador.transform(lista_commen))
    pred_scores = ['Positive' if score==1 else 'Negative' for score in pred]
    return set_format(lista_commen, pred_scores)