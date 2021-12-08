from dotenv import load_dotenv
import os
import praw
from praw.models import MoreComments
from tempfile import TemporaryDirectory
from RedditPostMaker import compileImagesToVideo, createPostHtml, createPostCommentHtml, htmlToImage, combineImages
from RedditAudioMaker import stitchAudioToMovie
from utils.ContentRegulation import commentHasUrl
from utils.TextToSpeech import createAudio
from pathlib import Path

load_dotenv()

projectDir = Path(os.getcwd()).parent.absolute()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(projectDir, "google_auth.json")
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
        postHtml = createPostHtml(
            subreddit.title,
            submission.title,
            submission.author.name,
            submission.selftext,
        )
        postCombinedText = submission.title + ' ' + submission.selftext
        postImg = combineImages([htmlToImage(postHtml, dir_path=tmpDir)], dir_path=tmpDir)
        frames = [postImg]
        submission.comment_sort = comment_sort_method
        num_comments = 0
        texts = [ postCombinedText ]
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
                commentImage = combineImages([htmlToImage(commentHtml, dir_path=tmpDir)], dir_path=tmpDir)
                texts.append(submission_comment.body)
                frames.append(commentImage)
        # create corresponding audio
        combinedAudioPath, postAudioLengths = createAudio(texts, dir_path=tmpDir)
        # stitch all audio and slides.
        videoPath = compileImagesToVideo(frames, postAudioLengths, dir_path=tmpDir)
        finalVideoPath = stitchAudioToMovie(videoPath, combinedAudioPath, dir_path=tmpDir)
        print(finalVideoPath)
        return finalVideoPath

def create_todays_top():
    for sub_to_scrape in subs_to_scrape:
        this_sub = reddit.subreddit(sub_to_scrape)
        for submission in this_sub.top("day", limit=questions_per_day):
            create_video(this_sub, submission)


create_todays_top()