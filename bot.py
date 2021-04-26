#어만사 전용 디스코드 봇

import discord
import asyncio
from discord.ext import tasks, commands
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
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")

#경마 조절 장치
loto_mal = True

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n시스템을 시작합니다" + 
        "\n==========================================")
    # 이 기능을 이용하여 봇의 상태를 출력
    mssg = discord.Game("!help|Made by Han_MangUl")
    await client.change_presence(status=discord.Status.online, activity=mssg)

#새로운 사람이 들어오면
@client.event
async def on_member_join(member):
    channel = client.get_channel(719907483069448223)
    await channel.send(member.author.mention + '님 어만사άλφα에 어서오세요!! \n' +
        '1. 대화 할 시 친하지 않은 상대방과 존대를 해오는 상대방에게는 꼭 존대로 응해주세요 \n' +
        '(초면에는 서로서로 한 발자국 거리두고 대화해 보아요) \n' +
        '2. 문제가 생길시 "벤"이 됩니다 \n'+
        '3. !게임정보 을 입력하여 명령어 확인 후 자신이 하는 게임에 닉네임을 등록해주세요! 서로 같이 게임하면서 친해질 수 있습니다 \n' +
        '4. 주변에 같이 이 디코방에서 즐길 사람있으면 언제든지 초대해주세요! 환영입니다!')

