from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# options = webdriver.ChromeOptions()
# #All are optional
# options.add_experimental_option("detach", True)
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-notifications")
# options.add_argument("--disable-Advertisement")
# options.add_argument("--disable-popup-blocking")
# options.add_argument("start-maximized")

# s=Service('./Users/ColeChalland/Documents/Selenium/Chrome/chromedriver.app')
# driver= webdriver.Chrome(service=s,options=options)

driver = webdriver.Firefox()

driver.get('https://www.youtube.com/@bbcvods5052/videos')
time.sleep(3)

item = []
SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.documentElement.scrollHeight")

item_count = 180

while item_count > len(item):
    driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")

    if new_height == last_height:
        break
    last_height = new_height
    

data = []
try:
    for e in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
        title = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('title')
        vurl = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('href')
        views= e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]').text
        date_time = e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]').text
        data.append({
            'video_url':vurl,
            'title':title,
            'date_time':date_time,
            'views':views
            })
except:
    pass
    
item = data
print(item)
print(len(item))
# df = pd.DataFrame(item)
# print(df)

driver.quit()