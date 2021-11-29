import requests
import os
import json
import time
from time import sleep
import sys

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")
tweet_fields = 'tweet.fields=author_id,conversation_id,created_at,public_metrics,text,referenced_tweets'

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    start = time.time()
    # os.chdir('../Data/CONVERSATIONS/TEMP')
    os.chdir('../Data/Graphs')
    filelist = [f for f in os.listdir('.') if '.json' in f]
    total_convs = len(filelist)
    step = total_convs // 100
    print('Total Convs: ' + str(total_convs))
    i = 0
    percent = 0
    conv_id_list = []
    # Create the list with each of the IDs
    for filename in filelist:
        conv_id_list.append(filename.split('_')[1].split('.')[0])
    
    # Use the list to query all tweets
    while i < total_convs:
        ids = 'ids='
        max = 10
        if (i + max) >= total_convs:
            max = total_convs - i - 1
        for count in range(0, max):
            ids = ids + conv_id_list[i] + ','
            i += 1
        ids = ids + conv_id_list[i]
        i += 1
        url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
        json_response = {}
        success = False
        while not success:
            try:
                json_response = connect_to_endpoint(url)
                success = True
            except:
                print("Error, trying again in 10 seconds")
                sleep(10)

        # Add each successful tweet to the results
        if 'data' in json_response.keys():
            for tweet in json_response['data']:
                filename = 'conv_' + tweet['id'] + '.json'
                json_data = {}
                with open(filename, 'r') as json_file:
                    json_data = json.load(json_file)
                if 'data' in json_data.keys():
                    json_data['data'].append(tweet)
                else:
                    json_data['data'] = [tweet]
                json_data['meta']['result_count'] = json_data['meta']['result_count'] + 1
                with open(filename, 'w') as json_file:
                    json_file.write(json.dumps(json_data, indent=4, sort_keys=True))

        sleep(3)

        # if ((i // step) > percent):
        #     percent = i // step
        #     totalTime = time.time() - start
        #     estTimeTotal = totalTime * (100 / percent)
        #     estTimeRemaining = int(estTimeTotal - totalTime)
        #     estHrs = int(estTimeRemaining // 3600)
        #     estMins = int((estTimeRemaining % 3600) // 60)
        #     estSecs = int((estTimeRemaining % 3600) % 60)
        #     print(str(percent) + "%, approximately " + str(estHrs) + ":" + str(estMins) + ":" + str(estSecs) + " remaining")
    
    


if __name__ == "__main__":
    main()