#서버를 나가면
@client.event
async def on_member_remove(member):
    channel = client.get_channel(719907483069448223)
    await channel.send(member.author.mention + ' 님이 서버에서 나가셨습니다.')

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return

    #받은 메세지 출력
    print(message.content)

    try:
        dirhelplist = db.reference('helplist/')
        helplist = dirhelplist.get()
        helplist = helplist['helplist']

        #봇방에는 채팅을 치지못하게 설정
        if str(message.channel.id) == "751716285129424897" or str(message.channel.id) == "823395883088871434" or str(message.channel.id) == "833629507939467274":
            trsText = message.content.split(" ")
            trsText = trsText[0]
            TRF = trsText in helplist
            if TRF == False:
                await message.delete()
                await message.channel.send("채팅은 채팅방에 입력하여주세요")
                return
            
        #명령어 사용 구역외에는 명령어 사용 불가능하게 설정
        if str(message.channel.id) != "809826202088898570" and str(message.channel.id) != "751716285129424897" and str(message.channel.id) != "823395883088871434" and str(message.channel.id) != "833629507939467274": #봇방이 아닌곳 채팅 제한
            trsText = message.content.split(" ")
            trsText = trsText[0]
            TRF = trsText in helplist
            if TRF:
                if trsText == "!TRS":
                    if str(message.channel.id) != "821752050948767754" and str(message.channel.id) == "792305492931772437":
                        await message.delete()
                        await message.channel.send("번역기는 전용 채팅방에 입력하여주세요")
                        return
                else:
                    await message.delete()
                    await message.channel.send("명령어는 봇방에 입력하여주세요")
                    return

        #~~명령어
        if message.content == "!help":
            embed = discord.Embed(title="명령어", color=0x5CD1E5)
            embed.add_field(name="일반", value="!translation, !레벨, !업데이트, !지진, !코로나, !날씨, !출첵", inline=False)
            embed.add_field(name="게임", value="!주사위, !게임, !랭킹", inline=False)
            embed.add_field(name="어만머니", value="!bank 비밀번호, !돈확인, !돈받기,  !세금, !예적금, !송금, !코드발급, !주식", inline=False)
            embed.add_field(name="어만고치", value="!어만고치, !상점, !인벤토리, !먹이, !고치샤워", inline=False)
            embed.add_field(name="게임&닉네임 등록 관리", value="!게임정보", inline=False)

            dirverand = db.reference('verand/')
            verand = dirverand.get()
            verand = verand['verand']

            embed.set_footer(text="시스템 버전 " + verand)
            await message.channel.send(embed=embed)

        if message.content == "!먹이":
            embed = discord.Embed(title="먹이 명령어 사용방법", description="!먹이주기 물품명 갯수\nEX)!먹이주기 라면 2", color=0x5CD1E5)
            await message.channel.send(embed=embed)

        if message.content == "!상점":
            embed = discord.Embed(title="상점 목록", description="!구입'물품명' 갯수 EX)!구입우유 5", color=0x5CD1E5)
            embed.add_field(name="우유", value="6250원", inline=True)
            embed.add_field(name="체다치즈", value="8200원", inline=True)
            embed.add_field(name="묶음라면", value="[10% 할인] 7627원\n<1봉 = 5개>", inline=True)
            embed.add_field(name="라면", value="1695원", inline=True)
            await message.channel.send(embed=embed)

        if message.content == "!송금":
            embed = discord.Embed(title="명령어", color=0x5CD1E5)
            embed.add_field(name="!이체 '금액'", value="'금액'원을 이체 예약 합니다", inline=False)
            embed.add_field(name="!수령이체 '코드'", value="'금액'원을 예금 통장에서 출금합니다", inline=False)
            await message.channel.send(embed=embed)

        if message.content == "!예적금":
            embed = discord.Embed(title="명령어", color=0x5CD1E5)
            embed.add_field(name="!예금 '금액'", value="'금액'원을 예금 통장에 입금합니다", inline=False)
            embed.add_field(name="!출금예금 '금액'", value="'금액'원을 예금 통장에서 출금합니다", inline=False)
            embed.add_field(name="!통장확인", value="통장 잔고를 확인합니다\n예금 이율은 시간당 0.3%이며 시스템이 업데이트 될때도 지급됩니다", inline=False)
            embed.add_field(name="!적금", value="적금관련 명령어를 확인합니다", inline=False)
            await message.channel.send(embed=embed)

        if message.content == "!translation": # 번역 명령어
            embed = discord.Embed(title="명령어", description="!TRS Language1*Language2 content", color=0x5CD1E5)
            embed.add_field(name="설명", value="Language1에는 번역할 언어의 코드를 Language2에는 번역될 언어의 코드를 적고 그 뒤(content)에 내용을 작성하면 AI가 판별 후 번역을 해줍니다", inline=False)
            embed.add_field(name="explanation", value="in Language1, write the code of the language that will be translated, and write the code of the language you want to translate in Language2 ou write down the contents after that, AI will judge and translate", inline=False)
            embed.add_field(name="Language Code", value="언어 코드는 하단 참고 \nLanguage code is at the bottom of the note", inline=False)
            embed.set_image(url="https://cdn.discordapp.com/attachments/718436389062180917/819230778113523732/a048c2a829301878.PNG")
            embed.add_field(name="EX", value="!TRS ko*ja 안녕하세요", inline=False)
            await message.channel.send('번역은 일반 채팅방에 쳐도 괜찮습니다', embed=embed)

        if message.content == "!게임정보": #게임 등록 정보 확인
            embed = discord.Embed(title="등록 방법", color=0x5CD1E5)
            embed.add_field(name="!게임리스트", value="현재 게임 리스트를 확인합니다", inline=False)
            embed.add_field(name="!게임등록 게임명", value="'게임명'을 게임 리스트에 새로 등록합니다\n[최대한 한글명으로 적어주세요]", inline=False)
            embed.add_field(name="!등록내역 게임명", value="'게임명'에 등록되어있는 유저를 확인합니다", inline=False)
            embed.add_field(name="!이름등록 게임명 닉네임", value="'게임명'에 '닉네임'을 등록합니다\n<닉네임은 디코 닉네임으로 입력하여주세요>", inline=False)
            await message.channel.send(embed=embed)

        if message.content == "!게임": #게임안내
            embed = discord.Embed(title="게임 명령어", color=0x5CD1E5)
            embed.add_field(name="!도박", value="일반 도박\n보유 금액이 8만 5천원 이상 혹은 3천원이하 일때는 불가능합니다", inline=False)
            embed.add_field(name="!홀짝 홀OR짝", value="홀짝 게임 5천원 이상일때만 가능\n성공시 자신의 돈의 1.5배 지급! 실패시 벌금! 자신의 돈의 1.5 ~ 1.75배 손실", inline=False)
            embed.add_field(name="!로토도박 금액 배팅", value="배팅을 최대 10까지 할 수 있는 상세 도박\n확률은 일반 도박보다 더 낮습니다", inline=False)
            embed.add_field(name="!경마 번호 매수", value="번호는 1~5번 이내로 지정해주세요 \n매수는 1매당 1천 5백원이며 최대 10매까지 구입이 가능합니다", inline=False)
            await message.channel.send( embed=embed)

        if message.content.startswith(""): #개인 레벨 경험치 부여
            send = str(message.author)  #메세지 송신자 ID 설정
            send = send.split("#")
            send = send[0] + "*" + send[1]
            
            dirlevel = db.reference('level/' + send) #레벨 값 가져오기
            level = dirlevel.get()

            direxp = db.reference('exp/' + send) #경험치 값 가져오기
            exp = direxp.get()

            if level == None: #저장된 정보가 없을시
                dirlevel.update({send:1}) #새로운 값 설정 저장
                direxp.update({send:0})
                
                role = discord.utils.get(message.guild.roles, name="한걸음<~9>") # 역할 부여
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + " 님에게 한걸음<~9>을/를 부여하였습니다")
            else: # 저장된 정보가 있을시
                level = level[send] #레벨 및 경험치 값 가져오기
                exp = exp[send]

                intstr = str(message.content) # 메세지를 String값으로 변환
                intstr = len(intstr) # 길이 계산

                ranin = random.uniform(1.0, 1.5)
                ran = ranin * intstr / 2
                ran = math.ceil(ran) # 길이에 랜덤값 계산후 정수값 저장

                if ran > 50: # 한번에 많은 경험치 부여 방지를 위해 최대값을 50으로 설정
                    ran = 50

                exp = exp + ran

                if exp > 1000: #경험치 값이 1천이 넘었을때
                    exp = exp - 1000 # 경험치에 1천을 제하고 저장
                    direxp.update({send:exp})

                    level = level + 1 # 레벨을 1 상승시킨 후 저장
                    dirlevel.update({send:level})

                    await message.channel.send(message.author.mention + "님의 레벨이 " + str(level) +" 으로/로 상승하였습니다") # 레벨업 정보 송신

                    if level == 10: #레벨에따라 (10의배수) 역할 부여 및 기존 역할 제거
                        role = discord.utils.get(message.guild.roles, name="입주자<~19>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 입주자<~19>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="한걸음<~9>")
                        await message.author.remove_roles(role)
                    elif level == 20:
                        role = discord.utils.get(message.guild.roles, name="설립자<~29>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 설립자<~29>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="입주자<~19>")
                        await message.author.remove_roles(role)
                    elif level == 30:
                        role = discord.utils.get(message.guild.roles, name="제작자<~39>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 제작자<~39>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="설립자<~29>")
                        await message.author.remove_roles(role)
                    elif level == 40:
                        role = discord.utils.get(message.guild.roles, name="고인물<~49>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 고인물<~49>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="제작자<~39>")
                        await message.author.remove_roles(role)
                    elif level == 50:
                        role = discord.utils.get(message.guild.roles, name="화석<~59>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 화석<~59>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="고인물<~49>")
                        await message.author.remove_roles(role)
                    elif level == 60:
                        role = discord.utils.get(message.guild.roles, name="석유<~69>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 석유<~69>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="화석<~59>")
                        await message.author.remove_roles(role)
                    elif level == 70:
                        role = discord.utils.get(message.guild.roles, name="구름<~79>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 구름<~79>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="석유<~69>")
                        await message.author.remove_roles(role)
                else: # 경험치가 충족하지 않았으면 그냥 저장
                    direxp.update({send:exp})

        if message.content == "!주사위": # 주사위
            x = random.randint(1, 6)
            await message.channel.send(message.author.mention + "님의 주사위 수는 : " + str(x) + " 입니다.")

        if message.content == "!레벨": #개인 레벨 안내
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirlevel = db.reference('level/' + send)
            level = dirlevel.get()

            direxp = db.reference('exp/' + send)
            exp = direxp.get()
            
            level = level[send]
            exp = exp[send]

            await message.channel.send(message.author.mention + " 님은 현재 총 " + str(exp) + "exp 가 있으며 레벨은 " + str(level) + "입니다")    

        if message.content == "!도박":
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirdobak = db.reference('money/' + send) # 돈 정보 값 가져오기
            dobak = dirdobak.get()

            if dobak == None:
                dirdobak.update({send:50000.0}) # 돈 정보가 없을시 5만원 저장 후 현재값을 5만원으로 설정
                dobak = 50000.0
            else:
                dobak = dobak[send]

            if dobak < 3000.0: # 3천원보다 적거나 8만 5천원보다 크면 사용 불가능하게 설정
                await message.channel.send("돈이 충분하지 않습니다")
                return
            if dobak > 85000.0:
                await message.channel.send("돈이 너무 많습니다 다른 도박을 이용해주세요")
                return

            be = round(random.uniform(10.0, 50.0) * 100, 3) # 배팅금액 랜덤 값
            ting = round(random.uniform(-3.5, 5.0), 3) # 배팅 배수 랜덤 값
            one = round(be * ting - be, 3) # 계산

            if one >= 0.00: # 이들을 봤을 시
                await message.channel.send(message.author.mention + "님은" + str(be) + "원을 배팅하게 되었습니다 \n" + "배율은 " + str(ting) + "배 입니다 \n" + "총 " + str(one) + "원을 이득을 봤습니다")
            else:
                if ting != 1.00: # 손해를 봤을 시
                    one = one * -1 # -가 붙으면 이상함으로 메세지 송출을 위해 역변환
                    await message.channel.send(message.author.mention + "님은" + str(be) + "원을 배팅하게 되었습니다 \n" + "배율은 " + str(ting) + "배 입니다 \n" + "총 " + str(one) + "원을 잃었습니다")
                    one = one * -1
                else:
                    one = 0.00 # 원금 회수시
                    await message.channel.send(message.author.mention + "님은" + str(be) + "원을 배팅하게 되었습니다 \n" + "배율은 " + str(ting) + "배 입니다 \n" + "원금을 회수하였습니다\n" +
                        "엄청난 확률로 원금 회수를 하셨군요! 321만 4321.987원을 추가 지급해드릴게요")
                    one = 3214321.987 # 보너스액 지급

            dobak = round(dobak + one, 3)

            if dobak < 0.00:  # 파산시 작동
                roto = random.randint(1, 100)
                if roto == 1: # 
                    await message.channel.send(message.author.mention + "님!" + " 스몰 로또 당첨! 10만원이 입금됩니다")
                    dirdobak.update({send:100000.0})
                else:
                    await message.channel.send(message.author.mention + "님의 소지금이 전부 사용되었습니다")
                    dirdobak.update({send:0.0})
            else:
                dirdobak.update({send:dobak})

        if message.content == "!돈확인": #돈 확인
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]
            
            await message.channel.send(message.author.mention + "님이" + " 현재 소지중인 돈은 : " + str(money) + "원입니다")

        if message.content.startswith("!홀짝"): # 홀짝 게임
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ")

            if money < 5000.00:
                await message.channel.send("돈이 충분하지 않습니다")
                return

            auto = random.randint(1, 2) #1은 홀 2는 짝

            if trsText[1] == "홀":
                if auto == 1:#성공 했을때는 보상금액 1.5 지급
                    await message.channel.send(message.author.mention + " 나온 수는 홀! 성공! " + str(round(money / 2, 3)) + "원이 지급됩니다")
                    inmey = round(money + money / 2, 3)
                    dirmoney.update({send:inmey})
                else:
                    bul = round(random.uniform(money/2, money/2 + money/4), 3) #실패 시 최소 1.5 ~ 1.75 차감

                    await message.channel.send(message.author.mention + " 나온 수는 짝! 실패! (っ °Д °;)っ 벌금은 " + str(bul) + "원 입니다")

                    if money - bul < 0.00: # 돈이 음수 일시
                        roto = random.randint(1, 100)
                        if roto == 1:#스몰 로또 당첨시
                            await message.channel.send(message.author.mention + "님!" + " 스몰 로또 당첨! 10만원이 입금됩니다")
                            dirmoney.update({send:100000.0})
                        else:#아니라면 공지후 0으로 초기화
                            await message.channel.send(message.author.mention + "님의 소지금이 전부 사용되었습니다")
                            dirmoney.update({send:0.0})
                    else:# 아니라면 일반 저장
                        inmey = round(money - bul, 3)
                        dirmoney.update({send:inmey})
            elif trsText[1] == "짝":
                if auto == 1:
                    bul = round(random.uniform(money/2, money/2 + money/4), 3)

                    await message.channel.send(message.author.mention + " 나온 수는 홀! 실패! (っ °Д °;)っ 벌금은 " + str(bul) + "원 입니다")
                    
                    if money - bul < 0.00: # 돈이 음수 일시
                        roto = random.randint(1, 100)
                        if roto == 1: # 로또 당첨시
                            await message.channel.send(message.author.mention + "님!" + " 스몰 로또 당첨! 10만원이 입금됩니다")
                            dirmoney.update({send:100000.0})
                        else:#아니라면 공지후 0으로 초기화
                            await message.channel.send(message.author.mention + "님의 소지금이 전부 사용되었습니다")
                            dirmoney.update({send:0.0})
                    else:# 돈이 양수라면 일반 저장
                        inmey = round(money - bul, 3)
                        dirmoney.update({send:inmey})
                else: #성공 했을때는 보상금액 1.5 지급
                    await message.channel.send(message.author.mention + " 나온 수는 짝! 성공! " + str(round(money / 2, 3)) + "원이 지급됩니다")
                    inmey = round(money + money / 2, 3)
                    dirmoney.update({send:inmey})
            else:# 설정한 값이 홀 OR 짝이 아닐 경우 거부
                await message.channel.send("홀과 짝중 하나만 입력하여 주세요")

        if message.content == "!돈받기":#돈지급
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirtime = db.reference('moneytime/' + send) # 수령 받은 시간 정보 받기
            times = dirtime.get()

            if times == None: # 시간정보가 없을시
                times = str(datetime.datetime.now()) # 현재 시간 저장 및 불러오기
                dirtime.update({send:times})
            else:
                times = times[send]
                times = datetime.datetime.strptime(times, "%Y-%m-%d %H:%M:%S.%f") # 시간값이 있다면 시간정보를 가져오고 계산가능한 값으로 변환

            now = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f") # 현재 계산 가능한 값으로 시각 가져오기

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

                if money + ye < 3000.0: # 통장과 돈의 합이 3천원 미만일때
                    give = round(random.uniform(100.00, 500.00) * 100, 3) #랜덤 만큼의 돈을 지급

                    await message.channel.send(message.author.mention + "님에게" + " 지원금 : " + str(give) + "원을 지급합니다")
                    dirmoney.update({send:money + give})

                    times = str(datetime.datetime.now() + datetime.timedelta(minutes=15)) # 15분후의 시간을 저장
                    dirtime.update({send:times})
                else:
                    await message.channel.send(message.author.mention + "님은 이미 충분한 돈을 가지고 있습니다")
            else: # 수령가능시간이 지나지 않았을 경우 거부
                await message.channel.send(message.author.mention + "님 지원금 수령 가능 시간이 되지 않았습니다")

        if message.content == "!통장확인": #예금확인
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirye = db.reference('ye/' + send) #통장값
            ye = dirye.get()

            if ye == None:
                dirye.update({send:0.0})
                ye = 0.0
            else:
                ye = ye[send]
            
            await message.channel.send(message.author.mention + "님이" + " 현재 보유중인 돈은 : " + str(ye) + "원입니다")

        if message.content == "!코로나":#코로나 정보
            driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
            driver.get("http://ncov.mohw.go.kr/")# 사이트 열람
            driver.implicitly_wait(10)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            embed = discord.Embed(title="코로나 정보", description="", color=0x5CD1E5) #임베드 생성

            einput = str(soup.select(
                'body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(1) > span.before'
            ))
            embed.add_field(name="질병관리청 공식 확진자 수 [전날 확진자 <AM 10시에 업데이트>]", value=einput[28:-9] + "명", inline=False) # 전날 확진자 선택 및 임베트 추가

            einput = str(soup.select(
                'body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(4) > span.before'
            ))
            embed.add_field(name="질병관리청 공식 사망자 수 [전날 사망자 <AM 10시에 업데이트>]", value=einput[23:-9] + "명", inline=False)# 전날 사망자 선택 및 임베트 추가

            driver.get("https://v1.coronanow.kr/live.html")# 사이트 열람
            driver.implicitly_wait(10)

            html = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html, 'html.parser')

            einput = str(soup.select(
                '#ALL_decidecnt_increase > b'
            ))

            embed.add_field(name="실시간 코로나 확진자 수", value=einput[4:-5], inline=False)#실시간 확진자 선택 및 임베트 추가

            await message.channel.send(embed=embed)

        if message.content.startswith("!TRS"): #번역기능
            baseurl = "https://openapi.naver.com/v1/papago/n2mt"
            # 띄어쓰기 : split처리후 [2:]을 for문으로 붙인다.
            trsText = message.content.split(" ")

            lengmsg = trsText[1]
            mainText = trsText[2:]

            if len(mainText) == 0: # 번역할 문자이 없을 시
                await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
            else:
                await message.delete()
                combineword = ""
                for word in mainText:
                    combineword += " " + word

                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                lengmsg = lengmsg.split("*") #언어 구분하기

                leng1 = str(lengmsg[0])
                leng2 = str(lengmsg[1])

                #언어 설정
                dataParmas = "source=" + leng1 + "&target=" + leng2 + "&text=" + combineword
                request = Request(baseurl)
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                if (responsedCode == 200): #오류 구분
                    response_body = response.read()
                    #디코드 utf-8
                    api_callResult = response_body.decode('utf-8')
                    api_callResult = json.loads(api_callResult)
                    # 수령 값 저장
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Translate", description= message.author.mention, color=0x5CD1E5)
                    embed.add_field(name=leng1, value=savedCombineword, inline=False)
                    embed.add_field(name="Translated "+ leng2, value=translatedText, inline=False)
                    embed.set_footer(text="API provided by Naver Open API")
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("Error Code : " + responsedCode)

        if message.content.startswith("!로토도박"): #도박
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)#돈 값 받기
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ") # 도박 금액 및 배팅 구분

            be = float(trsText[1]) # 베팅
            ting = int(trsText[2]) # 배수

            if money >= be * 7: # 기본 배팅 가능 금액 확인
                if ting > 0 and ting <= 10:
                    one = round(100 / ting / 2, 3)# 배팅 성공 수
                    be = round(be, 3)

                    ranone = random.randint(1, 100) # 랜덤수

                    won = 0 # 외부 사용을 위해 초기화
                    
                    if one > ranone: # 배팅 성공 수와 랜덤 수 확인
                        won = be * ting # 성공 금액 계산
                        await message.channel.send(message.author.mention + "님은" + str(be) + "원을 배팅 하였습니다 \n" + "배율은 " + str(ting) + "배 입니다 도박 성공!! \n" + "총 " + str(won) + "원 이득을 봤습니다")
                    else:
                        won = be * ting + be # 실패 금액 계산
                        await message.channel.send(message.author.mention + "님은" + str(be) + "원을 배팅 하였습니다 \n" "배율은 " + str(ting) + "배 입니다 도박 실패!! \n" + "총 " + str(won) + "원을 잃었습니다")
                        won = won * -1

                    money = round(money + won, 3) # 돈에 해당 계산 도하기

                    if money < 0.0:#돈이 음수 일시
                        roto = random.randint(1, 100)

                        if roto == 1:
                            await message.channel.send(message.author.mention + "스몰 로또 당첨! 10만원이 입금됩니다")
                            dirmoney.update({send:100000.0})
                        else:
                            await message.channel.send(message.author.mention + "님의 소지금이 전부 사용되었습니다")
                            dirmoney.update({send:0.0})
                    else:
                        dirmoney.update({send:money})
                else:# 배팅 숫자가 인식 불가능 할 시
                    await message.channel.send("배팅율을 다시 입력하여주세요")
            else: # 소지 금액이 적을 시
                await message.channel.send("벌금을 낼 수 있는 금액보다 너무 큰 금액입니다. 배팅 금액을 다시 입력해주세요\n신용 금액은 평균 금액인 배팅액 * 7 원으로 측정됩니다")

        if message.content == "!지진": #최근 지진 정보 접속 및 안내
            driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
            driver.get("https://www.weather.go.kr/w/eqk-vol/recent-eqk.do")# 사이트 열람
            driver.implicitly_wait(10)

            html = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html, 'html.parser')

            embed = discord.Embed(title="최근 지진 정보", description="", color=0x5CD1E5) # 임베드 생성
            
            einput = str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(1) > td'))[17:-6] # 가져올 값 선택
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

            await message.channel.send(embed=embed)

        if message.content == "!코드발급":#비밀코드를 어드민만 볼 수 있게 생성
            dircode = db.reference('bankcode/') #값 가져오기
            code = dircode.get()
            code = code['code']
            print(code) # 명령창에 코드가 뜨도록 설정

        if message.content.startswith("!bank"): #비밀코드 돈받기
            dircode = db.reference('bankcode/') # 저장된 비밀코드 가져오기
            code = dircode.get()['code']
            
            if message.content.split(" ")[1] == code: # 사용자가 작성한 비밀 코드 가져온후 저장된 비밀코드와 비교
                send = str(message.author)#메세지 송출자 확인
                send = send.split("#")
                send = send[0] + "*" + send[1]

                dirmoney = db.reference('money/' + send)#돈 가져오기
                money = dirmoney.get()

                if money == None:#정보가 없을 시 초기화 작업
                    dirmoney.update({send:50000.0})
                    money = 50000.0
                else:
                    money = money[send]
                
                inbank = round(random.uniform(5.0, 15.0) * 10000, 3) #5만 ~ 15만원 중 랜덤 지급
                dirmoney.update({send:inbank + money})

                dircode.update({'code':str(random.randint(0, 999999) * random.randint(0, 999999) * random.randint(0, 999999) + 123456789)}) # 랜덤 비밀 코드 새로 저장
                await message.channel.send("5만원 ~ 15만원 중 랜덤으로 입금됩니다 \n" +message.author.mention + "님에게 총 " + str (inbank) + "원이 입급되었습니다")
            else: #코드가 없거나 틀렸을 시
                await message.channel.send("비밀코드가 틀렸습니다 다시 입력하여주세요")

        if message.content.startswith("!경마"): # 경마 게임
            global loto_mal # 경마 변수 사용 설정
            if loto_mal: # 경마가 진행 중이지 않을 시
                send = str(message.author)
                send = send.split("#")
                send = send[0] + "*" + send[1]#송출자 ID 확인

                dirmoney = db.reference('money/' + send)#돈 가져오기
                money = dirmoney.get()

                if money == None: # 돈값이 없다면 초기화
                    dirmoney.update({send:50000.0})
                    money = 50000.0
                else:
                    money = money[send]

                msg = await message.channel.send("경마를 시작합니다!")
                trsText = message.content.split(" ")

                bunho = int(float(trsText[1])) #경마 말 번호 확인
                mesu = int(float(trsText[2])) # 구입매수 확인

                loto_mal = False # 실행중으로 인식

                if bunho < 1 or bunho > 5: # 경마 말 번호가 이상할시
                    await msg.edit(content="경마말 번호를 다시 선택하여주세요")
                    loto_mal = True
                    return

                if mesu < 1 or bunho > 10: # 매수량 이상시
                    await msg.edit(content="매수량을 다시 입력하여주세요")
                    loto_mal = True
                    return

                if money < mesu * 1500.00: # 보유 금액이 부족 할 시
                    await msg.edit(content="보유금이 부족합니다")
                    loto_mal = True
                    return
                
                cout = [0, 0, 0, 0, 0] # 경마 말 위치 초기화
                mamal = ["", "", "", "", ""] # 경마 UI 초기화

                while cout[0] < 9 and cout[1] < 9 and cout[2] < 9 and cout[3] < 9 and cout[4] < 9: # 경마말이 결승선에 도달 할때까지 반복 
                    mamal[0] = ""
                    mamal[1] = ""
                    mamal[2] = ""
                    mamal[3] = ""
                    mamal[4] = "" # 경마 라인 초기화

                    for i in range(0, 5): # 말 1~5번 위치 별로 라인과 말위치 배치
                        for j in range(0, 10):
                            if cout[i] == j:
                                mamal[i] += "🐴"
                            else:
                                mamal[i] += "🎞"

                    await msg.edit(content="경마 시작!!\n" + mamal[0] + "\n"+ mamal[1] + "\n"+ mamal[2] + "\n"+ mamal[3] + "\n"+ mamal[4] + "\n")

                    ranmal = random.randint(0, 4) #이동할 말 랜덤 선택
                    event = random.randint(1, 2)#이동할 거리 랜덤 선택
                    cout[ranmal] += event # 이동한 거리 계산

                win = 0
                for i in range(0, 5): # 결승선 도달 시 결승점 설정
                    if cout[i] >= 9:
                        win = i + 1
                        mamal[i] = ""
                        for j in range(0, 9):
                            mamal[i] += "🎞"
                        mamal[i] += "🦓"
                        break

                val = "경마 결과 발표\n" + mamal[0] + "\n"+ mamal[1] + "\n"+ mamal[2] + "\n"+ mamal[3] + "\n"+ mamal[4] + "\n" # 결과 발표하기
                val += str(win) + "번 말 승리!\n"
                await msg.edit(content=val)

                if win == bunho:# 승리 말 맞췄을 시
                    await msg.edit(content=val + "맞췄습니다! 원금과 " + str(mesu) + " * 1050.75원이 입금됩니다")
                    inputme = round(money + (mesu * 1050.75), 3) #구입한 매수 만큼 승리 급액 주기
                    dirmoney.update({send:inputme})
                else: # 승리 말 틀렸을 시
                    await msg.edit(content=val + "아쉽네요 총 " + str(mesu) + " * 3250.68원을 잃습니다")

                    if money - mesu * 3500.00 < 0.00: # 돈이 음수 일시
                        roto = random.randint(1, 100)
                        if roto == 1:
                            await msg.edit(content=message.author.mention + "님!" + " 파산 로또 당첨! 10만원이 입금됩니다")
                            dirmoney.update({send:100000.0})
                        else:
                            await msg.edit(content=message.author.mention + "님의" + "보유금이 전부 사용되었습니다")
                            dirmoney.update({send:0.0})
                    else: #보유 금액이 양수 일 시
                        inputme = round(money - (mesu * 3250.68), 3)
                        dirmoney.update({send:inputme})
                loto_mal = True # 경마가 가능하게 설정
            else:
                await message.channel.send("이미 경마가 진행중입니다")

        if message.content == "!날씨": # 날씨 위치 정보가 없을시 사용법 안내
            await message.channel.send("사용법은 !날씨 '지역이름' 을 적으시면 AI가 자동으로 검색하여줍니다\n날씨 정보 왼측 선의 색은 미세먼지 정도에 따라 변화합니다")
        elif message.content.startswith("!날씨"): # 날씨 위치 정보를 입력했을시 해당지역 날씨 확인
            learn = message.content.split(" ")
            location = learn[1]
            enc_location = urllib.parse.quote(location+'날씨')
            hdr = {'User-Agent': 'Mozilla/5.0'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location # 네이버 사이트에서 위치에 대한 날씨 정보 가져오기

            req = Request(url, headers=hdr)
            html = urllib.request.urlopen(req)
            bsObj = BeautifulSoup(html, "html.parser")
            todayBase = bsObj.find('div', {'class': 'main_info'})

            todayTemp1 = todayBase.find('span', {'class': 'todaytemp'})
            todayTemp = todayTemp1.text.strip()  # 온도

            todayValueBase = todayBase.find('ul', {'class': 'info_list'})
            todayValue2 = todayValueBase.find('p', {'class': 'cast_txt'})
            todayValue = todayValue2.text.strip()  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌

            todayFeelingTemp1 = todayValueBase.find('span', {'class': 'sensible'})
            todayFeelingTemp = todayFeelingTemp1.text.strip()  # 체감온도

            todayMiseaMongi1 = bsObj.find('div', {'class': 'sub_info'})
            todayMiseaMongi2 = todayMiseaMongi1.find('div', {'class': 'detail_box'})
            todayMiseaMongi3 = todayMiseaMongi2.find('dd')
            todayMiseaMongi = todayMiseaMongi3.text  # 미세먼지

            tomorrowBase = bsObj.find('div', {'class': 'table_info weekly _weeklyWeather'})
            tomorrowTemp1 = tomorrowBase.find('li', {'class': 'date_info'})
            tomorrowTemp2 = tomorrowTemp1.find('dl')
            tomorrowTemp3 = tomorrowTemp2.find('dd')
            tomorrowTemp = tomorrowTemp3.text.strip()  # 오늘 오전,오후온도

            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowMoring1 = tomorrowAreaBase.find('div', {'class': 'main_info morning_box'})
            tomorrowMoring2 = tomorrowMoring1.find('span', {'class': 'todaytemp'})
            tomorrowMoring = tomorrowMoring2.text.strip()  # 내일 오전 온도

            tomorrowValue1 = tomorrowMoring1.find('div', {'class': 'info_data'})
            tomorrowValue = tomorrowValue1.text.strip()  # 내일 오전 날씨상태, 미세먼지 상태

            tomorrowAreaBase = bsObj.find('div', {'class': 'tomorrow_area'})
            tomorrowAllFind = tomorrowAreaBase.find_all('div', {'class': 'main_info morning_box'})
            tomorrowAfter1 = tomorrowAllFind[1]
            tomorrowAfter2 = tomorrowAfter1.find('p', {'class': 'info_temperature'})
            tomorrowAfter3 = tomorrowAfter2.find('span', {'class': 'todaytemp'})
            tomorrowAfterTemp = tomorrowAfter3.text.strip()  # 내일 오후 온도

            tomorrowAfterValue1 = tomorrowAfter1.find('div', {'class': 'info_data'})
            tomorrowAfterValue = tomorrowAfterValue1.text.strip()

            color = todayMiseaMongi.split("/㎥")
            color = color[1]

            embed = discord.Embed()

            if color == "좋음": # 미세먼지에 따라 임베트 라인색 변경
                embed = discord.Embed(
                title=learn[1]+ ' 날씨 정보',
                description=learn[1]+ ' 날씨 정보입니다.',
                colour=discord.Color.blue()
                )
            elif color == "보통":
                embed = discord.Embed(
                title=learn[1]+ ' 날씨 정보',
                description=learn[1]+ ' 날씨 정보입니다.',
                colour=discord.Color.green()
                )
            elif color == "나쁨":
                embed = discord.Embed(
                title=learn[1]+ ' 날씨 정보',
                description=learn[1]+ ' 날씨 정보입니다.',
                colour=discord.Color.gold()
                )
            elif color == "매우나쁨":
                embed = discord.Embed(
                title=learn[1]+ ' 날씨 정보',
                description=learn[1]+ ' 날씨 정보입니다.',
                colour=discord.Color.red()
                )

            embed.add_field(name='현재온도', value=todayTemp + '˚', inline=False)  # 현재온도
            embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
            embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
            embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
            embed.add_field(name='오늘 오전 / 오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨
            embed.add_field(name='내일 오전온도', value=tomorrowMoring+'˚', inline=False)  # 내일오전날씨
            embed.add_field(name='내일 오전날씨상태, 미세먼지 상태', value=tomorrowValue, inline=False)  # 내일오전 날씨상태
            embed.add_field(name='내일 오후온도', value=tomorrowAfterTemp + '˚', inline=False)  # 내일오후날씨
            embed.add_field(name='내일 오후날씨상태, 미세먼지 상태', value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태

            await message.channel.send(embed=embed)

        if message.content.startswith("!예금"): #예금 입금 시스템
            send = str(message.author) #송출자 ID 확인
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send) #돈 가져오기
            money = dirmoney.get()
                    
            dirye = db.reference('ye/' + send) # 통장 값 가져오기
            ye = dirye.get()

            if ye == None: # 통장 및 소지금 값이 없을 시 초기화 작업
                dirye.update({send:0.0})
                ye = 0.0
            else:
                ye = ye[send]

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ")
            yein = round(float(trsText[1]), 3) # 입금 요청 금액 확인

            if money >= yein: # 요청 금액이 소지금 보다 적다면
                money = round(money - yein, 3) # 정상 계산 처리 후 정보 업데이트
                ye = round(ye + yein, 3)

                dirmoney.update({send:money})
                dirye.update({send:ye})

                await message.channel.send("예금 통장에 " + str(yein) + "원을 입금하였습니다")
            else:# 요청 금액이 소지금 보다 크다면 거부
                await message.channel.send("소지금 보다 많습니다 다시 입력하여주세요")

        if message.content.startswith("!출금예금"): #예금 출금 시스템 **위 시스템과 완전 일치**
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()
                    
            dirye = db.reference('ye/' + send)
            ye = dirye.get()

            if ye == None:
                dirye.update({send:0.0})
                ye = 0.0
            else:
                ye = ye[send]

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ")
            yein = round(float(trsText[1]), 3)

            if ye >= yein:
                ye = round(ye - yein, 3)
                money = round(money + yein, 3)

                dirmoney.update({send:money})
                dirye.update({send:ye})

                await message.channel.send("예금 통장에서 " + str(yein) + "원을 출금하였습니다")
            else:
                await message.channel.send("보유금 보다 많습니다 다시 입력하여주세요")

        if message.content.startswith("!이체"): #돈을 이체합니다
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] #송출자 ID 확인

            dirmoney = db.reference('money/' + send) #돈 가져오기
            money = dirmoney.get()

            if money == None:#돈값없을시 초기화
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ")
            trsText = round(float(trsText[1]), 3)#이체금액 확인

            if trsText <= money:#이체금액이 소지금보다 작다면 OR 같다면
                code = "" # 비밀코드 초기화
                codelist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" # 랜덤 코드 배열 주기
                for cou in range(20): # 위 코드 배열에서 랜덤으로 20자 선택
                    rani = random.randint(0, 51)
                    code += codelist[rani]

                money = round(money - trsText, 3) # 돈 정상 계산 후 업데이트
                dirmoney.update({send:money})

                dirgive = db.reference('givemoney/' + code) # 랜덤 코드 및 사용자 정보 저장
                dirgive.update({send:trsText})

                await message.channel.send("정상적으로 " +  code + " 코드로 " + str(trsText) +"원을 이체를 예약하였습니다")
            else: # 소지금 보다 많이 요청시 거부
                await message.channel.send("이체 금액이 소지 금액보다 많습니다")

        if message.content.startswith("!수령이체"): #이체 예약 수령
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 송출자 ID 확인

            dirmoney = db.reference('money/' + send) # 송출자의 돈 값 불러오기
            money = dirmoney.get()

            if money == None: # 돈 정보가 없다면 초기화 작업
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ") # 입력한 이체코드 자르고 가져오기
            trsText = trsText[1]

            dirgive = db.reference('givemoney/' + trsText) # 해당 이체 코드 불러오기
            give = dirgive.get()

            if give == None: # 해당 코드가 없다면 거부
                await message.channel.send("없는 코드입니다")
            else: #있다면 ~
                dirgivein = db.reference('givemoney/' + trsText + "/" + list(give.keys())[0]) # 코드 예약자와 예약 금액 조회
                givein = dirgivein.get() # 예약 금액
                keyin = list(give.keys())[0] # 이체 예약자

                if send == keyin: # 수령자와 이체자의 명의가 같을 시 거무
                    await message.channel.send(message.author.mention + "님 이체 수령은 본인 수령이 불가합니다")
                else: #다를시
                    money = round(money + givein, 3) #정상 계산 후 업데이트
                    dirmoney.update({send:money})

                    dirgive.delete() # 해당 이체 정보 삭제
                    await message.channel.send(message.author.mention + "님께 정상적으로 수령되었습니다")

        if message.content.startswith("!게임등록"): #게임 리스트 추가
            dirgame = db.reference('gamelist/') # 게임 리스트 가져온 후 배열로 변환
            gmaelist = dirgame.get()
            gmaelist = list(gmaelist.keys())

            trsText = message.content.split(" ") # 저장하고자 하는 게임 char 읽기
            trsText = trsText[1:]
            combineword = ""
            for word in trsText:
                combineword += str(word)
            
            if combineword in gmaelist: #이미 등록 되어있다면 거부
                await message.channel.send(combineword + " 은/는 이미 등록되어있는 게임입니다")
            else:#등록되어있지 않다면 새로 저장
                dirgame.update({combineword + "/0":""})

                await message.channel.send(combineword + " 을/를 정상 등록하였습니다")

        if message.content.startswith("!이름등록"): #게임에 사용자 등록
            trsText = message.content.split(" ")

            gamename = str(trsText[1]) # 저장하고자 하는 게임 가져오기
            usernamein = trsText[2:] # 저장하고자 하는 닉네임 가져오기

            username = "" # 닉네임 char 읽기
            for nameinput in usernamein:
                username += nameinput + " "
            username = username[0:-1]

            dirgame = db.reference('gamelist/') #게임 리스트 가져오기
            gamelistch = dirgame.get()
            gamelistch = list(gamelistch.keys())

            if gamename in gamelistch: #해당 게임이 있따면
                gamelist = dirgame.get() # 해당 닉네임이 이미 있는지 조회
                gamelist = gamelist[gamename]

                if username in gamelist: #있다면 거부
                    await message.channel.send(username + "님은/는 " + gamename + " 게임에 이미 등록되어있습니다")
                else:# 없다면 리스트로 저장
                    dirgame.update({gamename + "/" + str(len(gamelist)):username})
                    await message.channel.send(username + "님을/를 " + gamename + " 게임에 정상 등록하였습니다")
            else:# 해당게임 없다면 거부
                await message.channel.send(gamename + " 은/는 게임리스트에 존재하지 않습니다 새로 등록하여주세요")

        if message.content == "!게임리스트": #게임 리스트 확인
            dirgame = db.reference('gamelist/') 
            gmaelist = dirgame.get()
            gmaelist = sorted(list(gmaelist.values())) #모든 게임리스트 가져온 후 리스트로 전환

            namelist = ""
            lenCC, chk = 1, 0
            lenchk = len(gmaelist) #리스트 길이 계산

            for word in gmaelist: #리스트 길이 만큼 게임 읽어오기
                chk += 1
                lenCC += 1
                
                #리스트 > String 통합
                if lenCC == lenchk + 1:
                    namelist += word.split(".txt")[0]
                else:
                    namelist += word.split(".txt")[0] + " , "

                    if chk == 3:
                        namelist += "\n"
                        chk = 0

            embed = discord.Embed(title="게임리스트", description=namelist, color=0x5CD1E5) #임베드 생성
            
            await message.channel.send(embed=embed)

        if message.content.startswith("!등록내역"): #게임에 대한 닉네임 리스트 확인
            dirgame = db.reference('gamelist/') # 게임리스트 가져오기
            gmaelistin = dirgame.get()
            gmaelist = list(gmaelistin.keys())

            trsText = message.content.split(" ") # 읽어올 게임 확인
            trsText = trsText[1:]
            combineword = ""
            for word in trsText:
                combineword += str(word)
            
            if combineword in gmaelist: # 게임리스트에 해당 요청 게임이 있다면
                gamelist = list(gmaelistin[combineword])[1:] # 해당 게임 등록 내역 읽어오기

                listword = "" # 저장 변수 초기화

                lenchk = len(gamelist) # 등록 내역 길이 확인
                lenCC = 1
                chk = 0
                #등록 닉네임 저장 변수에 붙이기
                for word in gamelist:
                    chk += 1
                    lenCC += 1

                    if lenCC == lenchk + 1:
                        listword += word
                    else:
                        listword += word + " , "

                        if chk == 3:
                            listword += "\n"
                            chk = 0
                
                embed = discord.Embed(title=combineword + " 유저 리스트", description=listword, color=0x5CD1E5) #임베드 생성
                await message.channel.send(embed=embed)
            else:#게임이 없을경우 거부
                await message.channel.send(combineword + " 은/는 게임리스트에 존재하지 않습니다 새로 등록하여주세요")

        if message.content == "!어만고치": #어만고치 만들기 및 상태확인
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 송출자 ID 설정

            dirgoci = db.reference('amangoci/' + send) # 어만고치 저장 위치로 이동 및 조회
            goci = dirgoci.get()

            exp, hung, dirt, level = 0, 0, 0.0, 0.0 # 외부 사용을 위해 초기화[경험치, 허기, 청결도, 레벨]

            if goci == None: # 어만고치가 없다면 새로 생성 후 초기화
                dirgoci.update({'exp':0})
                dirgoci.update({'level':1})
                dirgoci.update({'hung':100.0})
                dirgoci.update({'dirt':100.0})

                exp, hung, dirt, level = 0, 100.0, 100.0, 1

                await message.channel.send("새로운 어만고치를 입양하였습니다")
            else: # 있다면 정보 조회
                exp = goci['exp']
                hung = goci['hung']
                dirt = goci['dirt']
                level = goci['level']

            embed = discord.Embed(title="어만고치 스테이터스", description=message.author.mention, color=0x5CD1E5) #임베트 생성 후 정보 출력
            embed.add_field(name="레벨", value=level, inline=True)
            embed.add_field(name="경험치", value=exp, inline=True)
            embed.add_field(name="포화도", value=hung, inline=True)
            embed.add_field(name="청결도", value=dirt, inline=True)
            embed.set_footer(text="포화도 및 청결도가 -100이 되면 사망합니다")
            await message.channel.send(embed=embed)

        if message.content.startswith("!구입체다치즈"): #체다치즈 구입 도우미
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 송출자 ID 확인

            dirmoney = db.reference('money/' + send)# 돈확인
            money = dirmoney.get()

            if money == None: #돈 정보 없으면 초기화 작업
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ") # 구입 갯수 확인
            trsText = round(float(trsText[1]), 0)

            if trsText * 8200 <= money: #금액이 충분할 경우
                name = "chechi" # 구입 상품 설정
                dirinven = db.reference('inven/' + send  + '/' + name) # 해당아이템 소지 조회
                inven = dirinven.get()
                money = round(money - trsText * 8200, 3)
                
                if inven == None: # 없다면 초기화
                    dirinven.update({name:0})
                    inven = 0
                else:
                    inven = inven[name]
                
                inven = inven + trsText #정상 계산 후 업데이트
                dirinven.update({name:inven})
                dirmoney.update({send:money})

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else: # 돈이 부족하다면 안내
                await message.channel.send("돈이 부족합니다")

        if message.content.startswith("!구입우유"): #우유 구입 도우미 **위 코딩과 구조 일치**
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ")
            trsText = round(float(trsText[1]), 0)

            if trsText * 6250 <= money:
                name = "mlk"
                dirinven = db.reference('inven/' + send  + '/' + name)
                inven = dirinven.get()
                money = round(money - trsText * 6250, 3)
                
                if inven == None:
                    dirinven.update({name:0})
                    inven = 0
                else:
                    inven = inven[name]
                
                inven = inven + trsText
                dirinven.update({name:inven})
                dirmoney.update({send:money})

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else:
                await message.channel.send("돈이 부족합니다")

        if message.content.startswith("!구입묶음라면"): #라면1봉 구입 도우미**위 코딩과 구조 일치**
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ")
            trsText = round(float(trsText[1]), 0)

            if trsText * 7627 <= money:
                name = "ramen"
                dirinven = db.reference('inven/' + send  + '/' + name)
                inven = dirinven.get()
                money = round(money - trsText * 7627, 3)
                
                if inven == None:
                    dirinven.update({name:0})
                    inven = 0
                else:
                    inven = inven[name]
                
                inven = inven + trsText * 5
                dirinven.update({name:inven})
                dirmoney.update({send:money})

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else:
                await message.channel.send("돈이 부족합니다")

        if message.content.startswith("!구입라면"): #라면1개 구입 도우미 **위 코딩과 구조 일치**
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
                money = 50000.0
            else:
                money = money[send]

            trsText = message.content.split(" ")
            trsText = round(float(trsText[1]), 0)

            if trsText * 1695 <= money:
                name = "ramen"
                dirinven = db.reference('inven/' + send  + '/' + name)
                inven = dirinven.get()
                money = round(money - trsText * 1695, 3)
                
                if inven == None:
                    dirinven.update({name:0})
                    inven = 0
                else:
                    inven = inven[name]
                
                inven = inven + trsText
                dirinven.update({name:inven})
                dirmoney.update({send:money})

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else:
                await message.channel.send("돈이 부족합니다")

        if message.content == "!인벤토리":#인벤토리 확인
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] #송출자 ID 확인

            embed = discord.Embed(title="인벤토리 열람", description=message.author.mention, color=0x5CD1E5)

            dirinven = db.reference('inven/' + send  + '/' + "ramen") #인벤토리 3개 분야 조회 및 초기화 후 임베트 추가
            inven = dirinven.get() #조회
            if inven == None:# 초기화
                dirinven.update({"ramen":0})
                inven = 0
            else:
                inven = inven["ramen"]
                embed.add_field(name="라면", value=str(inven) + "개", inline=True) #추가
            
            dirinven = db.reference('inven/' + send  + '/' + "chechi")
            inven = dirinven.get()
            if inven == None:
                dirinven.update({"chechi":0})
                inven = 0
            else:
                inven = inven["chechi"]
                embed.add_field(name="체다치즈", value=str(inven) + "개", inline=True)

            dirinven = db.reference('inven/' + send  + '/' + "mlk")
            inven = dirinven.get()
            if inven == None:
                dirinven.update({"mlk":0})
                inven = 0
            else:
                inven = inven["mlk"]
                embed.add_field(name="우유", value=str(inven) + "개", inline=True)

            await message.channel.send(embed=embed)

        if message.content == "!고치샤워": #어만고치 샤워하기
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] #송출자 Id 확인

            dirgoci = db.reference('amangoci/' + send) #청결도 조회
            goci = dirgoci.get()
            goci = goci['dirt']

            if goci == None: # 어만고치 없다면 거부
                await message.channel.send(message.author.mention + "님은 어만고치가 없습니다")
            else:#있다면 100으로 업데이트
                await message.channel.send(message.author.mention + "님의 어만고치가 깨끗해 졌습니다")
                dirgoci.update({'dirt':100.0})

        if message.content == "!랭킹":#랭킹 안내
            dirmoney = db.reference('money/')
            money = dirmoney.get()
            moneykey = list(money.keys()) #소지금이 있는 모든 사람 조회

            ussc = []
            usname = []
            cou = 0
            for sco in moneykey:#조회된 사람들의 금액 읽은 값 및 ID에 ID코드 제거 후 이름만 저장
                dirmoney = db.reference('money/' + sco)
                money = dirmoney.get()
                ussc.insert(cou, money[sco])

                usname.insert(cou, sco[:-5])

                cou += 1
            
            for size in reversed(range(len(ussc))): # 소지금에 따른 배열 정렬
                max_i = 0
                for i in range(0, 1+size):
                    if ussc[i] < ussc[max_i]:
                        max_i = i
                ussc[max_i], ussc[size] = ussc[size], ussc[max_i]
                usname[max_i], usname[size] = usname[size], usname[max_i]
            
            embed = discord.Embed(title="랭킹", description="랭킹은 통장 제외 소지 금액만 인정됩니다", color=0x5CD1E5)

            for scor in range(0, len(ussc)):#상위 10명만 출력
                embed.add_field(name=str(scor + 1) + "등 ID : " + usname[scor], value=str(ussc[scor]) + "원", inline=True)
                if scor == 11:
                    break

            await message.channel.send( embed=embed)

        if message.content.startswith("!먹이주기"): #어만고치 먹이주기
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 송출자 ID 저장

            trs = message.content.split(" ") 
            trswhat = trs[1] # 주고자하는 먹이 확인
            trssel = int(float(trs[2]))# 갯수확인

            wiin = 0.0

            name = ""

            if trswhat == "라면": # 주고자하는 먹이의 포화 차지수 확인
                name = "ramen"
                wiin = 3.3
            elif trswhat == "우유":
                name = "mlk"
                wiin = 8.68
            elif trswhat == "체다치즈":
                name = "chechi"
                wiin = 11.38
            else:#입력한 먹이가 없다면 거부
                await message.channel.send(message.author.mention + "물품명을 다시 입력하여 주세요.")
                return

            dirinven = db.reference('inven/' + send  + '/' + name) # 해당 먹이를 인벤토리에서 조회
            inven = dirinven.get()

            if inven == None:#없다면 초기화 작업
                dirinven.update({name:0})
                inven = 0
            else:
                inven = inven[name]

            if inven > 0 and inven >= trssel and trssel > 0.0: # 해당 먹이가 충분하거나 0이상할때만 작동
                inven = inven - trssel
                dirinven.update({name:inven}) # 정상 차감 후 업데이트

                diramangociin = db.reference('amangoci/' + send) # 배고픔 조회
                amangociin = diramangociin.get()
                hungin  = amangociin['hung']

                hungwi = round(hungin + wiin * trssel, 3) # 배고픔 계싼

                if hungwi > 100: # 배고픔이 오버될시
                    await message.channel.send(message.author.mention + "님의 어만고치가 배불러 합니다")
                    diramangociin.update({'hung':100.0}) #초기화 후 저장
                else:#해당 조건이 아닐시
                    await message.channel.send(message.author.mention + "님의 어만고치가 먹이를 맛있게 먹습니다")
                    diramangociin.update({'hung':hungwi}) # 일반 저장

        if message.content == "!세금": #세금 안내
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 조회자 ID 확인

            dirsegum = db.reference('segum/' + send) # 세금 조회
            segum = dirsegum.get()

            if segum == None: # 정보가 없다면
                await message.channel.send("세금을 내신적이 없습니다")
            else: #있다면
                dirlastsegum = db.reference('lastsegum/' + send) #세금 조회
                lastsegum = dirlastsegum.get()

                segum = segum[send] # 누적 세금
                lastsegum = lastsegum[send] # 제일 최근 납부 금액

                await message.channel.send("[세금 기준]\n10만원 이하 5.5% 20만원 이하 10% 30만원 이하 23.5% 40만원 이하 35% 50만원 이하 40% 그외 50%\n세금은 00시, 12시에 납부됩니다\n내신 세금의 총합은 : " + str(segum) + "원입니다\n제일 최근에 낸 세금액은 " + str(lastsegum) + " 원입니다")

        if message.content == "!업데이트": #업데이트 안내 시스템
            dirupdata = db.reference('updata/') #업데이트 정보 조회
            updata = dirupdata.get()
            updata = updata['updata']

            embed = discord.Embed(title="최근 업데이트 내용", description=updata, color=0x5CD1E5)

            dirverand = db.reference('verand/') #버전 정보 조회
            verand = dirverand.get()
            verand = verand['verand']

            embed.set_footer(text=verand)
            await message.channel.send(embed=embed)

        if message.content == "!적금": #적금 시스템 안내
            dirmukye = db.reference('mukye/')
            mukye = dirmukye.get()
            mukye = list(mukye['mukye']) #적금 내열 조회 및 리스트 변환

            embed = discord.Embed(title="적금상품", color=0x5CD1E5)
            for input in mukye:
                embed.add_field(name="상품", value=input, inline=False)
            embed.set_footer(text="상품 가입 방법 >> !적금가입 '상품번호'")
            await message.channel.send(embed=embed)

        if message.content == "!출첵": #출석체크
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 출첵 송출자 ID 확인

            dirtime = db.reference('sekitime/' + send) # 해당일 출석체크 정보 조회
            times = dirtime.get()

            if times == None: # 출석체크일 정보가 없다면 초기화 및 업데이트
                times = str(datetime.datetime.now() + datetime.timedelta(days=-1)).split(" ")[0]
                dirtime.update({send:times})
            else: #있다면 조회
                times = times[send]

            times = datetime.datetime.strptime(times, "%Y-%m-%d") # 저장된 정보를 계산가능하게 변경
            now = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d") #금일 날자 계싼

            if times < now: # 출첵일이 금일 이전이라면
                dirseki = db.reference('seki/' + send) # 출첵 횟수 조회
                seki = dirseki.get()

                dirmoney = db.reference('money/' + send) # 돈조회
                money = dirmoney.get()

                if seki == None: #출첵한적이 없다면
                    await message.channel.send("출석체크를 시작합니다! 첫 출석체크를 축하드립니다\n첫 출석체크 기념 5만원을 지급합니다")
                    dirseki.update({send:1}) # 출첵일 초기화

                    if money == None: #없다면 초기화
                        dirmoney.update({send:100000.0})
                    else:
                        money = money[send]
                        dirmoney.update({send:money + 50000})
                else:
                    seki = seki[send]
                    dirseki.update({send:seki + 1}) #출첵일 계산 후 업데이트

                    if (seki + 1) % 10 == 0: # 출첵일이 10의 배수일시
                        await message.channel.send(message.author.mention + "님 출석체크 완료 지금까지" + str(seki + 1) +"일 출석하셨습니다\n출석 보상 20만원을 지급합니다")

                        if money == None: #돈 정보가 없다면
                            dirmoney.update({send:250000.0}) #기본지금액 + 상금
                        else:
                            money = money[send]
                            dirmoney.update({send:money + 200000}) # 원래돈 + 상금
                    else:
                        await message.channel.send(message.author.mention + "님 출석체크 완료 지금까지 " + str(seki + 1) +"일 출석하셨습니다")

                dirtime.update({send:str(datetime.datetime.now()).split(" ")[0]}) # 출첵 정보일 저장
            else: # 저장된 출첵일이 금일과 같다면
                await message.channel.send(message.author.mention + "님 오늘은 이미 출석하셨습니다")

        if message.content == "!적금가입 00":#적금 00상품 가입
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 송출자 ID 저장

            dirmoney = db.reference('money/' + send) #돈확인
            money = dirmoney.get()

            if money == None: # 정보가 없을시 초기화
                dirmoney.update({send:50000.0})
            else:
                money = money[send]

            if money >= 50000: # 돈이 충분히 있을시에
                dirmukye00 = db.reference('mukye00/' + send)
                mukye00 = dirmukye00.get()

                if mukye00 != None: # 이미 가입되어있따면
                    await message.channel.send(message.author.mention + "님 적금 상품 00번에 이미 가입되어있습니다") 
                    return

                dirmukye00.update({send:str(datetime.datetime.now() + datetime.timedelta(days=3)).split(" ")[0]}) # 만기일 등록

                dirmukye00in = db.reference('mukye00in/' + send) # 납부 정보 등록
                dirmukye00in.update({send:str(datetime.datetime.now()).split(" ")[0]})

                dirmukye00cou = db.reference('mukye00cou/' + send) # 납부 획수 등록
                dirmukye00cou.update({send:1})

                money = money - 50000 # 돈 정상 계산 후 업데이트
                dirmoney.update({send:money})

                await message.channel.send(message.author.mention + "님 적금 상품 00번 사흘 적금에 정상 가입하였습니다\n납부 방법은 '!적금납부 00' 입니다") 
            else: # 돈이 부족할 시
                await message.channel.send(message.author.mention + "님 소지금액이 부족하여 상품 구입이 불가합니다")
            
        if message.content == "!적금납부 00":#적금 00상품 납부
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] # 송출자 ID 확인

            dirmoney = db.reference('money/' + send) # 돈확인
            money = dirmoney.get()

            if money == None: #정보 없을 시 초기화
                dirmoney.update({send:50000.0})
            else:
                money = money[send]

            if money >= 50000: #돈이 충분하다면
                dirmukye00 = db.reference('mukye00/' + send)
                mukye00 = dirmukye00.get()

                if mukye00 == None: # 가입 정보가 없을 시 거부
                    await message.channel.send(message.author.mention + "님은 현재 적금 상품 00번에 가입되어있지 않습니다") 
                    return

                dirmukye00in = db.reference('mukye00in/' + send) #금일 납부 했는지 조회
                mukye00in = dirmukye00in.get()
                mukye00in = mukye00in[send]

                mukye00in = datetime.datetime.strptime(mukye00in, "%Y-%m-%d")
                now = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")

                if mukye00in < now: #납부 안했다면
                    dirmukye00in.update({send:str(datetime.datetime.now()).split(" ")[0]}) # 금일 납부 처리

                    money = money - 50000 #돈 정상 계산 후 업데이트
                    dirmoney.update({send:money})

                    dirmukye00cou = db.reference('mukye00cou/' + send) # 납부 횟수 조회 및 업데이트
                    mukye00cou = dirmukye00cou.get()
                    mukye00cou = mukye00cou[send]
                    dirmukye00cou.update({send:mukye00cou + 1})

                    await message.channel.send(message.author.mention + "님 적금 상품 00번 사흘 적금에 정상 납부되었습니다") 
                else: #납부를 이미 했다면
                    await message.channel.send(message.author.mention + "님 금일은 이미 납부되었습니다") 
            else:#돈이 부족할 시 거부
                await message.channel.send(message.author.mention + "님 소지금액이 부족하여 상품 구입이 불가합니다")

        if message.content == "!적금가입 01":#적금 01상품 가입 **적금가입 00과 코드 일치**
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
            else:
                money = money[send]

            if money >= 35000:
                dirmukye01 = db.reference('mukye01/' + send)
                mukye01 = dirmukye01.get()

                if mukye01 != None:
                    await message.channel.send(message.author.mention + "님 적금 상품 01번에 이미 가입되어있습니다") 
                    return

                dirmukye01.update({send:str(datetime.datetime.now() + datetime.timedelta(days=5)).split(" ")[0]})

                dirmukye01in = db.reference('mukye01in/' + send)
                dirmukye01in.update({send:str(datetime.datetime.now()).split(" ")[0]})

                dirmukye01cou = db.reference('mukye01cou/' + send)
                dirmukye01cou.update({send:1})

                money = money - 35000
                dirmoney.update({send:money})

                await message.channel.send(message.author.mention + "님 적금 상품 01번 닷새 적금에 정상 가입하였습니다\n납부 방법은 '!적금납부 01' 입니다") 
            else:
                await message.channel.send(message.author.mention + "님 소지금액이 부족하여 상품 구입이 불가합니다")
            
        if message.content == "!적금납부 01":#적금 01상품 납부 **적금납부 00과 코드 일치**
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1]

            dirmoney = db.reference('money/' + send)
            money = dirmoney.get()

            if money == None:
                dirmoney.update({send:50000.0})
            else:
                money = money[send]

            if money >= 35000:
                dirmukye01 = db.reference('mukye01/' + send)
                mukye01 = dirmukye01.get()

                if mukye01 == None:
                    await message.channel.send(message.author.mention + "님은 현재 적금 상품 01번에 가입되어있지 않습니다") 
                    return

                dirmukye01in = db.reference('mukye01in/' + send)
                mukye01in = dirmukye01in.get()
                mukye01in = mukye01in[send]

                mukye01in = datetime.datetime.strptime(mukye01in, "%Y-%m-%d")
                now = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")

                if mukye01in < now:
                    dirmukye01in.update({send:str(datetime.datetime.now()).split(" ")[0]})

                    money = money - 35000
                    dirmoney.update({send:money})

                    dirmukye01cou = db.reference('mukye01cou/' + send)
                    mukye01cou = dirmukye01cou.get()
                    mukye01cou = mukye01cou[send]
                    dirmukye01cou.update({send:mukye01cou + 1})

                    await message.channel.send(message.author.mention + "님 적금 상품 01번 사흘 적금에 정상 납부되었습니다") 
                else:
                    await message.channel.send(message.author.mention + "님 금일은 이미 납부되었습니다") 
            else:
                await message.channel.send(message.author.mention + "님 소지금액이 부족하여 상품 구입이 불가합니다")

        if message.content == "!주식":#주식 안내
            jusiclist = ["ju01","ju02","ju03"] #조회할 주식 초기화

            embed = discord.Embed(title="주식 현황" ,description="주식은 1만 ~ 10만까지 있습니다" , color=0x5CD1E5)
            for wordin in jusiclist:
                dirjusic = db.reference('ju/')
                jusic = dirjusic.get()
                jusic = jusic[wordin] #특정 주식 조회 및 값 저장

                embed.add_field(name="주식 번호 " + wordin[-2:], value= str(jusic) + "원", inline=False)

            embed.set_footer(text="주식 구입 방법 >> !주식구입 ju'주식번호' EX)!주식구입 ju01")
            await message.channel.send(embed=embed)

        if message.content.startswith("!주식구입"): #주식 구입하기
            send = str(message.author)
            send = send.split("#")
            send = send[0] + "*" + send[1] #구입 요청자 ID 확인

            dirmoney = db.reference('money/' + send) #돈확인
            money = dirmoney.get()

            if money == None: #정보가 없다면 초기화 후 저장
                dirmoney.update({send:50000.0})
            else:
                money = money[send]

            trs = message.content.split(" ") #구입하고자 하는 주식코드 확인
            trswhat = trs[1]

            dirjusic = db.reference('ju/') # 해당 주식 가격 조회
            jusic = dirjusic.get()
            jusic = jusic[trswhat]

            if money >= jusic: #돈이 충분하다면
                dirjusicin = db.reference(trswhat + '/' + send) # 해당 사용자 주식 정보 조회
                jusic = dirjusicin.get()

                if jusic == None: # 정보가 없다면 초기화
                    dirjusicin.update({send:0})
                    jusic = 0
                else:
                    jusic = jusic[send]

                dirjusicin.update({send:jusic + 1}) # 해당 사용자에게 해당 주식 1주 추가

                money = money - jusic #돈 정상 계산 후 업데이트
                dirmoney.update({send:money})

                await message.channel.send(message.author.mention + "님 주식 구입이 완료되었습니다")
            else:#돈이 부족할시 거부
                await message.channel.send(message.author.mention + "님 소지 금액이 부족합니다")
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")

client.run(token)