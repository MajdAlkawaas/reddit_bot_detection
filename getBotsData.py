import praw
import json
import urllib.request
import pandas as pd
from items import Redditor, Post, Comment
from os import getenv
import os

PASSWORD     = 'j=HUZ`6S8B'
USERNAME     = 'CMPS287_project'
CLIENT_ID    = 'd5w9jc7mmyeLEL2DG1wtxg'
SECRET_TOKEN = 'HIOuTew4HunOVSJeFT47Yi4sCkdBCA'

print("###########", os.environ.get('CLIENT_ID'))

reddit = praw.Reddit(client_id  = CLIENT_ID, 
                     client_secret = SECRET_TOKEN, 
                     user_agent = 'MyAPI/0.0.1')

def filter_usernames(usernames):
    authors = []
    for username in usernames:
        if username != 'AutoModerator' and username != '[deleted]':
            authors.append(username)
    return authors

# Scrape user information and store it in csv file
def scrape_users(usernames, is_bot):
    data = {}
    i, deleted_count, exiting_count = 0, 0, 0
    for author in filter_usernames(usernames):
        redditor = Redditor()
        try:
            user = reddit.redditor(author)
                         
            redditor.username      = author
            redditor.post_karma    = user.link_karma
            redditor.comment_karma = user.comment_karma
            redditor.cake_day      = user.created_utc
            redditor.is_bot        = is_bot
            print('pass user #{} {}'.format(exiting_count, author))
            exiting_count +=1
        except Exception as e:
            print("Reddit account {} has been deleted #{}".format(author, deleted_count) )
            deleted_count += 1
            continue
        redditor.comments = get_user_comments(author)
        redditor.posts = get_user_posts(author)
        
        data = [redditor.username, redditor.post_karma, redditor.comment_karma , redditor.cake_day , redditor.comments , redditor.posts , redditor.is_bot]
        i+=1
    dataframe = pd.DataFrame(data)
    dataframe.to_csv('bots.csv')


def get_user_comments(author):
    comment_counter = 500
    last_utc = '1428624000'
    comments = []

    # Loop through all comments between 1428624000 (4/10/2015) to 1523318400 (4/10/18)
    # These are the dates that the bots were active
    while comment_counter == 500:
        comment_counter = 0

        # Add each comment to the user
        for comment in get_comment_data_from_user(author, last_utc)['data']:
            comments.append(create_comment_object_from_comment_data(comment))
            comment_counter = comment_counter + 1
            last_utc = str(comment['created_utc'] + 1)

    return comments

# Call Push Shift API to get Reddit user comments
def get_comment_data_from_user(author, last_utc):
    url = 'https://api.pushshift.io/reddit/comment/search?after=' + last_utc + '&before=1523318400&size=500&author=' + author
    web_url = urllib.request.urlopen(url)
    contents = web_url.read()
    encoding = web_url.info().get_content_charset('utf-8')
    data = json.loads(contents.decode(encoding))
    return data

def create_comment_object_from_comment_data(comment):
    # In case the subreddit has been deleted
    try:
        subreddit = comment['subreddit']
    except:
        subreddit = ''

    comment_object = {
        'body': comment['body'],
        'created_utc': comment['created_utc'],
        'score': comment['score'],
        'subreddit': subreddit
    }
    return comment_object

def get_user_posts(author):
    post_counter = 500
    last_utc = '1428624000'
    posts = []

    # Loop through all posts between 1428624000 (4/10/2015) to 1523318400 (4/10/2018)
    # These are the dates that the bots were active
    while post_counter == 500:
        post_counter = 0

        # Add each post to the user
        for post in get_post_data_from_user(author, last_utc)['data']:
            posts.append(create_post_object_from_post_data(post))
            post_counter = post_counter + 1
            last_utc = str(post['created_utc'] + 1)

    return posts

def create_post_object_from_post_data(post):
    # In case the subreddit has been deleted
    try:
        subreddit = post['subreddit']
    except:
        subreddit = ''

    post_object = {
        'created_utc': post['created_utc'],
        'num_comments': post['num_comments'],
        'over_18': post['over_18'],
        'score': post['score'],
        'subreddit': subreddit,
        'title': post['title']
    }

    # Some posts don't have selftext
    try:
        post_object['selftext'] = post['selftext']
    except KeyError:
        post_object['selftext'] = ''

    return post_object


# Call Push Shift API to collect user post data
def get_post_data_from_user(author, last_utc):
    url = 'https://api.pushshift.io/reddit/submission/search?after=' + last_utc \
        + '&before=1523318400&size=500&author=' + author
    web_url = urllib.request.urlopen(url)
    contents = web_url.read()
    encoding = web_url.info().get_content_charset('utf-8')
    data = json.loads(contents.decode(encoding))
    return data

def get_reddit_users_after_utc(last_utc):
    url = 'https://api.pushshift.io/reddit/comment/search?after=' + last_utc + '&before=1523318400&size=500'
    url = urllib.request.urlopen(url)
    contents = url.read()
    encoding = url.info().get_content_charset('utf-8')
    data = json.loads(contents.decode(encoding))
    return data

# Get account names from random reddit users
# We search all comments starting from 4/10/2015 0:00:00 (UTC)
def get_account_names_from_reddit(limit):
    last_utc = '1428624000'
    authors = []
 
    while len(authors) < limit:

        data = get_reddit_users_after_utc(last_utc)

        for comment in data['data']:
            authors.append(comment['author'])
            last_utc = str(comment['created_utc']+1)

    return authors[:limit]


def get_bot_usernames():

    # read bot file
    with open('_bots.txt', 'r') as data:
        lines = data.readlines()

    bot_usernames = []

    for line in lines:
        bot_usernames.append(line.split('\t')[0].split('/')[1])

    bot_redditors = []

    for name in bot_usernames:
        bot_redditors.append(reddit.redditor(name).name)
    
    bot_redditors.reverse()
    
    return bot_redditors


def getbots():
    with open('_bots2.txt', 'r') as data:
        lines = data.readlines()
    
    bot_usernames2 = []
    for line in lines:
        bot_usernames2.append(line.split('\n')[0].split('/')[2])
        bot_redditors2 = []
    for name in bot_usernames2:
        bot_redditors2.append(reddit.redditor(name).name)
    
    bot_redditors2.reverse()
    return bot_redditors2

  


accounts = get_bot_usernames()
accounts2 = getbots()

accounts2.extend(accounts)

accounts2 = list(set(accounts2))
print(len(accounts2))
scrape_users(list(set(accounts2)), True)