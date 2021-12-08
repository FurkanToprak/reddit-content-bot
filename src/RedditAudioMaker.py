from uuid import uuid4
from moviepy.editor import VideoFileClip, AudioFileClip
import os

def stitchAudioToMovie(moviePath, audioPath, dir_path=''):
    videoPath = os.path.join(dir_path, f'final-sound-{uuid4()}.mp4')
    videoClip = VideoFileClip(moviePath)
    print('taking audio from', audioPath)
    audioClip = AudioFileClip(audioPath)
    videoClip.audio = audioClip
    videoClip.write_videofile(videoPath)
    videoClip.close()
    return videoPath