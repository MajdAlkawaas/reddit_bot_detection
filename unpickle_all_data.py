# import this file and use the functions for your work

import pickle
import os
import pprint as pp

 
COMMENTS_PATH = os.path.join("data", "comments" )
POSTS_PATH    = os.path.join("data", "posts")

def unpickle_comments(path= COMMENTS_PATH):
    """
        - unpickle the comments data files.
        - each consist of a list of data
        @param path of the comments data folder
        @return comments_data dictionary of lists with the following keys:
            ['X_comments', 'X_comments_sub', 'Y_comments', 'Y_comments_sub']
    """

    # Retrieve the the list of files in the target folder
    files_list = os.listdir(path)

    # dictionary where the data of each file is gonna be stored
    comments_data = {}

    for file in files_list:
        file_path = os.path.join(path, file)
        # unpickling
        with open(file_path, 'rb') as f:
            # removing the .pkl from the file name
            key_name = file.split(".")[0]
            # using the file name as the dictionary keys
            comments_data[key_name] = pickle.load(f)  
    return comments_data 



def unpickle_posts(path= POSTS_PATH):
    """
        - unpickle the posts data files.
        - each consist of a list of data
        @param path of the posts data folder
        @return posts_data dictionary of lists with the following keys:
            ['X_posts', 'X_posts_sub', 'Y_posts', 'Y_posts_sub']
    """

    # Retrieve the the list of files in the target folder
    files_list = os.listdir(path)

    # dictionary where the data of each file is gonna be stored
    posts_data = {}

    for file in files_list:
        file_path = os.path.join(path, file)

        # unpickling
        with open(file_path, 'rb') as f:
            # removing the .pkl from the file name
            key_name = file.split(".")[0]

            # using the file name as the dictionary keys
            posts_data[key_name] = pickle.load(f)     
    return posts_data 


comments_data = unpickle_comments()
posts_data    = unpickle_posts()

print("Comments data: {}".format(comments_data.keys()))
print("Posts data:    {}".format(posts_data.keys()))