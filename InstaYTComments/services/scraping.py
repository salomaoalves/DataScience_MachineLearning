import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
#import chromedriver_binary

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
    with Chrome('/home/salomao/Desktop/DSProject/NLP/services/chromedriver', options=options) as driver:
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
    with Chrome('/home/salomao/Desktop/DSProject/NLP/services/chromedriver', options=options) as driver:
        wait = WebDriverWait(driver,15)
        driver.get(url)

        while n>i:
            try:
                driver.find_element_by_class_name('dCJp8').click()
            except NoSuchElementException:
                break
            time.sleep(15)
            i =+ 1

        for comment in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "C4VMK"))):
            data.append(comment.text.split('\n')[1])

    return data[1:] #drop legend