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

def enterZoom(driver, waitTime=1):
    print("Entering zoom.us")
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

#CHANGE WAITTIME IF WIFI SLOW
def joinMeeting(driver, lastUrl, waitTime=0.7):
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

def countParticipants(driver):
      return 20

def countHands(driver):
      return 20

def start_driver(headless=False):
    print("Starting driver")
    # setup webdriver settings
    options = webdriver.ChromeOptions()  # hiding startup info that pollutes terminal
    options.headless = headless  # headless or not, passed as arg
    # make window size bigger to see all buttons
    options.add_argument("--window-size=1600,1200")
    # start webdriver
    return webdriver.Chrome(path, chrome_options=options)


def getUrl(link):
    newLink = re.sub("/j/", "/wc/join/", link)
    return newLink

# click_chat(driver) - opens or closes chat window
# refactor: combine this with open_participants to make general menu opener
def click_chat(driver):
	time.sleep(1)
	# had to handle making window size bigger because participants list cut off button
	# see driver_start() for solution
	try: # try to click it right away
		# find it using the chat icon
		driver.find_element_by_class_name("footer-button__chat-icon").click()
	except: # if it isn't clickable (sometimes takes a sec to load properly)
		print("\tFailed. Trying again, please wait...\n")
		time.sleep(2)
		driver.find_element_by_class_name("footer-button__chat-icon").click()
	return # successfully clicked (hopefully)

# open_chat() -  opens chat popup
def open_chat(driver):
	print("\tOpening chat menu...\n")
	click_chat(driver) # click on the chat button
	print("\tOpened chat menu.\n")
	return

# close_chat() - closes chat popup
def close_chat(driver):
	print("\tClosing chat menu...\n")
	click_chat(driver) # click on the chat button
	print("\tClosed chat menu.\n")
	return

def sendPublicMessage(driver, message = "mamba out"):
      open_chat(driver)
      driver.find_element_by_class_name("chat-box__chat-textarea").send_keys(message)
      driver.find_element_by_class_name("chat-box__chat-textarea").send_keys(Keys.ENTER)
      close_chat(driver)
      
      
def leaveMeeting(driver):
      print("\tLeaving meeting...\n")
      sendPublicMessage(driver)
      driver.find_element_by_class_name("footer__leave-btn").click()
      time.sleep(1.3)
      driver.find_element_by_class_name("leave-meeting-options__btn").click()
      
