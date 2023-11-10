import praw
import json 
import requests 
import sys, getopt
from bs4 import BeautifulSoup
import re
import os
import datetime

# Reddit API credentials and password stored in reddit_config.json file
# Function to create a Reddit instance

def redditObjectCreator(jsonFile="reddit_config.json", json_key="reddit"):
    with open(jsonFile, 'r') as f:
        config = json.load(f)
    reddit_credentials = config[json_key]
    #authentication, uses reddit_config.json:
    reddit = praw.Reddit(
        client_id=reddit_credentials['client_id'],
        client_secret=reddit_credentials['client_secret'],
        user_agent=reddit_credentials['user_agent'],
        username=reddit_credentials['username'],
        password=reddit_credentials['password'],
        
        check_for_updates=False,
        comment_kind="t1",
        message_kind="t4",
        redditor_kind="t2",
        submission_kind="t3",
        subreddit_kind="t5",
        trophy_kind="t6",
        oauth_url="https://oauth.reddit.com",
        reddit_url="https://www.reddit.com",
        short_url="https://redd.it",
    )
    return reddit


# Function to extract extra URLs included from post's body of text
def extract_urls(text):
    urls = []
    pattern = re.compile(r'(http[s]?:\/\/[^\s]+)')
    matches = re.findall(pattern, text)
    for match in matches:
        urls.append(match)
    return urls

def main(argv): 
    inputfile = 'seedfile.txt'
    outputfile = 'crypto_hot_' 
    
    # inputfile = input("Enter an input file or d for default(seedfile.txt): ")
    # if inputfile == "d":
    #     inputfile = "seedfile.txt"
    # outputfile = input("Enter an output file or d for default(reddits): ")
    # if outputfile == "d":
    #     outputfile = "reddits" 

    if (len(sys.argv) > 0):     
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        for opt, arg in opts:
            if opt == '-h':
                print ('test.py -i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
        print ('Input file is', inputfile)
        print ('Output file is', outputfile)
    

    reddit = redditObjectCreator()

    seedfile = open(inputfile, "r")
    subreddits = seedfile.readline().strip().split(", ")
    listings = seedfile.readline().strip().split(", ")
    print(subreddits) 
    print(listings) 

    #needs to parase file for root pages into subreddit for topic
    # subreddits = ['crypto', 'stockmarket'] 
    #need to parse file for listings type of post (Hot, New, Top)
    # listings = ['new', 'hot', 'top']
    #need to pass args into Max_file_Count to set number of MBs crawled
    seedfile.close(); 

    MAX_FILE_COUNT = 9

    file_count = 0
    file_size_mb= 0
    MAX_FILE_SIZE = 10

    commentList = [] 
    postURLs = []
    # Loop through new, hot, and top posts
    for topic in subreddits:
        for sort_type in listings:
            while file_count < MAX_FILE_COUNT:
                for submission in reddit.subreddit(topic).__getattribute__(sort_type)(limit=1000):
                    # If post is not pinned to the top of the subreddit (i.e. not visible to all users):
                    if not submission.stickied: 
                        # Get all the comments and replies to the post, and to other comment replies:
                        submission.comments.replace_more(limit=None)
                        for comment in submission.comments.list():
                            commentList.append(comment.body)

                        # EXTRA CREDIT: get URLs within the post
                        postURLs = extract_urls(submission.selftext)
                                            
                        # Setting up JSON data for each post/submission:
                        data = {
                            "id": str(submission.id),
                            "title": str(submission.title),
                            "url": str(submission.url),
                            "Created (UTC)": str(datetime.datetime.fromtimestamp(submission.created_utc)),
                            "body": submission.selftext,
                            "post URL info": postURLs,
                            "author": str(submission.author),
                            "ups": str(submission.ups),
                            "downs": str(submission.downs),
                            "number of comments": str(submission.num_comments),
                            "comments": commentList
                        }

                        # Save JSON data to file:
                        f = open(f"{outputfile}{file_count}.json", 'a')
                        json.dump(data, f)
                        f.write("\n")
                        commentList = [] 
                        postURLs = []
                        file_size_mb = os.path.getsize(f"{outputfile}{file_count}.json") / (1024 * 1024) #the division converts bytes to megabytes.

                        if file_size_mb >= MAX_FILE_SIZE:
                            f.close()
                            file_count += 1
                            f = open(f"{outputfile}{file_count}.json", 'a')
                            file_size_mb = 0

if __name__ == "__main__":
    main(sys.argv[1:])
