import sys
import os
import json
import numpy as np
import time
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    mpl.use('Agg')
import matplotlib.pyplot as plt

# This lays out all of the information
sc_avg = 0
sc_std = 0
rbg_avg = 0
rbg_std = 0
acb_avg = 0
acb_std = 0
total_tweets = 0

full_list = [[[] * 3 for i in range(3)] * 3 for j in range(4)]      # full_list[tag][sentiment][###IND_VALS###]
full_means = [[0] * 3 for i in range(4)]                            # full_means[tag][sentiment]
full_std = [[0] * 3 for i in range(4)]                            # full_std[tag][sentiment]

days = [[[0] * 61 for i in range(3)] for j in range(4)]             # days[tag{SC/RBG/ACB/TOTAL}][sentiment][day]
days_count = [[0] * 61 for i in range(4)]                           # days_count[tag{SC/RBG/ACB/TOTAL}][day]
weighted_days = [[[0] * 61 for i in range(3)] for j in range(4)]    # wdays[tag{SC/RBG/ACB/TOTAL}][sentiment][day]
weighted_days_count = [[0] * 61 for i in range(4)]                  # wdays_count[tag{SC/RBG/ACB/TOTAL}][day]

data_ref = ['sentiment', 'subjectivity', 'vader']
data_ref_cap = ['Sentiment', 'Subjectivity', 'VADER']
figure_ref = ['SC', 'RBG', 'ACB', 'TOTAL']

levels_sentiment = [[[[0]*5 for i in range(3)] for j in range(5)] for k in range(4)] # levels_sentiment[tag{SC/RBG/ACB/TOTAL}][convSize][sentiment][level]
levels_count = [[[0] * 5 for i in range(5)] for j in range(4)] # levels_count[tag{SC/RBG/ACB/TOTAL}][convSize][level]
conv_sizes = [[0] * 5 for j in range(4)] # conv_sizes[tag{SC/RBG/ACB/TOTAL}][convSize]



