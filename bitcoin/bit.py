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
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code
import datetime
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")

driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
driver.get("https://www.bithumb.com/")


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
    
    
    channel = client.get_channel(844801705726967809)
    msg = await channel.send("시작합니다!")
    
    while True:
        try:
            
            Select(driver.find_element_by_xpath('//*[@id="selectRealTick"]')).select_by_visible_text('30분')
            
            list = "업데이트 시각 : " + str(datetime.datetime.now()) + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealBTC_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceBTC_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateBTC_KRW"]').text
            
            list += "비트코인 정보 [변동률 30분]\n<비트코인>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealXRP_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceXRP_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateXRP_KRW"]').text
            
            list += "<리플>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealETH_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceETH_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateETH_KRW"]').text
            
            list += "<이더리움>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            await msg.edit(content=list)
            await asyncio.sleep(1)
        except:
            await msg.edit(content="오류 발생 재접속을 시도합니다")
            driver.get("https://www.bithumb.com/")
            
            
async def back1():
    await client.wait_until_ready()
    
    
    channel = client.get_channel(844830345164750858)
    msg = await channel.send("시작합니다!")
    
    while True:
        try:
            
            Select(driver.find_element_by_xpath('//*[@id="selectRealTick"]')).select_by_visible_text('1시간')
    
            list = "업데이트 시각 : " + str(datetime.datetime.now()) + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealBTC_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceBTC_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateBTC_KRW"]').text
            
            list += "비트코인 정보 [변동률 1시간]\n<비트코인>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealXRP_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceXRP_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateXRP_KRW"]').text
            
            list += "<리플>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealETH_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceETH_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateETH_KRW"]').text
            
            list += "<이더리움>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            await msg.edit(content=list)
            await asyncio.sleep(1)
        except:
            await msg.edit(content="오류 발생 재접속을 시도합니다")
            driver.get("https://www.bithumb.com/")
            
            
async def back12():
    await client.wait_until_ready()
    
    
    channel = client.get_channel(844830636321275945)
    msg = await channel.send("시작합니다!")
    
    while True:
        try:
            
            Select(driver.find_element_by_xpath('//*[@id="selectRealTick"]')).select_by_visible_text('12시간')  
    
            list = "업데이트 시각 : " + str(datetime.datetime.now()) + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealBTC_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceBTC_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateBTC_KRW"]').text
            
            list += "비트코인 정보 [변동률 12시간]\n<비트코인>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealXRP_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceXRP_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateXRP_KRW"]').text
            
            list += "<리플>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealETH_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceETH_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateETH_KRW"]').text
            
            list += "<이더리움>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            await msg.edit(content=list)
            await asyncio.sleep(1)
        except:
            await msg.edit(content="오류 발생 재접속을 시도합니다")
            driver.get("https://www.bithumb.com/")
            
            
async def back24():
    await client.wait_until_ready()
    
    
    channel = client.get_channel(844830659519840257)
    msg = await channel.send("시작합니다!")
    
    while True:
        try:
            
            Select(driver.find_element_by_xpath('//*[@id="selectRealTick"]')).select_by_visible_text('24시간')
    
            list = "업데이트 시각 : " + str(datetime.datetime.now()) + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealBTC_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceBTC_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateBTC_KRW"]').text
            
            list += "비트코인 정보 [변동률 24시간]\n<비트코인>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealXRP_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceXRP_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateXRP_KRW"]').text
            
            list += "<리플>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealETH_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceETH_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateETH_KRW"]').text
            
            list += "<이더리움>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            await msg.edit(content=list)
            await asyncio.sleep(1)
        except:
            await msg.edit(content="오류 발생 재접속을 시도합니다")
            driver.get("https://www.bithumb.com/")
            

async def back0():
    await client.wait_until_ready()
    
    
    channel = client.get_channel(844830680625184788)
    msg = await channel.send("시작합니다!")
    
    while True:
        try:
            
            Select(driver.find_element_by_xpath('//*[@id="selectRealTick"]')).select_by_visible_text('전일대비')
    
            list = "업데이트 시각 : " + str(datetime.datetime.now()) + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealBTC_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceBTC_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateBTC_KRW"]').text
            
            list += "비트코인 정보 [변동률 전일대비]\n<비트코인>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealXRP_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceXRP_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateXRP_KRW"]').text
            
            list += "<리플>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            si = driver.find_element_by_xpath('//*[@id="assetRealETH_KRW"]').text
            ch = driver.find_element_by_xpath('//*[@id="assetRealPriceETH_KRW"]').text
            chpu = driver.find_element_by_xpath('//*[@id="assetRealRateETH_KRW"]').text
            
            list += "<이더리움>\n실시간 시세 : " + si  + "\n변동률 " + ch + " / " + chpu + "\n"
            
            await msg.edit(content=list)
            await asyncio.sleep(1)
        except:
            await msg.edit(content="오류 발생 재접속을 시도합니다")
            driver.get("https://www.bithumb.com/")
            
        
client.loop.create_task(back())
client.loop.create_task(back1())
#client.loop.create_task(back12())
#client.loop.create_task(back24())
#client.loop.create_task(back0())
client.run(token)