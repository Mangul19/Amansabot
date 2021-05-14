#어만사 전용 디스코드 봇 백

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
sys.path.insert(0, "D:/Desktop/bot-Amansa/__pycache__")
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
cred = credentials.Certificate("D:/Desktop/bot-Amansa/__pycache__/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

async def background_backcov(): # 코로나 정보 조회 시스템 **!코로나 명령어와 시스템 동일**
    await client.wait_until_ready()

    while True:
        try:
            if "10:01" ==  time.strftime('%H:%M', time.localtime(time.time())): #특정 시간에 작동
                driver.get("http://ncov.mohw.go.kr/")# 사이트 열람
                driver.implicitly_wait(60)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                embed = discord.Embed(title="코로나 정보", color=0x5CD1E5) #임베드 생성

                einput = str(soup.select(
                    'body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(1) > span.before'
                ))
                embed.add_field(name="질병관리청 공식 확진자 수 [전날 확진자 <AM 10시에 업데이트>]", value=einput[28:-9] + "명", inline=False) # 전날 확진자 선택 및 임베트 추가

                einput = str(soup.select(
                    'body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(4) > span.before'
                ))
                embed.add_field(name="질병관리청 공식 사망자 수 [전날 사망자 <AM 10시에 업데이트>]", value=einput[23:-9] + "명", inline=False)# 전날 사망자 선택 및 임베트 추가

                driver.get("https://v1.coronanow.kr/live.html")# 사이트 열람
                driver.implicitly_wait(60)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                einput = str(soup.select(
                    '#ALL_decidecnt_increase > b'
                ))

                embed.add_field(name="실시간 코로나 확진자 수", value=einput[4:-5], inline=False)#실시간 확진자 선택 및 임베트 추가

                channel = client.get_channel(832799360210436107)
                await channel.send(embed=embed)

                channel = client.get_channel(833629507939467274)
                await channel.send(embed=embed)
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(60*1)

async def background_heijisin():#해외 지진 자동 감지 시스템 **!지진 시스템과 대부분 일치**
    await client.wait_until_ready()

    while True:
        try:
            dirji = db.reference('jisinout/')
            ji = dirji.get()
            ji = ji['jisin']

            driver.get("https://www.weather.go.kr/w/eqk-vol/search/worldwide.do")# 사이트 열람
            driver.implicitly_wait(60)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            einput = str(soup.select('#excel_body > tbody > tr:nth-child(1) > td:nth-child(2) > span'))[7:-8] # 가져올 값 선택 

            if ji != einput and einput != "":
                dirji.update({'jisin':einput})

                embed = discord.Embed(title="경고! 해외에 강진이 발생하였습니다", description="지진 자동 감지 시스템", color=0x5CD1E5)

                einlist = ["발생시각", "규모", "발생 깊이", "위치"]
                listin = 2
                TFL = False

                for insite in einlist:
                    einput = str(soup.select('#excel_body > tbody > tr:nth-child(1) > td:nth-child(' + str(listin) + ') > span'))[7:-8]
                    embed.add_field(name=insite, value=einput, inline=TFL)

                    listin += 1
                    TFL = True
                    if listin == 5:
                        listin = 7
                        TFL = False
                
                embed.set_image(url=str(soup.select('#excel_body > tbody > tr:nth-child(1) > td:nth-child(8) > a'))[10:-51])

                channel = client.get_channel(832799360210436107)
                await channel.send(embed=embed)

                channel = client.get_channel(833629507939467274)
                await channel.send(embed=embed)
            elif einput == "":
               print("불러오기 오류 다음에 다시 시도합니다") 
        except:
            print("오류 발생 다음에 다시 시도합니다")
        await asyncio.sleep(60*1)

async def background_backjisin():#지진 자동 감지 시스템 **!지진 시스템과 일치**
    await client.wait_until_ready()

    while True:
        try:
            dirji = db.reference('jisinin')
            ji = dirji.get()
            ji = ji['jisin']

            driver.get("https://www.weather.go.kr/w/eqk-vol/recent-eqk.do")# 사이트 열람
            driver.implicitly_wait(60)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            einput = str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(1) > td'))[17:-6] # 가져올 값 선택

            if ji != einput and einput != "":
                dirji.update({'jisin':einput})
                
                embed = discord.Embed(title="[경고! 지진이 발생하였습니다]", description="지진 자동 감지 시스템", color=0x5CD1E5)

                embed.add_field(name='발생시각', value=einput, inline=False)#임베드 추가
                einput = str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(2) > td > strong'))[9:-17] # 가져올 값 선택
                embed.add_field(name='규모', value=einput, inline=True)#임베드 추가
                einput = str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(3) > td > strong > font:nth-child(1)'))[22:-8] # 가져올 값 선택
                embed.add_field(name='최대진도', value=einput, inline=True)#임베드 추가
                einput = str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(4) > td:nth-child(4)'))[5:-6] # 가져올 값 선택
                embed.add_field(name='발생깊이', value=einput, inline=True)#임베드 추가
                einput = str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(4) > td.td_loc'))[20:-48] # 가져올 값 선택
                embed.add_field(name='위치', value=einput, inline=False)#임베드 추가
                einput = str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(5) > td'))[17:-6] # 가져올 값 선택
                embed.add_field(name='안내사항', value=einput, inline=False)#임베드 추가
                embed.set_image(url="https://www.weather.go.kr/" + str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div:nth-child(3) > div > img'))[32:-4])

                channel = client.get_channel(832799360210436107)
                await channel.send(embed=embed)

                channel = client.get_channel(833629507939467274)
                await channel.send(embed=embed)
            elif einput == "":
               print("불러오기 오류 다음에 다시 시도합니다") 
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(60*1)

async def background_backrank():#랭킹 지원금
    await client.wait_until_ready()

    while True:
        timeran = random.randint(4, 5)
        timeranbun = random.randint(0, 60)
        await asyncio.sleep(60*60*timeran + 60*timeranbun)#랜덤 시간동안 기다리기

        try:
            dirmoney = db.reference('money/')
            money = dirmoney.get()
            moneykey = list(money.keys()) #돈을 소지하고 있는 유저 전부 조회
            
            #유저 조회 후 조회된 정보 저장
            ussc = []
            usname = []
            trs = []
            cou = 0
            for sco in moneykey:
                dirmoney = db.reference('money/' + sco)
                money = dirmoney.get()
                ussc.insert(cou, money[sco]) #돈 정보
                usname.insert(cou, sco[:-5]) #닉네임 정보
                trs.insert(cou, sco) #ID 전체 정보

                cou += 1

            #정렬
            for size in reversed(range(len(ussc))):
                max_i = 0
                for i in range(0, 1+size):
                    if ussc[i] < ussc[max_i]:
                        max_i = i
                ussc[max_i], ussc[size] = ussc[size], ussc[max_i]
                usname[max_i], usname[size] = usname[size], usname[max_i]
                trs[max_i], trs[size] = trs[size], trs[max_i]

            embed = discord.Embed(title="랭킹 지원금", description="랭킹 지원금은 1~10등까지만 지원됩니다\n랭킹 지원금은 4시간 ~ 6시간 간격으로 랜덤 지급됩니다", color=0x5CD1E5)
            for scor in range(0, len(ussc)):
                meyin = ussc[scor] / 100 * (100 / (scor + 1) / 4) # 레벨에 따라 본인 금액에 따른 기본 지급 금액 계싼

                if  scor + 1 >= 2 and scor + 1 < 5: #등수에 따른 차등 배수 적용
                    meyin = meyin * 1.5 / 3
                elif scor + 1 >= 5 and scor + 1 < 8:
                    meyin = meyin * 1.25 / 3
                elif scor + 1 >= 8:
                    meyin = meyin * 1.2 / 2
                
                meyin = round(meyin, 3)

                if meyin > 10000000.0: # 상금이 100만원을 넘지 못하게 설정
                    meyin = 10000000.0

                embed.add_field(name=str(scor + 1) + "등 ID : " + usname[scor], value=str(ussc[scor]) + "원\n" + str(meyin) + " 원을 지급합니다", inline=True)

                meyin = round(ussc[scor] + meyin, 3)

                dirmoney = db.reference('money/' + trs[scor]) #돈 금액 정상계산 후 업데이트
                dirmoney.update({trs[scor]:meyin})

                if scor == 9:
                    break

            channel = client.get_channel(832799360210436107)
            await channel.send(embed=embed)

            channel = client.get_channel(833629507939467274)
            await channel.send(embed=embed)
        except:
            print("오류 발생 다음에 다시 시도합니다")

async def background_amangochicdirt():#어만고치 청결도 시스템
    await client.wait_until_ready()

    while True:
        await asyncio.sleep(60 * random.randint(5, 15)) #일정 시간 슬립

        try:
            diramangoci = db.reference('amangoci/') #존재하는 어만고치 조회
            amangoci = diramangoci.get()
            amangoci = list(amangoci.keys())

            for word in amangoci:
                diramangociin = db.reference('amangoci/' + word) #존재하는 어만고치의 ID로 하나씩 변경
                amangociin = diramangociin.get()

                hungin  = amangociin['dirt'] # 변경할 시스템 조회

                randomhung = round(random.uniform(0.4, 0.65), 3) #랜덤 수 지정 및 계싼
                hungin = round(hungin - randomhung, 3)

                if hungin <= -100: # 계산된 수가 100이하일시
                    await channel.send("ID : " + word[:-5] + "님의 어만고치가 병사하였습니다 벌금 50%를 부과합니다")
                    diramangociin.delete() #해당 어만고치의 정보 삭제

                    dirmoney = db.reference('money/' + word) # 돈 조회
                    money = dirmoney.get()

                    if money == None: # 돈 정보가 없을시 초기화
                        dirmoney.update({word:50000.0})
                        money = 50000.0
                    else:
                        money = money[word]

                    money = round(money / 2, 3)

                    dirmoney.update({word:money}) # 벌금 계산 후 업데이트

                    dirmoney = db.reference('ye/' + word) #통장 조회
                    money = dirmoney.get()

                    if money == None: #통장 정보가 없을시 초기화
                        dirmoney.update({word:50000.0})
                        money = 50000.0
                    else:
                        money = money[word]

                    money = round(money / 2, 3)

                    dirmoney.update({word:money}) #벌금 계산 후 업데이트
                else:
                    diramangociin.update({'dirt':hungin}) # 일반 업데이트
                    if hungin >= 70: #조건 달성할때 경험치 일부 추가
                        exp  = amangociin['exp'] #경험치 조회
                        level  = amangociin['level']#레벨 조회
                        
                        if level < 1.0: # (구)레벨 정보를 가지고 있을시 1.0으로 초기화
                            level = 1.0

                        exp = round(exp + (10 / level), 3) #경험치를 레벨별로 차등 지급

                        if exp >= 100.0: # 경험치가 100 넘을 시 레벨 업 계산
                            exp = round(exp - 100, 3)
                            diramangociin.update({'exp':exp}) #경험치에서 100 제하고 업데이트

                            level = level + 1 
                            diramangociin.update({'level':level}) #레벨 하나 상승수 업데이트

                            dirmoney = db.reference('money/' + word) #돈 조회
                            money = dirmoney.get()

                            if money == None:#돈 정보가 없을시 초기화
                                dirmoney.update({word:50000.0})
                                money = 50000.0
                            else:
                                money = money[word]

                            money = round(money  + (100000.0 * level), 3) #레벨 업 상금 레벨에 따라 차등 지급 
                            dirmoney.update({word:money})

                            channel = client.get_channel(832799360210436107)
                            await channel.send("ID : " + word[:-5] + "님의 어만고치의 레벨이 상승하였습니다 상금 " + str(10 * level) + "만원을 지급합니다")

                            channel = client.get_channel(833629507939467274)
                            await channel.send("ID : " + word[:-5] + "님의 어만고치의 레벨이 상승하였습니다 상금 " + str(10 * level) + "만원을 지급합니다")  
                        else:#경험치로 인한 레벨 변화가 없을시
                            diramangociin.update({'exp':exp}) #일반 업데이트
        except:
            print("오류 발생 다음에 다시 시도합니다")

async def background_amangochichung():#어만고치 허기도 시스템 ** 어만고치 청결도 시스템과 구조가 같거나 비슷 **
    await client.wait_until_ready()

    while True:
        await asyncio.sleep(60 * random.randint(5, 15))

        try:
            channel = client.get_channel(751716285129424897)

            diramangoci = db.reference('amangoci/')
            amangoci = diramangoci.get()
            amangoci = list(amangoci.keys())

            for word in amangoci:
                diramangociin = db.reference('amangoci/' + word)
                amangociin = diramangociin.get()

                hungin  = amangociin['hung']

                randomhung = round(random.uniform(0.4, 0.65), 3)
                hungin = round(hungin - randomhung, 3)

                if hungin <= -100:
                    await channel.send("ID : " + word[:-5] + "님의 어만고치가 병사하였습니다 벌금 50%를 부과합니다")
                    diramangociin.delete()

                    dirmoney = db.reference('money/' + word)
                    money = dirmoney.get()

                    if money == None:
                        dirmoney.update({word:50000.0})
                        money = 50000.0
                    else:
                        money = money[word]

                    money = round(money / 2, 3)

                    dirmoney.update({word:money})

                    dirmoney = db.reference('ye/' + word)
                    money = dirmoney.get()

                    if money == None:
                        dirmoney.update({word:50000.0})
                        money = 50000.0
                    else:
                        money = money[word]

                    money = round(money / 2, 3)

                    dirmoney.update({word:money})
                else:
                    diramangociin.update({'hung':hungin})
                    if hungin >= 70:
                        exp  = amangociin['exp']
                        level  = amangociin['level']
                        
                        if level < 1.0:
                            level = 1.0

                        exp = round(exp + (10 / level), 3)

                        if exp >= 100.0:
                            exp = round(exp - 100, 3)
                            diramangociin.update({'exp':exp})

                            level = level + 1
                            diramangociin.update({'level':level})

                            dirmoney = db.reference('money/' + word)
                            money = dirmoney.get()

                            if money == None:
                                dirmoney.update({word:50000.0})
                                money = 50000.0
                            else:
                                money = money[word]

                            money = round(money  + (100000.0 * level), 3)
                            dirmoney.update({word:money})

                            channel = client.get_channel(832799360210436107)
                            await channel.send("ID : " + word[:-5] + "님의 어만고치의 레벨이 상승하였습니다 상금 " + str(10 * level) + "만원을 지급합니다")

                            channel = client.get_channel(833629507939467274)
                            await channel.send("ID : " + word[:-5] + "님의 어만고치의 레벨이 상승하였습니다 상금 " + str(10 * level) + "만원을 지급합니다")
                        else:
                            diramangociin.update({'exp':exp}) 
        except:
            print("오류 발생 다음에 다시 시도합니다")

async def background_se(): #자동 세금 시스템 - 소지금
    await client.wait_until_ready()

    while True:
        try:
            if "00:00" ==  time.strftime('%H:%M', time.localtime(time.time())) or "12:00" ==  time.strftime('%H:%M', time.localtime(time.time())) :#해당 시간에만 작동하게 설정
                dirmoney = db.reference('money/') #소지금이 있는 모든 사람 조회
                money = dirmoney.get()
                moneykey = list(money.keys())

                for word in moneykey:
                    dirmoney = db.reference('money/' + word) #조회된 사람의 소지금 개별 조회
                    money = dirmoney.get()
                    money = money[word]

                    mey = 0

                    if money <= 100000.00: #소지금액에 따른 세금 계산
                        mey = round(money / 100 * 5.5, 3)
                    elif money <= 200000.00:
                        mey = round(money / 100 * 10, 3)
                    elif money <= 300000.00:
                        mey = round(money / 100 * 23.5, 3)
                    elif money <= 400000.00:
                        mey = round(money / 100 * 35, 3)
                    elif money <= 500000.00:
                        mey = round(money / 100 * 40, 3)
                    else:
                        mey = round(money / 100 * 50, 3)

                    money = round(money - mey, 3) #세금 제한 금액 계산 후 업데이트
                    dirmoney.update({word:money})

                    dirsegum = db.reference('segum/' + word) # 납부한 세금을 세금 내역에 업데이트
                    segum = dirsegum.get()
                    if segum == None: #세금 내역이 없을시 초기화 후 처리
                        dirsegum.update({word:mey})
                    else:
                        segum = segum[word]
                        segum = round(segum + mey, 3)
                        dirsegum.update({word:segum})

                    dirlastsegum = db.reference('lastsegum/' + word) #마지막으로 낸 세금 초기화 후 업데이트
                    dirlastsegum.update({word:mey})
            
                channel = client.get_channel(832799360210436107)
                await channel.send("소지금 세금을 납부하게 하였습니다")

                channel = client.get_channel(833629507939467274)
                await channel.send("소지금 세금을 납부하게 하였습니다") 
        except:
            print("오류 발생 다음에 다시 시도합니다")
        await asyncio.sleep(60*1)

async def background_segum(): #자동 세금 시스템 - 보유금 ***자동 세금 시스템 - 소지금 과 일치하거나 비슷***
    await client.wait_until_ready()

    while True:
        try:
            if "00:00" ==  time.strftime('%H:%M', time.localtime(time.time())) or "12:00" ==  time.strftime('%H:%M', time.localtime(time.time())) :#해당 시간에만 작동하게 설정
                dirmoney = db.reference('ye/')
                money = dirmoney.get()
                moneykey = list(money.keys())

                for word in moneykey:
                    dirmoney = db.reference('ye/' + word)
                    money = dirmoney.get()
                    money = money[word]

                    mey = 0

                    if money <= 100000.00:
                        mey = round(money / 100 * 5.5, 3)
                    elif money <= 200000.00:
                        mey = round(money / 100 * 10, 3)
                    elif money <= 300000.00:
                        mey = round(money / 100 * 23.5, 3)
                    elif money <= 400000.00:
                        mey = round(money / 100 * 35, 3)
                    elif money <= 500000.00:
                        mey = round(money / 100 * 40, 3)
                    else:
                        mey = round(money / 100 * 50, 3)

                    money = round(money - mey, 3)
                    dirmoney.update({word:money})

                    dirsegum = db.reference('segum/' + word) #파일 존재 유무를 *소지금 세금에서 계산하기 때문에 처리할 필요가 없음
                    segum = dirsegum.get()
                    segum = segum[word]
                    segum = round(segum + mey, 3)
                    dirsegum.update({word:segum})

                    dirlastsegum = db.reference('lastsegum/' + word)
                    segum = dirlastsegum.get()
                    segum = segum[word]
                    segum = round(segum + mey, 3)
                    dirlastsegum.update({word:segum}) #마지막으로 납부한 세금 *소지금 세금과 합쳐서 계산 업데이트

                channel = client.get_channel(832799360210436107)
                await channel.send("보유금 세금을 납부하게 하였습니다")

                channel = client.get_channel(833629507939467274)
                await channel.send("보유금 세금을 납부하게 하였습니다") 
        except:
            print("오류 발생 다음에 다시 시도합니다")
        await asyncio.sleep(60*1)

async def background_ye(): #자동 예금 
    await client.wait_until_ready()
    stratran = random.randint(10, 30)
    await asyncio.sleep(60*stratran) #시작후 일정 시간 대기

    while True: # 계속 반복
        try:
            dirye = db.reference('ye/')
            ye = dirye.get()
            yekey = list(ye.keys()) #통장을 가진 모든 사람 조회

            for word in yekey:
                diryegum = db.reference('ye/' + word) #조회된 사람들의 통장 내역 조회
                yegum = diryegum.get()
                yegum = yegum[word]

                yegum = round(yegum + (yegum / 100 * 0.35), 3) #이자를 더한 후 정상 업데이트
                diryegum.update({word:yegum})
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(60*30)

async def background_code00mukye(): #코드 00번 적금 자동 해지
    await client.wait_until_ready()

    while True:
        try:
            channel = client.get_channel(751716285129424897)

            if "00:00" ==  time.strftime('%H:%M', time.localtime(time.time())): #자정에 실행되도록 설정
                dirmukye00 = db.reference('mukye00/') #해당 적금을 가입한 모든 사람 조회
                mukye00 = dirmukye00.get()
                mukye00 = list(mukye00.keys())

                for word in mukye00:
                    dirmukye00 = db.reference('mukye00/' + word) #가입한 사람들의 가입 일자 조회를 위해 한명씩 개별 조회
                    mukye00 = dirmukye00.get() 
                    mukye00 = mukye00[word]
                    
                    mukye00 = datetime.datetime.strptime(mukye00, "%Y-%m-%d")
                    now = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")

                    if mukye00 == now: #만기일이 다 되었으면
                        dirmukye00cou = db.reference('mukye00cou/' + word) #몇번 납부했는지 조회
                        mukye00cou = dirmukye00cou.get()
                        mukye00cou = mukye00cou[word]

                        givemoney = round(random.uniform(1, 50) * 1000, 3) #기본 지급 금액 계산후 납부한 횟수에 따라 더 많은 돈을 지급
                        for count in range(mukye00cou):
                            givemoney = round(50000 + (givemoney / 100 * 10), 3)
                            count

                        dirmoney = db.reference('money/' + word) #돈조회 - 주식을 살때 돈 정보가 있는지 미리 확인함으로 초기화 작업 불필요
                        money = dirmoney.get()
                        money = money[word]

                        dirmoney.update({word:round(money + givemoney, 3)}) # 해지금액 정상 처리후 업데이트

                        dirmukye00cou.delete()
                        dirmukye00.delete()
                        dirmukye00in = db.reference('mukye00in/' + word)
                        dirmukye00in.delete() #해당 유저에 대한 주식 00번 정보 삭제


                        channel = client.get_channel(832799360210436107)
                        await channel.send("ID : " + word[:-5] + "님의 사흘적금이 만기되었습니다 원금 + 이자 + 보너스  총 " + str(givemoney) + "원이 입금됩니다")

                        channel = client.get_channel(833629507939467274)
                        await channel.send("ID : " + word[:-5] + "님의 사흘적금이 만기되었습니다 원금 + 이자 + 보너스  총 " + str(givemoney) + "원이 입금됩니다")
        except:
            print("오류 발생 다음에 다시 시도합니다")
        
        await asyncio.sleep(60*1)      

async def background_code01mukye(): #코드 01번 적금 자동 해지 **코드 00번 적금 자동해지와 시스템이 비슷하거나 같음**
    await client.wait_until_ready()

    while True:
        try:
            channel = client.get_channel(751716285129424897)

            if "00:00" ==  time.strftime('%H:%M', time.localtime(time.time())):
                dirmukye01 = db.reference('mukye01/')
                mukye01 = dirmukye01.get()
                mukye01 = list(mukye01.keys())

                for word in mukye01:
                    dirmukye01 = db.reference('mukye01/' + word)
                    mukye01 = dirmukye01.get()
                    mukye01 = mukye01[word]
                    
                    mukye01 = datetime.datetime.strptime(mukye01, "%Y-%m-%d")
                    now = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")

                    if mukye01 == now:
                        dirmukye01cou = db.reference('mukye01cou/' + word)
                        mukye01cou = dirmukye01cou.get()
                        mukye01cou = mukye01cou[word]

                        givemoney = round(random.uniform(1, 35) * 1000, 3)
                        for count in range(mukye01cou):
                            givemoney = round(35000 + (givemoney / 100 * 15), 3)
                            count

                        dirmoney = db.reference('money/' + word)
                        money = dirmoney.get()
                        money = money[word]

                        dirmoney.update({word:round(money + givemoney, 3)})

                        dirmukye01cou.delete()
                        dirmukye01.delete()
                        dirmukye01in = db.reference('mukye01in/' + word)
                        dirmukye01in.delete() #해당 유저에 대한 주식 01번 정보 삭제

                        channel = client.get_channel(832799360210436107)
                        await channel.send("ID : " + word[:-5] + "님의 닷새적금이 만기되었습니다 원금 + 이자 + 보너스 총 " + str(givemoney) + "원이 입금됩니다")

                        channel = client.get_channel(833629507939467274)
                        await channel.send("ID : " + word[:-5] + "님의 닷새적금이 만기되었습니다 원금 + 이자 + 보너스 총 " + str(givemoney) + "원이 입금됩니다")
        except:
            print("오류 발생 다음에 다시 시도합니다")
        
        await asyncio.sleep(60*1)

async def background_jusic():#주식 변환시스템
    await client.wait_until_ready()
    jusiclist = ["ju01","ju02","ju03"] #변화시킬 주식 미리 저장

    while True:
        try: 
            for wordin in jusiclist:
                dirjusic = db.reference('ju/')
                jusic = dirjusic.get()
                jusic = jusic[wordin] # 변화시킬 주식의 가격을 조회

                ran = round(random.uniform(-100, 100), 3) #랜덤 %지정

                jusic = round(jusic + (10 * ran), 3) #정상 계산

                if jusic <= 10000: # 주식의 가격이 폭등하거나 폭락하지 않도록 제한 선 설정
                    jusic = round(random.uniform(10000, 25000), 3)
                elif jusic >= 100000:
                    jusic = round(random.uniform(85000, 100000), 3)

                dirjusic.update({wordin:jusic}) #계산후 정상 업데이트
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(5) #5초 대기

async def background_backcovlive(): # 실시간 코로나 정보 조회 시스템 **!코로나 명령어와 시스템 동일**
    await client.wait_until_ready()

    while True:
        try:
            dircov = db.reference('cov19')
            cov = dircov.get()
            cov1 = cov['cov1']

            driver.get("https://v1.coronanow.kr/live.html")# 사이트 열람
            driver.implicitly_wait(60)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            einput1 = str(soup.select("#ALL_decidecnt_increase > div.live-table > div:first-child > div > span > p:nth-child(1) > b"))[29:-5]

            if cov1 != einput1 and einput1 != "":
                einput2 = str(soup.select("#ALL_decidecnt_increase > div.live-table > div:first-child > div > span > p:nth-child(3)"))[117:-5]

                embed = discord.Embed(title="실시간 코로나 정보", description="[코로나 확진자 자동 알림]", color=0x5CD1E5) #임베드 생성

                embed.add_field(name="위치 및 확진자 수", value=einput1, inline=False)
                embed.add_field(name="상세 정보", value=einput2, inline=False)

                dircov.update({'cov1':einput1})

                channel = client.get_channel(832799360210436107)
                await channel.send(embed=embed)

                channel = client.get_channel(833629507939467274)
                await channel.send(embed=embed)
            elif einput1 == "":
               print("불러오기 오류 다음에 다시 시도합니다") 
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(60*1)

async def background_jisinle(): #상위의 지진 시스템과 거의 동일
    await client.wait_until_ready()

    while True:
        try:
            dirjisin = db.reference('jisinle')
            jisin = dirjisin.get()
            jisin = jisin['jisin']
            
            driver.get("http://necis.kma.go.kr/necis-dbf/usermain/new/common/userMainNewForm.do")# 사이트 열람
            driver.implicitly_wait(60)

            #로그인
            driver.find_element_by_name('email').send_keys(code.necisid)
            driver.find_element_by_name('pPasswd').send_keys(code.necispaw)
            driver.find_element_by_xpath("//*[@id='necisLoginVO']/div/div[1]/a").click()
            driver.implicitly_wait(1)

            #정보 찾으러 클릭
            driver.find_element_by_xpath("//*[@id='lnb']/div/ul/li[3]/ul/li[3]/a").click()
            driver.implicitly_wait(1)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            einput1 = str(soup.select("#gridTbody > tr:nth-child(1)"))
            print(einput1)
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(60*1)

#선언
client.loop.create_task(background_backcov())
client.loop.create_task(background_heijisin())
client.loop.create_task(background_backjisin())
client.loop.create_task(background_backrank())
client.loop.create_task(background_amangochichung())
client.loop.create_task(background_amangochicdirt())
client.loop.create_task(background_se())
client.loop.create_task(background_segum())
client.loop.create_task(background_ye())
client.loop.create_task(background_code00mukye())
client.loop.create_task(background_code01mukye())
client.loop.create_task(background_jusic())
client.loop.create_task(background_backcovlive())
#client.loop.create_task(background_jisinle())

client.run(token)