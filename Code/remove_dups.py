import json
import os
import sys

os.chdir('../Data/CONVERSATIONS')
filelist = [f for f in os.listdir('.') if '.json' in f]
for filename in filelist:
    json_data = {}
    try:
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
        tweet_list = []
        for tweet in json_data['data']:
            if tweet not in tweet_list:
                tweet_list.append(tweet)
        json_data['data'] = tweet_list
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(json_data, indent=4, sort_keys=True))
    except:
        print("Error with file " + filename + ", continuing on")