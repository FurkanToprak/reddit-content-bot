import re

URLRegexPattern = '(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))?'
def commentHasUrl(comment):
    return re.search(URLRegexPattern, comment.body) is not None

def postHasUrl(post):
    pass

def postHasPic(post):
    pass

def commentHasPic(post):
    pass