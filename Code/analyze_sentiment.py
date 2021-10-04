import os
import sys
import json
from textblob import TextBlob

def main():
    directory = sys.argv[1]
    cwd = os.getcwd()
    # Analyze each file
    os.chdir(directory)
    filelist = [f for f in os.listdir('.') if '.json' in f]
    for filename in filelist:
        # file_prefix = filename.split('.')[0]
        json_data = {}
        # Open the old file
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
        
        # Analyze each Tweet
        for tweet in json_data['data']:
            tweet_textblob = TextBlob(tweet['text'])
            tweet['sentiment'] = tweet_textblob.sentiment.polarity
            tweet['subjectivity'] = tweet_textblob.sentiment.subjectivity
        
        # Write to a new file
        os.chdir(cwd)
        os.chdir('../Data/Graphs')
        with open(filename, 'w') as write_file:
            write_file.write(json.dumps(json_data, indent=4, sort_keys=True))
        os.chdir(cwd)
        os.chdir(directory)

if __name__ == "__main__":
    main()