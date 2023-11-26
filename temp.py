import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def authenticate():
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

def download_authenticated_video(video_id, output_path='.'):
    # Authenticating and creating a YouTube API service
    credentials = authenticate()
    youtube = build('youtube', 'v3', credentials=credentials)

    # Retrieving video details
    try:
        video_info = youtube.videos().list(part='snippet', id=video_id).execute()
        title = video_info['items'][0]['snippet']['title']

        # Printing video title
        print(f"Video title: {title}")

        # Downloading the video (add your logic for downloading here)
        # ...
        
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")

# Example usage
video_id = "your_video_id"
download_authenticated_video(video_id)
