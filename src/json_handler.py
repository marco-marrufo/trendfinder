import json
import pandas as pd

def save_json(news, jsonPath):
    print('Saving articles . . . in {}'.format(jsonPath))
    with open(jsonPath, 'w') as outfile:
        json.dump(news, outfile)

def load_json(jsonPath):
    with open(jsonPath) as json_data:
        news = json.load(json_data)
        return news

def json_to_pd(news):
    df_pred = pd.DataFrame()
    # Creates a dataframa from all articles, one row per articles
    for i, firm in enumerate((list(news['firms']))):
        articles = list(news['firms'][firm]['articles'])
        if i == 0:
            df_pred = pd.DataFrame.from_dict(articles)
        else:
            new_df = pd.DataFrame.from_dict(articles)
            df_pred = pd.concat([df_pred, new_df], ignore_index = True)

    return df_pred
