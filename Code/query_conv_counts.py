import requests
import os
import json
from time import sleep
import sys
import datetime

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/counts/all"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    sleep(3)
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    print("Starting at " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    os.chdir('../Data')
    id_list = {}
    total_tweets = 0
    with open('conv_ids_og.json', 'r') as conv_id_file:
        id_list = json.load(conv_id_file)
    total_convs = len(id_list['conv_ids'])
    step = total_convs // 100
    i = 0
    id_list['counts'] = {}
    for conv_id in id_list['conv_ids']:
        query_str = f'conversation_id:{conv_id}'
        query_params = {'query': query_str,'granularity': 'day', 'start_time': '2020-08-01T00:00:00Z'}
        month = 8
        success = 0
        json_response = {}
        while success != 1:
            try:
                json_response = connect_to_endpoint(search_url, query_params)
                success = 1
            except:
                sleep(10)
                
        total = json_response['meta']['total_tweet_count']
        while 'next_token' in json_response['meta'].keys():
            query_params['next_token']=json_response['meta']['next_token']
            json_response = {}
            while success != 1:
                try:
                    json_response = connect_to_endpoint(search_url, query_params)
                    success = 1
                except:
                    sleep(10)
            total = total + json_response['meta']['total_tweet_count']
            if 'next_token' in json_response['meta'].keys():
                next_token = json_response['meta']['next_token']
            else:
                next_token = 0
            month = month + 1
            if month > 10:
                break
        id_list['counts'][conv_id] = total
        total_tweets = total_tweets + total
        
        i = i + 1
        if (i % step == 0):
            print(str((i / total_convs) * 100) + '%' + ' at time' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if (i % 100 == 0):
            with open('conv_ids_count.json', 'w') as conv_id_file:
                conv_id_file.write(json.dumps(id_list, indent=4, sort_keys=False))
    with open('conv_ids_count.json', 'w') as conv_id_file:
        conv_id_file.write(json.dumps(id_list, indent=4, sort_keys=False))
    
    print("Total tweets: " + str(total))


if __name__ == "__main__":
    main()