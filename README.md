# reddit-content-bot
Uploads automated videos made from scraped reddit posts using text-to-speech.
# Dependencies
## Browser
Requires `Chrome` or `Chromium` browser for `HTML2Image`.
## Installing
`pipenv install`
## Activate Environment
`pipenv shell`
# .env file
Keep a file named `.env` at the root of the project directory. The format should look like:
```
REDDIT_USER_AGENT=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USERNAME=
REDDIT_PASSWORD=
```
# Set Environment Variable to Google OAuth JSON

# Run
```
./make_vids.sh
```

# Aborting and Error Catching
Sometimes the google text-to-speech API will corrupt (probably input-based) or the Youtube API will meet some quota or spam filter. If any of these errors occur, or you'd like to prematurely abort by using [Ctrl + C] on the terminal, you will get the output in the form of an array of JSONS:
```
[{
title: string; # video title
video: string; # path to video
thumbnail; string # path to thumbnail
}...]
```
# Configuring Cloud Credentials
* Enable `Youtube Data API v3` and `Text-To-Speech API` on [google console.](https://console.cloud.google.com/apis/)
* Generate a service account 
* save the credentials in `.env` under the aforementioned schema.
* Generate an OAuth 2.0 Client ID (Desktop Client) and save the json on disk.
* Then set the environment variable: `export GOOGLE_APPLICATION_CREDENTIALS = "PATH/TO/GOOGLE_AUTH.json"`

# The results
The program can automatically upload to YouTube as well (must be enabled through the code (See `VideoPoster.py`)), but the videos may be caught in a "Spam Filter", which is against the YouTube ToS and will be uploaded as private, non-monetized videos.

The program will open to your temp directory with all of the content and component content if you want to edit anything in/out. If you're just interested in seeing the final output, just search for `"["` within the file explorer and you'll narrow it down to your titles, thumbnails, and videos.

# Customize your channel
Replace `icons/logo.png` with any icon, thumbnail-memes/ with a meme folder (`.jpg`, `.png`, `.webp`), and `sounds/intro.png` with any sound you wish.

## Memes on the thumbnails
In an attempt to make sexier thumbnails, I take a randomly selected wojak and I paste it in the thumbnail. Get your own meme folder and employ it for engagement purposes.
