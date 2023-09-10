import os
import re
import json
import time
import logging
import requests
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from youtube_transcript_api import YouTubeTranscriptApi

logger = logging.getLogger()


class Youtube:
    def __init__(self, url):
        """
        :param url:
        """
        self._channel_name = ""
        self._channel_url = url
        self._filename = ""
        self._data = []
        self._data_len = 0
        self._items = []
        self._item_count = 180
        self.SCROLL_PAUSE_TIME = 1
        
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Firefox(gvars.SELENIUM_FIREFOX)
        self.driver.get(url)
    
    
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
    
    
    def _start_up(self) -> None:
        self._channel_name = self.driver.find_element(By.CSS_SELECTOR,'yt-formatted-string#text').text
        time.sleep(3)
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        
        while self._item_count > len(self._items):
            self.driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            time.sleep(self.SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        try:
            for e in WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
                title = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('title')
                vurl = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('href')
                views= e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]').text
                date_time = e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]').text
                yt_id = vurl.split('=')[-1]
                captions = YouTubeTranscriptApi.get_transcript(yt_id)
                print(captions)
                
                # self._data.append({'yt_id': yt_id, 'video_url': vurl, 'title': title, 'date_time': date_time, 'views': views})
        except:
            pass
        
        self._data_len = len(self._data)
        print(self._data)
        
        self.stop_driver()
    
    
    
    def filter_on_captions(self, yt_id: str):
        print(yt_id)
    
    
    def save_json(self) -> None:
        self._filename = gvars.DATA_PATH + self._channel_name + ".json"
        # Serializing json
        json_object = json.dumps(self._data, indent=4)
        # Writing to sample.json
        with open(self._filename, "w+") as outfile:
            outfile.write(json_object)
    
    
    def stop_driver(self) -> None:
        self.driver.quit()
    
    
    def read_data(self):
        print(self._data)






if __name__ == '__main__':  # Execute the following code only when executing main.py (not when importing it)
    sample_channel_url = 'https://www.youtube.com/@bbcvods5052/videos'
    sample_video_url = "https://www.youtube.com/watch?v=psFCaWqVthI"
    
    yt = Youtube(sample_channel_url)
    yt._start_up()
    # yt.filter_on_captions(sample_video_url)