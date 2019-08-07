import sys
import time
import os
import os.path
from os import path

####
import reader
import peak_detection
import trends
import news_scraper
import fake_news_classifier
import text_cleaner
import json_handler
import xlsx_to_csv
import filters
####

from googlesearch import search_news
from newspaper import Article

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
OUTPUT_XLSX = '../data/output_data.xlsx'
# File path to our input firm List
INPUT_FIRMS = ''

###################################################################

# TODO:
# - Finish rankings.
# - Implement relevancy filtering.
# - Implement fake news filtering.
# - Add command line shortcuts to skip menu.
# - Document
# - Finish accompying jupyter notebook examples.
# - Fix print lines inconsistencies (Print at the top!)
# - Move article download from acquisitions to news_scraper.
# - Add timestamp to output files
# - Enter to continue before clearing.
# - Check to see if TrendFinder runs from current directory.

def acquisitions():

    # Naive method -- news scraper downloads articles and compares title against acquisition matches list.
    acquisition_matches = ["buys", "buy", "bought", "acquires", "acquire", "acquisitions", "acquisition", "purchases", "purchase",
                           "merger", "merge", "merges, ""merging", "invested", "invests", "invest", "secure"]

    # Lambda functions used to check if the news article contains any acqusition terms.
    contains_acquisition = lambda x: sub_contains(x)
    sub_contains = lambda y: all(y in s for s in acquisition_matches)

    # Ensure that there's an input path to download firms from.
    if not INPUT_FIRMS:
        print('No firms are loaded to run Acquisitions.')
        input("Press Enter to continue...")
        return

    # If neither of our fake news classifiers exist, create & store them
    if not path.exists(TFIDF_PKL) or not path.exists(NB_PKL):
        fake_news_classifier.create_model(TRAIN_PKL, TFIDF_PKL, NB_PKL)
    tfidf = fake_news_classifier.load_model(TFIDF_PKL)
    nb_body = fake_news_classifier.load_model(NB_PKL)

    firms = reader.read_firms(INPUT_FIRMS)

    all_news = {}
    all_news['firms'] = {}
    for firm in firms:
        newsPaper = {
            "articles": []
        }
        print("------------------------------------------------------------")
        print("Searching for acuisitions: ", firm)
        for result in search_news(query=firm+" acquisition", tld="co.in", num=10, stop=5, pause=2):
            try:
                article = {}
                news = Article(result)
                news.download()
                news.parse()
                news.nlp()
                print("Downloaded: ", news.title)
                if any([x in acquisition_matches for x in news.title.lower().split()]):
                    print("*"*10 + "Acquisition found." + "*"*10)
                    article['link'] = result
                    article['title'] = news.title
                    article['text'] = news.text
                    article['firm'] = firm
                    article['keywords'] = news.keywords
                    if news.publish_date:
                        article['published'] = news.publish_date.isoformat()
                    else:
                        article['published'] = news.publish_date
                    article['author'] = news.authors
                    newsPaper['articles'].append(article)
            except Exception as e:
                print("Error: Article could not be downloaded.")
        if bool(newsPaper['articles']):
            newsPaper = news_scraper.mark_relevancy(newsPaper)
            all_news['firms'][firm] = newsPaper

    df_acq = json_handler.json_to_pd(all_news)
    if not df_acq.empty:
        df_acq = text_cleaner.clean(df_acq)
        # Removes some unnecessary columns.
        df_acq = df_acq.drop(columns = 'text')
        df_acq = df_acq.drop(columns = 'author')
        df_acq = fake_news_classifier.classify(tfidf, nb_body, df_acq)
        # Removes any rows in our df that are fake or do not have enough relevancy to the firm.
        print("Filtering dataframe for labels and relevancy.")
        df_acq = filters.filter_label(df_acq)
        df_acq = filters.filter_relevancy(df_acq)
        df_acq.to_excel(OUTPUT_XLSX)
        print("All relevant news articles downloaded to ", OUTPUT_XLSX)
    else:
        df_acq.to_excel(OUTPUT_XLSX)
        print("No articles found.")
    input("Press Enter to continue...")

