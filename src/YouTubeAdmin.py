from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# loggin into the channel
channel = Channel()
channel.login("yt_client_secret.json", "credentials.storage") # client secret path, storage path

def uploadYoutube(videoPath, title, description, tags, category, thumbnailPath):
    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path=videoPath)

    # setting snippet
    video.set_title(title)
    video.set_description(description)
    video.set_tags(tags)
    video.set_category(category)
    video.set_default_language("en-US")

    # setting status
    video.set_embeddable(True)
    video.set_license("creativeCommon")
    video.set_privacy_status("public")
    video.set_public_stats_viewable(True)

    # setting thumbnail
    video.set_thumbnail_path(thumbnailPath)

    # uploading video and printing the results
    video = channel.upload_video(video)