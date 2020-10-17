#!/usr/bin/python2.7
# if required install twython with pip2.7 install --user twython
# the input filename is limit_post.csv in line 36, change it as needed. Must be a single column file.
# output file is sentiment_data.xlsx, change it when running the script multiple times. The 4th column (compound)
# has the sentiment scores.
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_sentiment(rating_data):
    """
    https: // github.com / cjhutto / vaderSentiment
    :return:
    """
    # from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    """rating_data['sent_neg'] = -10
    rating_data['sent_neu'] = -10
    rating_data['sent_pos'] = -10
    rating_data['sent_compound'] = -10"""
    for i in range(len(rating_data)):
        sentence = rating_data['Sentences'][i]
        print(sentence)
        print(sentence)
        ss = sid.polarity_scores(sentence)
        print(ss['pos'])
        rating_data.iloc[i, 1] = float(ss['neg'])
        # print(rating_data.TypeError: can only concatenate str (not "int") to striloc[i, 1])
        rating_data.iloc[i, 2] = ss['neu']
        rating_data.iloc[i, 3] = ss['pos']
        rating_data.iloc[i, 4] = ss['compound']
    return rating_data


rating_data = pd.read_csv("popular_tweets.csv", encoding='latin1')
rating_data = rating_data.rename(columns={rating_data.columns[0]: "Sentences"})


sentiment_data = get_sentiment(rating_data)
sentiment_data.to_excel("test_sentiment.xlsx", index = False)
print(" Written to test_sentiment.xlsx")
