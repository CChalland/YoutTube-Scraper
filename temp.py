import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import yt_dlp

def authenticate():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
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
            # credentials = flow.run_local_server(port=0)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    return credentials

def download_captions(youtube, video_id, output_path='.', language='en'):
    try:
        captions = youtube.captions().list(part='snippet', videoId=video_id).execute()

        if 'items' in captions and captions['items']:
            for caption in captions['items']:
                caption_id = caption['id']
                caption_info = youtube.captions().download(id=caption_id, tfmt='srt').execute()
                caption_content = caption_info['body']
                caption_language = caption['snippet']['language']

                if caption_language.lower() == language.lower():
                    # Save the English caption content to a file
                    caption_filename = f'{output_path}/{video_id}_caption_{caption_id}_{language}.srt'
                    with open(caption_filename, 'w', encoding='utf-8') as caption_file:
                        caption_file.write(caption_content)

                    print(f"English caption downloaded: {caption_filename}")
        else:
            print(f"No captions found for video {video_id}")

    except HttpError as e:
        if e.resp.status == 403:
            print(f"Permission error: {e}")
        else:
            print(f"An HTTP error occurred while downloading captions: {e}")

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

        # Downloading the video using youtube_dl
        stream_url = f'https://www.youtube.com/watch?v={video_id}'
        ydl_opts = {
            'outtmpl': f'{output_path}/{title}.mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([stream_url])

        # Downloading English captions
        download_captions(youtube, video_id, output_path, language='en')

        print(f"Video '{title}' downloaded successfully.")

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")



# Example usage
video_id = "eHixo19tBEg"
# download_authenticated_video(video_id)

credentials = authenticate()
youtube = build('youtube', 'v3', credentials=credentials)
download_captions(youtube, video_id)