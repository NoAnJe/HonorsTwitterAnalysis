import json
import os
import sys

def getFileKey(filename):
    if 'ACB' in filename:
        return 'ACB'
    elif 'RBG' in filename:
        return 'RBG'
    elif 'SC' in filename:
        return 'SC'

# Catalog all of the conversations by going through the given directory
# Should be used to catalog convs from initial tweets
def catalog_convs(directory):
    cwd = os.getcwd()
    # Step 1: Catalog
    convs = {}
    os.chdir(directory)
    filelist = [f for f in os.listdir('.') if '.json' in f]
    for filename in filelist:
        json_data = {}
        fileKey = getFileKey(filename)

        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
        
        for tweet in json_data['data']:    
            conv_id = tweet['conversation_id']
            
            if conv_id not in convs.keys():
                convs[conv_id] = [fileKey]
            else:
                if fileKey not in convs[conv_id]:
                    convs[conv_id].append(fileKey)
    # Step 2: Store data
    os.chdir(cwd)
    os.chdir('../Data')
    with open('conv_keys.json', 'w') as keysFile:
        keysFile.write(json.dumps(convs, indent=4, sort_keys=False))

# Assign the tags from the catalog
def assign_tags(directory):
    cwd = os.getcwd()
    os.chdir('../Data')
    convs = {}
    with open('conv_keys.json', 'r') as keysFile:
        convs = json.load(keysFile)
    os.chdir(cwd)
    os.chdir(directory)
    
    filelist = [f for f in os.listdir('.') if '.json' in f]
    for filename in filelist:
        conv_id = filename.split('_')[1].split('.')[0]
        conv_file_data = {}
        with open(filename, 'r') as conv_file:
            conv_file_data = json.load(conv_file)
        conv_file_data['meta']['init_tags'] = convs[conv_id]
        with open(filename, 'w') as conv_file:
            conv_file(json.dumps(conv_file_data, indent=4, sort_keys=False))
        

def main():
    arg = sys.argv[1]
    directory = sys.argv[2]

    if '-c' in arg:
        catalog_convs(directory)
    elif '-a' in arg:
        assign_tags(directory)


if __name__ == "__main__":
    main()