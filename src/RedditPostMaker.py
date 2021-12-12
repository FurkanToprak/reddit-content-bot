import os
from uuid import uuid4
from html2image import Html2Image
from PIL import Image
import cv2
from utils.Paths import getRandomMemePath, logoPath


def createIntroHtml():
    return f'<div style="background-color: #ff571e;display: flex; align-items: center; flex-direction: column;"><img src="{logoPath}" style="max-height: 600;"/><div style="font-family: sans-serif; color: white; font-size: 50px;text-align: center;">Lost Inside <b>Reddit</b></div><div style="font-family: sans-serif; color: white; font-size: 30px;text-align: center;">subscribe for daily content!</div></div>'


def createPostHtml(subreddit, title, author, body, imgUrl):
    parsedBody = "".join(
        list(map(lambda bodyLine: f"<div>{bodyLine}</div>", body.split("\n")))
    )
    bodyHtml = f"<div>{parsedBody}</div>"
    imgHtml = (
        "" if imgUrl is None else f'<img style="max-height:350px;" src="{imgUrl}">'
    )
    return f'<div style="background-color: #030303;font-family: sans-serif;">{imgHtml}<div><h style="color:#FF5700;font-size: 55px;"><b>r/{subreddit}</b></div><div><h style="color:#fff;font-size: 30px;"><b>{title}</b></h><div style="color:#818384">Posted by u/{author}</div></div><div style="color:#fff">{bodyHtml}</div></div>'


def createPostCommentHtml(author, body):
    parsedBody = "".join(
        list(map(lambda bodyLine: f"<div>{bodyLine}</div>", body.split("\n")))
    )
    bodyHtml = f"<div>{parsedBody}</div>"
    return f'<div style="background-color: #030303;font-family: sans-serif;"><div style="color:#FF5700;font-size: 25px;">u/{author}</div><div style="color:#fff;margin-left:20;padding-left:10;border-left:3px solid #343536;">{bodyHtml}</div></div>'


def htmlToImage(html, prefix="", dir_path=""):
    hti = Html2Image(output_path=dir_path)
    file_name = f"{prefix}-{uuid4()}.png"
    save_path = os.path.join(dir_path, file_name)
    with open(save_path, "w"):
        pass
    try:
        hti.screenshot(html_str=html, save_as=file_name, size=(1280, 720))
    except Exception as err:
        print('error')
        print(err)
    return save_path


def combineImages(
    images,
    outputPath,
    dir_path="",
    backgroundColor="#030303",
    size=(1280, 720),
):
    combinedImage = Image.new("RGB", size, color=backgroundColor)
    for image in images:
        image_path = os.path.join(dir_path, image)
        pil_image = Image.open(image_path)
        center_image_height = (size[1] - pil_image.size[1]) // 2
        combinedImage.paste(pil_image, (0, center_image_height))
    combinedImage.save(outputPath)
    return outputPath


def compileImagesToVideo(images, frame_lengths, dir_path="", size=(1280, 720), fps=4):
    videoPath = os.path.join(dir_path, f"{uuid4()}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    videoWriter = cv2.VideoWriter(videoPath, fourcc, fps, size)
    # add intro
    intro_image = htmlToImage(createIntroHtml(), "intro-img", dir_path=dir_path)
    intro_frame = cv2.imread(intro_image)
    intro_frame_length = round(frame_lengths[0] * fps)
    for _frame_step_intro in range(intro_frame_length):
        videoWriter.write(intro_frame)
    # add content
    for i in range(len(images)):
        frame_length = round(frame_lengths[1 + i] * fps)
        frame = cv2.imread(images[i])
        for _frame_step in range(frame_length):
            videoWriter.write(frame)
    videoWriter.release()
    return videoPath


def createThumbnailBanner(subreddit, dir_path=""):
    print(getRandomMemePath())
    html = f'<div style="width: 1280;height:720;text-align: center;display:flex;flex-direction:column;justify-content:center;align-items:center;background-color: #ff571e;"><div><img src="{logoPath}" style="max-height:300px"/><img src="{getRandomMemePath()}" style="max-height:300px"/><div><div style="color: #fff;font-family: sans-serif;font-size: 50px;padding-top: 30px;"><b><u>r/{subreddit}</u></b></div></div>'
    return htmlToImage(html, prefix="thumbnail", dir_path=dir_path)


def createThumbnail(subreddit, thumbnailPath, dir_path=""):
    titleBannerImage = createThumbnailBanner(subreddit, dir_path=dir_path)
    thumbnailPath = combineImages(
        [titleBannerImage],
        thumbnailPath,
        dir_path=dir_path,
        backgroundColor="#ff571e",
        size=(1280, 720),
    )
    return thumbnailPath
