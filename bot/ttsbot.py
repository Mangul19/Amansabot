#어만사 전용 tts 봇

import discord
from discord.ext import commands
import asyncio
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code
import os
from glob import glob
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

intents = discord.Intents.all()
#clinet
client = discord.Client(intents=intents)
#discord bot tokken
token = code.ttstoken

inme = ''
count = 0

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\ntts 시스템을 시작합니다" + 
        "\n==========================================")
    mssg = discord.Game("`할말|Made by MangUl")
    await client.change_presence(status=discord.Status.online, activity=mssg)

#정보 변화시
@client.event
async def on_voice_state_update(member, before, after):
    global count

    #봇일 경우 무시
    if member == client.user or member.id == 806935645703634944:
        return

    if before.channel == None:
        if after.channel != None:
            count += 1
            print(str(count) + "명 입장 중")
    elif before.channel != None:
        if  after.channel == None:
            count -= 1
            print(str(count) + "명 입장 중")

            if count == 0 and len(client.voice_clients) > 0:
                await client.voice_clients[0].disconnect()

#메세지 수신시
@client.event
async def on_message(message):
    global inme
    #봇일 경우 무시
    if message.author == client.user:
        return

    try:
        if str(message.channel.id) == "718436389062180917":
            if message.content.startswith('`'):
                try:
                    channel = message.author.voice.channel
                except:
                    await message.delete()
                    await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 통화방에 입장해야 사용이 가능합니다",colour = 0x2EFEF7))
                    return

                if len(client.voice_clients) > 0:
                    if inme != message.author.voice.channel:
                        await client.voice_clients[0].disconnect()
                        inme = message.author.voice.channel
                        channel = inme
                        await channel.connect()
                else:
                    inme = message.author.voice.channel
                    channel = inme
                    await channel.connect()

                if client.voice_clients[0].is_playing():
                    await message.delete()
                    await message.channel.send("이미 대화 중입니다. 잠시후에 사용해주세요")
                    return

                word = message.content.split('`')[1]
                print(word)
                audio_created = gTTS(text=word, lang='ko', slow=False)
                audio_created.save('bot/ko.mp3')

                voice = client.voice_clients[0]
                voice.play(discord.FFmpegPCMAudio(executable = 'D:/ffmpeg/bin/ffmpeg.exe', source='bot/ko.mp3')) #다운받은 음원 재생
    except:
        await message.delete()
        await message.channel.send("tts 실행 중 오류가 발생하였습니다 다시 시도해주세요")

client.run(token)