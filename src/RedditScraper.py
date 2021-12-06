from dotenv import load_dotenv
import os
import praw
from praw.models import MoreComments

load_dotenv()
reddit_user_agent = os.environ.get("REDDIT_USER_AGENT")
reddit_client_id = os.environ.get("REDDIT_CLIENT_ID")
reddit_client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
reddit_username = os.environ.get("REDDIT_USERNAME")
reddit_password = os.environ.get("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    password=reddit_password,
    user_agent=reddit_user_agent,
    username=reddit_username,
)

subs_to_scrape = [
    "AskReddit",
    # "facepalm",
    # "gaming",
    # "antiwork",
    # "wallstreetbets",
    # "MaliciousCompliance",
    # "NoStupidQuestions",
    # "AmItheAsshole",
    # "AskMen",
    # "AskWomen",
    # "unpopularopinion",
    # "todayilearned",
    # "tifu",
    # "explainlikeimfive",
    # "LifeProTips",
    # "TrueOffMyChest",
    # "TooAfraidToAsk",
    # "askscience",
    # "Showerthoughts",
    # "Jokes",
    # "AskHistorians"
]
comment_limit = 10


def create_todays_top():
    for sub_to_scrape in subs_to_scrape:
        this_sub = reddit.subreddit(sub_to_scrape)
        for submission in this_sub.top("day", limit=1):
            submission.comment_sort = "top"
            comments = []
            print(
                this_sub.title,
                submission.title,
                submission.author.name,
                submission.selftext,
            )
            for submission_comment in submission.comments[:comment_limit]:
                if isinstance(submission_comment, MoreComments):
                    continue
                else:
                    comment_summary = [
                        submission_comment.author.name,
                        submission_comment.body,
                        submission_comment.score,
                    ]
                    comments.append(comment_summary)
            # print(comments)


create_todays_top()
