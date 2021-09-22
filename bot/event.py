#어만사 전용 디스코드 봇

import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import math
import requests
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

intents = discord.Intents.all()
#clinet
client = discord.Client(intents=intents)
#discord bot tokken
token = code.token
#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n이벤트 시스템을 시작합니다" + 
        "\n==========================================")

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return
    try:
        if str(message.channel.id) == "889062442787815444":
            if message.content == "참여":
                send = str(message.author.id)

                direvent = db.reference('event/' + send)
                event = direvent.get()

                if event == None:
                    x = random.randint(1, 3)
                    print(x)

                    if x == 1:
                        dirlevel = db.reference('level/' + send) #레벨 값 가져오기
                        level = dirlevel.get()
                        level = level[send]

                        direxp = db.reference('exp/' + send) #경험치 값 가져오기
                        exp = direxp.get()
                        exp = exp[send]
                        
                        exp += round(level * 37.5, 3)
                        direxp.update({send:exp})

                        direvent.update({send:"Yes"})
                        await message.channel.send(message.author.mention + "님 당첨되었습니다!! " + str(level * 37.5) + " exp 가 지급됩니다")
                    else:
                        direvent.update({send:"No"})
                        await message.channel.send(message.author.mention + "님 아쉽게도 이번 이벤트는 미당첨입니다\n하지만 기회는 한번더 있습니다 ' 재참여 ' 를 입력해보세요")
                else:
                    await message.channel.send(message.author.mention + "님은 이미 참여하였습니다")
            elif message.content == "재참여":
                send = str(message.author.id)

                direvent = db.reference('event/' + send)
                event = direvent.get()

                if event == None:
                    await message.channel.send(message.author.mention + "님 '참여' 를 먼저해주세요")
                else:
                    event = event[send]

                    if event == "No" and event != "NoNoNo" :
                        x = random.randint(1, 2)
                        print(x)

                        if x == 1:
                            dirlevel = db.reference('level/' + send) #레벨 값 가져오기
                            level = dirlevel.get()
                            level = level[send]

                            direxp = db.reference('exp/' + send) #경험치 값 가져오기
                            exp = direxp.get()
                            exp = exp[send]
                            
                            exp += round(level * 37.5, 3)
                            direxp.update({send:exp})

                            direvent.update({send:"Yes"})
                            await message.channel.send(message.author.mention + "님 당첨되었습니다!! " + str(level * 37.5) + " exp 가 지급됩니다")
                        else:
                            direvent.update({send:"NoNo"})
                            await message.channel.send(message.author.mention + "님 아쉽게도 재참여 이벤트는 미당첨입니다 마지막으로 부활전 을 입력해보세요")
                    else:
                        await message.channel.send(message.author.mention + "님은 재참여 대상자가 아닙니다")
            elif message.content == "부활전":
                send = str(message.author.id)

                direvent = db.reference('event/' + send)
                event = direvent.get()

                if event == None:
                    await message.channel.send(message.author.mention + "님은 부활전 대상자가 아닙니다 참여를 먼저 하셔야합니다")
                else:
                    event = event[send]

                    if event == "NoNo":
                        x = random.randint(1, 4)
                        print(x)

                        if x != 1:
                            dirlevel = db.reference('level/' + send) #레벨 값 가져오기
                            level = dirlevel.get()
                            level = level[send]

                            direxp = db.reference('exp/' + send) #경험치 값 가져오기
                            exp = direxp.get()
                            exp = exp[send]
                            
                            exp += round(level * 26.25, 3)
                            direxp.update({send:exp})

                            direvent.update({send:"Yes"})
                            await message.channel.send(message.author.mention + "님 당첨되었습니다!! " + str(level * 26.25) + " exp 가 지급됩니다")
                        else:
                            direvent.update({send:"NoNoNo"})
                            await message.channel.send(message.author.mention + "님 아쉽게도 부활전 이벤트는 미당첨입니다 이번 경험치 이벤트는 여기서 종료입니다 아쉽네요")
                    else:
                        await message.channel.send(message.author.mention + "님은 부활전 대상자가 아닙니다 당첨자 이거나 재참여를 먼저 하셔야합니다")
                    
            await message.delete()
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")

client.run(token)