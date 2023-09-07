import json
import time
import logging
import gvars
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger()

class Channel:
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
        self._start_up()



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
                self._data.append({'video_url': vurl, 'title': title, 'date_time': date_time, 'views': views})
        except:
            pass
        
        self._data_len = len(self._data)



    def save_json(self) -> None:
        self._filename = gvars.DATA_PATH + self._channel_name + ".json"
        # Serializing json
        json_object = json.dumps(self._data, indent=4)
        # Writing to sample.json
        with open(self._filename, "w+") as outfile:
            outfile.write(json_object)


    def stop_driver(self) -> None:
        self.driver.quit()




if __name__ == '__main__':  # Execute the following code only when executing main.py (not when importing it)
    url = 'https://www.youtube.com/@bbcvods5052/videos'
    channel = Channel(url)
    channel.stop_driver()