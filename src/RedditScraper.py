from dotenv import load_dotenv
import os
import praw
from praw.models import MoreComments
from tempfile import TemporaryDirectory
from RedditPostMaker import createPostHtml, createPostCommentHtml, htmlToImage
from utils.ContentRegulation import commentHasUrl
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
questions_per_day = 1
comment_limit = 10
comment_sort_method = "top"

def create_video(subreddit, submission):
    with TemporaryDirectory() as tmpDir:
        submission.comment_sort = comment_sort_method
        comments = []
        num_comments = 0
        for submission_comment in submission.comments:
            if num_comments == comment_limit:
                break
            else:
                num_comments += 1
            if isinstance(submission_comment, MoreComments):
                continue
            elif commentHasUrl(submission_comment):
                continue # skip URLS so text-to-speech doesn't mess up
            else:
                commentHtml = createPostCommentHtml(submission_comment.author.name, submission_comment.body)
                commentImage = htmlToImage(commentHtml, dir_path=tmpDir)
                print('comment', num_comments, commentImage)
                comments.append(commentImage)
        postHtml = createPostHtml(
            subreddit.title,
            submission.title,
            submission.author.name,
            submission.selftext,
        )
        postImg = htmlToImage(postHtml, dir_path=tmpDir)
        print(postImg)
        exit()


def create_todays_top():
    for sub_to_scrape in subs_to_scrape:
        this_sub = reddit.subreddit(sub_to_scrape)
        for submission in this_sub.top("day", limit=questions_per_day):
            create_video(this_sub, submission)


create_todays_top()