def trend_menu():

    # switch-case for Trend Menu
    def trend_switch(menu_choice):
        switcher = {
            0: settings,
            1: run,
            9: back
        }
        return switcher.get(menu_choice)
    # Loads input list while still keeping environment inside of the menu
    def load_prompt():
        global INPUT_FIRMS
        clear()
        title('Load Firm List')
        print('\n\n\n\n\n')
        print('*'*30)
        print('NOTE: All data files are to be stored under the data folder. Any files not saved in this folder',
        'will not be accessible.')
        print('Acceptable Firm Lists include .xlsx and .csv files')
        print('Do NOT include \'../data/\' in your file path.')
        print('\n\n\n')
        print("Current Firm List Input: {0}".format(INPUT_FIRMS if bool(INPUT_FIRMS) else "nothing loaded"))
        print('\n')
        input_filename = input("Please enter the firm list file name or 'quit' to return to the Trend Menu.\n>>> ")
        if input_filename.lower() == 'quit':
            print('Quitting without saving.')
            input("Press Enter to continue...")
        else:
            INPUT_FIRMS = '../data/' + input_filename
            print('Firm list file name updated!')
            input("Press Enter to continue...")

    def settings():
        print("Not yet implemented.")
        input("Press Enter to continue...")

    def run():
        nonlocal done
        # If no firms are loaded, return to the trend menu.
        if not INPUT_FIRMS:
            print('No firms are loaded to run Trend Finder.')
            input("Press Enter to continue...")
            return
        # Pass CSV to reader to clean & load firm names.
        firms = reader.read_firms(INPUT_FIRMS)

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
                print("-"*40)
                print("Searching for trends in: ", firm)
            except Exception as e:
                print(e)
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
                print("Peak Detected!")
                newsPaper = news_scraper.download_articles(firm)
                newsPaper = news_scraper.mark_relevancy(newsPaper)
                news['firms'][firm] = newsPaper

        df_peaks = json_handler.json_to_pd(news)
        if not df_peaks.empty:
            df_peaks = text_cleaner.clean(df_peaks)
            # Removes some unnecessary columns.
            df_peaks = df_peaks.drop(columns = 'text')
            df_peaks = df_peaks.drop(columns = 'author')
            df_peaks = fake_news_classifier.classify(tfidf, nb_body, df_peaks)
            # Removes any rows in our df that are fake or do not have enough relevancy to the firm.
            print("Filtering dataframe for labels and relevancy.")
            df_peaks = filters.filter_label(df_peaks)
            df_peaks = filters.filter_relevancy(df_peaks)
            df_peaks.to_excel(OUTPUT_XLSX)
            print("All relevant news articles downloaded to ", OUTPUT_XLSX)
        else:
            df_peaks.to_excel(OUTPUT_XLSX)
            print("No articles found.")
         = False
        input("Press Enter to continue...")

    def back():
        nonlocal done
        done = True

    done = False
    while(not done):
        clear()
        print('{0:^30s}'.format('Trend Options'))
        print('-'*40)
        print("\n\n\n")
        print("Please select an option:\n")
        print("[0] Adjust Settings")
        print("[1] Run")
        print("[9] Back")
        print("\n")
        menu_choice = input("Enter Integer Choice.\n>>> ")

        try:
            menu_choice = eval(menu_choice)
            trend_switch(menu_choice)()
        except Exception as e:
            print(e)
            print("Error -- invalid input entered.")
            input("Press Enter to continue...")
            continue


def ranking_menu():
    print("Not yet implemented")
    input("Press Enter to continue...")

