import sys
import os
import json
import numpy as np
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('No display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

dataDayRef = ["RBG_DAY", "ACB_DAY", "SCOTUS_DAY"]
dataRef = ["RBG", "ACB", "SCOTUS"]
dates = []
for date in range(1,31):
    dates.append("09"+str(date).zfill(2))
for date in range(1,32):
    dates.append("10"+str(date).zfill(2))

acb_data = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
rbg_data = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]
scotus_data = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

# Plot the data against each other
def plot_data(date, acb, rbg, scotus, title, y_label, save):
    fig = plt.figure()
    plt.plot(date, acb, label="ACB Data")
    plt.plot(date, rbg, label="RBG Data")
    plt.plot(date, scotus, label="SCOTUS Data")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel(y_label)
    # plt.xticks(np.arange(min(dates), max(dates), 10))
    fig.suptitle(title)
    fig.savefig(save)

def main():
    with open('conv_id_tags.json','r') as graph_file:
        json_obj = json.load(graph_file)
        for conv in json_obj:
            datestr = json_obj[conv]['date'].split('-')[1] + json_obj[conv]['date'].split('-')[2]
            if 'ACB' in json_obj[conv]['tags']:
                pos = dates.index(datestr)
                acb_data[pos] = acb_data[pos] + 1
            if 'RBG' in json_obj[conv]['tags']:
                pos = dates.index(datestr)
                rbg_data[pos] = rbg_data[pos] + 1
            if 'SC' in json_obj[conv]['tags']:
                pos = dates.index(datestr)
                scotus_data[pos] = scotus_data[pos] + 1
        os.chdir("../Data/Graphs")
        plot_data(dates, acb_data, rbg_data, scotus_data,
            "Total Conversation Comparison", "Number of Conversations",
            "ConvsDaily.png")

if __name__ == "__main__":
    main()