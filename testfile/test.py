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
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return

    if message.content == "!돈줘":#돈지급
        send = str(message.author.id)
        dirtime = db.reference('moneytime/' + send) # 수령 받은 시간 정보 받기
        times = dirtime.get()

        if times == None: # 시간정보가 없을시
            times = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f') # 현재 시간 저장 및 불러오기
        else:
            times = times[send]
            times = datetime.datetime.strptime(times, "%Y-%m-%d %H:%M:%S.%f") # 시간값이 있다면 시간정보를 가져오고 계산가능한 값으로 변환

        now = datetime.datetime.strptime(str(datetime.datetime.now()), '%Y-%m-%d %H:%M:%S.%f')

        if times < now: # 수령 가능시간이 지났을경우
            dirmoney = db.reference('money/' + send) # 돈 값 가져오기
            money = dirmoney.get()
                
            dirye = db.reference('ye/' + send) # 통장 값 가져오기
            ye = dirye.get()

            if ye == None: # 값이 없다면 새로 만들고 초기화
                dirye.update({send:0.0})
                ye = 0.0
            else: #있다면 값 가져오기
                ye = ye[send]

            if money == None: # 위와 같은 시스템
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            if (money + ye) > 3000.0: # 통장과 돈의 합이 3천원 미만일때
                give = round(random.uniform(10000.00, 50000.00), 3) #랜덤 만큼의 돈을 지급

                await message.channel.send(message.author.mention + "님에게" + " 지원금 : " + str(give) + "원을 지급합니다")
                money += give
                dirmoney.update({send:money})

                times = str(datetime.datetime.now() + datetime.timedelta(minutes=15)) # 15분후의 시간을 저장
                dirtime.update({send:times})
            else:
                await message.channel.send(message.author.mention + "님은 이미 충분한 돈을 가지고 있습니다")
        else: # 수령가능시간이 지나지 않았을 경우 거부
            await message.channel.send(message.author.mention + "님 지원금 수령 가능 시간이 되지 않았습니다")

client.run(token)