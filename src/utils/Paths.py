import os
from pathlib import Path
cwd = os.getcwd()

projectPath = Path(__file__).parent.parent.parent.absolute()
iconsPath = os.path.join(projectPath, "icons")
flippedRedditPath = os.path.join(iconsPath, "flipped_reddit.png")
ytSecretPath = os.path.join(projectPath, "yt_client_secret.json")
credentialStoragePath = os.path.join(projectPath, "credentials.storage")
introMusicPath = os.path.join(projectPath, "sounds", "intro.mp3")