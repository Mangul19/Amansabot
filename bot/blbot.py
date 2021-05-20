#bl 전용 디스코드 봇

import discord
import asyncio
from discord.ext import commands
import sys
sys.path.insert(0, "D:/Desktop/중요파일/bot-Amansa/noup")
import code

#clinet
client = discord.Client()
#discord bot tokken
token = code.bltoken

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\nbl봇 시스템을 시작합니다" + 
        "\n==========================================")
    # 이 기능을 이용하여 봇의 상태를 출력
    mssg = discord.Game("Made by Han_MangUl")
    await client.change_presence(status=discord.Status.online, activity=mssg)
    
#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return

    #받은 메세지 및 입력자 출력
    print(str(message.author) + str(message.author.mention) + " : " + str(message.content))
    
    if message.content.startswith("익숙해 지고나면"):
        await message.delete()
    elif message.content.startswith("익숙해지고나면"):
        await message.delete()

client.run(token)