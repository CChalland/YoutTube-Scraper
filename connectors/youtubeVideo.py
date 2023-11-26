import json
import time
import logging
import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yt_dlp


HOME = str(os.getcwd())
FILES_FOLDER = HOME + '/'
DATA_PATH = FILES_FOLDER + "data/"
logger = logging.getLogger()
api_service_name = "youtube"
api_version = "v3"

class YouTubeVideo:
    def __init__(self, channel_name, channel_json):
        self._path = os.path.join(DATA_PATH, channel_name, "videos")
        self.channel_name = channel_name
        self.channel_json = channel_json



    def authenticate(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        credentials = None
        SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

        if os.path.exists('token.json'):
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_file('token.json')

        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(google.auth.transport.requests.Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', SCOPES)
                credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())

        return credentials


    def download_captions(self, youtube, video_id, output_path='.', language='en'):
        try:
            captions = youtube.captions().list(part='snippet', videoId=video_id).execute()
            print(captions)

        except HttpError as e:
            if e.resp.status == 403:
                print(f"Permission error: {e}")
            else:
                print(f"An HTTP error occurred while downloading captions: {e}")


    def download_authenticated_video(self, video_id, output_path):
        # Authenticating and creating a YouTube API service
        credentials = self.authenticate()
        youtube = build('youtube', 'v3', credentials=credentials)

        # Retrieving video details
        try:
            video_info = youtube.videos().list(part='snippet', id=video_id).execute()
            title = video_info['items'][0]['snippet']['title']

            # Printing video title
            print(f"Video title: {title}")

            # Downloading the video using youtube_dl
            stream_url = f'https://www.youtube.com/watch?v={video_id}'
            ydl_opts = {
                'outtmpl': f'{output_path}/{title}.mp4',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([stream_url])

            # Downloading English captions
            self.download_captions(youtube, video_id, output_path, language='en')

            print(f"Video '{title}' downloaded successfully.")

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")

    def videos(self):
        if not os.path.exists(self._path):
            logger.info("Path not found at %s", str(self._path))
            os.mkdir(self._path)
            logger.info("Created path at %s", str(self._path))
        else:
            logger.info("Path found at %s", str(self._path))
                
        for item in self.channel_json:
            video_path = os.path.join(self._path, item["yt_id"])
            if not os.path.exists(video_path):
                logger.info("Path not found at %s", str(video_path))
                os.mkdir(video_path)
                logger.info("Created path at %s", str(video_path))
            else:
                logger.info("Path found at %s", str(video_path))
            
            self.download_authenticated_video(item["yt_id"], video_path)
            




if __name__ == '__main__':  # Execute the following code only when executing main.py (not when importing it)
    url = 'https://www.youtube.com/@bbcvods5052/videos'