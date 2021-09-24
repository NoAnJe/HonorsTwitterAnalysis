import requests
import os
import json
from time import sleep

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/search/all"

# Query string - for searching actual terms
acb = '(ACB OR (Amy Coney Barrett) OR Barrett OR Barret OR (Amy Coney))'
rbg = '(RBG OR (Ruth Ginsberg) OR Ginsberg)'
abortion = '(abortion OR (Roe Wade) OR (Planned Parenthood) OR Casey OR #RightToLife)'
not_rt = '-is:retweet'
rbg_query_str = f'{not_rt} {rbg} {abortion} lang:en'
acb_query_str = f'{not_rt} {acb} {abortion} lang:en'
sc_query_str = f'{not_rt} -{rbg} -{acb} {abortion} (SCOTUS OR Supreme Court OR (Justice Kennedy)) lang:en'

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
    # Set the appropriate times
    start_time = '2020-09-01T00:00:00Z' # Inclusive
    end_time = '2020-11-01T00:00:00Z'   # Exclusive

    os.chdir('../Data')

    conversation_ids = []

    # Loop until entire date/time set run
    while ('2020-09-01T00:00' not in end_time) and (': {' not in end_time):
        # Combine the entire request
        # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
        # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
        query_params = {'query': query_str,'tweet.fields': tweet_fields,
                        'start_time': start_time, 'end_time': end_time, 'max_results': '500'}
        json_response = connect_to_endpoint(search_url, query_params)

        # Set up the file
        filename = "ACB_"+end_time.replace(":", "").replace("Z","")+".json"
        with open(filename, 'w') as json_file:
            json_file.write(json.dumps(json_response, indent=4, sort_keys=True))

        # Calculate the next time to search
        end_time_size = len(json.dumps(json_response, indent=4, sort_keys=True).split("created_at"))
        end_time = json.dumps(json_response, indent=4, sort_keys=True).split("created_at")[end_time_size-1].split('\"')[2].split('.')[0] + 'Z'

        # With limitations on search size, must limit to searching less than 3 seconds
        sleep(3)
    
    for conv_id in conversation_ids:

if __name__ == "__main__":
    main()