from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent

import sys
import re
import urllib.request as urlr
import time
import random

# change path if your not zeta IMPORTANT
global path
path = r"C:\Users\Mauricio\Documents\chromedriver_win32\chromedriver.exe"
global mail
mail = "zoomerapp00@gmail.com"
global passw
passw = "Zommer.00"

#CHANGE WAITTIME IF WIFI SLOW
def joinMeeting(driver, lastUrl, waitTime=0.95):
    # go to regular zoom.us
    driver.get("https://zoom.us")
    time.sleep(waitTime)
    # login to our SUPER google account
    try:
        driver.find_element_by_class_name('signin').click()
        time.sleep(waitTime)
        try:
            driver.find_element_by_class_name('login-btn-google').click()
            time.sleep(waitTime)
            try:
                driver.find_element_by_id('identifierId').send_keys(mail)
                time.sleep(waitTime)
                try:
                    driver.find_element_by_class_name('VfPpkd-RLmnJb').click()
                    time.sleep(waitTime)
                    try:
                        driver.find_element_by_class_name(
                            'whsOnd').send_keys(passw)
                        time.sleep(waitTime)
                        try:
                            driver.find_element_by_class_name(
                                'VfPpkd-RLmnJb').click()
                            time.sleep(waitTime)
                        except:
                            print("no next")
                            sys.exit()
                    except:
                        print("no password")
                        sys.exit()
                except:
                    print("no next")
                    sys.exit()
            except:
                print("no mail input")
                sys.exit()
        except:
            print("no google buton")
            sys.exit()
    except:
        print("no sign in located")
        sys.exit()

    # actually joining the meeting
    try:
        driver.get(lastUrl)
        time.sleep(waitTime)
        try:
            driver.find_element_by_id('joinBtn').click()
            time.sleep(waitTime)
        except:
            print("could not join to the link")
            sys.exit()
    except:
        print("wrong url or sth else... SORRY")
        sys.exit()

# start_driver() - starts the webdriver and returns it
# reference: https://browsersize.com/
# reference: https://stackoverflow.com/questions/23381324/how-can-i-control-chromedriver-open-window-size


def start_driver(headless=False):
    # setup webdriver settings
    options = webdriver.ChromeOptions()  # hiding startup info that pollutes terminal
    options.headless = headless  # headless or not, passed as arg
    # make window size bigger to see all buttons
    options.add_argument("--window-size=800,1000")
    # start webdriver
    return webdriver.Chrome(path, chrome_options=options)


def getUrl(link):
    newLink = re.sub("/j/", "/wc/join/", link)
    return newLink


def mainBot(link):
    # start driver
    driver = start_driver()
    # get goal link to access via web
    lastUrl = getUrl(link)
    # join meeting with ZOOMER BOT
    joinMeeting(driver, lastUrl)


print("conpila")
