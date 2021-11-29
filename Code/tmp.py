import os
import json

os.chdir('../Data/CONVERSATIONS')
filelist = [f for f in os.listdir('.') if '.json' in f]
total = 0
for filename in filelist:
    with open(filename, 'r') as tweet_file:
        json_obj = json.load(tweet_file)
        total += json_obj['meta']['result_count']
print("Total tweets: " + str(total))