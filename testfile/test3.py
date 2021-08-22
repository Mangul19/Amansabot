#어만사 전용 디스코드 봇 백

from typing import Text
import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import math
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from urllib.request import Request
from urllib.parse import quote
import json
import time
import urllib
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code
import bs4

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
#options.add_argument('headless')
options.add_argument('window-size=854x480')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

#준비 될 시 시작
@client.event
async def on_ready():
    driver.get("https://www.weather.go.kr/w/eqk-vol/search/korea.do")# 사이트 열람
    driver.implicitly_wait(2)
        
    embed = discord.Embed(title="국내의 최근 지진을 불러옵니다", description="지진 시스템", color=0x5CD1E5)

    einlist = ["발생시각", "규모", "발생 깊이","최대 진도" ,"위치"]
    listin = 2
    TFL = False

    for insite in einlist:
        einput = driver.find_element_by_css_selector('#excel_body > tbody > tr:nth-child(1) > td:nth-child(' + str(listin) + ') > span').text
        embed.add_field(name=insite, value=einput, inline=TFL)

        listin += 1
        TFL = True
        if listin == 6:
            listin = 8
            TFL = False

    einput = driver.find_element_by_css_selector('#excel_body > tbody > tr:nth-child(1) > td:nth-child(10) > a').get_attribute('href')

    try:
        driver.get(einput)
        driver.implicitly_wait(2)

        einput = driver.find_element_by_css_selector('#img2').get_attribute('src')
        embed.set_image(url=einput)
    except:
        embed.add_field(name="이미지 오류", value="이미지는 없습니다", inline=False)
        embed = driver.find_element_by_css_selector('body > embed')

    channel = client.get_channel(832799360210436107)
    await channel.send(embed=embed)

client.run(token)