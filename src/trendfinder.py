import sys
import time
import os
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
# File path to our input firm List
INPUT_FIRMS = ''

#################
SLEEP_TIME = 1

def acquisition_menu():
    print("Not yet implemented")
    time.sleep(SLEEP_TIME)

def trend_menu():

    # switch-case for Trend Menu
    def trend_switch(menu_choice):
        switcher = {
            0: load_prompt,
            1: output_prompt,
            2: settings,
            3: run,
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
            time.sleep(SLEEP_TIME)
        else:
            INPUT_FIRMS = '../data/' + input_filename
            print('Firm list file name updated!')
            time.sleep(SLEEP_TIME)

    def output_prompt():
        print("Not yet implemented.")
        time.sleep(SLEEP_TIME)

    def settings():
        print("Not yet implemented.")
        time.sleep(SLEEP_TIME)

    def run():
        nonlocal not_done
        # If no firms are loaded, return to the trend menu.
        if not INPUT_FIRMS:
            print('No firms are loaded to run Trend Finder.')
            time.sleep(SLEEP_TIME)
            return
        # Pass CSV as first command line argument
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
            df_peaks = df_peaks.drop(columns = 'text')
            df_peaks = fake_news_classifier.classify(tfidf, nb_body, df_peaks)
            df_peaks.to_excel(PEAK_XLSX)
            print("All relevant news articles downloaded to ", PEAK_XLSX)
        else:
            df_peaks.to_excel(PEAK_XLSX)
            print("No articles found.")
        not_done = False
        time.sleep(SLEEP_TIME)

    def back():
        nonlocal not_done
        not_done = False

    not_done = True
    while(not_done):
        clear()
        print('{0:^30s}'.format('Trend Options'))
        print('-'*40)
        print("\n\n\n")
        print("Please select an option:\n")
        print("[0] Load Firm List XLSX")
        print("[1] Set Output XLSX")
        print("[2] Adjust Settings")
        print("[3] Run")
        print("[9] Back")
        print("\n")
        menu_choice = input("Enter Integer Choice.\n>>> ")

        try:
            menu_choice = eval(menu_choice)
            trend_switch(menu_choice)()
        except Exception as e:
            print("Error -- invalid input entered.")
            time.sleep(SLEEP_TIME)
            continue


def ranking_menu():
    print("Not yet implemented")
    time.sleep(SLEEP_TIME)

def main():

    # switch-case used for the Main Menu
    def menu_switch(menu_choice):
        switcher = {
            0: trend_menu,
            1: acquisition_menu,
            2: ranking_menu,
            9: exit
        }
        return switcher.get(menu_choice)

    def exit():
        nonlocal not_done
        not_done = False
        clear()

    not_done = True
    while(not_done):
        clear()
        title('TrendFinder Main Menu')
        print("\n\n\n\n\n")
        print("Please select a feature to run:\n")
        print("[0] Trends")
        print("[1] Acquisitions")
        print("[2] Rankings")
        print("[9] Exit")
        print("\n\n")
        menu_choice = input("Enter Integer Choice.\n>>> ")

        try:
            menu_choice = eval(menu_choice)
            menu_switch(menu_choice)()
        except Exception as e:
            print("Error -- invalid input entered.")
            time.sleep(SLEEP_TIME)
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
