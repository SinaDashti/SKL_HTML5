"""
Written by Sina Dashti 18/11/2019
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import os


# Defining the output values
Dl = []
Up = []
Ping = []
Jitter = []

path = os.getcwd() + "/TestScreenshot"
os.makedirs(path)


def test_start_func():
    # Opening the page
    global driver
    driver = webdriver.Chrome()
    driver.get("http://speedprobe-test.skylogicnet.com")

    # Waiting for the page
    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_is("Tooway Speed Test"))

    # Starting the test
    driver.find_element_by_xpath('//*[@id="belowbefore"]/a').click()


def test_restart_func():
    # Restarting the page after the first test
    global driver
    driver.find_element_by_xpath('//*[@id="startStopBtn"]').click()


def wait_func():
    # Waiting for the test
    global driver
    run = True
    while run:
        try:
            driver.find_element_by_xpath('//*[@class="running"]')
            time.sleep(1)
        except Exception:
            run = False


def result_func():
    # Blueprint of result source page
    result = BeautifulSoup(driver.page_source, 'lxml')

    # Speed Group
    speedGroup = result.find_all('div', class_='testGroup')[0]

    global Dl
    global DlUnit
    global Up
    global UpUnit
    global Ping
    global PingUnit
    global Jitter
    global JitterUnit

    # Download Group
    Dl.append(result.find('div', id='dlText').text)
    DlGroup = speedGroup.find_all('div', class_='testArea')[0]
    DlUnit = DlGroup.find_all('div', class_='unit')[0].text

    # Upload Group
    Up.append(result.find('div', id='ulText').text)
    UpGroup = speedGroup.find_all('div', class_='testArea')[1]
    UpUnit = UpGroup.find_all('div', class_='unit')[0].text

    # Latency Group
    latencyGroup = result.find_all('div', class_='testGroup')[1]

    # Ping Group
    if result.find('div', id='pingText').text is '':
        Ping.append('0')
    else:
        Ping.append(result.find('div', id='pingText').text)
    PingGroup = latencyGroup.find_all('div', class_='testArea')[0]
    PingUnit = PingGroup.find_all('div', class_='unit')[0].text

    # Jitter Group
    if result.find('div', id='jitText').text is '':
        Jitter.append('0')
    else:
        Jitter.append(result.find('div', id='jitText').text)
    JittGroup = latencyGroup.find_all('div', class_='testArea')[1]
    JittUnit = JittGroup.find_all('div', class_='unit')[0].text


def test_rep_func():
    # Test repeat function
    global testNum
    global path
    if testNum.isnumeric() and int(testNum) >= 0:
        test_start_func()
        wait_func()
        result_func()
        name = path + "/test" + "1" + ".png"
        driver.save_screenshot(name)
        if int(testNum) >= 1:
            for i in range(int(testNum) - 1):
                test_restart_func()
                wait_func()
                result_func()
                name = path + "/test" + str(i + 2) + ".png"
                driver.save_screenshot(name)
    else:
        print("Please run the test again and insert an integer number >= 0 !")


def txt_out_func():
    # Result visualization
    global driver
    c1 = 'Download ' + DlUnit
    c2 = 'Upload ' + UpUnit
    c3 = 'Ping ' + PingUnit
    c4 = 'Jitter ' + PingUnit

    df = pd.DataFrame({c1: Dl,
                       c2: Up,
                       c3: Ping,
                       c4: Jitter
                       })
    df.index += 1
    print(tabulate(df, headers='keys', tablefmt='psql'))


# Starting the test
testNum = input("Please indicate the number of tests: ")
print("Please wait...\n")

test_rep_func()
txt_out_func()

# Closing the browser
driver.close()
