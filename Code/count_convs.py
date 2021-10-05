import os
import sys
import json
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('No display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

data = {'0': 0, '1': 0, '10': 0, '100': 0, '1000': 0}

def count_vals():
    os.chdir('../Data/CONVERSATIONS')
    filelist = [f for f in os.listdir('.') if '.json' in f]
    length = len(filelist)
    inc = 0
    step = length // 100
    for filename in filelist:
        # Get the count
        count = 0
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
            count = json_data['meta']['result_count']
        
        # Put the count in the correct bracket
        if count == 0:
            data['0'] = data['0'] + 1
        elif count < 10:
            data['1'] = data['1'] + 1
        elif count < 100:
            data['10'] = data['10'] + 1
        elif count < 1000:
            data['100'] = data['100'] + 1
        else:
            data['1000'] = data['1000'] + 1
        
        # Print the percentage if at a whole percent
        inc = inc + 1
        if inc % step == 0:
            print(str(inc) + ' / ' + str(length) + ' conversations analyzed')
    
    # Print the results
    os.chdir('..')
    print(data)
    with open('conv_count.json', 'w') as count_file:
        count_file.write(json.dumps(data, indent=4, sort_keys=True))

def graph_count():
    x = ['0', '1', '10', '100', '1000']
    bars = []

    os.chdir('../Data')
    with open('conv_count.json', 'r') as count_file:
        data = json.load(count_file)

    bars.append(data['0'])
    bars.append(data['1'])
    bars.append(data['10'])
    bars.append(data['100'])
    bars.append(data['1000'])
    
    os.chdir('Graphs')
    fig = plt.figure()
    plt.bar(x, bars)
    fig.savefig("ConvCount.png")

def main():
    input_res = sys.argv[1]
    if ('-a' in input_res) or ('-cg' in input_res) or ('-gc' in input_res):
        count_vals()
        graph_count()
    elif '-c' in input_res:
        count_vals()
    elif '-g' in input_res:
        graph_count()

if __name__ == "__main__":
    main()