from google.cloud import texttospeech
from mutagen.mp3 import MP3
from uuid import uuid4
import os
from moviepy.editor import concatenate_audioclips, AudioFileClip
client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)


def createAudio(paragraphs, dir_path=''):
    audios = []
    audio_lengths = []
    for paragraph in paragraphs:
        synthesis_input = texttospeech.SynthesisInput(text=paragraph)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        mp3Path = os.path.join(dir_path, f"{uuid4()}.mp3")
        with open(mp3Path, "wb") as mp3Output:
            mp3Output.write(response.audio_content)
        audio_mp3 = MP3(mp3Path)
        audio_lengths.append(audio_mp3.info.length)
        mp3 = AudioFileClip(mp3Path)
        audios.append(mp3)
    final_clips = concatenate_audioclips(audios)
    final_path = os.path.join(dir_path, f"combined-{uuid4()}.mp3")
    final_clips.write_audiofile(final_path)
    return final_path, audio_lengths
