import os
from pathlib import Path
cwd = os.getcwd()

projectPath = Path(__file__).parent.parent.parent.absolute()
iconsPath = os.path.join(projectPath, "icons")
flippedRedditPath = os.path.join(iconsPath, "flipped_reddit.png")
