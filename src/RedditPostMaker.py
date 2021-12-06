def createPostHtml(subreddit, title, author, body):
    parsedBody = "".join(
        list(map(lambda bodyLine: f"<div>{bodyLine}</div>", body.split("\n")))
    )
    bodyHtml = f"<div>{parsedBody}</div>"
    return f'<div style="background-color: #030303;font-family: sans-serif;"><div><h style="color:#FF5700;font-size: 55px;"><b>r/{subreddit}</b></div><div><h style="color:#fff;font-size: 30px;"><b>{title}</b></h><div style="color:#818384">Posted by u/{author}</div></div><div style="color:#fff">{bodyHtml}</div></div>'


new_html = createPostHtml(
    "AskReddit",
    "What is your job and how much do you get paid?",
    "BigPlunk",
    "an\n\n\n\nexample of a wow\n really \n\ncool\n\n\nplace",
)
print(new_html)
