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
Ge a service credential from Google Cloud, with Text-To-Speech API enabled.
Then set the environment variable:
```
export GOOGLE_APPLICATION_CREDENTIALS = "PATH/TO/GOOGLE_AUTH.json"
```