#어만사 전용 디스코드 봇

import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code
import math

intents = discord.Intents.all()
#clinet
client = discord.Client(intents=intents)
#discord bot tokken
token = code.token
#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

namelist = []
guild = ""
voiTF = {}
spTF = {}

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n어만사 경험치 시스템을 시작합니다" + 
        "\n==========================================")

#메세지 수신시
@client.event
async def on_message(message):
    global guild
    guild = message.guild.roles

    #봇일 경우 무시
    if message.author == client.user:
        return

    send = str(message.author.id)  #메세지 송신자 ID 설정
    
    dirlevel = db.reference('level/' + send) #레벨 값 가져오기
    level = dirlevel.get()

    direxp = db.reference('exp/' + send) #경험치 값 가져오기
    exp = direxp.get()

    if level == None: #저장된 정보가 없을시
        dirlevel.update({send:1}) #새로운 값 설정 저장
        direxp.update({send:0})
    else: # 저장된 정보가 있을시
        level = level[send] #레벨 및 경험치 값 가져오기
        exp = exp[send]

        intstr = str(message.content) # 메세지를 String값으로 변환
        intstr = len(intstr) # 길이 계산

        und = 100 / level
        ran = random.uniform(und, und + 20) * intstr / level

        if ran > 100: # 한번에 많은 경험치 부여 방지를 위해 최대값을 100으로 설정
            ran = 100

        print(send + " : " + str(ran))
        exp = round(exp + ran, 3)

        if exp > (100 * level * 1.5): #경험치 값이 넘었을때
            exp = exp - (100 * level * 1.5) # 경험치에 1천을 제하고 저장
            exp = round(exp, 3)
            direxp.update({send:exp})

            level = level + 1 # 레벨을 1 상승시킨 후 저장
            dirlevel.update({send:level})

            await message.channel.send(message.author.mention + "님의 레벨이 " + str(level) +" 으로/로 상승하였습니다") # 레벨업 정보 송신

            if level == 10: #레벨에따라 (10의배수) 역할 부여 및 기존 역할 제거
                role = discord.utils.get(guild, name="입주자<~19>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 입주자<~19>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="한걸음<~9>")
                await message.author.remove_roles(role)
            elif level == 20:
                role = discord.utils.get(guild, name="설립자<~29>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 설립자<~29>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="입주자<~19>")
                await message.author.remove_roles(role)
            elif level == 30:
                role = discord.utils.get(guild, name="제작자<~39>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 제작자<~39>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="설립자<~29>")
                await message.author.remove_roles(role)
            elif level == 40:
                role = discord.utils.get(guild, name="고인물<~49>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 고인물<~49>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="제작자<~39>")
                await message.author.remove_roles(role)
            elif level == 50:
                role = discord.utils.get(guild, name="화석<~59>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 화석<~59>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="고인물<~49>")
                await message.author.remove_roles(role)
            elif level == 60:
                role = discord.utils.get(guild, name="석유<~69>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 석유<~69>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="화석<~59>")
                await message.author.remove_roles(role)
            elif level == 70:
                role = discord.utils.get(guild, name="구름<~79>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 구름<~79>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="석유<~69>")
                await message.author.remove_roles(role)
            elif level == 80:
                role = discord.utils.get(guild, name="위성<~89>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 위성<~89>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="구름<~79>")
                await message.author.remove_roles(role)
            elif level == 90:
                role = discord.utils.get(guild, name="행성<~99>")
                await message.author.add_roles(role)
                await message.channel.send(message.author.mention + "님에게 행성<~99>을/를 부여하였습니다")
                role = discord.utils.get(guild, name="위성<~89>")
                await message.author.remove_roles(role)
        else: # 경험치가 충족하지 않았으면 그냥 저장
            direxp.update({send:exp})

#정보 변화시
@client.event
async def on_voice_state_update(member, before, after):
    global namelist
    global voiTF
    global spTF

    #봇일 경우 무시
    if member == client.user:
        return

    if before.channel == None:
        namelist.append(member)
        voiTF[member] = "reset"
        spTF[member] = "reset"
        listch(namelist)
    elif after.channel == None:
        namelist.remove(member)
        listch(namelist)
        return

    deaf = after.self_deaf
    mute = after.self_mute

    if voiTF[member] != deaf:
        if deaf:
            voiTF[member] = deaf
            print(str(member) + "님의 듣기 상태가 OFF 입니다")
            return
        elif deaf == False:
            voiTF[member] = deaf
            print(str(member) + "님의 듣기 상태가 ON 입니다")

    if spTF[member] != mute:
        if mute:
            spTF[member] = mute
            print(str(member) + "님의 마이크 상태가 OFF 입니다")
        elif mute == False:
            spTF[member] = mute
            print(str(member) + "님의 마이크 상태가 ON 입니다")

def listch(namelist):
    print("--통화방 입장 리스트 변경됨--")
        
    for name in namelist:
        print(name)

async def levelin():
    global namelist
    global voiTF
    global spTF

    while True:
        await asyncio.sleep(60*1)

        for name in namelist:
            send = str(name.id)  #메세지 송신자 ID 설정

            dirlevel = db.reference('level/' + send) #레벨 값 가져오기
            level = dirlevel.get()

            direxp = db.reference('exp/' + send) #경험치 값 가져오기
            exp = direxp.get()

            if level == None: #저장된 정보가 없을시
                dirlevel.update({send:1}) #새로운 값 설정 저장
                direxp.update({send:0})
            else: # 저장된 정보가 있을시
                level = level[send] #레벨 및 경험치 값 가져오기
                exp = exp[send]

                top = 100 / level
                ran = random.uniform(0.1, top) * top 

                if voiTF[name]:
                    print(str(name) + " 님은 현재 헤드셋 OFF 상태로 경험치를 100% 감소시킵니다")
                    ran = 0
                elif spTF[name]:
                    print(str(name) + " 님은 현재 마이크 OFF 상태로 경험치를 50% 감소시킵니다")
                    ran -= ran / 2

                print("통화 - " + send + " : " + str(ran))
                exp = round(exp + ran, 3)

                if exp > (100 * level * 1.5): #경험치 값이 넘었을때
                    exp = exp - (100 * level * 1.5) # 경험치 제하고 저장
                    exp = round(exp, 3)
                    direxp.update({send:exp})

                    level = level + 1 # 레벨을 1 상승시킨 후 저장
                    dirlevel.update({send:level})

                    channel = client.get_channel(832799360210436107)
                    await channel.send(name.mention + "님의 레벨이 " + str(level) +" 으로/로 상승하였습니다") # 레벨업 정보 송신

                    global guild
                    if level == 10: #레벨에따라 (10의배수) 역할 부여 및 기존 역할 제거
                        role = discord.utils.get(guild, name="입주자<~19>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 입주자<~19>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="한걸음<~9>")
                        await name.remove_roles(role)
                    elif level == 20:
                        role = discord.utils.get(guild, name="설립자<~29>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 설립자<~29>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="입주자<~19>")
                        await name.remove_roles(role)
                    elif level == 30:
                        role = discord.utils.get(guild, name="제작자<~39>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 제작자<~39>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="설립자<~29>")
                        await name.remove_roles(role)
                    elif level == 40:
                        role = discord.utils.get(guild, name="고인물<~49>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 고인물<~49>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="제작자<~39>")
                        await name.remove_roles(role)
                    elif level == 50:
                        role = discord.utils.get(guild, name="화석<~59>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 화석<~59>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="고인물<~49>")
                        await name.remove_roles(role)
                    elif level == 60:
                        role = discord.utils.get(guild, name="석유<~69>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 석유<~69>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="화석<~59>")
                        await name.remove_roles(role)
                    elif level == 70:
                        role = discord.utils.get(guild, name="구름<~79>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 구름<~79>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="석유<~69>")
                        await name.remove_roles(role)
                    elif level == 80:
                        role = discord.utils.get(guild, name="위성<~89>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 위성<~89>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="구름<~79>")
                        await name.remove_roles(role)
                    elif level == 90:
                        role = discord.utils.get(guild, name="행성<~99>")
                        await name.add_roles(role)
                        await channel.send(name.mention + "님에게 행성<~99>을/를 부여하였습니다")
                        role = discord.utils.get(guild, name="위성<~89>")
                        await name.remove_roles(role)
                else: # 경험치가 충족하지 않았으면 그냥 저장
                    direxp.update({send:exp})

client.loop.create_task(levelin())
client.run(token)