def load_prompt():
    global INPUT_FIRMS
    clear()
    title('Load Firm List')
    print('\n\n\n\n\n')
    print('*'*30)
    print('NOTE: All data files are to be stored under the data folder. Any files not saved in this folder',
    'will not be accessible.')
    print('Acceptable Firm Lists include .xlsx and .csv files')
    print('.xlsx will automatically be converted to .csv')
    print('Do NOT include \'../data/\' in your file path.')
    print('\n\n\n')
    print("Current Firm List Input: {0}".format(INPUT_FIRMS if bool(INPUT_FIRMS) else "nothing loaded"))
    print('\n')
    input_filename = input("Please enter the firm list file name or 'back' to return to the Main Menu.\n>>> ")

    if input_filename.lower() == 'back':
        print('Returning to the Main Menu.')
        input("Press Enter to continue...")
    elif '.xlsx' in input_filename:
        input_filename = '../data/' + input_filename
        if path.exists(input_filename):
            print('Converting to .csv')
            xlsx_to_csv.convert(input_filename)
            INPUT_FIRMS = input_filename.split('.xlsx')[0] + '.csv'
            print('Firm list file name updated!')
            input("Press Enter to continue...")
        else:
            print('File does not exist.')
            input("Press Enter to continue...")
            load_prompt()
    elif '.csv' in input_filename:
        input_filename = '../data/' + input_filename
        if path.exists(input_filename):
            INPUT_FIRMS = input_filename
            print('Firm list file name updated!')
            input("Press Enter to continue...")
        else:
            print('File does not exist.')
            input("Press Enter to continue...")
            load_prompt()
    else:
        print('Improper file format entered. Please try again.')
        input("Press Enter to continue...")
        load_prompt()

def output_prompt():
    global OUTPUT_XLSX
    clear()
    title('Output File Location')
    print('\n\n\n\n\n')
    print('*'*30)
    print('NOTE: All data files are saved under the /data/ folder.')
    print('Output file format is a .xlsx.')
    print('Do NOT include \'../data/\' in your file path.')
    print('\n\n\n')
    print("Current Ouput File Location: {0}".format(OUTPUT_XLSX))
    print('\n')
    output_filename = input("Please enter the output file name or 'back' to return to the Trend Menu.\n>>> ")

    if output_filename.lower() == 'back':
        print('Returning to the Main Menu.')
        input("Press Enter to continue...")
    elif '.xlsx' in output_filename:
        print('Changing output file location.')
        OUTPUT_XLSX = '../data/' + output_filename
        print("Current Ouput File Location: {0}".format(OUTPUT_XLSX))
        input("Press Enter to continue...")
    else:
        print('Improper file format entered. Please try again.')
        input("Press Enter to continue...")
        output_prompt()

def main():

    # switch-case used for the Main Menu
    def menu_switch(menu_choice):
        switcher = {
            0: trend_menu,
            1: acquisitions,
            2: ranking_menu,
            3: load_prompt,
            4: output_prompt,
            9: exit
        }
        return switcher.get(menu_choice)

    def exit():
        nonlocal done
        done = True
        clear()

    done = False
    while(not done):
        clear()
        title('TrendFinder Main Menu')
        print("\n\n\n\n\n")
        print("Please select a feature to run:\n")
        print("[0] Trends")
        print("[1] Acquisitions")
        print("[2] Rankings")
        print("[3] Load Firm List")
        print("[4] Change Output File Location")
        print("[9] Exit")
        print("\n\n")
        menu_choice = input("Enter Integer Choice.\n>>> ")

        try:
            menu_choice = eval(menu_choice)
            menu_switch(menu_choice)()
        except Exception as e:
            print(e)
            print("Error -- invalid input entered.")
            input("Press Enter to continue...")
            continue



# Clears terminal/command prompt.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
# Prints menu title
def title(title):
    print('{0:^30s}'.format(title))
# Runs main on calling the script from the command line.
if __name__ == "__main__":
    main()
