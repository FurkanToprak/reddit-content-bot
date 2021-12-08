from uuid import uuid4
from moviepy.editor import VideoFileClip, AudioFileClip 
import os

def stitchAudioToMovie(moviePath, audioPath, dir_path=''):
    videoPath = os.path.join(dir_path, f'final-sound-{uuid4()}.mp4')
    videoClip = VideoFileClip(moviePath)
    audioClip = AudioFileClip(audioPath)
    videoClip.set_audio(audioClip)
    videoClip.write_videofile(videoPath)
    return videoPath