import pandas as pd
import joblib
import nltk
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, recall_score, precision_score
from sklearn.naive_bayes import MultinomialNB

def create_model(dfPath, tfidfPath, nbPath):
    df = pd.read_pickle(dfPath)

    print('Creating TFIDF & NB Models.')
    # Preparing the target and predictors for modeling.
    X_body_text = df['clean_text'].values
    y = df['label'].values

    # Creating and saving our TFIDF Vectorizer
    tfidf = TfidfVectorizer(ngram_range=(1,2), max_df=0.85, min_df=0.01)
    X_body_tfidf = tfidf.fit_transform(X_body_text)
    joblib.dump(tfidf, tfidfPath)

    # Seperating our data in training/test sets.
    indices = df.index.values
    X_body_tfidf_train, X_body_tfidf_test, \
    y_body_train, y_body_test, \
    indices_body_train, indices_body_test = train_test_split(X_body_tfidf,y,indices,test_size=0.2,random_state=42)

    # Creating and saving our NB Polynomial Classifier
    nb_body = MultinomialNB()
    nb_body.fit(X_body_tfidf_train, y_body_train)
    joblib.dump(nb_body, nbPath)

    # Printing Accuracy & F1 Scores from Training/Testing sets

    y_body_train_pred = nb_body.predict(X_body_tfidf_train)
    # Print metrics for Training Set
    print('Naive Bayes In Sample F1 and Accuracy Scores:')
    print('F1 score {:.4}%'.format(f1_score(y_body_train, y_body_train_pred, average='macro')*100))
    print ('Accuracy score {:.4}%'.format(accuracy_score(y_body_train, y_body_train_pred)*100))

    y_body_pred = nb_body.predict(X_body_tfidf_test)
    # Print metrics for Test Set
    print('Naive Bayes F1 and Accuracy Scores:')
    print('F1 score {:.4}%'.format(f1_score(y_body_test, y_body_pred, average='macro')*100))
    print ('Accuracy score {:.4}%'.format(accuracy_score(y_body_test, y_body_pred)*100))

def load_model(modelPath):
    print('Loading ', modelPath, ' . . .')
    model = joblib.load(modelPath)
    return model

def classify(tfidf, nb_body, df):
    pred_body_text = df['clean text'].values
    pred_body_tfidf = tfidf.transform(pred_body_text)

    df['label'] = nb_body.predict(pred_body_tfidf)

    return df
