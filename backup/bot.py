import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import unicodedata
import json
import random
import os.path
from discord.utils import get
import glob
import datetime
import math
from PIL import Image
import time
from distutils.dir_util import copy_tree
import shutil
from discord.voice_client import VoiceClient
import urllib.request

client = discord.Client()

#discord bot tokken
token = "-----"
#Naver Open API application ID
client_id = "-----"
#Naver Open API application token
client_secret = "-----"

loto_bank = random.uniform(0, 999999) * random.uniform(0, 999999) * random.uniform(0, 999999) + 123456789
loto_bank = round(loto_bank)
loto_mal = True

listhelp = ["!help", "!translation", "!레벨", "!업데이트", "!지진", "!코로나", "!주사위",
    "!게임", "!bank 비밀번호", "!돈확인", "!돈받기", "!랭킹", "!세금", "!예적금", "!송금", "!게임정보", "!코드발급",
    "!이체", "!수령이체", "!예금", "!출금예금", "!통장확인", "!TRS", "!도박", "!홀짝", "!로토도박", "!경마", "!어만고치",
    "!상점", "!구입체다치즈", "!구입라면", "!구입묶음라면", "!구입우유","!인벤토리", "!먹이주기", "!게임리스트", "!게임등록", "!등록내역",
    "!이름등록", "!게임이름변경", "!게임삭제", "!고치샤워", "!먹이", "!날씨", "!봇보이스"]

verand = "V-3.1.0\n[명령어줄 2799줄, 파일 248개, 폴더 22개, 프로세스 16개]"

@client.event
async def on_ready():  #화면에 봇의 아이디, 닉네임 출력
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n시스템을 시작합니다" + 
        "\n==========================================")
    # 이 기능을 이용하여 봇의 상태를 출력
    mssg = discord.Game("!help|Made by Han_MangUl")
    await client.change_presence(status=discord.Status.online, activity=mssg)


async def background_join():
    await client.wait_until_ready()
    @client.event
    async def on_member_join(member):
        channel = client.get_channel(719907483069448223)
        await channel.send(member.author.mention + '님 어만사άλφα에 어서오세요!! \n' +
            '1. 대화 할 시 친하지 않은 상대방과 존대를 해오는 상대방에게는 꼭 존대로 응해주세요 \n' +
            '(초면에는 서로서로 한 발자국 거리두고 대화해 보아요) \n' +
            '2. 문제가 생길시 "벤"이 됩니다 \n'+
            '3. !게임정보 을 입력하여 명령어 확인 후 자신이 하는 게임에 닉네임을 등록해주세요! 서로 같이 게임하면서 친해질 수 있습니다 \n' +
            '4. 주변에 같이 이 디코방에서 즐길 사람있으면 언제든지 초대해주세요! 환영입니다!')

async def background_remove():
    await client.wait_until_ready()
    @client.event
    async def on_member_remove(member):
        channel = client.get_channel(719907483069448223)
        await channel.send(member.author.mention + ' 님이 서버에서 나가셨습니다.')

