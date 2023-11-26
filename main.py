import logging
import gvars as gvars
from connectors.youtubeChannel import Channel
from connectors.youtubeVideo import YouTubeVideo

# Create and configure the logger object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Overall minimum logging lovel

stream_handler = logging.StreamHandler()    # Configure the logging messages displayed in the Terminal
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)   # Minimum logging level for the StreamHandler

file_handler = logging.FileHandler(gvars.LOGS_PATH + 'info.log')  # Configure the logging messages written to a file
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)    # Minimum logging level for th FileHandler

logger.addHandler(stream_handler)
logger.addHandler(file_handler)




if __name__ == '__main__':  # Execute the following code only when executing main.py (not when importing it)
    url = 'https://www.youtube.com/@bbcvods5052/videos'
    channel = Channel(url, "BBCVODS", data_path=gvars.DATA_PATH)

    channel_videos = YouTubeVideo("BBCVODS", channel.get_channel_json())
    channel_videos.videos()