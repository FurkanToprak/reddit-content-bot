import os
import random
from pathlib import Path
cwd = os.getcwd()

projectPath = Path(__file__).parent.parent.parent.absolute()
iconsPath = os.path.join(projectPath, "icons")
memesPath = os.path.join(projectPath, "thumbnail-memes")
memesPaths = os.listdir(memesPath)
memesPaths.remove('.keep')
def getRandomMemePath():
    randomMemeIndex = random.randint(0, len(memesPaths) - 1)
    randomMemePath = os.path.join(memesPath, memesPaths[randomMemeIndex])
    return randomMemePath
logoPath = os.path.join(iconsPath, "logo.png")
ytSecretPath = os.path.join(projectPath, "yt_client_secret.json")
credentialStoragePath = os.path.join(projectPath, "credentials.storage")
introMusicPath = os.path.join(projectPath, "sounds", "intro.mp3")