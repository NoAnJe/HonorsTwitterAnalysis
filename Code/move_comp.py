import sys
import os
import json

os.chdir('../Data')
filelist = [f for f in os.listdir('CONVERSATIONS') if '.json' in f]
length = len(filelist)
step = int(length / 100)
count = 0
for f in filelist:
    count = count + 1
    if count % step == 0:
        print(str(count / length))
    is_complete = False
    with open('CONVERSATIONS/' + f, 'r') as json_file:
        curr_conv_json = json.load(json_file)
        if 'next_token' not in curr_conv_json['meta'].keys():
            is_complete = True
    if is_complete:
        os.rename('CONVERSATIONS/'+f, 'CONV_COMPLETE/'+f)
