import pandas as pd
import numpy as np
import string
import re
from nltk.corpus import stopwords
nltk_stopwords = stopwords.words('english')
remove_punctuation = '!"$%&\'()*+,-./:;<=>?@[\\]“”^_`{|}~’'

def clean(df):
    df_copy = df.copy()
    df_copy = clean_column(df_copy, 'text', 'clean text')
    filtration(df_copy, 'clean text')
    return df_copy

def clean_column(dataframe, column_to_clean, new_col):
    df_copy = dataframe.copy()
    df_copy['copied_column'] = df_copy[column_to_clean]
    df_copy['copied_column'] = df_copy['copied_column'].str.lower()
    cleaned_column = []
    for label in df_copy.index:
        row = df_copy.loc[label, :]['copied_column']
        clean = [x for x in row.split() if x not in string.punctuation]
        clean = [x for x in clean if x not in nltk_stopwords]
        clean = [x for x in clean if x not in string.digits]
        clean = [x for x in clean if x not in remove_punctuation]
        clean = [x for x in clean if len(x) != 1]
        clean = " ".join(clean)
        clean = clean.strip()
        cleaned_column.append(clean)
    df_copy[new_col] = cleaned_column
    del df_copy['copied_column']
    return df_copy

def filtration(dataframe, column):
    # clean = list(map(lambda x: x.replace("#", ""), clean)) #we want to maintain hashtags!
    dataframe[column] = dataframe[column].apply(lambda x: x.replace('"', ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("’", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(":", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("…", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(".",""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("⋆", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ⋆ ", " "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("  ", " "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("$", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(",", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" alime ", " all time "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" alltime ", " all time "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(";", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("alime", "all time "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("atm", "at the moment"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ath ", " all time high "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("str8", "straight"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" v ", " very "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" #d", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ddos ", " distributed denial of service "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("btce", "btc"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("bitcoina", "bitcoin"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("rbitcoin", "bitcoin"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" – ", " "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("-&gt;", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ➤ ", " "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("◄►", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("◄", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ur ", " your "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" u ", " you "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("forthen", "for then"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("&gt;", "greater than"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("&lt;", "less than"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("lt", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("gt", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(":", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("&amp;", "and"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("ampamp", "and"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" amp ", " and "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("amp", "and"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" bu ", " but "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("/", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("...", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("(", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(")", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("“", '"'))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("”", '"'))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("‘", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("’", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("-"," "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("*", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("!", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("⬛️", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("\u200d", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f986", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f942", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f92f", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f911", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001F193", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ⭕ ", " "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("🤔", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("☞ ", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("[", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("]", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("{", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("}", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("ô", "o"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("ó", "o"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("é", "e"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("ï","i"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("®", ""))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("á", "a"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("ã", "a"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace("ç", "c"))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" jan ", " january "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" feb ", " february "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" mar ", " march "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" apr ", " april "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" jun ", " june "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" jul ", " july "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" aug ", " august "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" sept ", " september "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" oct ", " october "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" nov ", " november "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" dec ", " december "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" washinon ", " washington "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" dming ", " direct messaging "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" cust ", " customer "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" wcust ", " with customer "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" cc ", " credit card "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" gopros ", " go pros "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ultimatelyi ", " ultimately i "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 1hr ", " one hour "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" rep ", " representative "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" wunited ", " with united "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" mp# ", " mileage plus number "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" hrs ", " hours "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 4hours ", " four hours "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" laxewr ", " lax ewr "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" iadlax ", " iad lax "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" julystill ", " july still "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 30mins ", " 30 minutes "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" mins ", " minutes "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 5hours ", " 5 hours "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" checkhowever ", " check however "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" familyno ", " family "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 2nd ", " second "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 6hour ", " six hour "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" cuz ", " because "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" cause ", " because "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ideabuy ", " idea buy "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" fixem ", " fix them "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" properthey ", " proper they "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" americanair ", " american air "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" yea ", " yes "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" gnteed ", " guaranteed "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 6mo ", " 6 months "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" believei ", " believe "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" btw ", " by the way "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" intl ", " international "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" thxs ", " thanks "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" plususual ", " plus usual "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" fridaycant ", " friday can not "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" lhr ", " 1 hour "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" wheelsup ", " wheels up "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" tryna ", " try and "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 2hours ", " 2 hours "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" 1st ", " first "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" creditcard ", " credit card "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" luv ", " love "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" obv ", " obviously "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" patientyou ", " patient you "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" youwe ", " you have "))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(" uraniumone ", " uranium one "))
