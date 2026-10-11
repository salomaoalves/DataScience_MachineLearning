import os
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import chromedriver_binary

def get_driver(options):
    '''Create the Chrome driver. Use CHROME_BIN/CHROMEDRIVER_PATH env vars if set,
        otherwise Selenium Manager finds (or downloads) Chrome and chromedriver'''
    if os.environ.get('CHROME_BIN'):
        options.binary_location = os.environ['CHROME_BIN']
    return Chrome(service=Service(os.environ.get('CHROMEDRIVER_PATH')), options=options)

def read_file(path):
    with open(path, 'r') as arq:
        lista = arq.readlines()
    return lista

def yt_scrap(url, n):
    '''Scraping YouTube videos comments
        url: video url; n: number of interation'''
    
    data = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    with get_driver(options) as driver:
        wait = WebDriverWait(driver,15)
        driver.get(url)

        for _ in range(n): 
            wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
            time.sleep(15)

        for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
            data.append(comment.text)
    return data[3:-1] # drop extra information


def insta_scrap(url, n):
    '''Scraping Instagram post comments.
        url: post url; n: number of interation'''

    data, i = [], 0
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    with get_driver(options) as driver:
        wait = WebDriverWait(driver,15)
        driver.get(url)

        while n>i:
            try:
                driver.find_element(By.CLASS_NAME, 'dCJp8').click()
            except NoSuchElementException:
                break
            time.sleep(15)
            i += 1

        for comment in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "C4VMK"))):
            data.append(comment.text.split('\n')[1])

    return data[1:] #drop legend