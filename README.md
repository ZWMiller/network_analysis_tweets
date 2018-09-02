# Network Analysis on Tweets

Twitter is a weird platform. The average Jill gets just as much
volume as a world renowned expert. This is seen often in political
discussions, and it becomes hard to tell who is driving conversations
versus who is just reacting to the conversations. To address this, 
this tool attempts to isolate the voices that are leading conversations
on specific topics and pick them out amongst all the noise.

## Example

Since Trump is a lightning rod for discussion, who is really driving conversations
about him? I used my network analyzer to find the voices that are often retweeted 
(based on 10 minutes of data on Sep. 01 2018). 

![Example Network]('images/example_network.png')

## Pipeline pieces

#### Twitter Streamer

This is a streaming tool built on the Tweepy module. It extends the
module by taking all tweets as published in real-time, then extracting
only retweets. From those retweets, the username of the retweeter and the 
original tweeter is extracted. These usernames are stored in a series of 
CSV files (note, this could easily be extended to database storage, but this
project was designed as a demo for network analysis and I don't want folks to
need a database to play with things). To change the topic of analysis, the 
user runs this file after replacing the topics in the last line.

#### Tweet Network Builder

The main file for creating networks and analyzing them. This is the main controller
that the user should interface with to run a network analysis. The main controls are
setting the number of "important hub users" to extract, updating the title of the plot,
and changing the filename of the output image.

#### Graph Builder

All of the tools for building the network graph. Reads the CSVs and creates the nodes
and edges, figures out the location of the nodes, does the hub analysis (based on degree
centrality), and plots the nodes/edges/hubs. Relies on networkx python module.

#### Cleaning Functions

Functions used for removing weird characters and normal twitter username junk.

#### Testing

A few tests to make sure the cleaning functions are properly cleaning the user names
and the networkx module is still identifying hubs correctly.

### Required Libraries

Streaming Data:

* Tweepy
* Twitter API keys
* OAuth

Analyzing Network:

* networkx
* matplotlib
* glob