# Simply print the percentage being done with basic data compilation
def printTime(start, count, length):
    percent = round(count * 100 / length, 2)
    totalTime = time.time() - start
    estTimeTotal = totalTime * (100 / percent)
    estTimeRemaining = int(estTimeTotal - totalTime)
    estHrs = int(estTimeRemaining // 3600)
    estMins = int((estTimeRemaining % 3600) // 60)
    estSecs = int((estTimeRemaining % 3600) % 60)
    print(str(percent) + "%, approximately " + str(estHrs) + ":" + str(estMins) + ":" + str(estSecs) + " remaining, " + str(total_tweets) + " Tweets analyzed, approx " + str(count) + " files")

# Get the data from each Tweet
def analyzeFile(jsonData):
    global total_tweets
    global full_list
    global days
    global days_count
    global weighted_days
    global weighted_days_count
    global levels_sentiment
    global levels_count
    global conv_sizes

    if ('data' in jsonData.keys()) and (jsonData['meta']['result_count'] > 0):
        # Find the size of the conversation
        conv_size = 0
        if jsonData['meta']['result_count'] < 10:
            conv_size = 0
        elif jsonData['meta']['result_count'] < 100:
            conv_size = 1
        elif jsonData['meta']['result_count'] < 1000:
            conv_size = 2
        elif jsonData['meta']['result_count'] < 10000:
            conv_size = 3
        else:
            conv_size = 4
        
        conv_sizes[3][conv_size] += 1
        for i in range(3):
            if figure_ref[i] in jsonData['meta']['init_tags']:
                conv_sizes[i][conv_size] += 1

        # analyze the indvidual tweet data
        for tweet in jsonData['data']:
            if ('2020-09' in tweet['created_at']) or ('2020-10' in tweet['created_at']):
                total_tweets += 1
                dateint = (int(tweet['created_at'].split('-')[1]) - 9) * 30 + int(tweet['created_at'].split('-')[2].split('T')[0]) - 1
                weight = (tweet['public_metrics']['like_count']+tweet['public_metrics']['retweet_count'])
                level = tweet['level']
                if level > 4:
                    level = 3
                elif level == -1:
                    level = 4
                else:
                    level -= 1
                # Start with the individual analyses
                for f in range(4):
                    if (figure_ref[f] in jsonData['meta']['init_tags']) or (f == 3):
                        for i in range(3):
                            full_list[f][i].append(tweet[data_ref[i]])
                            days[f][i][dateint]+=tweet[data_ref[i]]
                            weighted_days[f][i][dateint]+=(tweet[data_ref[i]]*weight)
                            levels_sentiment[f][conv_size][i][level]+=tweet[data_ref[i]]
                        days_count[f][dateint]+=1
                        weighted_days_count[f][dateint]+=weight
                        levels_count[f][conv_size][level]+=1

def summarizeTweets():
    global full_list
    global full_means
    global full_std
    global days
    global days_count
    global weighted_days
    global weighted_days_count
    global levels_sentiment
    global levels_count
    global conv_sizes

    print('Done gathering all of the data, onto compilation')
    # Averaging Loops
    for tag in range(4):
        for sentiment in range(3):
            for day in range(61):
                if days_count[tag][day] > 0:
                    days[tag][sentiment][day] /= days_count[tag][day]
                    weighted_days[tag][sentiment][day] /= weighted_days_count[tag][day]

    for conv_size in range(5):
        for tag in range(4):
            for sentiment in range(3):
                for level in range(5):
                    if levels_count[tag][conv_size][level] > 0:
                        levels_sentiment[tag][conv_size][sentiment][level] /= levels_count[tag][conv_size][level]

    for tag in range(4):
        for sentiment in range(3):
            tmp_arr = np.array(full_list[tag][sentiment])
            full_means[tag][sentiment] = np.mean(tmp_arr)
            full_std[tag][sentiment] = np.std(tmp_arr)

    # Write all the data as a backup
    data_summary = {}
    data_summary['conv_sizes'] = conv_sizes
    data_summary['full_means'] = full_means
    data_summary['full_std'] = full_std
    data_summary['weighted_days'] = weighted_days
    data_summary['days'] = days
    data_summary['levels_sentiment'] = levels_sentiment
    with open('conv_data.json', 'w') as conv_data:
        conv_data.write(json.dumps(data_summary, indent=4, sort_keys=True))

def loadTweetData():
    global full_means
    global full_std
    global weighted_days
    global days
    global levels_sentiment
    global conv_sizes
    data_summary = {}
    with open('conv_data.json', 'r') as conv_data:
        data_summary = json.load(conv_data)
    full_means = data_summary['full_means']
    full_std = data_summary['full_std']
    weighted_days = data_summary['weighted_days']
    days = data_summary['days']
    levels_sentiment = data_summary['levels_sentiment']
    conv_sizes = data_summary['conv_sizes']

def outputData():
    print('Done gathering all the data, now working on graphing')
    dates = []
    for date in range(1,31):
        dates.append("09-"+str(date).zfill(2))
    for date in range(1,32):
        dates.append("10-"+str(date).zfill(2))
    
    # X = np.arange(4)
    X = [0, 1, 2, 3, 4]
    conv_sizes_labels = ['1', '10', '100', '1000', '10000']

    # Start with figure on conversation data
    fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    plt.bar([v - 0.25 for v in X], conv_sizes[0], color = 'b', width = 0.25, label=figure_ref[0])
    plt.bar([v + 0.0 for v in X], conv_sizes[1], color = 'r', width = 0.25, label=figure_ref[1])
    plt.bar([v + 0.25 for v in X], conv_sizes[2], color = 'g', width = 0.25, label=figure_ref[2])
    plt.xticks(X, conv_sizes_labels)
    plt.xlabel('Conversation Size (Exponential Base)')
    plt.ylabel('Number of Conversations')
    plt.legend()
    fig.suptitle('Conversation Sizes')
    fig.tight_layout()
    fig.savefig('ConvSizes.png')
    fig.clear()

    # Compare the values for each sentiment - mean and std deviation
    X = [0, 1, 2]
    plt.bar([v - 0.25 for v in X], full_means[0], color = 'b', width = 0.25, label=figure_ref[0])
    plt.bar([v for v in X], full_means[1], color = 'r', width = 0.25, label=figure_ref[1])
    plt.bar([v + 0.25 for v in X], full_means[2], color = 'g', width = 0.25, label=figure_ref[2])
    plt.xticks(X, data_ref_cap)
    plt.xlabel('Analysis Version')
    plt.ylabel('Mean Value of Analysis')
    plt.legend()
    fig.suptitle('Mean Value of Analysis Types Across All Tweets')
    fig.savefig('MeanConvValues.png')
    fig.clear()

    plt.bar([v - 0.25 for v in X],  full_std[0], color = 'b', width = 0.25, label=figure_ref[0])
    plt.bar([v + 0.0 for v in X], full_std[1], color = 'r', width = 0.25, label=figure_ref[1])
    plt.bar([v + 0.25 for v in X],  full_std[2], color = 'g', width = 0.25, label=figure_ref[2])
    plt.xticks(X, data_ref_cap)
    plt.xlabel('Analysis Version')
    plt.ylabel('Standard Deviation of Analysis')
    plt.legend()
    fig.suptitle('Standard Deviation of Analysis Types Across All Tweets')
    fig.savefig('StdConvValues.png')
    fig.clear()

    dates5 = []
    i = 0
    for date in dates:
        if i == 5:
            i = 0
        if i == 0:
            dates5.append(date)
        i+=1

    # Next, create a figure on the daily data
    for sentiment in range(len(data_ref)):
        plt.plot(dates, days[0][sentiment], label="ACB Data")
        plt.plot(dates, days[1][sentiment], label="RBG Data")
        plt.plot(dates, days[2][sentiment], label="SCOTUS Data")
        fig.legend()
        plt.xticks()
        plt.xticks(dates5, dates5)
        plt.xlabel("Date")
        plt.ylabel("Average " + data_ref_cap[sentiment] + " Value")
        fig.legend()
        fig.suptitle("Average Daily Values of " + data_ref_cap[sentiment])
        fig.savefig(data_ref[sentiment] + 'ConvDays.png')
        fig.clear()

    # Same thing, but weighted
    for sentiment in range(len(data_ref)):
        plt.plot(dates, weighted_days[0][sentiment], label="ACB Data")
        plt.plot(dates, weighted_days[1][sentiment], label="RBG Data")
        plt.plot(dates, weighted_days[2][sentiment], label="SCOTUS Data")
        fig.legend()
        plt.xticks()
        plt.xticks(dates5, dates5)
        plt.xlabel("Date")
        plt.ylabel("Average Weighted " + data_ref_cap[sentiment] + " Value")
        fig.legend()
        fig.suptitle("Average Weighted Daily Values of " + data_ref_cap[sentiment])
        fig.savefig(data_ref[sentiment] + 'ConvWeightedDays.png')
        fig.clear()
    
    os.chdir('Levels')
    for sentiment in range(len(data_ref)):
        for conv_size in range(5):
            X = [0, 1, 2, 3, 4]
            plt.bar([v - 0.25 for v in X], levels_sentiment[0][conv_size][sentiment], color = 'b', width = 0.25, label=figure_ref[0])
            plt.bar([v + 0.0 for v in X], levels_sentiment[1][conv_size][sentiment], color = 'r', width = 0.25, label=figure_ref[1])
            plt.bar([v + 0.25 for v in X], levels_sentiment[2][conv_size][sentiment], color = 'g', width = 0.25, label=figure_ref[2])
            plt.xticks(X, ['1', '2', '3', '4+', 'UND'])
            plt.xlabel('Tweet Level')
            plt.ylabel('Average Sentiment at Level')
            plt.legend()
            fig.suptitle(data_ref_cap[sentiment] + ' Levels for Conv Size ' + conv_sizes_labels[conv_size])
            fig.tight_layout()
            fig.savefig(data_ref[sentiment] + 'Level_ConvSize' + conv_sizes_labels[conv_size] + '.png')
            fig.clear()

def main():
    global total_tweets
    total_tweets = 0
    backup = sys.argv[1]

    os.chdir('../Data')
    if '-f' in backup:
        filelist = [f for f in os.listdir('./CONV_COMPLETE') if '.json' in f]
        filelist2 = [f for f in os.listdir('./CONVERSATIONS') if '.json' in f]
        length = len(filelist) + len(filelist2)
        step = int(length / 100)
        start = time.time()
        count = 0

        os.chdir('./CONV_COMPLETE')
        for filename in filelist:
            # Open the file itself
            with open(filename,'r') as tweet_file:
                json_obj = json.load(tweet_file)
                analyzeFile(json_obj)
            count = count + 1
            if count % step == 0:
                printTime(start, count, length)
        
        os.chdir('../CONVERSATIONS')
        for filename in filelist2:
            # Open the file itself
            with open(filename,'r') as tweet_file:
                json_obj = json.load(tweet_file)
                analyzeFile(json_obj)
            count = count + 1
            if count % step == 0:
                printTime(start, count, length)
        os.chdir('..')

        print('Total Tweets analyzed: ' + str(total_tweets))
        summarizeTweets()
    elif '-b' in backup:
        loadTweetData()
    os.chdir('Graphs')
    outputData()

if __name__ == "__main__":
    main()