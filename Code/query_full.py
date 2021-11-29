import requests
import os
import json
import time
from time import sleep
from bisect import bisect_left
import copy
import sys

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/all"

# Query string - for searching actual terms
acb = '(ACB OR (Amy Coney Barrett) OR Barrett OR Barret OR (Amy Coney) OR #ACB OR #AmyConeyBarrett)'
rbg = '(RBG OR (Ruth Ginsberg) OR Ginsberg OR #Ginsberg OR #RBG or #RuthBaderGinsberg)'
abortion = '(abortion OR (Roe Wade) OR (Planned Parenthood) OR Casey OR #RightToLife)'
not_rt = '-is:retweet'
rbg_query_str = f'{not_rt} {rbg} {abortion} lang:en'
acb_query_str = f'{not_rt} {acb} {abortion} lang:en'
sc_query_str = f'{not_rt} -{rbg} -{acb} {abortion} (SCOTUS OR Supreme Court OR (Justice Kennedy)) lang:en'
query_str = [rbg_query_str, acb_query_str, sc_query_str]
file_str = ['RBG', 'ACB', 'SC']

# Fields explained:
#   author_id : Twitter ID of the author
#   conversation_id : Conversation ID. Useful for tracking threads
#   created_at : Tweet time
#   public_metrics : Public metrics of the tweet, including Retweets, Likes, and Replies
#   text : Text of the Tweet
tweet_fields = 'author_id,conversation_id,created_at,public_metrics,text,referenced_tweets'

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_individual_tweets():
    # Set the appropriate times
    start_time = '2020-09-01T00:00:00Z' # Inclusive
    end_time = '2020-11-01T00:00:00Z'   # Exclusive

    os.chdir('../Data/INITIAL_SEARCH')
    conversation_ids = []
    id_tracker = []

    for file_start, querystr in zip(file_str, query_str):
        print("Starting on all Tweets in " + file_start)

        # Do the initial query
        query_params = {'query': querystr,'tweet.fields': tweet_fields,
                        'start_time': start_time, 'end_time': end_time, 'max_results': '500'}
        json_response = connect_to_endpoint(search_url, query_params)
        sleep(3)

        # Set up the file
        time = json_response['data'][0]['created_at']
        filename = file_start+time.replace(":", "").replace("Z","").replace(".000","")+".json"
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(json_response, indent=4, sort_keys=True))
        for tweet in json_response['data']:
            if ((int(tweet['conversation_id']) != int(tweet['id'])) or (int(tweet['public_metrics']['reply_count']) > 0)):
                if tweet['conversation_id'] not in id_tracker:
                    conversation_ids.append([tweet['id']])
                    id_tracker.append(tweet['conversation_id'])
                else:
                    position = id_tracker.index(tweet['conversation_id'])
                    conversation_ids[position].append(tweet['id'])
        total = json_response['meta']['result_count']
    
        # Loop until entire date/time set run
        while ("next_token" in json_response['meta'].keys()):
            # Update the next_token so that the next page is grabbed and run the next query
            query_params['next_token'] = json_response['meta']['next_token']
            json_response = connect_to_endpoint(search_url, query_params)
    
            # Set up the next file
            time = json_response['data'][0]['created_at']
            filename = file_start+time.replace(":", "").replace("Z","").replace(".000","")+".json"
            with open(filename, 'w') as json_file:
                json_file.write(json.dumps(json_response, indent=4, sort_keys=True))

            # Get all of the conversation IDs - if it's already in the list of IDs, ignore it
            for tweet in json_response['data']:
                if ((int(tweet['conversation_id']) != int(tweet['id'])) or (int(tweet['public_metrics']['reply_count']) > 0)):
                    if tweet['conversation_id'] not in id_tracker:
                        conversation_ids.append([tweet['id']])
                        id_tracker.append(tweet['conversation_id'])
                    else:
                        position = id_tracker.index(tweet['conversation_id'])
                        conversation_ids[position].append(tweet['id'])

            # With limitations on search size, must limit to searching less than 3 seconds
            total = total + json_response['meta']['result_count']
            sleep(3)

        # print(conversation_ids)
        print(total)
        print(len(conversation_ids))
    os.chdir('..')
    with open("conv_ids.json", 'w') as conv_id_file:
        conv_id_file.write(json.dumps({'tweet_ids': conversation_ids,
                                        'conv_ids': id_tracker},
                                        indent=4, sort_keys=False))

