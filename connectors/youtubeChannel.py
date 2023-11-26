import os
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger()

class Channel:
    def __init__(self, url, channel_name, data_path):
        """
        :param url:
        """
        self._path_data = os.path.join(data_path, channel_name)
        self._channel_url = url
        self._filename = ""
        self._len_data = 0
        self._items = []
        self._item_count = 180
        self.SCROLL_PAUSE_TIME = 1
        self.channel_name = channel_name
        self.data = []
        self._load_data()



    def _load_data(self):
        raw_file_data = []
        if not os.path.exists(self._path_data):
            logger.error("Data folder not found at %s", str(self._path_data))
        
        for root, dir_names, file_names in os.walk(self._path_data):
            for file in file_names:
                try:
                    with open(root + "/" + file) as f:
                        raw_file_data = json.load(f)
                except Exception as e:
                    logger.error('WARNING_JS: failed to load json file: %s', str(e))
                print(raw_file_data)
            
            for item in raw_file_data:
                self.data.append(item)


    def _save_json(self) -> None:
        if not os.path.exists(self._path_data):
            logger.info("Path found at %s", str(self._path_data))
            os.mkdir(self._path_data)
            self._filename = self._path_data + "/videos.json"
            # Serializing json
            json_object = json.dumps(self.data, indent=4)
            # Writing to sample.json
            with open(self._filename, "w+") as outfile:
                outfile.write(json_object)
        else:
            logger.info("Path not found at %s", str(self._path_data))



    def webcrawl(self) -> None:
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Firefox(gvars.SELENIUM_FIREFOX)
        self.driver.get(url)
        self.channel_name = self.driver.find_element(By.CSS_SELECTOR,'yt-formatted-string#text').text
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

                self.data.append({'yt_id': yt_id, 'video_url': vurl, 'title': title, 'date_time': date_time, 'views': views})
        except:
            pass
        
        self._len_data = len(self.data)
        self.driver.quit()
        self._save_json()




    def get_channel_name(self):
        return self.channel_name
    
    def get_channel_json(self):
        return self.data




if __name__ == '__main__':  # Execute the following code only when executing main.py (not when importing it)
    home = str(os.getcwd())
    FILES_FOLDER = home + '/'
    DATA_PATH = FILES_FOLDER + "data/"
    url = 'https://www.youtube.com/@bbcvods5052/videos'
    
    channel = Channel(url, "BBCVODS", data_path=DATA_PATH)
    channel.stop_driver()