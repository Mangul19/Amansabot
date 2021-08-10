import discord
import asyncio
from discord.ext import commands
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code
import re
import youtube_dl
import random
import pafy

intents = discord.Intents.all()
#clinet
client = discord.Client(intents=intents)
#discord bot tokken
token = code.token

songlist = []
now = ""
count = 0

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n어만사 음악 시스템을 시작합니다" + 
        "\n==========================================")

#정보 변화시
@client.event
async def on_voice_state_update(member, before, after):
    global count
    global songlist
    global now

    #봇일 경우 무시
    if member == client.user:
        return

    if before.channel == None or before.channel.id != 751452064865058867:
        if after.channel.id == 751452064865058867:
            count += 1
    elif before.channel.id == 751452064865058867:
        if after.channel == None or after.channel.id != 751452064865058867:
            count -= 1

            if count == 0 and len(client.voice_clients) > 0:
                channel = client.get_channel(873984166897807470)
                await channel.send(embed=discord.Embed(title="복합방에서 모두 퇴장하셨습니다 연결을 종료합니다",colour = 0x2EFEF7))
                await client.voice_clients[0].disconnect()
                songlist = []
                now = "없음"

#메세지 수신시
@client.event
async def on_message(message):
    global now

    #봇일 경우 무시
    if message.author == client.user:
        return

    #받은 메세지 및 입력자 출력
    if message.channel.id == 873984166897807470:
        print(str(message.author) + str(message.author.mention) + " : " + str(message.content))
        if not message.content.startswith("!취소") and not message.content == ("!재생목록") and not message.content == ("!음악") and not message.content.startswith("!추가") and not message.content == ("!일시정지") and not message.content == ("!재생") and not message.content == ("!스킵"):
            await message.delete()
            await message.channel.send("해당방은 뮤직 시스템 전용방입니다")
            return
    else:
        if message.content.startswith("!취소") or message.content == ("!재생목록") or message.content == ("!음악") or message.content.startswith("!추가") or message.content == ("!일시정지") or message.content == ("!재생") or message.content == ("!스킵"):
            await message.delete()
            await message.channel.send("해당방에서는 뮤직 시스템 이용이 불가능 합니다")
            return
        return

    if message.content == ("!음악"):
        embed = discord.Embed(title="음악 시스템 명령어", color=0x5CD1E5)
        embed.add_field(name="!추가 'URL'", value="음악을 재생하며 이미 재생중일때는 재생목록에 추가합니다", inline=False)
        embed.add_field(name="!일시정지", value="음악을 일시중지합니다", inline=False)
        embed.add_field(name="!재생", value="일시중지한 음악을 다시 재생합니다", inline=False)
        embed.add_field(name="!스킵", value="현재 음악을 스킵하고 다음 곡으로 넘어갑니다", inline=False)
        embed.add_field(name="!재생목록", value="현재 재생중인 음악 포함 재생목록을 보여줍니다", inline=False)
        embed.add_field(name="!취소 '번호'", value="재생목록의 번호 번째 항목을 제거합니다", inline=False)
        embed.set_footer(text="음량은 기본적으로(20%) 기본 설정되어있으며 복합방에서만 재생이 가능합니다")
        await message.channel.send(embed=embed)

    try:
        channel = message.author.voice.channel
        if channel.id != 751452064865058867:
            await message.delete()
            await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 복합방에서만 이용이 가능합니다",colour = 0x2EFEF7))
            return
    except:
        await message.delete()
        await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 통화방에 입장해야 사용이 가능합니다",colour = 0x2EFEF7))
        return

    if message.content.startswith("!추가"):
        try:
            if message.content.split(" ")[1] == None:
                await message.channel.send(embed=discord.Embed(title=":no_entry_sign: url을 제대로 입력해주세요.",colour = 0x2EFEF7))
                await message.delete()
                return

            url = message.content.split(" ")[1]
            if "&list=" in url:
                await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 리스트는 재생이 불가능합니다",colour = 0x2EFEF7))
                await message.delete()
                return

            url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', url) #정규 표현식을 사용해 url 검사
            if url1 == None:
                await message.channel.send(embed=discord.Embed(title=":no_entry_sign: youtube만 재생이 가능합니다",colour = 0x2EFEF7))
                await message.delete()
                return

            if len(client.voice_clients) > 0:
                if client.voice_clients[0].is_playing():
                    video = pafy.new(url)
                    await message.channel.send(embed=discord.Embed(title="이미 봇이 음악을 재생중입니다\n" + video.title + " 을 재생목록에 추가합니다",colour = 0x2EFEF7))
                    songlist.append(url)
                else:
                    now = url
                    play(url)
                    video = pafy.new(url)
                    await message.channel.send(embed=discord.Embed(title=video.title + " 을 재생합니다",colour = 0x2EFEF7))
            else:
                channel = message.author.voice.channel
                await channel.connect()
                now = url
                play(url)
                video = pafy.new(url)
                await message.channel.send(embed=discord.Embed(title=video.title + " 을 재생합니다",colour = 0x2EFEF7))
        except:
            await message.delete()
            await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 잘못입력하여 인식이 중지되었습니다",colour = 0x2EFEF7))

    if message.content == ("!일시정지"):
        if not client.voice_clients[0].is_paused():
            client.voice_clients[0].pause()
            await message.channel.send(embed=discord.Embed(title="곡 재생을 일시정지 하였습니다",colour = 0x2EFEF7))
        else:
            await message.channel.send(embed=discord.Embed(title="이미 일시정지 상태입니다",colour = 0x2EFEF7))

    if message.content == ("!재생"):
        try:
            if client.voice_clients[0].is_paused():
                client.voice_clients[0].resume()
                video = pafy.new(now)
                await message.channel.send(embed=discord.Embed(title="곡을 다시 재생합니다\n 현재곡은 " + video.title + " 입니다",colour = 0x2EFEF7))
            elif client.voice_clients[0].is_playing():
                await message.channel.send(embed=discord.Embed(title="이미 재생 상태입니다",colour = 0x2EFEF7))
            else:
                await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 재생정보가 없습니다",colour = 0x2EFEF7))
        except:
            await message.delete()
            await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 재생정보가 없습니다",colour = 0x2EFEF7))
    
    if message.content == ("!스킵"):
        try:
            if client.voice_clients[0].is_playing():
                if len(songlist) > 0:
                    now = songlist[0]
                    video = pafy.new(now)
                    await message.channel.send(embed=discord.Embed(title="곡을 스킵하였습니다\n" + video.title + " 을 재생합니다",colour = 0x2EFEF7))
                    client.voice_clients[0].stop()
                else:
                    await message.channel.send(embed=discord.Embed(title="더이상 곡이 없습니다 종료합니다",colour = 0x2EFEF7))
                    await client.voice_clients[0].disconnect()
        except:
            await message.channel.send(embed=discord.Embed(title="이미 정지 상태입니다",colour = 0x2EFEF7))
    
    if message.content == ("!재생목록"):
        if now == "없음":
           await message.channel.send(embed=discord.Embed(title="음악을 재생하고 있지 않습니다",colour = 0x2EFEF7)) 
           await message.delete()
           return

        cou = 0

        embed = discord.Embed(title="음악 재생목록", color=0x5CD1E5)
        video = pafy.new(now)
        embed.add_field(name="[현재] 번호 : " + str(cou) + "\n제목 : " + video.title, value="길이 : " + str(video.length // 60) + "분 " + str(round(video.length % 60, 2)) + "초", inline=False)

        for inname in songlist:
            cou += 1
            video = pafy.new(inname)
            embed.add_field(name="번호 : " + str(cou) + "\n제목 : " + video.title, value="길이 : " + str(video.length // 60) + "분 " + str(round(video.length % 60, 2)) + "초", inline=False)

        await message.channel.send(embed=embed)

    if message.content.startswith("!취소"):
        try:
            num = int(float(message.content.split(" ")[1]))

            if num == 0:
                await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 현재 재생중인 곡은 !스킵 으로 넘어가 주세요",colour = 0x2EFEF7))
                await message.delete()
                return
            elif num < 1 or num > len(songlist):
                await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 번호를 다시 확인해 주세요",colour = 0x2EFEF7))
                await message.delete()
                return
        except:
            await message.channel.send(embed=discord.Embed(title=":no_entry_sign: 번호를 다시 확인해 주세요",colour = 0x2EFEF7))
            await message.delete()
            return

        num -= 1
        video = pafy.new(songlist[num])
        await message.channel.send(embed=discord.Embed(title=video.title + " 을 취소 하였습니다",colour = 0x2EFEF7))
        songlist.pop(num)

    await message.delete()

def play_next():
    global now
    
    if len(songlist) > 0:
        now = songlist[0]
        play(songlist[0])
        songlist.pop(0)
    else:
        now = "없음"

def play(url):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
    voice = client.voice_clients[0]
    voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS, executable="D:/ffmpeg/bin/ffmpeg.exe"),after=lambda e: play_next())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.2

client.run(token)