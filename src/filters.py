import pandas as pd


def filter_label(df):
    df = df[df.label != 1]
    return df

def filter_relevancy(df):
    df = df[df.relevancy != 0]
    return df 