async def background_main():
    await client.wait_until_ready()
    # 봇이 새로운 메시지를 수신했을때 동작되는 코드
    @client.event
    async def on_message(message):
        # 답장할 채널은 메세지 받은 채널로 설정
        if message.author == client.user:
            return

        channel = message.channel
        print(message.content)

        if str(message.channel.id) == "751716285129424897": #봇방에 채팅 제한
            trsText = message.content.split(" ")
            trsText = trsText[0]
            TRF = trsText in listhelp
            if TRF == False:
                await message.delete()
                await message.channel.send("채팅은 채팅방에 입력하여주세요")
                return
        
        if str(message.channel.id) != "809826202088898570" and str(message.channel.id) != "751716285129424897" and str(message.channel.id) != "823395883088871434": #봇방이 아닌곳 채팅 제한
            trsText = message.content.split(" ")
            trsText = trsText[0]
            TRF = trsText in listhelp
            if TRF:
                if trsText == "!TRS":
                    if str(message.channel.id) != "821752050948767754":
                        await message.delete()
                        await message.channel.send("번역기는 전용 채팅방에 입력하여주세요")
                        return
                else:
                    await message.delete()
                    await message.channel.send("명령어는 봇방에 입력하여주세요")
                    return

        if message.content == "!help":
            embed = discord.Embed(title="명령어", description="", color=0x5CD1E5)
            embed.add_field(name="일반", value="!translation, !레벨, !업데이트, !지진, !코로나, !날씨", inline=False)
            embed.add_field(name="게임", value="!주사위, !게임, !랭킹", inline=False)
            embed.add_field(name="어만사 머니", value="!bank 비밀번호, !돈확인, !돈받기,  !세금, !예적금, !송금", inline=False)
            embed.add_field(name="어만고치", value="!어만고치, !상점, !인벤토리, !먹이, !고치샤워", inline=False)
            embed.add_field(name="게임&닉네임 등록 관리", value="!게임정보", inline=False)
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
            embed = discord.Embed(title="명령어", description="", color=0x5CD1E5)
            embed.add_field(name="!이체 '금액'", value="'금액'원을 이체 예약 합니다", inline=False)
            embed.add_field(name="!수령이체 '코드'", value="'금액'원을 예금 통장에서 출금합니다", inline=False)
            await message.channel.send(embed=embed)

        if message.content == "!예적금":
            embed = discord.Embed(title="명령어", description="", color=0x5CD1E5)
            embed.add_field(name="!예금 '금액'", value="'금액'원을 예금 통장에 입금합니다", inline=False)
            embed.add_field(name="!출금예금 '금액'", value="'금액'원을 예금 통장에서 출금합니다", inline=False)
            embed.add_field(name="!통장확인", value="통장 잔고를 확인합니다\n예금 이율은 시간당 0.3%이며 시스템이 업데이트 될때도 지급됩니다", inline=False)
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
            embed = discord.Embed(title="등록 방법", description="", color=0x5CD1E5)
            embed.add_field(name="!게임리스트", value="현재 게임 리스트를 확인합니다", inline=False)
            embed.add_field(name="!게임등록 게임명", value="'게임명'을 게임 리스트에 새로 등록합니다\n[특수문자는 제외해주세요 <,: 기타 등등]", inline=False)
            embed.add_field(name="!등록내역 게임명", value="'게임명'에 등록되어있는 유저를 확인합니다", inline=False)
            embed.add_field(name="!이름등록 게임명 닉네임", value="'게임명'에 '닉네임'을 등록합니다\n<닉네임은 디코 닉네임으로 입력하여주세요>", inline=False)
            embed.add_field(name="!게임이름변경 기존게임명 바꿀게임명", value="'기존게임명'을 '바꿀게임명'으로 변경합니다", inline=False)
            embed.add_field(name="!게임삭제 게임명", value="'게임명'과 관련된 모든 정보를 전부 삭제합니다", inline=False)
            await message.channel.send(embed=embed)

        if message.content == "!게임": #게임안내
            embed = discord.Embed(title="게임 명령어", description="", color=0x5CD1E5)
            embed.add_field(name="!도박", value="일반 도박\n보유 금액이 8만 5천원 이상 혹은 3천원이하 일때는 불가능합니다", inline=False)
            embed.add_field(name="!홀짝 홀OR짝", value="홀짝 게임 5천원 이상일때만 가능\n성공시 자신의 돈의 1.5배 지급! 실패시 벌금! 자신의 돈의 1.5 ~ 1.75배 손실", inline=False)
            embed.add_field(name="!로토도박 금액 배팅", value="배팅을 최대 10까지 할 수 있는 상세 도박\n확률은 일반 도박보다 더 낮습니다", inline=False)
            embed.add_field(name="!경마 번호 매수", value="번호는 1~5번 이내로 지정해주세요 \n매수는 1매당 1천 5백원이며 최대 10매까지 구입이 가능합니다", inline=False)
            await message.channel.send( embed=embed)

        if message.content.startswith(""): #개인 레벨 경험치 부여
                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/level/"
                send = targerdir + str(message.author)

                if os.path.isfile(send + ".txt") == False:
                    f = open(send + ".txt", 'w')
                    f.write("1")
                    f.close()

                    f = open(send + "level.txt", 'w')
                    f.write("1")
                    f.close()

                    role = discord.utils.get(message.guild.roles, name="한걸음<~9>")
                    await message.author.add_roles(role)
                    await message.channel.send(message.author.mention + " 님에게 한걸음<~9>을/를 부여하였습니다")

                fr = open(send + ".txt")
                Sin = fr.read()
                fr.close()

                Sin = float(Sin)
                Sin = int(Sin)

                intstr = str(message.content)
                intstr = len(intstr)
                ranin = random.uniform(1.0, 1.5)
                ranin = round(ranin, 2)

                ran = ranin * intstr / 2
                ran = math.ceil(ran)

                if ran > 50:
                    ran = 50

                plus = Sin + ran

                f = open(send + ".txt", 'w')
                f.write(str(plus))
                f.close()

                if plus > 1000:
                    fr = open(send + ".txt")
                    Sin = fr.read()
                    fr.close()

                    Sin = float(Sin)
                    Sin = int(Sin)

                    plus = Sin - 1000

                    f = open(send + ".txt", 'w')
                    f.write(str(plus))
                    f.close()

                    #레벨 상승
                    fr = open(send + "level.txt")
                    Sin = fr.read()
                    fr.close()

                    Sin = float(Sin)
                    Sin = int(Sin)

                    plus = Sin + 1
                    await message.channel.send(message.author.mention + "님의 레벨이 " + str(plus) +" 으로/로 상승하였습니다")

                    f = open(send + "level.txt", 'w')
                    f.write(str(plus))
                    f.close()

                    if plus == 10:
                        role = discord.utils.get(message.guild.roles, name="입주자<~19>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 입주자<~19>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="한걸음<~9>")
                        await message.author.remove_roles(role)

                    if plus == 20:
                        role = discord.utils.get(message.guild.roles, name="설립자<~29>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 설립자<~29>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="입주자<~19>")
                        await message.author.remove_roles(role)

                    if plus == 30:
                        role = discord.utils.get(message.guild.roles, name="제작자<~39>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 제작자<~39>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="설립자<~29>")
                        await message.author.remove_roles(role)

                    if plus == 40:
                        role = discord.utils.get(message.guild.roles, name="고인물<~49>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 고인물<~49>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="제작자<~39>")
                        await message.author.remove_roles(role)

                    if plus == 50:
                        role = discord.utils.get(message.guild.roles, name="화석<~59>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 화석<~59>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="고인물<~49>")
                        await message.author.remove_roles(role)

                    if plus == 60:
                        role = discord.utils.get(message.guild.roles, name="석유<~69>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 석유<~69>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="화석<~59>")
                        await message.author.remove_roles(role)
                        
                    if plus == 70:
                        role = discord.utils.get(message.guild.roles, name="구름<~79>")
                        await message.author.add_roles(role)
                        await message.channel.send(message.author.mention + "님에게 구름<~79>을/를 부여하였습니다")
                        role = discord.utils.get(message.guild.roles, name="석유<~69>")
                        await message.author.remove_roles(role)

        if message.content == "!주사위": # 주사위
            x = random.randint(1, 6)
            await message.channel.send(message.author.mention + "님의 주사위 수는 : " + str(x) + " 입니다.")

        if message.content == "!레벨": #개인 레벨 안내
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/level/"
            send = targerdir + str(message.author)
            msg = await message.channel.send("경험치는 채팅 길이에 따라 부여되며 1회 최대 50EXP까지 얻을 수 있습니다.")

            fr = open(send + ".txt")
            Sin = fr.read()
            fr.close()

            fr = open(send + "level.txt")
            Sin2 = fr.read()
            fr.close()

            await msg.edit(content=message.author.mention + " 님은 현재 총 " + Sin + "exp 가 있으며 레벨은 " + Sin2 + "입니다")

        if message.content == "!도박": #도박
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            if os.path.isfile(send + "alltime.txt") == False:
                await message.channel.send("시간 정보가 없어 새로 등록합니다")
                f = open(send + "alltime.txt", 'w')
                settime = datetime.datetime.now()
                f.write(str(settime))
                f.close()

            settime = datetime.datetime.now()

            fr = open(send + "alltime.txt")
            intime = fr.read()
            fr.close()

            intime = datetime.datetime.strptime(intime, "%Y-%m-%d %H:%M:%S.%f")

            if intime < settime:
                msg = await message.channel.send("도박은 1회당 1 ~ 5천원을 랜덤으로 걸고 -3.5 ~ 5배율 배팅으로 합니다 \n" + "도박을 시작합니다.")

                fr = open(send + "money.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)
                mey = round(mey, 3)

                if mey < 3000.00:
                    await msg.edit(content="돈이 충분하지 않습니다")
                    return
                if mey > 85000.00:
                    await msg.edit(content="돈이 너무 많습니다 다른 도박을 이용해주세요")
                    return
                
                f = open(send + "alltime.txt", 'w')
                settime = datetime.datetime.now() + datetime.timedelta(seconds=1)
                f.write(str(settime))
                f.close()

                be = random.uniform(100.00, 500.00) * 10
                ting = random.uniform(-3.50, 5.00)
                
                be = round(be, 3)
                ting = round(ting, 3)

                one = be * ting - be
                one = round(one, 3)
                
                if one >= 0.00:
                    await msg.edit(content=message.author.mention + "님은" + str(be) + "원을 배팅하게 되었습니다 \n" + "배율은 " + str(ting) + "배 입니다 \n" + "총 " + str(one) + "원을 이득을 봤습니다")
                else:
                    if ting != 1.00:
                        one = one * -1
                        await msg.edit(content=message.author.mention + "님은" + str(be) + "원을 배팅하게 되었습니다 \n" + "배율은 " + str(ting) + "배 입니다 \n" + "총 " + str(one) + "원을 잃었습니다")
                        one = one * -1
                    else:
                        one = 0.00
                        await msg.edit(content=message.author.mention + "님은" + str(be) + "원을 배팅하게 되었습니다 \n" + "배율은 " + str(ting) + "배 입니다 \n" + "원금을 회수하였습니다\n" +
                            "엄청난 확률로 원금 회수를 하셨군요! 321만 4321.987원을 추가 지급해드릴게요")
                        one = 3214321.987


                mey = round(mey + one, 3)

                if mey < 0.00:
                    roto = random.randint(1, 100)
                    if roto == 1:
                        await message.channel.send(message.author.mention + "님!" + " 스몰 로또 당첨! 8만원이 입금됩니다")
                        f = open(send + "money.txt", 'w')
                        f.write(str(80000.00))
                        f.close()
                    else:
                        await message.channel.send(message.author.mention + "님의 소지금이 전부 사용되었습니다")
                        f = open(send + "money.txt", 'w')
                        f.write(str(0.00))
                        f.close()
                else:
                    f = open(send + "money.txt", 'w')
                    f.write(str(mey))
                    f.close()
            else:
                await message.channel.send(message.author.mention + "님 도박가능 시간이 아직 되지 않았습니다")

        if message.content == "!돈확인": #돈 확인
            msg = await message.channel.send("돈을 확인합니다")
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            await msg.edit(content=message.author.mention + "님이" + " 현재 보유 중인 돈은 : " + str(mey) + "원입니다")

        if message.content.startswith("!홀짝"): # 홀짝 게임
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await msg.edit(content="시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            msg = await message.channel.send("성공시 자신의 돈의 1.5배 지급! 실패시 벌금! 자신의 돈의 1.5 ~ 1.75배 손실")

            trsText = message.content.split(" ")

            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            auto = random.randint(1, 2)
            bul = random.uniform(mey/2, mey/2 + mey/4)
            bul = round(bul, 3)

            if mey < 5000.00:
                await msg.edit(content="돈이 충분하지 않습니다")
                return

            if trsText[1] == "홀":
                if auto == 1:
                    await msg.edit(content=message.author.mention + " 나온 수는 홀! 성공! " + str(round(mey / 2, 3)) + "원이 지급됩니다")
                    f = open(send + "money.txt", 'w')
                    inmey = round(mey + mey / 2, 3)
                    f.write(str(inmey))
                    f.close()
                else:

                    await msg.edit(content=message.author.mention + " 나온 수는 짝! 실패! (っ °Д °;)っ 벌금은 " + str(bul) + "원 입니다")

                    if mey - bul < 0.00:
                        roto = random.randint(1, 100)
                        if roto == 1:
                            await msg.edit(content=message.author.mention + "님!" + " 스몰 로또 당첨! 8만원이 입금됩니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(80000.00))
                            f.close()
                        else:
                            await msg.edit(content=message.author.mention + "님의 소지금이 전부 사용되었습니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(0.00))
                            f.close()
                    else:
                        f = open(send + "money.txt", 'w')
                        inmey = round(mey - bul, 3)
                        f.write(str(inmey))
                        f.close()
            elif trsText[1] == "짝":
                if auto == 1:
                    await msg.edit(content=message.author.mention + " 나온 수는 홀! 실패! (っ °Д °;)っ 벌금은 " + str(bul) + "원 입니다")
                    if mey - bul < 0.00:
                        roto = random.randint(1, 100)
                        if roto == 1:
                            await message.channel.send(message.author.mention + "님!" + " 스몰 로또 당첨! 8만원이 입금됩니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(80000.00))
                            f.close()
                        else:
                            await message.channel.send(message.author.mention + "님의 소지금이 전부 사용되었습니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(0.00))
                            f.close()
                    else:
                        f = open(send + "money.txt", 'w')
                        inmey = round(mey - bul)
                        f.write(str(inmey))
                        f.close()
                else:
                    await msg.edit(content=message.author.mention + " 나온 수는 짝! 성공! " + str(round(mey / 2, 3)) + "원이 지급됩니다")
                    f = open(send + "money.txt", 'w')
                    inmey = round(mey + mey / 2, 3)
                    f.write(str(inmey))
                    f.close()
            else:
                await msg.edit(content="홀과 짝중 하나만 입력하여 주세요")

        if message.content.startswith("!로토도박"): #도박
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await msg.edit(content="시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            msg = await message.channel.send("로토 도박은 순서대로 배팅 배율로 적용됩니다 \n" + "도박을 시작합니다.")

            trsText = message.content.split(" ")

            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            be = float(trsText[1])
            ting = int(trsText[2])

            if mey >= be * 7:
                if ting > 0 and ting <= 10:
                    one = 100 / ting / 2
                    one = round(one, 3)
                    be = round(be, 3)

                    ranone = random.randint(1, 100)

                    won = be * ting - be
                    won = round(won, 3)
                    
                    if one > ranone:
                        await msg.edit(content=message.author.mention + "님은" + str(be) + "원을 배팅 하였습니다 \n" + "배율은 " + str(ting) + "배 입니다 도박 성공!! \n" + "총 " + str(won) + "원 이득을 봤습니다")
                    else:
                        won = won + be + be
                        await msg.edit(content=message.author.mention + "님은" + str(be) + "원을 배팅 하였습니다 \n" "배율은 " + str(ting) + "배 입니다 도박 실패!! \n" + "총 " + str(won) + "원을 잃었습니다")
                        ting = ting * -1
                        won = won + be

                    mey = mey + be * ting - be
                    mey = round(mey, 3)

                    if mey < 0.00:
                        roto = random.randint(1, 100)
                        if roto == 1:
                            await message.channel.send(message.author.mention + "스몰 로또 당첨! 5만원이 입금됩니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(50000.00))
                            f.close()
                        else:
                            await message.channel.send(message.author.mention + "님의 소지금이 전부 사용되었습니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(0.00))
                            f.close()
                    else:
                        f = open(send + "money.txt", 'w')
                        f.write(str(mey))
                        f.close()
                else:
                    await msg.edit(content="배팅율을 다시 입력하여주세요")
            else:
                await msg.edit(content="벌금을 낼 수 있는 금액보다 너무 큰 금액입니다. 배팅 금액을 다시 입력해주세요\n신용 금액은 평균 금액인 배팅액 * 7 원으로 측정됩니다")


        if message.content == "!게임리스트": #게임 리스트 확인
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/game"
            files = os.listdir(targerdir)

            gamelist = sorted(files)

            namelist = ""
            lenCC, chk = 1, 0
            lenchk = len(gamelist)

            for word in gamelist:
                chk += 1
                lenCC += 1

                if lenCC == lenchk + 1:
                    namelist += word.split(".txt")[0]
                else:
                    namelist += word.split(".txt")[0] + " , "

                    if chk == 3:
                        namelist += "\n"
                        chk = 0


            embed = discord.Embed(title="게임리스트", description=namelist, color=0x5CD1E5)
            
            await message.channel.send(embed=embed)

        if message.content.startswith("!게임등록"): #게임 리스트 추가
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/game/"

            trsText = message.content.split(" ")
            trsText = trsText[1:]
            combineword = ""
            for word in trsText:
                combineword += str(word)
            
            if os.path.isfile(targerdir + combineword + ".txt"):
                await message.channel.send(combineword + " 은/는 이미 등록되어있는 게임입니다")
            else:
                f = open(targerdir + combineword + ".txt", 'w')
                f.close()

                await message.channel.send(combineword + " 을/를 정상 등록하였습니다")

        if message.content.startswith("!이름등록"): #게임에 사용자 등록
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/game/"

            trsText = message.content.split(" ")

            gamename = str(trsText[1])
            usernamein = trsText[2:]

            username = ""

            for nameinput in usernamein:
                username += nameinput + " "

            username = username[0:-1]

            if os.path.isfile(targerdir + gamename + ".txt"):
                f = open(targerdir + gamename + ".txt", 'r')
                namechlist = f.read()
                f.close()

                namechlist = namechlist.split("&")

                nameis = True

                for namech in namechlist: 
                    if namech == username:
                        nameis = False
                
                if nameis:
                    f = open(targerdir + gamename + ".txt", 'r')
                    namelist = f.read()
                    f.close()

                    f = open(targerdir + gamename + ".txt", 'w')
                    f.write(namelist + username + "&")
                    f.close()

                    await message.channel.send(username + "님을/를 " + gamename + " 게임에 정상 등록하였습니다")
                else:
                    await message.channel.send(username + "님은/는 " + gamename + " 게임에 이미 등록되어있습니다")
            else:
                await message.channel.send(gamename + " 은/는 게임리스트에 존재하지 않습니다 새로 등록하여주세요")

        if message.content.startswith("!등록내역"): #게임 리스트 확인
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/game/"

            trsText = message.content.split(" ")
            trsText = trsText[1:]
            combineword = ""
            for word in trsText:
                combineword += str(word)

            if os.path.isfile(targerdir + combineword + ".txt"):
            
                f = open(targerdir + combineword + ".txt", 'r')
                gamelist = f.read()
                f.close()

                gamelist = gamelist.split("&")

                gamelist = gamelist[0:-1]
                gamelist = sorted(gamelist)
                
                listword = ""

                lenchk = len(gamelist)
                lenCC = 1
                chk = 0
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
                    
                
                embed = discord.Embed(title=combineword + " 유저 리스트", description=listword, color=0x5CD1E5)
                await message.channel.send(embed=embed)

            else:
                await message.channel.send(combineword + " 은/는 게임리스트에 존재하지 않습니다 새로 등록하여주세요")

        
        if message.content.startswith("!게임삭제"): #게임 및 등록 정보 삭제
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/game/"

            trsText = message.content.split(" ")
            trsText = trsText[1:]
            combineword = ""
            for word in trsText:
                combineword += str(word)

            if os.path.isfile(targerdir + combineword + ".txt"):
                os.remove(targerdir + combineword + ".txt")
                await message.channel.send(combineword + " 게임과 등록 정보를 폐기하였습니다")
            else:
                await message.channel.send(combineword + " 은/는 게임리스트에 존재하지 않습니다")

        if message.content.startswith("!게임이름변경"): #게임 이름 변경
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/game/"

            trsText = message.content.split(" ")

            gamename = str(trsText[1])
            combineword = trsText[2:]

            regamename = ""
            for word in combineword:
                regamename += str(word)
                print(regamename)

            if os.path.isfile(targerdir + gamename + ".txt"):
                os.rename(targerdir + gamename + ".txt", targerdir + regamename + ".txt")
                await message.channel.send(gamename + " 게임을 " + regamename + "으로 게임명이 변경되었습니다")
            else:
                await message.channel.send(gamename + " 은/는 게임리스트에 존재하지 않습니다")

        if message.content == "!랭킹":#랭킹 안내
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            files = os.listdir(targerdir)

            condition = targerdir + "*money.txt"
            csvfiles = glob.glob(condition)
            

            cou = 0
            trs = []

            for word in csvfiles:
                trs.insert(cou, word)
                cou += 1 

            ussc = []
            usname = []
            cou = 0
            for sco in trs:
                f = open(sco, 'r')
                scin = f.read()
                f.close()
                ussc.insert(cou, float(scin))

                trsText = sco.split("#")
                trsText = trsText[0]
                usname.insert(cou, str(trsText[40:]))

                cou += 1
            

            for size in reversed(range(len(ussc))):
                max_i = 0
                for i in range(0, 1+size):
                    if ussc[i] < ussc[max_i]:
                        max_i = i
                ussc[max_i], ussc[size] = ussc[size], ussc[max_i]
                usname[max_i], usname[size] = usname[size], usname[max_i]
            

            embed = discord.Embed(title="랭킹", description="랭킹은 통장 제외 소지 금액만 인정됩니다", color=0x5CD1E5)
            for scor in range(0, len(ussc)):
                embed.add_field(name=str(scor + 1) + "등 ID : " + usname[scor], value=str(ussc[scor]) + "원", inline=True)
                if scor == 11:
                    break

            await message.channel.send( embed=embed)

        if message.content.startswith("!bank"): #비밀 대출
            global loto_bank
            loto_bank = "!bank " + str(loto_bank)   

            if message.content == loto_bank:
                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
                send = targerdir + str(message.author)

                fr = open(send + "money.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)
                mey = round(mey, 3)

                f = open(send + "money.txt", 'w')
                inbank = random.uniform(5000.00, 15000.00) * 10
                inbank = round(inbank, 3)
                f.write(str(mey + inbank))
                f.close()

                loto_bank = random.uniform(0, 999999) * random.uniform(0, 999999) * random.uniform(0, 999999) + 123456789
                loto_bank = round(loto_bank, 0)
                await message.channel.send("5만원 ~ 15만원 중 랜덤으로 입금됩니다 \n" +message.author.mention + "님에게 총 " + str (inbank) + "원이 입급되었습니다")
            else:
                await message.channel.send("비밀코드가 틀렸습니다 다시 입력하여주세요")
            
        if message.content == "!코드발급":#비밀코드를 어드민만 볼 수 있게 생성
            loto_bank = random.uniform(0, 999999) * random.uniform(0, 999999) * random.uniform(0, 999999) + 123456789
            loto_bank = round(loto_bank, 0)
            print(loto_bank)

        if message.content == "!돈받기":#돈지급
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
            sendye = targerdir + str(message.author)
            msg = await message.channel.send("지원금을 받습니다 지원금은 소유금 및 보유금의 합이 3천원 이하일때 가능\n[15분마다 1번씩 가능]")

            if os.path.isfile(send + "money.txt") == False:
                await msg.edit(content="시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            if os.path.isfile(sendye + "ye.txt") == False:
                await message.channel.send("소지하신 통장이 없어 예금통장을 새로 만들었습니다")
                f = open(sendye + "ye.txt", 'w')
                f.write("0.00")
                f.close()

            if os.path.isfile(send + "time.txt") == False:
                await msg.edit(content="시간 정보가 없어 새로 등록합니다")
                f = open(send + "time.txt", 'w')
                settime = datetime.datetime.now()
                f.write(str(settime))
                f.close()

            settime = datetime.datetime.now()
            fr = open(send + "time.txt")
            intime = fr.read()
            fr.close()

            intime = datetime.datetime.strptime(intime, "%Y-%m-%d %H:%M:%S.%f")

            if intime < settime:
                fr = open(send + "money.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)
                mey = round(mey, 3)

                fr = open(sendye + "ye.txt")
                meyye = fr.read()
                fr.close()

                meyye = float(meyye)
                meyye = round(meyye, 3)

                mey = meyye + mey

                if mey < 3000.00:
                    give = random.uniform(100.00, 500.00) * 100
                    give = round(give, 3)
                    await msg.edit(content=message.author.mention + "님에게" + " 지원금 : " + str(give) + "원을 지급합니다")
                    f = open(send + "money.txt", 'w')
                    f.write(str(give))
                    f.close()

                    f = open(send + "time.txt", 'w')
                    settime = datetime.datetime.now() + datetime.timedelta(minutes=15)
                    f.write(str(settime))
                    f.close()
                else:
                    await msg.edit(content=message.author.mention + "님은 이미 충분한 돈을 가지고 있습니다")
            else:
                await msg.edit(content=message.author.mention + "님 지원금 수령 가능 시간이 되지 않았습니다")
            
        if message.content.startswith("!TRS"): #번역기능
            baseurl = "https://openapi.naver.com/v1/papago/n2mt"
            # 띄어쓰기 : split처리후 [2:]을 for문으로 붙인다.
            trsText = message.content.split(" ")

            lengmsg = trsText[1]
            mainText = trsText[2:]

            try:
                if len(mainText) == 0:
                    await message.channel.send("단어 혹은 문장이 입력되지 않았어요. 다시한번 확인해주세요.")
                else:
                    await message.delete()
                    combineword = ""
                    for word in mainText:
                        combineword += " " + word
                    # if entered value is sentence, assemble again and strip blank at both side
                    savedCombineword = combineword.strip()
                    combineword = quote(savedCombineword)
                    # Make Query String.

                    lengmsg = lengmsg.split("*")

                    leng1 = str(lengmsg[0])
                    leng2 = str(lengmsg[1])

                    #Simplified Chinese
                    dataParmas = "source=" + leng1 + "&target=" + leng2 + "&text=" + combineword
                    # Make a Request Instance
                    request = Request(baseurl)
                    # add header to packet
                    request.add_header("X-Naver-Client-Id", client_id)
                    request.add_header("X-Naver-Client-Secret", client_secret)
                    response = urlopen(request, data=dataParmas.encode("utf-8"))

                    responsedCode = response.getcode()
                    if (responsedCode == 200):
                        response_body = response.read()
                        # response_body -> byte string : decode to utf-8
                        api_callResult = response_body.decode('utf-8')
                        # JSON data will be printed as string type. So need to make it back to type JSON(like dictionary)
                        api_callResult = json.loads(api_callResult)
                        # Final Result
                        translatedText = api_callResult['message']['result']["translatedText"]
                        embed = discord.Embed(title="Translate", description= message.author.mention, color=0x5CD1E5)
                        embed.add_field(name=leng1, value=savedCombineword, inline=False)
                        embed.add_field(name="Translated "+ leng2, value=translatedText, inline=False)
                        embed.set_footer(text="API provided by Naver Open API")
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("Error Code : " + responsedCode)
            except HTTPError as e:
                await message.channel.send("번역 실패, 접속 오류 발생") 

        if message.content.startswith("!공지"): #공지 변경
            send = str(message.author)
            if send == "Han_MangUl#3856":
                await message.channel.send("공지가 정상적으로 수정되었습니다")
                
                maincut = message.content
                maincut = maincut.split("!공지")

                maincut = maincut[1]

                f = open("main.txt", 'w', encoding='utf-16')
                f.write(str(maincut))
                f.close()
            else:
                await message.channel.send("관리자가 아닙니다")

        if message.content == "!지진": #최근 지진 정보 접속 및 안내
            await message.channel.send("사이트에 접속중입니다")

            html = urlopen("https://www.weather.go.kr/weather/earthquake_volcano/domesticlist.jsp")
            bsObject = BeautifulSoup(html, "html.parser")

            embed = discord.Embed(title="최근 지진 정보", description="", color=0x5CD1E5)

            einlist = ["발생시각", "규모", "깊이", "최대진도" ,"위치"]
            listin = 2
            TFL = False

            for insite in einlist:
                einput = str(bsObject.select("#excel_body > tbody > tr:nth-child(1) > td:nth-child( " + str(listin) + ")"))

                if listin < 8:
                    einput = einput[5:-6]
                else:
                    einput = einput[24:-6]

                embed.add_field(name=insite, value=einput, inline=TFL)

                listin += 1
                TFL = True
                if listin == 6:
                    listin = 8
                    TFL = False
            
            await message.channel.send(embed=embed) 

        if message.content.startswith("!경마"): # 경마 게임
            global loto_mal
            if loto_mal:
                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
                send = targerdir + str(message.author)

                if os.path.isfile(send + "money.txt") == False:
                    await msg.edit(content="시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                    f = open(send + "money.txt", 'w')
                    f.write("50000.00")
                    f.close()

                msg = await message.channel.send("경마를 시작합니다!")
                trsText = message.content.split(" ")

                bunho = int(float(trsText[1]))
                mesu = int(float(trsText[2]))

                loto_mal = False

                if bunho < 1 or bunho > 5:
                    await msg.edit(content="경마말 번호를 다시 선택하여주세요")
                    loto_mal = True
                    return
                if mesu < 1 or bunho > 10:
                    await msg.edit(content="매수량을 다시 입력하여주세요")
                    loto_mal = True
                    return

                fr = open(send + "money.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)
                mey = round(mey, 3)

                if mey < mesu * 1500.00:
                    await msg.edit(content="보유금이 부족합니다")
                    loto_mal = True
                    return
                
                cout = [0, 0, 0, 0, 0]
                mamal = ["", "", "", "", ""]

                while cout[0] < 9 and cout[1] < 9 and cout[2] < 9 and cout[3] < 9 and cout[4] < 9:
                    mamal[0] = ""
                    mamal[1] = ""
                    mamal[2] = ""
                    mamal[3] = ""
                    mamal[4] = ""

                    for i in range(0, 5):
                        for j in range(0, 10):
                            if cout[i] == j:
                                mamal[i] += "🐴"
                            else:
                                mamal[i] += "🎞"

                    await msg.edit(content="경마 시작!!\n" + mamal[0] + "\n"+ mamal[1] + "\n"+ mamal[2] + "\n"+ mamal[3] + "\n"+ mamal[4] + "\n")

                    ranmal = random.randint(0, 4)
                    event = random.randint(1, 10)

                    if event < 5:
                        cout[ranmal] += 2
                    else:
                        cout[ranmal] += 1

                win = 0
                if cout[0] > 9:
                    win = 1
                    mamal[0] = ""
                    for j in range(0, 9):
                        mamal[0] += "🎞"
                    mamal[0] += "🐴"
                elif cout[1] > 9:
                    mamal[1] = ""
                    win = 2
                    for j in range(0, 9):
                        mamal[1] += "🎞"
                    mamal[1] += "🐴"
                elif cout[2] > 9:
                    mamal[2] = ""
                    win = 3
                    for j in range(0, 9):
                        mamal[2] += "🎞"
                    mamal[2] += "🐴"
                elif cout[3] > 9:
                    mamal[3] = ""
                    win = 4
                    for j in range(0, 9):
                        mamal[3] += "🎞"
                    mamal[3] += "🐴"
                else:
                    mamal[4] = ""
                    win = 5
                    for j in range(0, 9):
                        mamal[4] += "🎞"
                    mamal[4] += "🐴"

                val = "경마 결과 발표\n" + mamal[0] + "\n"+ mamal[1] + "\n"+ mamal[2] + "\n"+ mamal[3] + "\n"+ mamal[4] + "\n"
                val += str(win) + "번 말 승리!\n"
                await msg.edit(content=val)

                if win == bunho:
                    await msg.edit(content=val + "맞췄습니다! 원금과 " + str(mesu) + " * 1050.75원이 입금됩니다")
                    f = open(send + "money.txt", 'w')
                    inputme = round(mey + (mesu * 1050.75), 3)
                    f.write(str(inputme))
                    f.close()
                else:
                    await msg.edit(content=val + "아쉽네요 총 " + str(mesu) + " * 3250.68원을 잃습니다")

                    if mey - mesu * 3500.00 < 0.00:
                        roto = random.randint(1, 100)
                        if roto == 1:
                            await msg.edit(content=message.author.mention + "님!" + " 파산 로또 당첨! 8만원이 입금됩니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(80000.00))
                            f.close()
                        else:
                            await msg.edit(content=message.author.mention + "님의" + "보유금이 전부 사용되었습니다")
                            f = open(send + "money.txt", 'w')
                            f.write(str(0.00))
                            f.close()
                    else:
                        f = open(send + "money.txt", 'w')
                        inputme = round(mey - (mesu * 3250.68), 3)
                        f.write(str(inputme))
                        f.close()

                loto_mal = True
            else:
                await message.channel.send("이미 경마가 진행중입니다")

        if message.content == "!세금": #세금 안내
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/se/"
            send = targerdir + str(message.author) + "money.txt"

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/lastse/"
            sendlast = targerdir + str(message.author) + "money.txt"
            
            if os.path.isfile(send):
                f = open(send, 'r')
                mey = f.read()
                f.close()

                mey = float(mey)
                mey = round(mey, 3)

                f = open(sendlast, 'r')
                mey2 = f.read()
                f.close()

                mey2 = float(mey2)
                me2y = round(mey2, 3)

                await message.channel.send("[세금 기준]\n10만원 이하 7.5% 20만원 이하 15% 30만원 이하 30% 40만원 이하 45% 50만원 이하 55% 그외 70%\n세금은 00시, 12시에 납부됩니다\n내신 세금의 총합은 : " + str(mey) + "원입니다\n제일 최근에 낸 세금액은 " + str(mey2) + " 원입니다")
            else:
                await message.channel.send("세금을 내신적이 없습니다")

        if message.content.startswith("!예금"): #예금 입금 시스템
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
            sendye = targerdir + str(message.author)

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(sendye + "ye.txt") == False:
                await message.channel.send("소지하신 통장이 없어 예금통장을 새로 만들었습니다")
                f = open(sendye + "ye.txt", 'w')
                f.write("0.00")
                f.close()

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()
                
            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            trsText = message.content.split(" ")
            yein = float(trsText[1])
            yein = round(yein, 3)

            if mey >= yein:
                mey = mey - yein
                mey = round(mey, 3)

                f = open(send + "money.txt", 'w')
                f.write(str(mey))
                f.close()

                fr = open(sendye + "ye.txt")
                meyye = fr.read()
                fr.close()

                meyye = float(meyye)
                meyye = meyye + yein
                meyye = round(meyye, 3)

                f = open(sendye + "ye.txt", 'w')
                f.write(str(meyye))
                f.close()

                await message.channel.send("예금 통장에 " + str(yein) + "원을 입금하였습니다")
            else:
                await message.channel.send("소지금 보다 많습니다 다시 입력하여주세요")
        
        if message.content.startswith("!출금예금"): #예금을 출금합니다
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            sendye = targerdir + str(message.author)

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "ye.txt") == False:
                await message.channel.send("소지하신 통장이 없어 예금통장을 새로 만들었습니다")
                f = open(send + "ye.txt", 'w')
                f.write("0.00")
                f.close()

            if os.path.isfile(sendye + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(sendye + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            fr = open(send + "ye.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            trsText = message.content.split(" ")
            yein = float(trsText[1])
            yein = round(yein, 3)

            if mey >= yein:
                mey = mey - yein

                f = open(send + "ye.txt", 'w')
                f.write(str(mey))
                f.close()

                fr = open(sendye + "money.txt")
                meyye = fr.read()
                fr.close()

                meyye = float(meyye)
                meyye = meyye + yein
                meyye = round(meyye, 3)

                f = open(sendye + "money.txt", 'w')
                f.write(str(meyye))
                f.close()

                await message.channel.send("성공적으로 출금하였습니다")
            else:
                await message.channel.send("소지금 보다 많습니다 다시 입력하여주세요")

        if message.content == "!통장확인": #예금확인
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
            sendye = targerdir + str(message.author)

            if os.path.isfile(sendye + "ye.txt") == False:
                await message.channel.send("소지하신 통장이 없어 예금통장을 새로 만들었습니다")
                f = open(sendye + "ye.txt", 'w')
                f.write("0.00")
                f.close()

            fr = open(sendye + "ye.txt")
            meyye = fr.read()
            fr.close()

            meyye = float(meyye)
            meyye = round(meyye, 3)

            await message.channel.send(message.author.mention + "님이" + " 통장 잔액은 : " + str(meyye) + "원입니다")

        if message.content == "!코로나":#코로나 정보
            await message.channel.send("사이트에 접속중입니다")

            html = urlopen("http://ncov.mohw.go.kr/")
            bsObject = BeautifulSoup(html, "html.parser")

            embed = discord.Embed(title="코로나 정보", description="", color=0x5CD1E5)

            einput = str(bsObject.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(1) > span.before"))
            embed.add_field(name="질병관리청 공식 확진자 수 [전날 확진자 <AM 10시에 업데이트>]", value=einput[28:-9] + "명", inline=False)

            einput = str(bsObject.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(4) > span.before"))
            embed.add_field(name="질병관리청 공식 사망자 수 [전날 사망자 <AM 10시에 업데이트>]", value=einput[23:-9] + "명", inline=False)

            html = urlopen("https://v1.coronanow.kr/")
            bsObject = BeautifulSoup(html, "html.parser")

            einput = str(bsObject.select("#live_board2 > div:nth-child(1) > h5"))

            embed.add_field(name="실시간 코로나 확진자 수", value=einput[129:-6], inline=False)

            
            await message.channel.send(embed=embed)

        if message.content.startswith("!이체"): #돈을 이체합니다
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            msg = await message.channel.send("이체를 시작합니다")

            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            trsText = message.content.split(" ")
            trsText = float(trsText[1])

            if trsText <= mey:
                code = ""
                for cou in range(20):
                    rani = random.randint(0, 19)
                    if rani == 0:
                        rani = "a"
                    elif rani == 1:
                        rani = "b"
                    elif rani == 2:
                        rani = "c"
                    elif rani == 3:
                        rani = "d"
                    elif rani == 4:
                        rani = "e"
                    elif rani == 5:
                        rani = "f"
                    elif rani == 6:
                        rani = "g"
                    elif rani == 7:
                        rani = "h"
                    elif rani == 8:
                        rani = "i"
                    elif rani == 9:
                        rani = "j"
                    elif rani == 10:
                        rani = "k"
                    elif rani == 11:
                        rani = "l"
                    elif rani == 12:
                        rani = "m"
                    elif rani == 13:
                        rani = "n"
                    elif rani == 14:
                        rani = "o"
                    elif rani == 15:
                        rani = "p"
                    elif rani == 16:
                        rani = "q"
                    elif rani == 17:
                        rani = "r"
                    elif rani == 18:
                        rani = "s"
                    elif rani == 19:
                        rani = "t"
                    elif rani == 20:
                        rani = "u"
                    elif rani == 21:
                        rani = "v"
                    elif rani == 22:
                        rani = "w"
                    elif rani == 23:
                        rani = "x"
                    elif rani == 24:
                        rani = "y"
                    else:
                        rani = "z"
                    code += rani

                mey = mey - trsText
                mey = round(mey, 3)

                fr = open(send + "money.txt", 'w')
                fr.write(str(mey))
                fr.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/givemoney/"
                sendi = targerdir + code

                fr = open(sendi + ".txt", 'w')
                fr.write(str(trsText))
                fr.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/homi/"
                sendho = targerdir + str(message.author)

                fr = open(sendho + code + ".txt", 'w')
                fr.write("0")
                fr.close()

                await msg.edit(content="정상적으로 " +  code + " 코드로 " + str(trsText) +"원을 이체를 예약하였습니다")
            else:
                await msg.edit(content="이체 금액이 소지 금액보다 많습니다")

        if message.content.startswith("!수령이체"): #돈을 이체합니다
            trsText = message.content.split(" ")

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/givemoney/"
            sendi = targerdir + trsText[1]

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/homi/"
            sendho = targerdir

            if os.path.isfile(sendho + str(message.author) + trsText[1] + ".txt") == False:
                if os.path.isfile(sendi + ".txt"):
                    fr = open(sendi + ".txt")
                    meyini = fr.read()
                    fr.close()

                    os.remove(sendi + ".txt")

                    condition = sendho + "*" + trsText[1] + ".txt"
                    csvfiles = glob.glob(condition)

                    os.remove(csvfiles[0])

                    targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
                    send = targerdir + str(message.author)

                    fr = open(send + "money.txt")
                    mey = fr.read()
                    fr.close()

                    mey = float(mey) + float(meyini)
                    mey = round(mey, 3)

                    fr = open(send + "money.txt", 'w')
                    fr.write(str(mey))
                    fr.close()
                    await message.channel.send(message.author.mention + "님께 정상적으로 수령되었습니다")
                else:
                    await message.channel.send("없는 코드입니다")
            else:
                await message.channel.send("본인이 직접 수령할 수 없습니다")

        if message.content == "!업데이트": #업데이트 안내
            fr = open("update.txt")
            update = fr.read()
            fr.close()

            embed = discord.Embed(title="업데이트 내용", description=str(update), color=0x5CD1E5)
            embed.set_footer(text="시스템 버전" + verand)
            await message.channel.send(embed=embed)

        if message.content == "!어만고치": #어만고치 만들기 및 상태확인
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amango/"
            send = targerdir + str(message.author) + "/"

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amangoitem/"
            senditem = targerdir + str(message.author) + "/"

            if os.path.isfile(send + "main.txt"):
                fr = open(send + "main.txt")
                main = fr.read()
                fr.close()

                fr = open(send + "hung.txt")
                hung = fr.read()
                fr.close()

                fr = open(send + "dir.txt")
                dirt = fr.read()
                fr.close()

                fr = open(send + "level.txt")
                level = fr.read()
                fr.close()

                main = float(main)
                hung = float(hung)
                dirt = float(dirt)
                level = float(level)

                embed = discord.Embed(title="어만고치 스테이터스", description=message.author.mention, color=0x5CD1E5)
                embed.add_field(name="레벨", value=level, inline=True)
                embed.add_field(name="상태", value=main, inline=True)
                embed.add_field(name="포화도", value=hung, inline=True)
                embed.add_field(name="청결도", value=dirt, inline=True)
                embed.set_footer(text="포화도 및 청결도가 -100이 되면 사망합니다")
                await message.channel.send(embed=embed)
            else:
                os.makedirs(send)

                if os.path.isdir(senditem) == False:
                    os.makedirs(senditem)

                fr = open(send + "main.txt", 'w')
                fr.write("0.0")
                fr.close()

                fr = open(send + "level.txt", 'w')
                fr.write("0.0")
                fr.close()

                fr = open(send + "hung.txt", 'w')
                fr.write("100.0")
                fr.close()

                fr = open(send + "dir.txt", 'w')
                fr.write("100.0")
                fr.close()

                await message.channel.send("어만고치가 없어 새로운 어만고치를 입양하였습니다")

        if message.content.startswith("!구입체다치즈"): #체다치즈 구입 도우미
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            trsText = message.content.split(" ")
            trsText = float(trsText[1])
            trsText = round(trsText, 0)

            if trsText * 8200 < mey:

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amangoitem/"
                senditem = targerdir + str(message.author) + "/"

                mey = mey - trsText * 8200
                mey = round(mey, 3)

                fr = open(send + "money.txt", 'w')
                fr.write(str(mey))
                fr.close()

                name = "chechi.txt"

                if os.path.isfile(senditem + name) == False:
                    fr = open(senditem + name, 'w')
                    fr.write("0")
                    fr.close()

                fr = open(senditem + name)
                item = fr.read()
                fr.close()
                
                item = float(item)
                item = item + trsText

                fr = open(senditem + name, 'w')
                fr.write(str(item))
                fr.close()

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else:
                await message.channel.send("돈이 부족합니다")
        
        if message.content.startswith("!구입우유"): #우유 구입 도우미
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            trsText = message.content.split(" ")
            trsText = float(trsText[1])
            trsText = round(trsText, 0)

            if trsText * 6250 < mey:

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amangoitem/"
                senditem = targerdir + str(message.author) + "/"

                mey = mey - trsText * 6250
                mey = round(mey, 3)

                fr = open(send + "money.txt", 'w')
                fr.write(str(mey))
                fr.close()

                name = "mlk.txt"

                if os.path.isfile(senditem + name) == False:
                    fr = open(senditem + name, 'w')
                    fr.write("0")
                    fr.close()

                fr = open(senditem + name)
                item = fr.read()
                fr.close()
                
                item = float(item)
                item = item + trsText

                fr = open(senditem + name, 'w')
                fr.write(str(item))
                fr.close()

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else:
                await message.channel.send("돈이 부족합니다")

        if message.content.startswith("!구입묶음라면"): #라면1봉 구입 도우미
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()

            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            trsText = message.content.split(" ")
            trsText = float(trsText[1])
            trsText = round(trsText, 0)

            if trsText * 7627 < mey:

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amangoitem/"
                senditem = targerdir + str(message.author) + "/"

                mey = mey - trsText * 7627
                mey = round(mey, 3)

                fr = open(send + "money.txt", 'w')
                fr.write(str(mey))
                fr.close()

                name = "ramen.txt"

                if os.path.isfile(senditem + name) == False:
                    fr = open(senditem + name, 'w')
                    fr.write("0")
                    fr.close()

                fr = open(senditem + name)
                item = fr.read()
                fr.close()
                
                item = float(item)
                item = item + trsText * 5

                fr = open(senditem + name, 'w')
                fr.write(str(item))
                fr.close()

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else:
                await message.channel.send("돈이 부족합니다")

        if message.content.startswith("!구입라면"): #라면1개 구입 도우미
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            send = targerdir + str(message.author)

            if os.path.isfile(send + "money.txt") == False:
                await message.channel.send("시스템에 등록되지 않은 유저로 신규 등록하였습니다")
                f = open(send + "money.txt", 'w')
                f.write("50000.00")
                f.close()
                
            fr = open(send + "money.txt")
            mey = fr.read()
            fr.close()

            mey = float(mey)
            mey = round(mey, 3)

            trsText = message.content.split(" ")
            trsText = float(trsText[1])
            trsText = round(trsText, 0)

            if trsText * 1695 < mey:

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amangoitem/"
                senditem = targerdir + str(message.author) + "/"

                mey = mey - trsText * 1695
                mey = round(mey, 3)

                fr = open(send + "money.txt", 'w')
                fr.write(str(mey))
                fr.close()

                name = "ramen.txt"

                if os.path.isfile(senditem + name) == False:
                    fr = open(senditem + name, 'w')
                    fr.write("0")
                    fr.close()

                fr = open(senditem + name)
                item = fr.read()
                fr.close()
                
                item = float(item)
                item = item + trsText

                fr = open(senditem + name, 'w')
                fr.write(str(item))
                fr.close()

                await message.channel.send(message.author.mention + "님 물품을 정상적으로 구입하였습니다")
            else:
                await message.channel.send("돈이 부족합니다")
        
        if message.content == "!인벤토리":#인벤토리 확인
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amangoitem/"
            senditem = targerdir + str(message.author) + "/"
            files = os.listdir(senditem)
    
            condition = senditem + '*.txt'
            csvfiles = glob.glob(condition)

            embed = discord.Embed(title="인벤토리 열람", description=message.author.mention, color=0x5CD1E5)

            for word in csvfiles:
                word = word.split(str(message.author))
                word = word[1]
                word = word[1:]
                
                if word == "chechi.txt":
                    fr = open(senditem + word)
                    item = fr.read()
                    fr.close()

                    embed.add_field(name="체다치즈", value=item + "개", inline=True)
                elif word == "mlk.txt":
                    fr = open(senditem + word)
                    item = fr.read()
                    fr.close()

                    embed.add_field(name="우유", value=item + "개", inline=True)
                elif word == "ramen.txt":
                    fr = open(senditem + word)
                    item = fr.read()
                    fr.close()

                    embed.add_field(name="라면", value=item + "개", inline=True)

            await message.channel.send(embed=embed)

        if message.content.startswith("!먹이주기"): #어만고치 먹이주기
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amango/"
            send = targerdir + str(message.author) + "/"

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amangoitem/"
            senditem = targerdir + str(message.author) + "/"

            trs = message.content.split(" ")
            trswhat = trs[1]
            trssel = trs[2]

            trssel = float(trssel)

            wiin = 0.0

            if trswhat == "라면":
                trswhat = "ramen.txt"
                wiin = 3.3
            elif trswhat == "우유":
                trswhat = "mlk.txt"
                wiin = 8.68
            elif trswhat == "체다치즈":
                trswhat = "chechi.txt"
                wiin = 11.38
            else:
                await message.channel.send(message.author.mention + "물품명을 다시 입력하여 주세요.")
                return
            
            if os.path.isfile(senditem + trswhat) == False:
                await message.channel.send(message.author.mention + "해당 물품이 없습니다")
                return

            fr = open(senditem + trswhat)
            incou = fr.read()
            fr.close()

            incou = float(incou)

            if incou > 0.0 and incou >= trssel and trssel > 0.0:
                incou = incou - trssel

                fr = open(senditem + trswhat, 'w')
                fr.write(str(incou))
                fr.close()

                fr = open(send + "hung.txt")
                hungwi = fr.read()
                fr.close()

                hungwi = float(hungwi)

                hungwi = hungwi + (wiin * trssel)
                hungwi = round(hungwi, 3)

                if hungwi > 100:
                    await message.channel.send(message.author.mention + "님의 어만고치가 배불러 합니다")

                    fr = open(send + "hung.txt", 'w')
                    fr.write("100.0")
                    fr.close()
                else:
                    await message.channel.send(message.author.mention + "님의 어만고치가 먹이를 맛있게 먹습니다")

                    fr = open(send + "hung.txt", 'w')
                    fr.write(str(hungwi))
                    fr.close()
            else:
                await message.channel.send(message.author.mention + "해당 물품이 부족하거나 수치가 이상합니다")

        if message.content == "!고치샤워": #어만고치 샤워하기
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amango/"
            send = targerdir + str(message.author) + "/"

            fr = open(send + "dir.txt", 'w')
            fr.write("100.0")
            fr.close()

            await message.channel.send(message.author.mention + "님의 어만고치가 깨끗해 졌습니다")
        
        if message.content == "!날씨":
            await message.channel.send("사용법은 !날씨 '지역이름' 을 적으시면 AI가 자동으로 검색하여줍니다\n날씨 정보 왼측 선의 색은 미세먼지 정도에 따라 변화합니다")
        elif message.content.startswith("!날씨"):
            learn = message.content.split(" ")
            location = learn[1]
            enc_location = urllib.parse.quote(location+'날씨')
            hdr = {'User-Agent': 'Mozilla/5.0'}
            url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + enc_location

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

            if color == "좋음":
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
            elif color == "매우 나쁨":
                embed = discord.Embed(
                title=learn[1]+ ' 날씨 정보',
                description=learn[1]+ ' 날씨 정보입니다.',
                colour=discord.Color.red()
            )
            
            embed.add_field(name='현재온도', value=todayTemp+'˚', inline=False)  # 현재온도
            embed.add_field(name='체감온도', value=todayFeelingTemp, inline=False)  # 체감온도
            embed.add_field(name='현재상태', value=todayValue, inline=False)  # 밝음,어제보다 ?도 높거나 낮음을 나타내줌
            embed.add_field(name='현재 미세먼지 상태', value=todayMiseaMongi, inline=False)  # 오늘 미세먼지
            embed.add_field(name='오늘 오전 / 오후 날씨', value=tomorrowTemp, inline=False)  # 오늘날씨
            embed.add_field(name='내일 오전온도', value=tomorrowMoring+'˚', inline=False)  # 내일오전날씨
            embed.add_field(name='내일 오전날씨상태, 미세먼지 상태', value=tomorrowValue, inline=False)  # 내일오전 날씨상태
            embed.add_field(name='내일 오후온도', value=tomorrowAfterTemp + '˚', inline=False)  # 내일오후날씨
            embed.add_field(name='내일 오후날씨상태, 미세먼지 상태', value=tomorrowAfterValue, inline=False)  # 내일오후 날씨상태

            await message.channel.send(embed=embed)
        
        if message.content.startswith("!봇보이스"):
            await message.author.voice.channel.connect()


#하단 텔포 끝 마지막

async def background_task():
    await client.wait_until_ready()

    while True:
        channel = client.get_channel(718436389062180917)

        fr = open("main.txt", encoding='utf-16')
        mainin = fr.read()
        fr.close()

        await asyncio.sleep(60*30 + 60*60*3)
        await channel.send("[서버 자동 공지 - 3시간 30분 주기] \n" + mainin) 

async def background_backup():
    await client.wait_until_ready()

    while True:
        channel = client.get_channel(751716285129424897)

        await asyncio.sleep(60*60*1 + 60*30)

        nowsettime = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))

        copy_tree("C:/Users/mulma/Desktop/bot-Amansa", "C:/Users/mulma/Desktop/백업/"+ str(nowsettime))

        targerdir = r"C:/Users/mulma/Desktop/백업/"
        files = os.listdir(targerdir)
        files = files[0]
        shutil.rmtree(targerdir + files)

async def background_se(): #자동 세금 시스템
    await client.wait_until_ready()

    while True:
        channel = client.get_channel(751716285129424897)

        if "00:00" ==  time.strftime('%H:%M', time.localtime(time.time())) or "12:00" ==  time.strftime('%H:%M', time.localtime(time.time())) :
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
            files = os.listdir(targerdir)
    
            condition = targerdir + '*money.txt'
            csvfiles = glob.glob(condition)

            cou = 0
            trs = []

            for word in csvfiles:
                trs.insert(cou, word)
                cou += 1


            for word in trs:
                fr = open(word)
                mey = fr.read()
                fr.close()

                mey = float(mey)
                mey = round(mey, 3)

                if mey <= 100000.00:
                    inmey = round(mey / 100 * 7.5, 3)
                    mey = mey - inmey
                elif mey <= 200000.00:
                    inmey = round(mey / 100 * 15, 3)
                    mey = mey - inmey
                elif mey <= 300000.00:
                    inmey = round(mey / 100 * 30, 3)
                    mey = mey - inmey
                elif mey <= 400000.00:
                    inmey = round(mey / 100 * 45, 3)
                    mey = mey - inmey
                elif mey <= 500000.00:
                    inmey = round(mey / 100 * 55, 3)
                    mey = mey - inmey
                else:
                    inmey = round(mey / 100 * 70, 3)
                    mey = mey - inmey

                f = open(word, 'w')
                mey = round(mey, 3)
                f.write(str(mey))
                f.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/se/"
                send = targerdir + word[40:]

                if os.path.isfile(send) == False:
                    f = open(send, 'w')
                    f.write(str(0.00))
                    f.close()

                f = open(send, 'r')
                semey = f.read()
                f.close()

                semey = float(semey)
                semey = round(semey, 3)

                f = open(send, 'w')
                inmey = 0.00
                if mey <= 100000.00:
                    inmey = semey + round(mey / 100 * 7.5, 3)
                elif mey <= 200000.00:
                    inmey = semey + round(mey / 100 * 15, 3)
                elif mey <= 300000.00:
                    inmey = semey + round(mey / 100 * 30, 3)
                elif mey <= 400000.00:
                    inmey = semey + round(mey / 100 * 45, 3)
                elif mey <= 500000.00:
                    inmey = semey + round(mey / 100 * 55, 3)
                else:
                    inmey = semey + round(mey / 100 * 70, 3)
                f.write(str(inmey))
                f.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/lastse/"
                send = targerdir + word[40:]
                f = open(send, 'w')
                inmey = 0.00
                if mey <= 100000.00:
                    inmey = round(mey / 100 * 7.5, 3)
                elif mey <= 200000.00:
                    inmey = round(mey / 100 * 15, 3)
                elif mey <= 300000.00:
                    inmey = round(mey / 100 * 30, 3)
                elif mey <= 400000.00:
                    inmey = round(mey / 100 * 45, 3)
                elif mey <= 500000.00:
                    inmey = round(mey / 100 * 55, 3)
                else:
                    inmey = round(mey / 100 * 70, 3)
                f.write(str(inmey))
                f.close()
        
            await channel.send("소지금 세금을 납부하게 하였습니다")
        await asyncio.sleep(60*1)

async def background_se2(): #자동 세금 시스템
    await client.wait_until_ready()
    
    while True:
        channel = client.get_channel(751716285129424897)

        if "00:00" ==  time.strftime('%H:%M', time.localtime(time.time())) or "12:00" ==  time.strftime('%H:%M', time.localtime(time.time())):
            await asyncio.sleep(1)

            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
            files = os.listdir(targerdir)
    
            condition = targerdir + '*money.txt'
            csvfiles = glob.glob(condition)

            cou = 0
            trs = []

            for word in csvfiles:
                trs.insert(cou, word)
                cou += 1


            for word in trs:
                fr = open(word)
                mey = fr.read()
                fr.close()

                mey = float(mey)
                mey = round(mey, 3)

                if mey <= 100000.00:
                    inmey = round(mey / 100 * 7.5, 3)
                    mey = mey - inmey
                elif mey <= 200000.00:
                    inmey = round(mey / 100 * 15, 3)
                    mey = mey - inmey
                elif mey <= 300000.00:
                    inmey = round(mey / 100 * 30, 3)
                    mey = mey - inmey
                elif mey <= 400000.00:
                    inmey = round(mey / 100 * 45, 3)
                    mey = mey - inmey
                elif mey <= 500000.00:
                    inmey = round(mey / 100 * 55, 3)
                    mey = mey - inmey
                else:
                    inmey = round(mey / 100 * 70, 3)
                    mey = mey - inmey

                f = open(word, 'w')
                mey = round(mey, 3)
                f.write(str(mey))
                f.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/se/"
                send = targerdir + word[40:]

                if os.path.isfile(send) == False:
                    f = open(send, 'w')
                    f.write(str(0.00))
                    f.close()

                f = open(send, 'r')
                semey = f.read()
                f.close()

                semey = float(semey)
                semey = round(semey, 3)

                f = open(send, 'w')
                f = open(send, 'w')

                inmey = 0.00
                if mey <= 100000.00:
                    inmey = semey + round(mey / 100 * 7.5, 3)
                elif mey <= 200000.00:
                    inmey = semey + round(mey / 100 * 15, 3)
                elif mey <= 300000.00:
                    inmey = semey + round(mey / 100 * 30, 3)
                elif mey <= 400000.00:
                    inmey = semey + round(mey / 100 * 45, 3)
                elif mey <= 500000.00:
                    inmey = semey + round(mey / 100 * 55, 3)
                else:
                    inmey = semey + round(mey / 100 * 70, 3)
                f.write(str(inmey))

                f.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/lastse/"
                send = targerdir + word[40:]

                fr = open(send)
                inmey = fr.read()
                fr.close()

                inmey = float(inmey)
                inmey = round(inmey, 3)

                f = open(send, 'w')
                if mey <= 100000.00:
                    inmey =  inmey + round(mey / 100 * 7.5, 3)
                elif mey <= 200000.00:
                    inmey = inmey + round(mey / 100 * 15, 3)
                elif mey <= 300000.00:
                    inmey = inmey + round(mey / 100 * 30, 3)
                elif mey <= 400000.00:
                    inmey = inmey + round(mey / 100 * 45, 3)
                elif mey <= 500000.00:
                    inmey = inmey + round(mey / 100 * 55, 3)
                else:
                    inmey = inmey + round(mey / 100 * 70, 3)
                f.write(str(inmey))
                f.close()
        
            await channel.send("보유금 세금을 납부하게 하였습니다")
        await asyncio.sleep(60*1)

async def background_ye(): #자동 예금
    await client.wait_until_ready()
    stratran = random.randint(10, 30)
    await asyncio.sleep(60*stratran)

    while True:
        channel = client.get_channel(751716285129424897)

        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
        files = os.listdir(targerdir)
    
        condition = targerdir + '*ye.txt'
        csvfiles = glob.glob(condition)

        cou = 0
        trs = []

        for word in csvfiles:
            trs.insert(cou, word)
            cou += 1


        for word in trs:
            fr = open(word)
            mey = fr.read()
            fr.close()

            mey = float(mey)

            mey = mey + (mey / 100 * 0.45)
            mey = round(mey, 3)

            f = open(word, 'w')
            f.write(str(mey))
            f.close()
        
        await asyncio.sleep(60*30)

async def background_backrank():#랭킹 지원금
    await client.wait_until_ready()
    stratran = random.randint(4, 6)
    await asyncio.sleep(60*60*stratran)

    while True:
        channel = client.get_channel(751716285129424897)

        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
        files = os.listdir(targerdir)

        condition = targerdir + "*money.txt"
        csvfiles = glob.glob(condition)
            

        cou = 0
        trs = []

        for word in csvfiles:
            trs.insert(cou, word)
            cou += 1 

        ussc = []
        usname = []
        cou = 0
        for sco in trs:
            f = open(sco, 'r')
            scin = f.read()
            f.close()
            ussc.insert(cou, float(scin))

            trsText = sco.split("#")
            trsText = trsText[0]
            usname.insert(cou, str(trsText[40:]))

            cou += 1

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
            meyin = ussc[scor] / 100 * (100 / (scor + 1) / 4)
            if  scor + 1 >= 2 and scor + 1 < 5:
                meyin = meyin * 1.5 / 3
            elif scor + 1 >= 5 and scor + 1 < 8:
                meyin = meyin * 1.25 / 3
            elif scor + 1 >= 8:
                meyin = meyin * 1.2 / 2
            
            meyin = round(meyin, 3)

            if meyin > 10000000.0:
                meyin = 10000000.0

            embed.add_field(name=str(scor + 1) + "등 ID : " + usname[scor], value=str(ussc[scor]) + "원\n" + str(meyin) + " 원을 지급합니다", inline=True)

            meyin = ussc[scor] + meyin
            meyin = round(meyin, 3)
            f = open(trs[scor], 'w')
            f.write(str(meyin))
            f.close()

            if scor == 9:
                break

        await channel.send(embed=embed)
        timeran = random.randint(2, 4)
        timeranbun = random.randint(1, 60)
        await asyncio.sleep(60*60*timeran + 60*timeranbun)

async def background_taskbot():
    await client.wait_until_ready()
    stratran = random.randint(5, 10)
    await asyncio.sleep(60*stratran)

    while True:
        channel = client.get_channel(751716285129424897)      
        await channel.send("봇 채팅방에는 일반 채팅은 칠수없으며\n번역기 이외에는 봇 채팅방 이외의 채널에서 사용이 불가능합니다")
        await asyncio.sleep(60*30 + 60*60*5)

async def background_backcov():
    await client.wait_until_ready()

    while True:
        if "10:01" ==  time.strftime('%H:%M', time.localtime(time.time())) or "23:59" ==  time.strftime('%H:%M', time.localtime(time.time())):
            channel = client.get_channel(718436389062180917)

            html = urlopen("http://ncov.mohw.go.kr/")
            bsObject = BeautifulSoup(html, "html.parser")

            embed = discord.Embed(title="코로나 정보", description="[10:01, 23:59 자동 코로나 알림]", color=0x5CD1E5)

            einput = str(bsObject.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(1) > span.before"))
            embed.add_field(name="질병관리청 공식 확진자 수 [전날 확진자 <AM 10시에 업데이트>]", value=einput[28:-9] + "명", inline=False)

            einput = str(bsObject.select("body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum > ul > li:nth-child(4) > span.before"))
            embed.add_field(name="질병관리청 공식 사망자 수 [전날 사망자 <AM 10시에 업데이트>]", value=einput[23:-9] + "명", inline=False)

            html = urlopen("https://v1.coronanow.kr/")
            bsObject = BeautifulSoup(html, "html.parser")

            einput = str(bsObject.select("#live_board2 > div:nth-child(1) > h5"))

            embed.add_field(name="실시간 코로나 확진자 수", value=einput[129:-6], inline=False)

                    
            await channel.send(embed=embed)

        await asyncio.sleep(60*1)

async def background_backjisin():#지진 자동 감지 시스템
    await client.wait_until_ready()

    while True:
        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/"
        files = targerdir + "ji.txt"

        fr = open(files)
        info = fr.read()
        fr.close()

        html = urlopen("https://www.weather.go.kr/weather/earthquake_volcano/domesticlist.jsp")
        bsObject = BeautifulSoup(html, "html.parser")

        einput = str(bsObject.select("#excel_body > tbody > tr:nth-child(1) > td:nth-child(2)"))
        einput = einput[5:-6]

        if info != einput:
            fr = open(files, 'w')
            fr.write(einput)
            fr.close()

            embed = discord.Embed(title="[경고! 지진이 발생하였습니다]", description="지진 자동 감지 시스템\n지진 발생시 자동으로 올라옵니다", color=0x5CD1E5)

            einlist = ["발생시각", "규모", "깊이", "최대진도" ,"위치"]
            listin = 2
            TFL = False

            for insite in einlist:
                einput = str(bsObject.select("#excel_body > tbody > tr:nth-child(1) > td:nth-child( " + str(listin) + ")"))

                if listin < 8:
                    einput = einput[5:-6]
                else:
                    einput = einput[24:-6]

                embed.add_field(name=insite, value=einput, inline=TFL)

                listin += 1
                TFL = True
                if listin == 6:
                    listin = 8
                    TFL = False
            
            channel = client.get_channel(718436389062180917)
            await channel.send(embed=embed)

            channel = client.get_channel(751716285129424897)
            await channel.send(embed=embed)
        await asyncio.sleep(60*1)

async def background_amangochi():#어만고치 포화도 시스템
    await client.wait_until_ready()

    while True:
        await asyncio.sleep(60 * random.randint(5, 15))
        channel = client.get_channel(751716285129424897)

        fd_list = os.listdir(f'C:/Users/mulma/Desktop/bot-Amansa/amango')

        for word in fd_list:
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amango/"
            send = targerdir + word + r"/"

            fr = open(send + "hung.txt")
            hungin  = fr.read()
            fr.close()

            hungin = float(hungin)

            randomhung = random.uniform(0.4, 0.65)
            randomhung = round(randomhung, 3)
            hungin = hungin - randomhung
            hungin = round(hungin, 3)

            if hungin <= -100:
                await channel.send("ID : " + word[:-5] + "님의 어만고치가 아사하였습니다 벌금 50%를 부과합니다")

                shutil.rmtree(targerdir + word)

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
                send = targerdir + word

                fr = open(send + "money.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)

                mey = mey / 2
                mey = round(mey, 3)

                f = open(send + "money.txt", 'w')
                f.write(str(mey))
                f.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
                send = targerdir + word

                fr = open(send + "ye.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)

                mey = mey / 2
                mey = round(mey, 3)

                f = open(send + "ye.txt", 'w')
                f.write(str(mey))
                f.close()
            else:
                fr = open(send + "hung.txt", 'w')
                fr.write(str(hungin))
                fr.close

                fr = open(send + "hung.txt")
                remove = fr.read()
                fr.close

                if hungin >= 70:
                    fr = open(send + "main.txt")
                    main = fr.read()
                    fr.close()

                    fr = open(send + "level.txt")
                    levein  = fr.read()
                    fr.close()

                    levein = float(levein)

                    if levein < 1.0:
                        levein = 1.0

                    main = float(main)
                    main = main + (10 / levein)
                    main = round(main, 3)

                    if main >= 100.0:
                        main = main - 100
                        main = round(main, 3)

                        fr = open(send + "main.txt", 'w')
                        fr.write(str(main))
                        fr.close

                        fr = open(send + "level.txt")
                        main  = fr.read()
                        fr.close()

                        main = float(main)
                        main = main + 1

                        fr = open(send + "level.txt", 'w')
                        fr.write(str(main))
                        fr.close

                        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
                        send = targerdir + word

                        fr = open(send + "money.txt")
                        mey = fr.read()
                        fr.close()

                        mey = float(mey)

                        mey = mey + (100000.0 * main)
                        mey = round(mey, 3)

                        f = open(send + "money.txt", 'w')
                        f.write(str(mey))
                        f.close()

                        await channel.send("ID : " + word[:-5] + "님의 어만고치의 레벨이 상승하였습니다 상금 " + str(10 * main) + "만원을 지급합니다")
                    else:
                        fr = open(send + "main.txt", 'w')
                        fr.write(str(main))
                        fr.close

                        fr = open(send + "main.txt")
                        ch = fr.read()
                        fr.close

async def background_amangochichung():#어만고치 청결도 시스템
    await client.wait_until_ready()

    while True:
        await asyncio.sleep(60 * random.randint(5, 15))
        
        channel = client.get_channel(751716285129424897)

        fd_list = os.listdir(f'C:/Users/mulma/Desktop/bot-Amansa/amango')

        for word in fd_list:
            targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/amango/"
            send = targerdir + word + r"/"

            fr = open(send + "dir.txt")
            hungin  = fr.read()
            fr.close()

            hungin = float(hungin)

            randomhung = random.uniform(0.4, 0.65)
            randomhung = round(randomhung, 3)

            hungin = hungin - randomhung
            hungin = round(hungin, 3)

            if hungin <= -100:
                await channel.send("ID : " + word[:-5] + "님의 어만고치가 병사하였습니다 벌금 50%를 부과합니다")

                shutil.rmtree(targerdir + word)

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
                send = targerdir + word

                fr = open(send + "money.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)

                mey = mey / 2
                mey = round(mey, 3)

                f = open(send + "money.txt", 'w')
                f.write(str(mey))
                f.close()

                targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/bank/"
                send = targerdir + word

                fr = open(send + "ye.txt")
                mey = fr.read()
                fr.close()

                mey = float(mey)

                mey = mey / 2
                mey = round(mey, 3)

                f = open(send + "ye.txt", 'w')
                f.write(str(mey))
                f.close()
            else:
                fr = open(send + "dir.txt", 'w')
                fr.write(str(hungin))
                fr.close

                fr = open(send + "dir.txt")
                remove = fr.read()
                fr.close

                if hungin >= 70:
                    fr = open(send + "main.txt")
                    main = fr.read()
                    fr.close()

                    fr = open(send + "level.txt")
                    levein  = fr.read()
                    fr.close()

                    levein = float(levein)
                    
                    if levein < 1.0:
                        levein = 1.0

                    main = float(main)
                    main = main + (10 / levein)
                    main = round(main, 3)

                    if main >= 100.0:
                        main = main - 100
                        main = round(main, 3)

                        fr = open(send + "main.txt", 'w')
                        fr.write(str(main))
                        fr.close

                        fr = open(send + "level.txt")
                        main  = fr.read()
                        fr.close()

                        main = float(main)
                        main = main + 1

                        fr = open(send + "level.txt", 'w')
                        fr.write(str(main))
                        fr.close

                        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/money/"
                        send = targerdir + word

                        fr = open(send + "money.txt")
                        mey = fr.read()
                        fr.close()

                        mey = float(mey)

                        mey = mey + (100000.0 * main)
                        mey = round(mey, 3)

                        f = open(send + "money.txt", 'w')
                        f.write(str(mey))
                        f.close()

                        await channel.send("ID : " + word[:-5] + "님의 어만고치의 레벨이 상승하였습니다 상금 " + str(10 * main) + "원을 지급합니다")
                    else:
                        fr = open(send + "main.txt", 'w')
                        fr.write(str(main))
                        fr.close

                        fr = open(send + "main.txt")
                        ch = fr.read()
                        fr.close

async def background_heijisin():#지진 자동 감지 시스템
    await client.wait_until_ready()

    while True:
        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/"
        files = targerdir + "jiwe.txt"

        fr = open(files)
        info = fr.read()
        fr.close()

        html = urlopen("http://www.weather.go.kr/weather/earthquake_volcano/internationallist.jsp")
        bsObject = BeautifulSoup(html, "html.parser")

        einput = str(bsObject.select("#content_weather > table > tbody > tr:nth-child(2) > td:nth-child(2)"))
        einput = einput[5:-6]

        if info != einput:
            fr = open(files, 'w')
            fr.write(einput)
            fr.close()

            embed = discord.Embed(title="경고! 해외에 강진이 발생하였습니다", description="지진 자동 감지 시스템\n지진 발생시 자동으로 올라옵니다", color=0x5CD1E5)

            einlist = ["발생시각", "규모", "깊이", "위치"]
            listin = 2
            TFL = False

            for insite in einlist:
                einput = str(bsObject.select("#content_weather > table > tbody > tr:nth-child(1) > td:nth-child( "+ str(listin) + ")"))

                if listin < 7:
                    einput = einput[5:-6]
                else:
                    einput = einput[24:-6]

                embed.add_field(name=insite, value=einput, inline=TFL)

                listin += 1
                TFL = True
                if listin == 5:
                    listin = 7
                    TFL = False
            
            channel = client.get_channel(718436389062180917)
            await channel.send(embed=embed)

            channel = client.get_channel(751716285129424897)
            await channel.send(embed=embed)
        await asyncio.sleep(60*1)

async def background_kmajisin():#KMA 지진 자동 감지 시스템
    await client.wait_until_ready()

    while True:
        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/"
        files = targerdir + "KMAji.txt"

        fr = open(files)
        info = fr.read()
        fr.close()

        login = "https://necis.kma.go.kr/necis-dbf/user/common/userLoginNewAction.do"
        html = "http://necis.kma.go.kr/necis-dbf/user/earthquake/selectEarthquakeList.do"

        Session = requests.session()

        params = dict()
        params['pLoginFailChecker'] = 'N'
        params['linkUrl'] = ' '
        params['email'] = 'mulmangul19@gmail.com'
        params['pPasswd'] = 'oe3fl6po'

        res = Session.post(login, data = params)
        res.raise_for_status()

        res = Session.get(html)
        bsObject = BeautifulSoup(res.content, 'html.parser')

        einput = str(bsObject.select("#cont > div.fl.recent_quake > div > div.article_body"))
        print(einput)

        #einput = einput[0:-1]

        if info == einput:
            fr = open(files, 'w')
            fr.write(einput)
            fr.close()

            embed = discord.Embed(title="[경고! 지진이 발생하였습니다]", description="지진 자동 감지 시스템\n지진 발생시 자동으로 올라옵니다", color=0x5CD1E5)

            einlist = ["발생시각", "종류", "규모", "깊이", "최대진도" ,"위치"]

            einput = str(bsObject.select("#gridTbody > tr:nth-child(1) > td:nth-child(5)"))
            einput = einput[0:-0]
            embed.add_field(name=einlist[0], value=einput, inline=True)
            einput = str(bsObject.select("#gridTbody > tr:nth-child(1) > td:nth-child(4)"))
            einput = einput[0:-0]
            embed.add_field(name=einlist[1], value=einput, inline=True)
            einput = str(bsObject.select("#gridTbody > tr:nth-child(1) > td:nth-child(6)"))
            einput = einput[0:-0]
            embed.add_field(name=einlist[2], value=einput, inline=True)
            einput = str(bsObject.select("#gridTbody > tr:nth-child(1) > td:nth-child(7)"))
            einput = einput[0:-0]
            embed.add_field(name=einlist[3], value=einput, inline=True)
            einput = str(bsObject.select("#gridTbody > tr:nth-child(1) > td:nth-child(8)"))
            einput = einput[0:-0]
            embed.add_field(name=einlist[4], value=einput, inline=True)
            einput = str(bsObject.select("#gridTbody > tr:nth-child(1) > td.alignL"))
            einput = einput[0:-0]
            embed.add_field(name=einlist[5], value=einput, inline=True)
            
            channel = client.get_channel(823395883088871434)
            await channel.send(embed=embed)

            #channel = client.get_channel(751716285129424897)
            #await channel.send(embed=embed)
        await asyncio.sleep(60*1)

async def background_livejisin():#KMA 지진 자동 감지 시스템
    await client.wait_until_ready()

    while True:
        targerdir = r"C:/Users/mulma/Desktop/bot-Amansa/"
        files = targerdir + "liveji.txt"

        fr = open(files)
        info = fr.read()
        fr.close()

        html = urlopen("https://www.weather.go.kr/pews/")
        bsObject = BeautifulSoup(html, "html.parser")

        einput = str(bsObject.select("body"))
        #document.querySelector("#fav > option")
        print(einput)

    
        if info == einput:
            fr = open(files, 'w')
            fr.write(einput)
            fr.close()

        await asyncio.sleep(3)
            

#선언 ~~
client.loop.create_task(background_task())
client.loop.create_task(background_backup())
client.loop.create_task(background_main())
client.loop.create_task(background_join())
client.loop.create_task(background_remove())
client.loop.create_task(background_se())
client.loop.create_task(background_se2())
client.loop.create_task(background_ye())
client.loop.create_task(background_backrank())
client.loop.create_task(background_taskbot())
client.loop.create_task(background_backcov())
client.loop.create_task(background_backjisin())
client.loop.create_task(background_amangochi())
client.loop.create_task(background_amangochichung())
client.loop.create_task(background_heijisin())
#client.loop.create_task(background_kmajisin())
#client.loop.create_task(background_livejisin())
client.run(token)