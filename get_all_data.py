import pymongo
import time
import datetime
import pandas as pd
import numpy as np
from urllib.parse import quote_plus
from urllib.error import HTTPError
from collections import Counter
import pickle
import os

# client = pymongo.MongoClient('mongodb://localhost:27017')

username = quote_plus('CMPS287_project')
password = quote_plus('CMPS287_project_password')

URI = "mongodb+srv://" + username + ":" + password + "@cluster0.unwq2.mongodb.net"
client = pymongo.MongoClient(URI)

db = client['redditors']
collection = db['redditors']
print(client.list_database_names())


def get_post_data_from_mongo_for_user(username):
    return get_post_data_from_mongo(username)


def get_comment_data_from_mongo_for_user(username):
    return get_comment_data_from_mongo(username)


def get_post_data_from_mongo_for_all():
    return get_post_data_from_mongo('')


def get_comment_data_from_mongo_for_all():
    return get_comment_data_from_mongo('')


def print_comment_numbers(X_comments, Y_comments):
    print('num comments: ' + str(len(X_comments)))
    print('\tnum bot comments: ' + str(Y_comments.count(1)))
    print('\tnum user comments: ' + str(Y_comments.count(0)))


def print_post_numbers(X_posts, Y_posts):
    print('num posts: ' + str(len(X_posts)))
    print('\tnum bot posts: ' + str(Y_posts.count(1)))
    print('\tnum user posts: ' + str(Y_posts.count(0)))


def get_comment_data_from_mongo(username):
    X_comments, Y_comments, X_comments_sub, Y_comments_sub = [], [], [], []
    # Get data from database
    for doc in get_redditor_collection().find({}):

        if doc['username'] == username:
            continue

        # Skip is account contains no comment and no posts
        if len(doc['comments']) < 1:
            continue

        X_comments_sub_obj = ''

        for comment in doc['comments']:
            X_comments_sub_obj = X_comments_sub_obj + comment['subreddit'] + ' '
            X_comments.append(comment['body'])
            if doc['is_bot']:
                Y_comments.append(1)
            else:
                Y_comments.append(0)

        # Add subreddit data
        X_comments_sub.append(X_comments_sub_obj)
        if doc['is_bot']:
            Y_comments_sub.append(1)
        else:
            Y_comments_sub.append(0)
    return (X_comments, X_comments_sub, Y_comments, Y_comments_sub)


def get_post_data_from_mongo(username):
    X_posts, Y_posts, X_posts_sub, Y_posts_sub = [], [], [], []
    # Get data from database
    for doc in get_redditor_collection().find({}):

        if doc['username'] == username:
            continue

        # Skip is account contains no comment and no posts
        if len(doc['posts']) < 1:
            continue

        X_posts_sub_obj = ''

        for post in doc['posts']:
            X_posts_sub_obj = X_posts_sub_obj + post['subreddit'] + ' '
            X_posts.append(post['title'])
            if doc['is_bot']:
                Y_posts.append(1)
            else:
                Y_posts.append(0)

        X_posts_sub.append(X_posts_sub_obj)
        if doc['is_bot']:
            Y_posts_sub.append(1)
        else:
            Y_posts_sub.append(0)
    return (X_posts, X_posts_sub, Y_posts, Y_posts_sub)


def get_redditor_collection():
    db = client['redditors']
    collection = db['redditors']
    return collection

def get_all_and_pickle():

    commets_data = get_comment_data_from_mongo_for_all()
    posts_data   = get_post_data_from_mongo_for_all()

    
    # pickle comments data
    names = ("X_comments", "X_comments_sub", "Y_comments", "Y_comments_sub")
    for i in range(len(commets_data)):
        path = os.path.join("data", "comments" , names[i]+'.pkl')
        with open(path, 'wb') as f:
           mynewlist = pickle.dump(commets_data[i], f)

    # pickle posts data
    names = ("X_posts", "X_posts_sub", "Y_posts", "Y_posts_sub")
    for i in range(len(commets_data)):
        path = os.path.join("data", "posts" , names[i]+'.pkl')
        
        with open( path, 'wb') as f:
            mynewlist = pickle.dump(posts_data[i], f)
    
    X_posts = posts_data[0]
    Y_posts = posts_data[2]

    X_comments = commets_data[0]
    Y_comments = commets_data[2]

    print('------------------------------------------------------------')
    print_post_numbers(X_posts, Y_posts)
    print_comment_numbers(X_comments, Y_comments)
    print('------------------------------------------------------------')

get_all_and_pickle()

client.close()
