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

namelist = []
guild = ""
voiTF = {}
spTF = {}


#정보 변화시
@client.event
async def on_voice_state_update(member, before, after):
    global namelist

    #봇일 경우 무시
    if member == client.user:
        return

    ID = member.id

    if before.channel == None:
        namelist.append(member)
        voiTF[ID] = 0
        spTF[ID] = 0
        listch(namelist)
    elif after.channel == None:
        namelist.remove(member)
        listch(namelist)

    deaf = after.self_deaf
    mute = after.self_mute

    if deaf and voiTF[ID] != deaf:
        voiTF[ID] = deaf
        print(str(member) + "님의 듣기 상태가 OFF 입니다")
        return
    elif deaf == False and voiTF[ID] != deaf:
        voiTF[ID] = deaf
        print(str(member) + "님의 듣기 상태가 ON 입니다")

    if mute and spTF[ID] != mute:
        spTF[ID] = mute
        print(str(member) + "님의 마이크 상태가 OFF 입니다")
    elif mute == False and spTF[ID] != mute:
        spTF[ID] = mute
        print(str(member) + "님의 마이크 상태가 ON 입니다")

def listch(namelist):
    print("--통화방 입장 리스트 변경됨--")
        
    for name in namelist:
        print(name)


client.run(token)