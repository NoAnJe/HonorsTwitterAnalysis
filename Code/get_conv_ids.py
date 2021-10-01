import sys
import os
import json

conv_id_data = {'conv_ids': [], 'init_tweets': {}}

def main():
    # directory = sys.argv[1]
    # Scan through every file in the directory... including name parsing
    os.chdir('../Data/INITIAL_SEARCH')
    filelist = [f for f in os.listdir('.') if '.json' in f]
    for filename in filelist:
        with open(filename, 'r') as json_file:
            print(filename)
            json_obj = json.load(json_file)
            tag = filename.split('2')[0]
            for tweet in json_obj['data']:
                if ((int(tweet['conversation_id']) != int(tweet['id'])) or (int(tweet['public_metrics']['reply_count']) > 0)):
                    if tweet['conversation_id'] not in conv_id_data.keys():
                        # conv_id_data['conv_ids'].append(tweet['conversation_id'])
                        # conv_id_data['init_tweets'][tweet['conversation_id']] = [tweet['id']]
                        conv_id_data[tweet['conversation_id']] = {}
                        conv_id_data[tweet['conversation_id']]['init_tweets'] = [tweet['id']]
                        conv_id_data[tweet['conversation_id']]['tags'] = [tag]
                        conv_id_data[tweet['conversation_id']]['date'] = tweet['created_at'].split('T')[0]
                    else:
                        conv_id_data[tweet['conversation_id']]['init_tweets'].append(tweet['id'])
                        if tag not in conv_id_data[tweet['conversation_id']]['tags']:
                            conv_id_data[tweet['conversation_id']]['tags'].append(tag)
                        # conv_id_data['init_tweets'][tweet['conversation_id']].append(tweet['id'])
    os.chdir('../../Code')
    with open('conv_id_tags.json', 'w') as results:
        results.write(json.dumps(conv_id_data, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()