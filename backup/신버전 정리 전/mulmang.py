#물망초 전용 디스코드 봇

import discord
import asyncio
from discord.ext import commands
import code
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

#clinet
client = discord.Client()
#discord bot tokken
token = code.multoken

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n시스템을 시작합니다" + 
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

    try:
        if message.content == "안녕":
            await message.channel.send("안녕하세요")
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")
        
async def background():
    await client.wait_until_ready()

    while True:
        try:
            driver.get("http://www.twitch.tv/hanmangul")# 사이트 열람
            driver.implicitly_wait(60)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            einput = str(soup.select('#root > div > div.tw-flex.tw-flex-column.tw-flex-nowrap.tw-full-height > div > main > div.root-scrollable.scrollable-area > div.simplebar-scroll-content > div > div > div.channel-root.channel-root--hold-chat.channel-root--live.channel-root--home.channel-root--unanimated > div.tw-flex.tw-flex-column > div.channel-root__info.channel-root__info--home > div > div.home-header-sticky.tw-mg-auto.tw-pd-t-2 > div.tw-align-items-center.tw-flex.tw-justify-content-between.tw-mg-b-2 > div.tw-align-items-start.tw-flex.tw-full-width > div.tw-mg-r-1 > div > div > a > div.ScHaloIndicator-sc-1l14b0i-1.jYqVGu.tw-halo__indicator > div > div > div > div > p'))
            print(einput)
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(60*1)

#선언
client.loop.create_task(background())
client.run(token)