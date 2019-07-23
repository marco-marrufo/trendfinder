import sys
import os.path
from os import path
import reader
import peak_detection
import trends
import news_scraper
import fake_news_classifier
import text_cleaner
import json_handler

############ PEAK DETECTION SETTINGS ############################

LAG = 5
THRESHOLD = 3
INFLUENCE = 0.5

# MODE can either be 'std' or 'mad'.
# --- 'std' ---
# Mean average
# Standard deviation
# --- 'mad' ---
# Median average
# Median absolute deviation

MODE = 'std'

# LOOK_BACK := How many days we want to look back from the last day for detecting peaks in our trend data.
# If you're not running TrendFinder daily, then you use look back to accomodate for any days where the app isn't run.
# E.G., If you run TrendFinder every 2 days, set LOOK_BACK to 1, every 3 days, set LOOK_BACK to 2, and so on.
LOOK_BACK = 0
###################################################################

##################### FILE PATH SETTINGS ##########################

# File path to store our training dataset for the Fake News classifiers
TRAIN_PKL = '../data/cleaned_df.pkl'
# File path for storing/loading TFIDF Vectorizer
TFIDF_PKL = '../data/tfidf.pkl'
# File path for storing/loading Naive Bayes Polynomial Classifier
NB_PKL = '../data/nb.pkl'
# File path to save news articles from peak detections as a JSON
PEAK_JSON = '../data/peak_articles.json'
# File path to save news articles from peak detections as XLSX
PEAK_XLSX = '../data/peak_articles.xlsx'

def main():
    # Pass CSV as first command line argument
    input_filename = sys.argv[1]
    firms = reader.read_firms(input_filename)

    # If neither of our fake news classifiers exist, create & store them
    if not path.exists(TFIDF_PKL) or not path.exists(NB_PKL):
        fake_news_classifier.create_model(TRAIN_PKL, TFIDF_PKL, NB_PKL)
    tfidf = fake_news_classifier.load_model(TFIDF_PKL)
    nb_body = fake_news_classifier.load_model(NB_PKL)

    news = {}
    news['firms'] = {}
    for firm in firms:
        # Downloading the trend data.
        try:
            trend = trends.get_trends(firm)
        except Exception as e:
            print(e)
            #print("Error downloading trend data for ", firm)
            continue
        # If there's no data to download, continue to the next firm.
        if trend.empty:
            continue
        # Getting only the trend values
        y=trend.iloc[:,0].values

        sig, avg, dev = peak_detection.thresh_alg(y, LAG, THRESHOLD, INFLUENCE, MODE)

        # Checking to see if our signal has any peaks (1's)
        end = len(sig) - 1
        if any(sig[end-LOOK_BACK:end+1]):
            # If a peak is detected, download news articles and adds relevancy score.
            print(firm, ": Peak Detected")
            newsPaper = news_scraper.download_articles(firm)
            newsPaper = news_scraper.mark_relevancy(newsPaper)
            news['firms'][firm] = newsPaper

    df_peaks = json_handler.json_to_pd(news)
    if not df_peaks.empty:
        df_peaks = text_cleaner.clean(df_peaks)
        df_peaks = fake_news_classifier.classify(tfidf, nb_body, df_peaks)
        print(df_peaks['title'], df_peaks['label'])
        df_peaks.to_excel()

# Runs main on calling the script from the command line.
if __name__ == "__main__":
    main()
