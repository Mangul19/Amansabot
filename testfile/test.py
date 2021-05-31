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
#options.add_argument('headless')
#options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")

global driver
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/중요파일/bot-Amansa/chromedriver.exe')


ji = 00

print("1")
driver.get("https://www.weather.go.kr/w/eqk-vol/search/korea.do")# 사이트 열람
driver.implicitly_wait(3)
print("2")
einput = driver.find_element_by_css_selector('#excel_body > tbody > tr:nth-child(1) > td:nth-child(2) > span').text # 가져올 값 선택
print("3")
if ji != einput and einput != "":
    einlist = ["발생시각", "규모", "발생 깊이","최대 진도" ,"위치"]
    listin = 2
    TFL = False
    print("4")
    for insite in einlist:
        print(driver.find_element_by_css_selector('#excel_body > tbody > tr:nth-child(1) > td:nth-child(' + str(listin) + ') > span').text)
        print("5")
        listin += 1
        TFL = True
        if listin == 6:
            listin = 8
            TFL = False
    print("6")
    driver.find_element_by_css_selector("#excel_body > tbody > tr:nth-child(1) > td:nth-child(9)").click()
    print(driver.find_element_by_css_selector("body > img"))
    print("8")
elif einput == "":
    print("국내 지진 시스템 불러오기 오류 다음에 다시 시도합니다") 