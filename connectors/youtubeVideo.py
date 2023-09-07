import json
import time
import os
import logging
from pytube import YouTube

logger = logging.getLogger()

class YouTubeVideo:
    def __init__(self, url):
        self._channel_url = url
        self._data = []
        self.caption_loaded_data = []
        self._load_data()
    
    
    def _load_data(self):
        raw_file_data = []
        dataFolder = '/Users/cchalland/Code/Python-3/Projects/Youtube/data'
        if not os.path.exists(dataFolder):
            logger.error("Data folder not found at %s", str(dataFolder))
        
        for root, dir_names, file_names in os.walk(dataFolder):
            for file in file_names:
                try:
                    with open(root + "/" + file) as f:
                        raw_file_data = json.load(f)
                except Exception as e:
                    logger.error('WARNING_JS: failed to load json file: %s', str(e))
                self._data.append({'filename': file, 'raw_data': raw_file_data, 'caption_loaded_data': []})
    
    
    def filter_on_captions(self):
        index = 0
        for channel in self._data:
            # print(channel['raw_data'])
            for video in channel['raw_data']:
                print("Video", index, ":", video['title'])
                index += 1
                yt = YouTube(video['video_url'])
                if len(yt.captions) > 0:
                    channel['caption_loaded_data'].append(video)
    
    
    
    def read_data(self):
        print(self._data)




if __name__ == '__main__':  # Execute the following code only when executing main.py (not when importing it)
    url = "https://www.youtube.com/watch?v=psFCaWqVthI"
    yt = YouTubeVideo(url)
    
    yt.filter_on_captions()
    yt.read_data()