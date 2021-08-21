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
options.add_argument('window-size=1920x1080')
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
        "\n끝말 잇기 시스템(기본)을 시작합니다" + 
        "\n==========================================")

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return

    if str(message.channel.id) == "871251097988235275" and message.content == "!초기화":
        send = str(message.author.id)

        if send == "265725373843636224":
            channel = client.get_channel(871251097988235275)

            mal = ["가", "나", "다", "라", "마" , "바" , "사", "아", "자" , "차", "카", "타", "파", "하"]
            malran = random.randint(0, len(mal) - 1)

            dirmallist = db.reference('mallist/inmallist')
            dirmallist.delete()
            dirmallist.update({'00':mal[malran]})
            dirdan = db.reference('dan/')
            dirdan.update({"dan":mal[malran]})
            dirmallist = db.reference('mallist')
            dirmallist.update({"last":"0"})

            await message.channel.purge(limit=int(999999999))
            await channel.send("초기화가 완료되었습니다 시작단어는 " + mal[malran] + " 입니다\n-규칙-\n1. 한방단어 금지 (한방단어는 관리자에게 미리 알려주세요)\n2. 두음법칙 없음 (북한어로 대체 가능합니다)\n3. 연속 참여 불가\n4. 검색불가 (순수 자신의 지식으로 해주세요)\n5. 한번 사용한 단어 사용 불가능\n6. 북한말, 고어 및 신어 그리고 동사 가능\n7. 끝말잇기 성공 판단은 전문가의 감수가 진행되고 있거나 판명된 모든 단어로 한다")
            return
        else:
            await channel.send("관리자가 아닙니다 해당방은 관리자만 초기화가 가능합니다.")
            return

    if str(message.channel.id) == "871251097988235275":
        #받은 메세지 및 입력자 출력
        print(str(message.author) + str(message.author.mention) + " : " + str(message.content))

        msg = await message.channel.send("해당 단어를 검사중입니다")
        try:
            dirmallist = db.reference('mallist/')
            dmallist = dirmallist.get()
            
            isstart = dmallist['isit']
            if isstart == 0:
                dirmallist.update({"isit":1})
            else:
                await message.delete()
                await msg.edit(content=message.author.mention + "님 이미 누군가 먼저 입력하여 검사중입니다")
                return
            
            if len(message.content) <= 1:
                await msg.edit(content=message.author.mention + "님 두글자 이상만 가능합니다")
                await message.delete()
                dirmallist.update({"isit":0})
                return

            mallist = dmallist['mallist']
            if message.content[-1:] in mallist:
                await msg.edit(content=message.author.mention + "님 한방단어는 불가능합니다")
                await message.delete()
                dirmallist.update({"isit":0})
                return

            send = str(message.author.id)

            mallist = dmallist['last']
            if send == mallist:
                await msg.edit(content=message.author.mention + "님은 방금 하셨습니다")
                await message.delete()
                dirmallist.update({"isit":0})
                return

            inmallist = dmallist['inmallist'].values()
            if message.content in inmallist:
                await msg.edit(content=message.author.mention + "님 해당 단어는 이미 사용한 단어입니다")
                await message.delete()
                dirmallist.update({"isit":0})
                return

            dirdan = db.reference('dan/') # 끝말 조회
            danm = dirdan.get()
            danm = danm["dan"]

            if message.content[:1] != danm:
                await msg.edit(content=message.author.mention + "님 끝말이 이어지지 않습니다")
                await message.delete()
                dirmallist.update({"isit":0})
                return

            driver.get("https://opendict.korean.go.kr/search/searchResult?focus_name=query&query=" + message.content + "&dicType=1&wordMatch=Y")# 사이트 열람
            driver.implicitly_wait(2)
            
            einput = driver.find_element_by_class_name("word_dis.ml5").get_attribute("innerHTML")
            print(einput + "성공(기본)")

            dirmylist = db.reference('mallist/mylist/' + send)
            mylist = dirmylist.get()
            if mylist == None: #저장된 정보가 없을시
                mylist = 1
                await message.channel.send(message.author.mention + "님!! 끝말잇기는 처음이시군요!\n명칭 '끝말잇기 입문자'를 드립니다!!")
                role = discord.utils.get(message.guild.roles, name="끝말잇기 입문자")
                await message.author.add_roles(role)
            else:
                mylist = mylist[send] + 1

            if mylist == 100:
                role = discord.utils.get(message.guild.roles, name="끝말잇기 입문자")
                await message.author.remove_roles(role)
                await message.channel.send("축하드립니다!! " + message.author.mention + "님!! " + str(mylist) + " 번째 끝말잇기 입니다!!\n명칭 '끝말잇기 초보'를 드립니다!!")
                role = discord.utils.get(message.guild.roles, name="끝말잇기 초보")
                await message.author.add_roles(role)
            elif mylist == 2500:
                role = discord.utils.get(message.guild.roles, name="끝말잇기 초보")
                await message.author.remove_roles(role)
                await message.channel.send("축하드립니다!! " + message.author.mention + "님!! " + str(mylist) + " 번째 끝말잇기 입니다!!\n명칭 '끝말잇기 중수'를 드립니다!!")
                role = discord.utils.get(message.guild.roles, name="끝말잇기 중수")
                await message.author.add_roles(role)
            elif mylist == 5500:
                role = discord.utils.get(message.guild.roles, name="끝말잇기 중수")
                await message.author.remove_roles(role)
                await message.channel.send("축하드립니다!! " + message.author.mention + "님!! " + str(mylist) + " 번째 끝말잇기 입니다!!\n명칭 '끝말잇기 고수'를 드립니다!!")
                role = discord.utils.get(message.guild.roles, name="끝말잇기 고수")
                await message.author.add_roles(role)
            elif mylist == 10000:
                role = discord.utils.get(message.guild.roles, name="끝말잇기 고수")
                await message.author.remove_roles(role)
                await message.channel.send("축하드립니다!! " + message.author.mention + "님!! " + str(mylist) + " 번째 끝말잇기 입니다!!\n명칭 '끝말잇기 정복자'를 드립니다!!")
                role = discord.utils.get(message.guild.roles, name="끝말잇기 정복자")
                await message.author.add_roles(role)

            dirmylist.update({send:mylist})

            if len(inmallist) % 1000 == 0:
                await message.channel.send("축하드립니다!! " + message.author.mention + "님!! " + str(len(inmallist)) + " 번째를 가져가셨습니다!!")

            dirdan.update({"dan":message.content[-1:]})
            dirmallist.update({"last":send})
            
            count = list(dmallist['inmallist'].keys())
            count = int(float(count[len(count) - 1])) + 1

            dirmallist = db.reference('mallist/inmallist')
            dirmallist.update({str(count):message.content})
            dirmallist = db.reference('mallist/')
            
            await msg.edit(content=message.author.mention + "님 성공!\n단어 의미 : " + einput + "\n현재 총 사용 단어 수 : " + str(len(inmallist)) + "\n본인 스코어 : " + str(mylist))
            dirmallist.update({"isit":0})
        except:
            await message.delete()
            dirmallist = db.reference('mallist/')
            dmallist = dirmallist.get()
            dirmallist.update({"isit":0})
            await msg.edit(content=message.author.mention + "님 해당 단어는 존재하지 않습니다")

client.run(token)