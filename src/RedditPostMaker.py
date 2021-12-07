import os
from uuid import uuid4
from html2image import Html2Image


def createPostHtml(subreddit, title, author, body):
    parsedBody = "".join(
        list(map(lambda bodyLine: f"<div>{bodyLine}</div>", body.split("\n")))
    )
    bodyHtml = f"<div>{parsedBody}</div>"
    return f'<div style="background-color: #030303;font-family: sans-serif;"><div><h style="color:#FF5700;font-size: 55px;"><b>r/{subreddit}</b></div><div><h style="color:#fff;font-size: 30px;"><b>{title}</b></h><div style="color:#818384">Posted by u/{author}</div></div><div style="color:#fff">{bodyHtml}</div></div>'


def createPostCommentHtml(author, body):
    parsedBody = "".join(
        list(map(lambda bodyLine: f"<div>{bodyLine}</div>", body.split("\n")))
    )
    bodyHtml = f"<div>{parsedBody}</div>"
    return f'<div style="background-color: #030303;font-family: sans-serif;"><div style="color:#FF5700;font-size: 25px;">u/{author}</div><div style="color:#fff;margin-left:20;padding-left:10;border-left:3px solid #343536;">{bodyHtml}</div></div>'


def htmlToImage(html, dir_path=''):
    hti = Html2Image()
    file_name = f"{uuid4()}.png"
    # save_path = os.path.join(dir_path, file_name) # TODO: save in dir_path
    with open(file_name, 'w'):
        pass
    hti.screenshot(html_str=html, save_as=file_name, size=(1080, 360))
    return file_name