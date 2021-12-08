#from YouTubeAdmin import uploadYoutube
from dotenv import load_dotenv
import os
import praw
from praw.models import MoreComments
from tempfile import TemporaryDirectory
from RedditPostMaker import compileImagesToVideo, createPostHtml, createPostCommentHtml, createThumbnail, htmlToImage, combineImages
from RedditAudioMaker import stitchAudioToMovie
from utils.ContentRegulation import commentHasUrl, hasImgUrl, hasVideoUrl
from utils.TextToSpeech import createAudio
from utils.Paths import projectPath
from YouTubeAdmin import uploadYoutube

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(projectPath, "google_auth.json")
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
    # "AskReddit",
    # "facepalm",
    # "antiwork",
    # "MaliciousCompliance",
    # "NoStupidQuestions",
    "AmItheAsshole",
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
questions_per_sub = 3
comment_limit = 15
comment_sort_method = "top"

def create_video(subreddit, submission, dir_path=''):
        postHtml = createPostHtml(
            subreddit.display_name,
            submission.title,
            submission.author.name,
            submission.selftext,
            submission.url if hasImgUrl(submission.url) else None
        )
        postCombinedText = submission.title + ' ' + submission.selftext
        postImg = combineImages([htmlToImage(postHtml, prefix='post-pic',dir_path=dir_path)], dir_path=dir_path)
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
                comment_author = submission_comment.author.name if submission_comment.author else "[deleted]"
                commentHtml = createPostCommentHtml(comment_author, submission_comment.body)
                commentImage = combineImages([htmlToImage(commentHtml, prefix='comment-pic',dir_path=dir_path)], dir_path=dir_path)
                texts.append(submission_comment.body)
                frames.append(commentImage)
        # create corresponding audio
        combinedAudioPath, postAudioLengths = createAudio(texts, dir_path=dir_path)
        # stitch all audio and slides.
        videoPath = compileImagesToVideo(frames, postAudioLengths, dir_path=dir_path)
        finalVideoPath = stitchAudioToMovie(videoPath, combinedAudioPath, dir_path=dir_path)
        finalVideoTitle = f'{submission.title} | r/{subreddit.display_name}'
        return finalVideoPath, submission.title, finalVideoTitle

def create_todays_top(uploadToYouTube=False):
    with TemporaryDirectory() as tmpDir:
        finalVids = []
        for sub_to_scrape in subs_to_scrape:
            this_sub = reddit.subreddit(sub_to_scrape)
            sub_title = this_sub.title
            for submission in this_sub.top("day", limit=questions_per_sub):
                if hasVideoUrl(submission.url): # filter options
                    print("Skipped reddit post:", submission.permalink)
                    continue # skip if links to something that is not an image
                sub_video, post_title, sub_video_title = create_video(this_sub, submission, tmpDir)
                thumbnail_path = createThumbnail(this_sub, post_title, tmpDir)
                sub_movie_description = f"Reddit shorts funny compilation. {sub_video_title}"
                sub_movie_tags = [ "reddit", "compilation", "funny", sub_title, f"r/{this_sub}" ]
                sub_movie_category = 1 # see: https://github.com/jonnekaunisto/simple-youtube-api/blob/master/simple_youtube_api/youtube_constants.py
                finalVids.append({'title': sub_video_title, 'video': sub_video, 'thumbnail': thumbnail_path})
                if uploadToYouTube:
                    uploadYoutube(sub_video, sub_video_title, sub_movie_description, sub_movie_tags, sub_movie_category, thumbnail_path)
        if not uploadToYouTube:
            print('Output directory:', tmpDir)
            print('Videos:', finalVids)
            while True:
                pass # suspend program so videos can be selected

create_todays_top()