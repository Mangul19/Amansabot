#어만사 전용 디스코드 봇 백

from typing import Text
import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from urllib.request import Request
from urllib.parse import quote
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code

#clinet
client = discord.Client()
#discord bot tokken
token = code.token
#Naver Open API application ID
client_id = code.client_id
#Naver Open API application token
client_secret = code.client_secret
#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")


global driver
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

while True:
    try:
        driver.get("https://v1.coronanow.kr/live.html")# 사이트 열람
        driver.implicitly_wait(3)
        print("통과 1")
        einput1 = driver.find_element_by_xpath("/html/body/div[2]/b/div[5]/div[1]/div/span/p[1]/b")
        print("통과 2")
        einput2 = driver.find_element_by_xpath("/html/body/div[2]/b/div[5]/div[1]/div/span/p[2]")
        print("통과 3")
        print("위치 및 확진자 수" + einput1)
        print("통과 4")
        print("상세 정보" + einput2)
        print("통과 5")
    except:
        print("실시간 코로나 시스템 오류 발생 다음에 다시 시도합니다")

    time.sleep(60*1)