# The purpose of this script is to transform and save the 
# training data of the Sentiment Analysis model in a txt file 

import pandas as pd

def get_data():
    folder = "./data/"
    #English
    with open(folder + "imdb_labelled.txt", "r") as files:
        data_en = files.read().split('\n')
    with open(folder + "amazon_cells_labelled.txt", "r") as files:
        data_en += files.read().split('\n')
    with open(folder + "yelp_labelled.txt", "r") as files:
        data_en += files.read().split('\n')
    #Portuguese
    df = pd.read_csv(folder + "Train3Classes.csv",sep=';').drop(columns=['id','tweet_date','query_used']).rename(columns={'tweet_text':'Comment','sentiment':'Score'}).to_csv('./data/train_pt.csv')
    return data_en

def data_munging_en(data):
    new_data = []
    for data_row in data:
        if len(data_row.split("\t")) == 2 and data_row.split("\t")[1] != "":
            new_data.append(data_row.split("\t"))
    return new_data

def save_data_en(new_data):
    pd.DataFrame(new_data, columns=['Comment','Score']).to_csv('./data/train_en.csv')

data_en = get_data()
new_data_en = data_munging_en(data_en)
save_data_en(new_data_en)