import os
import sys
import json

def flip_tree(json_obj):
    tmp_dict = {}
    for tweet in json_obj["data"]:
        if "referenced_tweets" in tweet.keys():
            for subtweet in tweet["referenced_tweets"]:
                if "replied_to" in subtweet["type"]:
                    parent_tweet = subtweet["id"]
                    id = tweet["id"]
                    if parent_tweet in tmp_dict.keys:
                        tmp_dict[parent_tweet].append(id)
                    else:
                        tmp_dict[parent_tweet] = [id]
    for tweet in json_obj["data"]:
        id = tweet["id"]
        if id in tmp_dict.keys:
            tweet["replied_tweets"] = tmp_dict[id]

def main():
    directory = sys.argv[1]
    os.chdir(directory)
    filelist = [f for f in os.listdir('.') if '.json' in f]
    for filename in filelist:
        json_obj = {}
        with open(filename, 'r') as json_file:
            json_obj = json.load(json_file)
        flip_tree(json_obj)
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(json_obj, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()