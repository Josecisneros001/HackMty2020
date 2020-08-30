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
#path = r"C:\Users\Mauricio\Documents\chromedriver_win32\chromedriver.exe"
path = r"C:\Users\josea\Documents\chromedriver_win32\chromedriver.exe"

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

# CHANGE WAITTIME IF WIFI SLOW


def joinMeeting(driver, lastUrl, waitTime=1.3):
    # actually joining the meeting
    time.sleep(waitTime)
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
    options.add_argument("--window-size=1400,700")
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
    try:  # try to click it right away
               # find it using the chat icon
        driver.find_element_by_class_name("footer-button__chat-icon").click()
    except:  # if it isn't clickable (sometimes takes a sec to load properly)
        print("\tFailed. Trying again, please wait...\n")
        time.sleep(2)
        driver.find_element_by_class_name("footer-button__chat-icon").click()
    return  # successfully clicked (hopefully)

# open_chat() -  opens chat popup


def open_chat(driver):
    print("\tOpening chat menu...\n")
    click_chat(driver)  # click on the chat button
    print("\tOpened chat menu.\n")
    return

# close_chat() - closes chat popup


def close_chat(driver):
    print("\tClosing chat menu...\n")
    click_chat(driver)  # click on the chat button
    print("\tClosed chat menu.\n")
    return

# click_participants() - click on the participants button
# originally always left open, made this to allow for closing to avoid interference
# refactor: combine this with click_chat() to make general menu opener


def click_participants(driver):
    time.sleep(2)
    try:  # try to click it right away
        # find it using the participants icon
        driver.find_element_by_class_name(
            "footer-button__participants-icon").click()
    except:  # if it isn't clickable (sometimes takes a sec to load properly)
        print("\tFailed. Trying again, please wait...\n")
        time.sleep(7)
        driver.find_element_by_class_name(
            "footer-button__participants-icon").click()
    return

# open_participants() - opens the participants menu, loads all members


def open_participants(driver):
    print("\tOpening participants list...\n")
    click_participants(driver)
    print("\tOpened participants list.\n")
    return

# close_participants() - opens the participants menu, loads all members


def close_participants(driver):
    print("\tClosing participants list...\n")
    click_participants(driver)
    print("\tClosed participants list.\n")
    return

# count_reaction() - counts the number of a chosen reaction at a given time


def count_reaction(driver, reaction_name="participants-icon__participants-raisehand"):
    # find elements of given reaction class (hand raise by default)
    react_list = driver.find_elements_by_class_name(reaction_name)
    print("\tNumber of hands raised: ", len(react_list), "\n")  # print total
    return len(react_list)  # return number of reactions

# who_participates() - checks who is currently participating (via reactions)
# reference: https://stackoverflow.com/questions/18079765/how-to-find-parent-elements-by-python-webdriver


def who_participates(driver, reaction_name="participants-icon__participants-raisehand"):
    participant_list = []  # empty list to hold participants
    # find elements of given reaction class (hand raise by default)
    react_list = driver.find_elements_by_class_name(reaction_name)
    for i in range(len(react_list)):  # for each reaction element (belongs to a person)
        # go to grandparent element, so we can check the name (store in curr element)
        react_list[i] = react_list[i].find_element_by_xpath("../..")
        # get the name element (store in curr element)
        react_list[i] = react_list[i].find_element_by_class_name(
            "participants-item__display-name")
        # refine to name string (store in curr element)
        react_list[i] = react_list[i].get_attribute("innerHTML")
    print("\tPeople raising hands: ", react_list, "\n")  # print total
    return react_list  # return list of people reacting

# call_on() - calls on the first person to raise their hand; if it can't tell, randomizes


def call_on(driver):
    # check who is raising their hand rn
    hand_raiser_list = who_participates(driver)
    if (len(hand_raiser_list) == 0):  # if no-one is raising their hand
        print("\tYou can't call on anyone if no-one is raising their hand!\n")
        return  # return no-one
    elif (len(hand_raiser_list) == 1):  # if one person is raising their hand
        print("\tThey raised their hand first, so you called on:",
              hand_raiser_list[0], "\n")  # print selection
        return hand_raiser_list[0]  # return the one person raising their hand
    else:  # if more than one person is raising their hand
        chosen_person = random.choice(
            hand_raiser_list)  # choose someone randomly
        print("\tYou didn't see who was first, so you guessed and called on:",
              chosen_person, "\n")  # print selection
        return chosen_person  # return your "guess" at who was first


def pick(driver):
    return
# identify_host() - identifies the name of the host


def identify_host(driver):
    # creates target variable to hold element that is current subject of focus
    target = driver.find_element_by_xpath(
        "//*[contains(text(), '(Host)')]")  # find the host's webElement
       # "//*[text()='(Host)']") # find the host's webElement
    # tried to accomodate for fake hosts, but had issues--not worth time in hackathon
    if (target.get_attribute("class") != "participants-item__name-label"):
        print("\tSome jerk named themself host to screw with this program.",
              "Make them change their name.\n")
        raise ValueError(
            "Too complicated to handle fake hosts during hackathon.\n")
    target = target.find_element_by_xpath("./..")  # go to parent element
    # get other child element of parent; contains host's name
    target = target.find_element_by_class_name(
        "participants-item__display-name")
    # get innerHTML of actual host's name
    recipient_name = target.get_attribute("innerHTML")
    print("\tThe name of the host is:", recipient_name, "\n")
    return recipient_name


def sendPublicMessage(driver, message="mamba out"):
    open_chat(driver)
    driver.find_element_by_class_name(
        "chat-box__chat-textarea").send_keys(message)
    driver.find_element_by_class_name(
        "chat-box__chat-textarea").send_keys(Keys.ENTER)
    close_chat(driver)


# take_attendance() - take attendance of who is there at current time
# I'd have avoided the second list creation, but attendee list was polluted by bot names
# could add filtering out prof later, but requires searching addditional elements
def take_attendance(driver):
    open_participants(driver)
    # collect all attendees into list by looking for spans with the following class
    attendee_list = driver.find_elements_by_class_name(
           "participants-item__display-name")
    new_attendee_list = []  # for storing refined list (filters out self)
    for i in range(len(attendee_list)):  # for each webElement in list of attendees
            if (attendee_list[i].get_attribute("innerHTML") != "Zoomer App"):  # if not bot
                       # then refine to name and add to the new list
                new_attendee_list.append(
                    attendee_list[i].get_attribute("innerHTML"))
    print("\tStudents: ", new_attendee_list, "\n")  # print list of attendee names
    return new_attendee_list  # return attendee list


def leaveMeeting(driver):
    print("\tLeaving meeting...\n")
    sendPublicMessage(driver)
    driver.find_element_by_class_name("footer__leave-btn").click()
    time.sleep(1.3)
    driver.find_element_by_class_name("leave-meeting-options__btn").click()
