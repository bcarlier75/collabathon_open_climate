import numpy as np
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode
import string
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sys import argv

#nltk.download('stopwords')
#nltk.download('punkt')


def pre_process_review(review):
    # convert input corpus to lower case.
    review = review.lower()
    # collecting a list of stop words from nltk and punctuation form
    # string class and create single array.
    stopset = stopwords.words('english') + list(string.punctuation)
    # remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input corpus in word tokens
    review = " ".join([i for i in word_tokenize(review) if i not in stopset])
    # remove non-ascii characters
    review = unidecode(review)
    return review


def pre_process_csv():
    # give the path of the file in first argument
    # --> eg: python pre_process reviews.csv
    df = pd.read_csv(argv[1])
    lemmatizer = WordNetLemmatizer()
    for i, sentence in enumerate(df.iloc[:, 1]):
        sentence = pre_process_review(sentence)
        words = word_tokenize(sentence)
        new_sentence = ' '.join(words)
        df.iloc[i, 1] = new_sentence
    df.to_csv('review_preprocess.csv', index=False)
    print('Preprocessed reviews strored to reviews_preprocess.csv')

pre_process_csv()