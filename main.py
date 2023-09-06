from connectors.youtubeChannel import Channel




if __name__ == '__main__':  # Execute the following code only when executing main.py (not when importing it)
    url = 'https://www.youtube.com/@bbcvods5052/videos'
    channel = Channel(url)
    channel.stop_driver()