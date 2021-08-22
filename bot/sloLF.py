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

#clinet
client = discord.Client()
#discord bot tokken
token = code.token
#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=854x480')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n끝말 잇기 시스템(자유)을 시작합니다" + 
        "\n==========================================")

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return
    
    if str(message.channel.id) == "872279702079963187" and message.content == "!초기화":
        channel = client.get_channel(872279702079963187)

        mal = ["가", "나", "다", "라", "마" , "바" , "사", "아", "자" , "차", "카", "타", "파", "하"]
        malran = random.randint(0, len(mal) - 1)

        dirmallist = db.reference('SOLmallist/')
        inmallist = dirmallist.get()
        inmallist = list(inmallist.values())
        dirmallist.delete()
        dirmallist.update({'00':mal[malran]})

        dirdan = db.reference('SOLdan/')
        dirdan.update({"SOLdan":mal[malran]})

        await message.channel.purge(limit=int(999999999))
        await channel.send("초기화가 완료되었습니다 시작단어는 " + mal[malran] + " 입니다")
        return

    if str(message.channel.id) == "872279702079963187":
        #받은 메세지 및 입력자 출력
        print(str(message.author) + str(message.author.mention) + " : " + str(message.content))

        msg = await message.channel.send("해당 단어를 검사중입니다")
        try:
            if len(message.content) <= 1:
                await msg.edit(content=message.author.mention + "님 두글자 이상만 가능합니다")
                await message.delete()
                return

            dirismallist = db.reference('SOLmalit/')
            dmallist = dirismallist.get()
            isstart = dmallist['isit']
            if isstart == 0:
                dirismallist.update({"isit":1})
            else:
                await message.delete()
                await msg.edit(content=message.author.mention + "님 이미 누군가 먼저 입력하여 검사중입니다")
                return

            dirmallist = db.reference('SOLmallist/')
            inmallist = dirmallist.get()
            inmallist = list(inmallist.values())

            if message.content in inmallist:
                await msg.edit(content=message.author.mention + "님 해당 단어는 이미 사용한 단어입니다")
                await message.delete()
                dirismallist.update({"isit":0})
                return

            dirdan = db.reference('SOLdan/') # 끝말 조회
            danm = dirdan.get()
            danm = danm["SOLdan"]

            if message.content[:1] != danm:
                await msg.edit(content=message.author.mention + "님 끝말이 이어지지 않습니다")
                await message.delete()
                dirismallist.update({"isit":0})
                return

            driver.get("https://opendict.korean.go.kr/search/searchResult?focus_name=query&query=" + message.content + "&dicType=1&wordMatch=Y")# 사이트 열람
            driver.implicitly_wait(2)
            
            einput = driver.find_element_by_class_name("word_dis.ml5").get_attribute("innerHTML")
            print(einput + "성공 (자유)")
            await msg.edit(content=message.author.mention + "님 성공!\n단어 의미 : " + einput + "\n현재 총 사용 단어 수 : " + str(len(inmallist)) )

            dirdan.update({"SOLdan":message.content[-1:]})
            dirmallist.update({str(len(inmallist)):message.content})
            dirismallist.update({"isit":0})
        except:
            await message.delete()
            dirismallist = db.reference('SOLmalit/')
            dmallist = dirismallist.get()
            dirismallist.update({"isit":0})
            await msg.edit(content=message.author.mention + "님 해당 단어는 존재하지 않습니다")

client.run(token)