def get_conversations():
    print("Getting the individual conversations from the previously gathered data")
    os.chdir("../Data")
    i = 0
    empty_queries = []
    num_tweets = 0

    # Load in the file
    with open("conv_ids.json", 'r') as conv_id_file:
        json_obj = json.load(conv_id_file)
        os.chdir("CONVERSATIONS")

        for conv_id in json_obj['conv_ids']:
            # Query for the conversation - this will follow a similar format
            # to before, as there are a great many conversations which are also
            # quite long / have hundreds of replies.
            conv_str = f'conversation_id:{conv_id}'
            query_params = {'query': conv_str,'tweet.fields': tweet_fields, 'start_time': '2020-08-01T00:00:00Z', 'max_results': '500'}
            filename = "conv_"+conv_id+".json"
            success = 0
            while success != 1:
                try:
                    json_response = connect_to_endpoint(search_url, query_params)
                    success = 1
                except:
                    # Wait for a longer period
                    sleep(10)
            sleep(3)
            json_response['initial_id'] = json_obj['init_tweets'][conv_id]

            # Write the file with the entire tree
            num_tweets = num_tweets + json_response['meta']['result_count']
            with open(filename, 'w') as json_file:
                json_file.write(json.dumps(json_response, indent=4, sort_keys=True))
            
            # Print progress to terminal
            i = i + 1
            if (i % 396 == 0):
                print(str(i / 396) + '%')
    os.chdir('..')
    with open('results_json', 'w') as results:
        response = {'num_tweets': num_tweets, 'misses': empty_queries}
        results.write(json.dumps(response))

def get_next_page_conv():
    print("Getting the individual conversations from the previously gathered data")
    os.chdir("../Data")
    i = 0
    num_tweets = 0
    percent = 0

    # Load in the file
    with open("conv_ids.json", 'r') as conv_id_file:
        json_obj = json.load(conv_id_file)
        num_convs = len(json_obj['conv_ids'])
        print("Updating ~" + str(num_convs) + " conversations")
        step = num_convs // 100
        if num_convs < 100:
            step = 1
        os.chdir("CONVERSATIONS")
        start = time.time()
        if (num_convs == 0):
            print("No more conversations")
            return -1

        for conv_id in json_obj['conv_ids']:
            json_response = {}
            filename = "conv_"+conv_id+".json"
            with open(filename, 'r') as json_file:
                json_response = json.load(json_file)
            # Query for the conversation - this will follow a similar format
            # to before, as there are a great many conversations which are also
            # quite long / have hundreds of replies.
            conv_str = f'conversation_id:{conv_id}'
            query_params = {'query': conv_str,
                            'tweet.fields': tweet_fields,
                            'start_time': '2020-08-01T00:00:00Z',
                            'end_time': '2020-12-01T00:00:00Z', # can you add a new tag onto a conversation where the token is set?
                            'max_results': '500',
                            'next_token':json_response['meta']['next_token']}
            success = 0
            json_response_tmp = {}
            error = False
            errorCount = 0
            while success != 1:
                try:
                    json_response_tmp = connect_to_endpoint(search_url, query_params)
                    success = 1
                except Exception as e:
                    errorCount = errorCount + 1
                    print(e)
                    if errorCount > 10:
                        error = True
                        break
                    print("Trying again in 10 seconds")
                    sleep(10)
            sleep(3)

            if error:
                print("Continues to fail; quitting now")
                return -1

            if 'next_token' in json_response_tmp['meta'].keys():
                json_response['meta']['next_token'] = json_response_tmp['meta']['next_token']
            else:
                json_response['meta'].pop('next_token')

            # # Loop until all pages have been grabbed and added to the dictionary
            # Copy over all of the tweets
            if (json_response_tmp['meta']['result_count'] > 0) and ('data' in json_response_tmp.keys()):
                for tweet in json_response_tmp['data']:
                    json_response['data'].append(tweet)
                json_response['meta']['result_count'] = json_response['meta']['result_count'] + json_response_tmp['meta']['result_count']
                json_response['meta']['newest_id'] = json_response_tmp['meta']['newest_id']

            # Write the file with the entire tree
            num_tweets = num_tweets + json_response_tmp['meta']['result_count']
            with open(filename, 'w') as json_file:
                json_file.write(json.dumps(json_response, indent=4, sort_keys=True))
            
            # Print progress to terminal
            i = i + 1
            if ((i // step) > percent):
                percent = i // step
                totalTime = time.time() - start
                estTimeTotal = totalTime * (100 / percent)
                estTimeRemaining = int(estTimeTotal - totalTime)
                estHrs = int(estTimeRemaining // 3600)
                estMins = int((estTimeRemaining % 3600) // 60)
                estSecs = int((estTimeRemaining % 3600) % 60)
                print(str(percent) + "%, approximately " + str(estHrs) + ":" + str(estMins) + ":" + str(estSecs) + " remaining")
    print("Total Tweets gathered: " + str(num_tweets))
    return 0

def main():
    run_choice = sys.argv[1]

    if '-c' in run_choice:
        get_conversations()
    elif '-p' in run_choice:
        get_next_page_conv()
    else:
        get_individual_tweets()

if __name__ == "__main__":
    main()