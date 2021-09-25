# Tutorial
## Disclaimer

This project is created as-is, with no guarantees of support or working code.

## Gathering Data

To gather the data, the following command should be run:

`python3 query_full.py`

This will gather the data for both the individual tweets and the conversations. The conversation tweets are based completely on the individual tweets. The conversation files also note which Tweet was the original Tweet that was flagged, so that data can be analyzed based on both that starting point and on the conversation head.

## Analyzing Data - Individual Level

There are three scripts that must be run, in order, to analyze data. The first is the sentiment analyzer, which simply analyzes the sentiment of each Tweet. This is relatively straightforward, as one simply must provide the directory to run through all the JSON files with the Tweets on. It will run on *all* of the files within this directory, overwriting them with the sentiment value of each Tweet added to the JSON for each Tweet as a new field.

`python analyze_sentiment.py <directory>`

The next step is to combine the data into both hourly and daily reports for further analysis. Very simply, this just combines the data into totals and averages for each step (the hourly and daily). Note that for things like Likes, this is a total based on the Tweet time, *not* the Like time. As with the sentiment analyzer, one simply must provide the directory, in which it will run on all of the included files. It will then put the results in a file labeled **compiled_data.json**.

`python analyze_ind.py <directory>`

The final step is creating the graphs. This will create graphs comparing, at least for my personal use, the results of ACB-, RBG-, and SCOTUS-related Tweets. There are currently three areas of comparison: Likes, ReTweets, and Total Tweets. There are two graphs created for each one: one which works on a daily step, and one which works on an hourly step. This can be run with the following command (where directory is the directory of the stored file, and file itself is (in this instance) **compiled_data.json**):

`python create_graph.py <directory> <file> <prefix>`

The **<prefix>** argument is an optional argument that will add at prefix to all of the files (i.e. if **<prefix>** is *ind*, *totalTweetsDaily.png* becomes *indTotalTweetsDaily.png*). The above command also requires that there is a **Graphs** directory, wherein the created graphs can be stored. This should be at the same level as the directory that **<file>** is in. One example would be:

 - Code
    - TweetData
    - Graphs

By running these commands in order, with the proper directories provided, you should end up with graphs comparing the averages and totals of the subjects (in this study, ACB, RBG, and SCOTUS).

## Analyzing Data - Conversation Level

Beyond an individual Tweet, a lot can be learned from analyzing conversations as a whole. The overall process is similar to analyzing tweets on an individual level - the sentiment is analyzed, then the data is compiled, and graphs are made. However, there are some important steps in the middle.

The first step is to, again, analyze the sentiment of each Tweet as a whole. This is done with the same script:

`python analyze_sentiment.py <directory>`

The second step is to organize each conversation. The general syntax for this is the same, in that it is simply the script and the directory. Each JSON file within the directory should contain one conversation. In this script, each Tweet will be updated with its children Tweets and the individual level (where the parent Tweet is at level 0, so on and so forth). This is an update from the Twitter query, which includes which Tweet the current Tweet *replied* to, or essentially, its parent.

`python organize_conv.py <directory>`

By updating the conversation to reference children, the average sentiment can be calculated for each conversation and sub-conversation. Therefore, this is done in a similar format to the individual Tweets, but the averaging across conversations must also be taken into consideration. To calculate across all Tweets, the following command can be used (resulting in the same **compiled_data.json** file):

`python analyze_ind.py <directory>`

To calculate in regards to conversation, though (with sentiment averaging being done across the conversation), the following command should be used (which results in **compiled_conv_data.json**):

`python analyze_conv.py <directory>`

After this, all that's left is to create graphs. Again, the following script can be used:

`python create_graph.py <directory> <file> <prefix>`