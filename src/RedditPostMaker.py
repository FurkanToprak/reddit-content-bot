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
    return f'<div style="background-color: #030303;font-family: sans-serif;"><div style="color:#fff;font-size: 25px;">u/{author}</div><div style="color:#fff;margin-left:20;padding-left:10;border-left:3px solid #343536;">{bodyHtml}</div></div>'

new_html = createPostCommentHtml(
    "BigPlunk",
    "an\n\n\n\nexample of a wow\n really \n\ncool\n\n\nplace",
)

print(new_html)
