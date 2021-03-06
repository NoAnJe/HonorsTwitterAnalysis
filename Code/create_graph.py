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

# [TOTAL_TWEETS, AVG_LIKES, AVG_RTS, AVG_SENT]
acb_data =    [[None]*61, [None]*61, [None]*61, [None]*61, [None]*61]
rbg_data =    [[None]*61, [None]*61, [None]*61, [None]*61, [None]*61]
scotus_data = [[None]*61, [None]*61, [None]*61, [None]*61, [None]*61]

# Same thing, but on an hourly basis
datesHr = []
for date in range(1,31):
    for hour in range(0,24):
        datesHr.append("09"+str(date).zfill(2)+str(hour).zfill(2))
for date in range(1,32):
    for hour in range(0,24):
        datesHr.append("10"+str(date).zfill(2)+str(hour).zfill(2))

acb_hr_data =    [[None]*61*24, [None]*61*24, [None]*61*24, [None]*61*24, [None]*61*24]
rbg_hr_data =    [[None]*61*24, [None]*61*24, [None]*61*24, [None]*61*24, [None]*61*24]
scotus_hr_data = [[None]*61*24, [None]*61*24, [None]*61*24, [None]*61*24, [None]*61*24]

# Compile the data into the format for the graphing
def compile_data(json_data, final_arr, date):
    for day in json_data:
        index = date.index(day)
        final_arr[0][index] = json_data[day]["TotalTweets"]
        final_arr[1][index] = json_data[day]["AvgLikes"]
        final_arr[2][index] = json_data[day]["AvgRts"]
        final_arr[3][index] = json_data[day]["AvgSent"]
        final_arr[4][index] = json_data[day]["AvgSubj"]

# Plot the data against each other
def plot_data(index, date, acb, rbg, scotus, title, y_label, save):
    fig = plt.figure()
    plt.plot(date, acb[index], label="ACB Data")
    plt.plot(date, rbg[index], label="RBG Data")
    plt.plot(date, scotus[index], label="SCOTUS Data")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel(y_label)
    # plt.xticks(np.arange(min(dates), max(dates), 10))
    fig.suptitle(title)
    fig.savefig(save)

def main():
    directory = sys.argv[1]
    file = sys.argv[2]
    prefix = ["", ""]
    try:
        prefix = [sys.argv[3]+"Total", sys.argv[3]+"Avg"]
    except:
        prefix = ["total", "avg"]

    # Scan through every file in the directory... including name parsing
    cwd = os.getcwd()
    os.chdir(directory)
    filelist = [f for f in os.listdir('.') if '.json' in f]
    if file in filelist:
        with open(file,'r') as graph_file:
            json_obj = json.load(graph_file)
            compile_data(json_obj[dataDayRef[0]], rbg_data, dates)
            compile_data(json_obj[dataDayRef[1]], acb_data, dates)
            compile_data(json_obj[dataDayRef[2]], scotus_data, dates)
            compile_data(json_obj[dataRef[0]], rbg_hr_data, datesHr)
            compile_data(json_obj[dataRef[1]], acb_hr_data, datesHr)
            compile_data(json_obj[dataRef[2]], scotus_hr_data, datesHr)
        os.chdir(cwd)
        os.chdir("../Data/Graphs")

        # First, plot out the daily data
        plot_data(0, dates, acb_data, rbg_data, scotus_data,
            "Total Tweet Comparison", "Number of Tweets",
            prefix[0] + "TweetsDaily.png")
        plot_data(1, dates, acb_data, rbg_data, scotus_data,
            "Average Like Comparison", "Avg Number of Likes",
            prefix[1] + "LikesDaily.png")
        plot_data(2, dates, acb_data, rbg_data, scotus_data,
            "Average ReTweet Comparison", "Avg Number of ReTweets",
            prefix[1] + "RtsDaily.png")
        plot_data(3, dates, acb_data, rbg_data, scotus_data,
            "Average Sentiment Comparison", "Avg Sentiment",
            prefix[1] + "SentimentDaily.png")
        plot_data(4, dates, acb_data, rbg_data, scotus_data,
            "Average Subjectivity Comparison", "Avg Subjectivity",
            prefix[1] + "SubjectivityDaily.png")

        # Secondly, plot out the hourly data
        plot_data(0, datesHr, acb_hr_data, rbg_hr_data, scotus_hr_data,
            "Total Tweet Comparison", "Number of Tweets",
            prefix[0] + "TweetsHourly.png")
        plot_data(1, datesHr, acb_hr_data, rbg_hr_data, scotus_hr_data,
            "Average Like Comparison", "Avg Number of Likes",
            prefix[1] + "LikesHourly.png")
        plot_data(2, datesHr, acb_hr_data, rbg_hr_data, scotus_hr_data,
            "Average ReTweet Comparison", "Avg Number of ReTweets",
            prefix[1] + "RtsHourly.png")
        plot_data(3, datesHr, acb_hr_data, rbg_hr_data, scotus_hr_data,
            "Average Sentiment Comparison", "Avg Sentiment",
            prefix[1] + "SentimentHourly.png")
        plot_data(4, datesHr, acb_hr_data, rbg_hr_data, scotus_hr_data,
            "Average Subjectivity Comparison", "Avg Subjectivity",
            prefix[1] + "SubjectivityHourly.png")

if __name__ == "__main__":
    main()