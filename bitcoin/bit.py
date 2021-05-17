from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import code
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
driver.get("https://www.bithumb.com/")
driver.implicitly_wait(3)
Select(driver.find_element_by_xpath('//*[@id="selectRealTick"]')).select_by_visible_text('30분')

#clinet
client = discord.Client()
#discord bot tokken
token = code.bittoken

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

async def back():
    await client.wait_until_ready()
    
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        embed = discord.Embed(title="비트코인 정보 [변동률 30분]", color=0x5CD1E5) #임베드 생성

        si = driver.find_element_by_xpath('//*[@id="assetRealBTC_KRW"]').text
        ch = driver.find_element_by_xpath('//*[@id="assetRealPriceBTC_KRW"]').text
        chpu = driver.find_element_by_xpath('//*[@id="assetRealRateBTC_KRW"]').text

        embed.add_field(name="비트코인", value="실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu, inline=False) # 임베드 추가
        
        channel = client.get_channel(839142822556860459)
        await channel.send(embed=embed)
        
        await asyncio.sleep(10)
        
client.loop.create_task(back())
client.run(token)