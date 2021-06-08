from time import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from urllib.request import Request
from urllib.parse import quote
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")

global driver
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/중요파일/bot-Amansa/chromedriver.exe')

while (True):
    driver.get("https://v1.coronanow.kr/live.html")# 사이트 열람
    driver.implicitly_wait(3)

    ei = driver.find_element_by_xpath('//*[@id="ALL_decidecnt_increase"]/div[5]').text
    ei = ei[1:].split("기타")[1].split("더보기")[0]

    print(ei)
    
    time.sleep(3)