#This scripts downloads all the user's facebook photos
import requests 
import time
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from lxml import html

#Creates a selenium browser session and logs in to the user's facebook account 
browser = webdriver.Firefox()
user = input("What is your username?")
passwd = input("What is your password?")
browser.implicitly_wait(1)
browser.get("https://www.facebook.com")
username = browser.find_element_by_id("email")
password = browser.find_element_by_id("pass")
username.send_keys(user)
password.send_keys(passwd)

#Navigates to the user's profile 
try:
    WebDriverWait(browser,4).until(EC.element_to_be_clickable((By.XPATH,"//button[@title='Accept All']"))).click()
except:
    browser.implicitly_wait(2)
    browser.find_element_by_name("login").click()

WebDriverWait(browser,30).until(EC.element_to_be_clickable((By.XPATH,"//a[@href = '/me/']"))).click()

WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.XPATH,"//a[contains(@href, '/photos')]"))).click()
browser.implicitly_wait(10)
#instructs selenium to scroll down
browser.find_element_by_xpath("//*[contains(@href, '/photos_by')]").click()
#Instructs selenium to scroll down till the end of the page
while True:
    old_height = browser.execute_script("return document.body.scrollHeight")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if old_height == new_height:
        break
html_source = browser.page_source
data = html_source
time.sleep(2)


elems = browser.find_elements_by_xpath("//a[contains(@href, 'photo.php')]")
lnkset = []
for lnk in elems:
    lnkset.append(lnk.get_attribute("href"))
number = len(lnkset)
#Manipulates the links using the mobile version of Facebook's view full size link. 

for i in range(number):
    facebook = lnkset[i]
    pos = facebook.find("w")
    facebook = facebook[0:pos] + "m" + facebook[pos+3:len(facebook)]
    pos = facebook.find("&")
    facebook = facebook[0:pos]
    facebook = facebook[0:28] + facebook[32:len(facebook)]
    facebook = facebook[0:28] + "/view_full_size/" + facebook[28:len(facebook)]
#Opens the links with selenium so javascript content is loaded
    browser.get(facebook)
    download = browser.current_url
#Creates a request session to download the target's content 
    r = requests.Session()
    home = os.path.expanduser("~")
    home.replace("\\","/")
    home+="/Downloads/MyFaceDownloads"
    if os.path.exists(home) == False:
        os.mkdir(home)
    home+="/" + str(i) + ".jpg"
#The image link for each facebook photo can now be downloaded with requests(without login info)
    with open(home,"wb") as f:
        f.write(r.get(download).content)

time.sleep(5000)

