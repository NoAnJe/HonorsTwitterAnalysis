import requests
import os
import json
from time import sleep

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/all"

# Fields explained:
#   author_id : Twitter ID of the author
#   conversation_id : Conversation ID. Useful for tracking threads
#   created_at : Tweet time
#   public_metrics : Public metrics of the tweet, including Retweets, Likes, and Replies
#   text : Text of the Tweet
tweet_fields = 'author_id,conversation_id,created_at,public_metrics,text'

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


def main():
    os.chdir('../Data')

    conv_id = 1441809772504752138
    query_params = {'query': 'conversation_id:'+str(conv_id), 'tweet.fields': tweet_fields, 'max_results': '500'}
    json_response = connect_to_endpoint(search_url, query_params)
    json_response['initial_id'] = "1234567890"

    # Set up the file
    filename = "testdata.json"
    with open(filename, 'w') as json_file:
        json_file.write(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()