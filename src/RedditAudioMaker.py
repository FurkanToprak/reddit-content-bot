from uuid import uuid4
from moviepy.editor import VideoFileClip, AudioFileClip
import os

def stitchAudioToMovie(moviePath, audioPath, outputPath, dir_path=''):
    videoClip = VideoFileClip(moviePath)
    audioClip = AudioFileClip(audioPath)
    videoClip.audio = audioClip
    videoClip.write_videofile(outputPath)
    videoClip.close()
    return outputPath