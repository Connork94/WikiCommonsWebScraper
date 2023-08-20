
from bs4 import BeautifulSoup
import requests
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import sys
print(sys.path)

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')
driver = webdriver.Firefox(options=options)


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}

parent_dir = "C:\\Users\Connor\\Documents\\Python Scripts\\WikiCommonsScrapper\\Images"

#add search term here
search_name = "John Anster Fitzgerald"

path = os.path.join(parent_dir, search_name)

try:
    os.mkdir(path)
    print("Directory '% s' created" % search_name)
except:
    print("Already a '% s'" % search_name)

# https://commons.wikimedia.org/wiki/Category:Images

# add to URL

search_name = search_name.replace(" ","+")
print(search_name)


driver.get("https://commons.wikimedia.org/w/index.php?search="+search_name+"&title=Special:MediaSearch&go=Go&type=image")
# scroll to bottom of page and wait in selenium
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)
print("scrolled once")
# 2nd scroll
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)
print("scrolled twice")
# 3rd scroll
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
time.sleep(3)
print("scrolled third")
wait=WebDriverWait(driver,2)
# it will wait for 250 seconds an element to come into view, you can change the #value
# getting the button by class name
try:
    buttons = driver.find_element_by_xpath("//button[@class='sd-button sdms-load-more sd-button--framed sd-button--progressive']/span[@class='sd-button__content']")
    print(buttons)
    # clicking on the button
    buttons.click()
    # scroll to bottom of page and wait in selenium
except:
    print("An exception occurred")
try:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    print("scrolled once")
except:
    print("An exception occurred")

# 2nd scroll
try:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    print("scrolled twice")
except:
    print("An exception occurred")
# 3rd scroll
try:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    print("scrolled three times")
except:
    print("An exception occurred")

try:
        wait = WebDriverWait(driver, 2)
        # it will wait for 250 seconds an element to come into view, you can change the #value
        # getting the button by class name
        buttons = driver.find_element_by_xpath(
            "//button[@class='sd-button sdms-load-more sd-button--framed sd-button--progressive']/span[@class='sd-button__content']")
        print(buttons)
        # clicking on the button
        buttons.click()
except:
    print("An exception occurred")



#commented out bc using selenium
# URL = "https://commons.wikimedia.org/w/index.php?search="+search_name+"&title=Special:MediaSearch&go=Go&type=image"
# page = requests.get(URL, headers=headers)

# This replaces the request function, since we are using selenium
page = driver.page_source

#print(page.text)

soup = BeautifulSoup(page, "html.parser")

# this will find all the links.
thumbnails = soup.find_all(class_='sdms-image-result')

# this will find one
# thumbnails = []
# thumbnails.append(soup.find(class_='sdms-image-result'))

links= []

for link in thumbnails:
    links.append(link.get('href'))

#print(links)
count = 0

for link in links:
    image_page = requests.get(link, headers=headers)
    image_soup = BeautifulSoup(image_page.content, "html.parser")
    image_element = image_soup.find(class_='fullImageLink')
    #print(image_element)
    image_a = image_element.find('a')
    #print(image_a)
    image_link = image_a.get('href')
    print(image_link)
    res = requests.get(image_link, headers=headers)
    res.raise_for_status()

    # Save the image to path.
    imageFile = open(os.path.join(path, os.path.basename(image_link)), 'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    print("saved " + image_link + "to" + path)
    #
    time.sleep(0.2)  # try not to get a 403
    count+=1
    print(count)


