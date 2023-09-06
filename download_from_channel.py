from selenium import webdriver
from time import sleep
from random import randint
from pytube import YouTube
import requests

# Open brower
driver = webdriver.Firefox('/Users/ColeChalland/Documents/Selenium/FireFox')

# YouTube channel
url = "https://www.youtube.com/@bbcvods5052"

# Get YouTube video
def get_video_youtube(driver, url):
    driver.get(url)
    sleep(randint(5, 9))
    driver.get(url + "/videos")
    
    ht = driver.execute_script("return document.documentElement.scrollHeight;")
    
    while True:
        prev_ht = driver.execute_script("return         document.documentElement.scrollHeight;")
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        sleep(2)
        ht = driver.execute_script("return document.documentElement.scrollHeight;")
        
        if prev_ht == ht:
            break
    
    links = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for link in links:
        title = link.get_attribute("title")
        href = link.get_attribute("href")
        print(f"Title: {title}, link: {href}")



get_video_youtube(driver,url)