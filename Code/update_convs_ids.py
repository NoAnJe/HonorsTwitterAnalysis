import sys
import os
import json

conv_id_data = {'conv_ids': [], 'init_tweets': {}}

def main():
    os.chdir('../Data')
    conv_ids = {}
    with open('conv_ids_tmp.json', 'r') as conv_id_tmp_file:
        conv_ids = json.load(conv_id_tmp_file)
    os.chdir('CONVERSATIONS')
    filelist = [f for f in os.listdir('.') if '.json' in f]
    for filename in filelist:
        conv_id = filename.split('_')[1].split('.')[0]
        if conv_id in conv_ids['conv_ids']:
            with open(filename, 'r') as curr_conv:
                curr_conv_json = json.load(curr_conv)
                if 'next_token' not in curr_conv_json['meta'].keys():
                    conv_ids['conv_ids'].remove(conv_id)
                    conv_ids['init_tweets'].pop(conv_id)
    os.chdir('..')
    with open('conv_ids.json', 'w') as conv_id_file:
        conv_id_file.write(json.dumps(conv_ids, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()