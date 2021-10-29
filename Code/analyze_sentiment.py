import os
import sys
import json
from textblob import TextBlob
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():
    directory = sys.argv[1]
    cwd = os.getcwd()
    # Analyze each file
    analyzer = SentimentIntensityAnalyzer()
    os.chdir(directory)
    filelist = [f for f in os.listdir('.') if '.json' in f]
    length = len(filelist)
    step = int(length / 100)
    count = 0
    for filename in filelist:
        # file_prefix = filename.split('.')[0]
        json_data = {}
        # Open the old file
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Analyze each Tweet
        if 'data' in json_data.keys():
            for tweet in json_data['data']:
                tweet_textblob = TextBlob(tweet['text'])
                tweet['sentiment'] = tweet_textblob.sentiment.polarity
                tweet['subjectivity'] = tweet_textblob.sentiment.subjectivity
                tweet['vader'] = analyzer.polarity_scores(tweet['text'])['compound']
        
        # Write to a new file
        # os.chdir(cwd)
        # os.chdir('../Data/Graphs')
        with open(filename, 'w') as write_file:
            write_file.write(json.dumps(json_data, indent=4, sort_keys=True))
        # os.chdir(cwd)
        # os.chdir(directory)
        count = count + 1
        if count % step == 0:
            print(str(count * 100 / length) + '%')

if __name__ == "__main__":
    main()