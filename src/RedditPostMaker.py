import os
from uuid import uuid4
from html2image import Html2Image
from PIL import Image
import cv2

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
    hti = Html2Image(output_path=dir_path)
    file_name = f"{uuid4()}.png"
    save_path = os.path.join(dir_path, file_name) # TODO: save in dir_path
    with open(save_path, 'w'):
        pass
    hti.screenshot(html_str=html, save_as=file_name, size=(1280, 360))
    return save_path

def combineImages(images, dir_path='', backgroundColor="#030303", size=(1280, 720)):
    combinedImage = Image.new("RGB", size, color=backgroundColor)
    for image in images:
        image_path = os.path.join(dir_path, image)
        pil_image = Image.open(image_path)
        center_image_height = pil_image.size[1]
        combinedImage.paste(pil_image, (0, center_image_height))
    imagePath = f'combined-{uuid4()}.png'
    fullImagePath = os.path.join(dir_path, imagePath)
    combinedImage.save(fullImagePath)
    return fullImagePath

def compileImagesToVideo(images, frame_lengths, dir_path='', size=(1280, 720), fps=1):
    videoPath = os.path.join(dir_path, f'{uuid4()}.mp4')
    fourcc= cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(videoPath, fourcc, fps, size)
    for i in range(len(images)):
        frame_length = round(frame_lengths[i])
        frame = cv2.imread(images[i])
        for _frame_step in range(frame_length):
            videoWriter.write(frame)
    videoWriter.release()
    return videoPath