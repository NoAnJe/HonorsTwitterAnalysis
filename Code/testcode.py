from twarc import Twarc2, expansions
import datetime
import json
import os

bearer_token = os.environ.get("BEARER_TOKEN")
# Replace your bearer token below
# client = Twarc2(bearer_token=bearer_token)


# def main():
#     # Specify the start time in UTC for the time period you want replies from
#     start_time = datetime.datetime(2020, 9, 1, 0, 0, 0, 0, datetime.timezone.utc)

#     # Specify the Tweet ID for which you want the conversation thread
#     query = "conversation_id:1322493790356197376"

#     # The search_all method call the full-archive search endpoint to get the Tweets (replies) for the conversation 
#     search_results = client.search_all(query=query, start_time=start_time, max_results=100)
#     print(search_results)

#     # Twarc returns all Tweets for the criteria set above, so we page through the results
#     for page in search_results:
#         # The Twitter API v2 returns the Tweet information and the user, media etc.  separately
#         # so we use expansions.flatten to get all the information in a single JSON
#         result = expansions.flatten(page)
#         for tweet in result:
#             # Here we are printing the full Tweet object JSON to the console
#             print(json.dumps(tweet))


# if __name__ == "__main__":
#     main()

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


def main():
    os.chdir('../Data')
    # tweet_id = 1441814771443978250
    start_time = '2020-08-01T00:00:00Z'
    conv_id = 1307383227896782849
    # query_params = {'query': '(I thought the same but did not want to be a Debbie downer)', 'tweet.fields': tweet_fields, 'max_results': '500'}
    # json_response = connect_to_endpoint(search_url, query_params)
    # print(json_response)
    # id:1322515804840230912
    conv_str = f'conversation_id:{conv_id}'
    # query = 'conversation_id:1300821114592129026' #+str(conv_id)
    query_params = {'query': conv_str,'tweet.fields': tweet_fields, 'start_time': start_time, 'max_results': '500'}
    # query_params = {'query': '', 'tweet.fields': tweet_fields}
    json_response = connect_to_endpoint(search_url, query_params)
    print(json_response)

    # conv_id = 1317864750940815365
    # query_params = {'query': 'conversation_id:'+str(conv_id), 'tweet.fields': tweet_fields, 'max_results': '500'}
    # json_response = connect_to_endpoint(search_url, query_params)
    # json_response['initial_id'] = "1234567890"

    # Set up the file
    # filename = "testdata.json"
    # with open(filename, 'w') as json_file:
        # json_file.write(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()