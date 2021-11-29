import os
import sys
import json
import time

def set_levels(json_obj):
    level_dict = {}
    if 'data' in json_obj.keys():
        topTweet = 0
        currList = []
        for tweet in json_obj['data']:
            level_dict[tweet['id']] = {}
            if 'replied_tweets' in tweet.keys():
                level_dict[tweet['id']]['child'] = tweet['replied_tweets']
            else:
                level_dict[tweet['id']]['child'] = []
            if tweet['id'] == tweet['conversation_id']:
                level_dict[tweet['id']]['level'] = 1
            if 'referenced_tweets' in tweet.keys():
                for subtweet in tweet['referenced_tweets']:
                    if ('replied_to' in subtweet['type']) and (subtweet['id'] == tweet['conversation_id']):
                        currList.append(tweet['id'])
                        level_dict[tweet['id']]['level'] = 2

        while len(currList) > 0:
            currID = currList.pop(0)
            for tweetID in level_dict[currID]['child']:
                level_dict[tweetID]['level'] = level_dict[currID]['level'] + 1
                currList.append(tweetID)
        
        for tweet in json_obj['data']:
            if 'level' in level_dict[tweet['id']].keys():
                tweet['level'] = level_dict[tweet['id']]['level']
            else:
                tweet['level'] = -1

def flip_tree(json_obj):
    tmp_dict = {}
    if 'data' in json_obj.keys():
        for tweet in json_obj["data"]:
            if "referenced_tweets" in tweet.keys():
                for subtweet in tweet["referenced_tweets"]:
                    if "replied_to" in subtweet["type"]:
                        parent_tweet = subtweet["id"]
                        tweet_id = tweet["id"]
                        if parent_tweet in tmp_dict.keys():
                            tmp_dict[parent_tweet].append(tweet_id)
                        else:
                            tmp_dict[parent_tweet] = [tweet_id]
        for tweet in json_obj["data"]:
            tweet_id = tweet["id"]
            if tweet_id in tmp_dict.keys():
                tweet["replied_tweets"] = tmp_dict[tweet_id]

def main():
    # org_level = sys.argv[1]
    directory = sys.argv[1]
    os.chdir(directory)
    filelist = [f for f in os.listdir('.') if '.json' in f]
    length = len(filelist)
    step = int(length / 100)
    count = 0
    start = time.time()
    for filename in filelist:
        json_obj = {}
        with open(filename, 'r') as json_file:
            json_obj = json.load(json_file)
        # if '-ft' in org_level:
        flip_tree(json_obj)
        # elif '-l' in org_level:?
        set_levels(json_obj)
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(json_obj, indent=4, sort_keys=True))
        count = count + 1
        if count % step == 0:
            percent = round(count * 100 / length, 2)
            totalTime = time.time() - start
            estTimeTotal = totalTime * (100 / percent)
            estTimeRemaining = int(estTimeTotal - totalTime)
            estHrs = int(estTimeRemaining // 3600)
            estMins = int((estTimeRemaining % 3600) // 60)
            estSecs = int((estTimeRemaining % 3600) % 60)
            print(str(percent) + "%, approximately " + str(estHrs) + ":" + str(estMins) + ":" + str(estSecs) + " remaining")

if __name__ == "__main__":
    main()