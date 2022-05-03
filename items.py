class Redditor:
    username = ''
    post_karma = 0
    comment_karma = 0
    cake_day = 0
    is_bot = False
    comments = []
    posts = []

    def Redditor(self):
        self.username = ''
        self.post_karma = 0
        self.comment_karma = 0
        self.cake_day = 0
        self.is_bot = False
        self.comments = []
        self.posts = []

    def __setitem__(self, key, value):
        self[key] = value

class Post:
    created_utc = ''
    num_comments = 0
    over_18 = True
    score = 0
    subreddit = False
    title = ""
    selftext = ""

    def Post(self):
        self.created_utc = ''
        self.num_comments = 0
        self.over_18 = True
        self.score = 0
        self.subreddit = False
        self.title = ""
        self.selftext = ""

class Comment:
    body = ''
    created_utc = 0
    subreddit = ""
    score = 0
    
    def Comment(self):
        self.body = ''
        self.created_utc = 0
        self.subreddit = ""
        self.score = 0