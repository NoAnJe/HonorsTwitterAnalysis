import json
import sys
import os

# First step: set up dictionary for likes, retweets, positivity, etc
data = {"RBG": {}, "ACB": {}, "SCOTUS": {}, "RBG_DAY": {}, "ACB_DAY": {}, "SCOTUS_DAY": {}}
dataRef = ["RBG", "ACB", "SCOTUS"]
dataDayRef = ["RBG_DAY", "ACB_DAY", "SCOTUS_DAY"]

for day in range(1,31):
    for hour in range(0,24):
        for name in dataRef:
            data[name]["09"+str(day).zfill(2)+str(hour).zfill(2)]= {
                "TotalTweets": 0, "TotalLikes": 0, "AvgLikes": 0, "TotalRts": 0,
                "AvgRts": 0, "SentimentTotal": 0, "AvgSentiment": 0}
for day in range(1,32):
    for hour in range(0,24):
        for name in dataRef:
            data[name]["10"+str(day).zfill(2)+str(hour).zfill(2)]= {
                "TotalTweets": 0, "TotalLikes": 0, "AvgLikes": 0, "TotalRts": 0,
                "AvgRts": 0, "SentimentTotal": 0, "AvgSentiment": 0}

for day in range(1,31):
    for name in dataDayRef:
        data[name]["09"+str(day).zfill(2)] = {
            "TotalTweets": 0, "TotalLikes": 0, "AvgLikes": 0, "TotalRts": 0,
            "AvgRts": 0, "SentimentTotal": 0, "AvgSentiment": 0}
for day in range(1,32):
    for name in dataDayRef:
        data[name]["10"+str(day).zfill(2)] = {
            "TotalTweets": 0, "TotalLikes": 0, "AvgLikes": 0, "TotalRts": 0,
            "AvgRts": 0, "SentimentTotal": 0, "AvgSentiment": 0}

# Save the data to a file
def output_data():
    filename = "compiled_data.json"
    with open(filename, 'w') as compiled_file:
        compiled_file.write(json.dumps(data, indent=4, sort_keys=True))

def analyze_tweet(tweet, nameRef):
    text = tweet['text']
    full_date_str = tweet['created_at']
    ref_str = full_date_str.split('-')[1] + \
                full_date_str.split('-')[2].split('T')[0] + \
                full_date_str.split('T')[1].split(':')[0]
    data[nameRef][ref_str]["TotalTweets"] = data[nameRef][ref_str]["TotalTweets"] + 1
    data[nameRef][ref_str]["TotalLikes"] = data[nameRef][ref_str]["TotalLikes"] + tweet["public_metrics"]["like_count"]
    data[nameRef][ref_str]["TotalRTs"] = data[nameRef][ref_str]["TotalRts"] + tweet["public_metrics"]["retweet_count"]

def summarize_tweets():
    for name in dataRef:
        for ref in data[name]:
            if (data[name][ref]["TotalTweets"] != 0):
                data[name][ref]["AvgLikes"] = data[name][ref]["TotalLikes"] / data[name][ref]["TotalTweets"]
                data[name][ref]["AvgRts"] = data[name][ref]["TotalRts"] / data[name][ref]["TotalTweets"]
    for name in dataRef:
        nameDay = name + "_DAY"
        for ref in data[nameDay]:
            for hour in range(0,23):
                hr_refstr = ref+str(hour).zfill(2)
                data[nameDay][ref]["TotalTweets"] = data[nameDay][ref]["TotalTweets"]+data[name][hr_refstr]["TotalTweets"]
                data[nameDay][ref]["TotalLikes"] = data[nameDay][ref]["TotalLikes"]+data[name][hr_refstr]["TotalLikes"]
                data[nameDay][ref]["TotalRts"] = data[nameDay][ref]["TotalRts"]+data[name][hr_refstr]["TotalRts"]
            if (data[nameDay][ref]["TotalTweets"] != 0):
                data[nameDay][ref]["AvgLikes"] = data[nameDay][ref]["TotalLikes"] / data[nameDay][ref]["TotalTweets"]
                data[nameDay][ref]["AvgRts"] = data[nameDay][ref]["TotalRts"] / data[nameDay][ref]["TotalTweets"]

def main():
    directory = sys.argv[1]
    # Scan through every file in the directory... including name parsing
    os.chdir(directory)
    filelist = [f for f in os.listdir('.') if '.json' in f]
    for filename in filelist:
        # Figure out which figure this belongs to - this ensures it's part of the right analysis
        ref_name = ""
        if dataRef[0] in filename:
            ref_name = dataRef[0]
        elif dataRef[1] in filename:
            ref_name = dataRef[1]
        elif dataRef[2] in filename:
            ref_name = dataRef[2]
        else:
            continue

        # Open the file itself
        with open(filename,'r') as tweet_file:
            json_obj = json.load(tweet_file)
            if(json_obj["meta"]["result_count"] != 0):
                for tweet in json_obj["data"]:
                    analyze_tweet(tweet, ref_name)
    
    summarize_tweets()
    output_data()

if __name__ == "__main__":
    main()