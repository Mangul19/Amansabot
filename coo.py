from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#clinet
client = discord.Client()
#discord bot tokken
cotoken = code.token
#firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

idin = {"mulmangul19@gmail.com","a94640020@gmail.com","vvyj4rawhn@privaterelay.appleid.com","kangsb9999@gmail.com","tdj666@naver.com","rladjsdk56@gmail.com","fourd0513@gmail.com","kgh9879@gmail.com"
    ,"tear_s1004@naver.com"}

code = "KINGDOMYUNIKO720"

warnings.filterwarnings(action='ignore')

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n시스템을 시작합니다" + 
        "\n==========================================")
    # 이 기능을 이용하여 봇의 상태를 출력
    mssg = discord.Game("!!help|Made by Han_MangUl")
    await client.change_presence(status=discord.Status.online, activity=mssg)

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return

    #받은 메세지 출력
    print(message.content)

    try:
        if message.content == "!!실행":
            driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

            dircooking = db.reference('cooking/')
            cooking = dircooking.get()
            cookingkey = list(cooking.keys())

            embed = discord.Embed(title="처리내용", color=0x5CD1E5)

            for inpu in cookingkey:
                driver.get("https://game.devplay.com/coupon/ck/ko")
                driver.implicitly_wait(5)
                driver.find_element_by_id('email-box').send_keys(inpu)
                driver.find_element_by_id('code-box').send_keys(code)
                driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                embed.add_field(name=inpu[:2] + "*****@" + inpu.split('@')[1] + "님에게 " + code + " 쿠폰 지급 신청을 합니다", value=driver.switch_to_alert().text, inline=False)
                driver.switch_to_alert().accept()
            
            await message.channel.send( embed=embed)
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")



driver.close()