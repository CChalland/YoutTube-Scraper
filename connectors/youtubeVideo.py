import json
import time
import os
import logging
from pytube import YouTube


HOME = str(os.getcwd())
FILES_FOLDER = HOME + '/'
DATA_PATH = FILES_FOLDER + "data/"
logger = logging.getLogger()

class YouTubeVideo:
    def __init__(self, channel_name, channel_json):
        self._path = os.path.join(DATA_PATH, channel_name, "videos")
        self.channel_name = channel_name
        self.channel_json = channel_json
        


    def videos(self):
        if not os.path.exists(self._path):
            logger.info("Path not found at %s", str(self._path))
            os.mkdir(self._path)
            logger.info("Created path at %s", str(self._path))
        else:
            logger.info("Path found at %s", str(self._path))
                
        for item in self.channel_json:
            self.download_video(item['video_url'], self._path)
    
    def download_video(self, url, output_path):
        try:
            # Create a YouTube object
            yt = YouTube(url)
            yt.bypass_age_gate()
            
            # Get the highest resolution stream
            video_stream = yt.streams.get_highest_resolution()
            
            # Download the video to the specified output path
            video_stream.download(output_path)
            print(f"Video '{yt.title}' downloaded successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")