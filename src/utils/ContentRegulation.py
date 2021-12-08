import re

URLRegexPattern = '(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))?'
imageRegexPattern = '.*\.(jpe?g|png|gif|bmp)'
videoRegexPattern = '.*\.(mov|avi|wmv|flv|3gp|mp4|mpg)'
def hasUrl(str):
    return re.search(URLRegexPattern, str) is not None

def hasVideoUrl(url):
    if not hasUrl(url):
        return False
    return re.search(videoRegexPattern, url) is not None

def hasImgUrl(url):
    if not hasUrl(url):
        return False
    return re.search(imageRegexPattern, url) is not None

def postSFW(post):
    return not post.over_18

def postHasUrl(post):
    return post.url is not None and len(post.url) > 0

def postHasPic(post):
    return hasImgUrl(post.url)

def commentHasUrl(comment):
    return hasUrl(comment.body)