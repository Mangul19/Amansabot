from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from selenium.webdriver.chrome.options import Options
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code
import time

#clinet
client = discord.Client()
#discord bot tokken
token = code.lohtoken
#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=854x480')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

iruain = True

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n로오히 반자동 쿠폰 수령 시스템을 시작합니다" + 
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
    print(str(message.author) + str(message.author.mention) + " : " + str(message.content))

    global iruain

    try:
        CHin = str(message.channel)
        if CHin != '질문채널' and CHin != '도움채널':
            if message.content != "!!help" and message.content.startswith("!!등록") == False and message.content.startswith("!!쿠폰등록") == False:
                await message.channel.send("대화는 금지!")
                await message.delete()
                return

        if CHin == '질문채널':
            if message.content == "!!help" or message.content.startswith("!!등록") or message.content.startswith("!!쿠폰등록"):
                await message.channel.send("여기는 질문창입니다 명령어는 명령어-입력-채널 에 입력해주세요")
                await message.delete()
                return

        if message.content == "!!help":
            await message.delete()
            embed = discord.Embed(title="명령어", color=0x5CD1E5)
            embed.add_field(name="!!등록 ID", value="'ID'를 등록하고 만료되지 않은 모든 쿠폰 수령을 시도합니다\nEX) !!등록 A1B2C34DE56F", inline=False)
            embed.add_field(name="!!쿠폰등록 쿠폰번호", value="쿠폰번호를 등록합니다 등록하면 ID 리스트에 등록된 모든 사람들에게 쿠폰 수령을 시도합니다\nEX) !!쿠폰등록 LOH1BDAY", inline=False)
            await message.channel.send( embed=embed)

        if message.content.startswith("!!등록"): #로오히 ID 리스트에 사용자 등록
            trsText = message.content.split(" ")[1]
            await message.delete()

            dirloh = db.reference('loh/') #ID 리스트 가져오기
            lohch = dirloh.get()
            lohch = list(lohch.values())

            if trsText in lohch: #해당 ID가 있다면
                await message.channel.send(message.author.mention + "님은 해당 ID는 이미 등록되어있습니다")
            else:# 없다면 리스트로 저장
                dirlohcou = db.reference('lohcou/') #ID 리스트 가져오기
                lohcou = dirlohcou.get()
                lohcouch = list(lohcou.keys())

                send = str(message.author)
                send = send.split("#")
                send = send[0] + "*" + send[1] # 송출자 ID 설정
                idput = 0
                if send in lohcouch: #해당 ID가 있다면
                    idput = lohcou[send] + 1
                else:
                    print("새로운 유저입니다")

                if idput >= 3:
                    await message.channel.send(message.author.mention + "님 등록 가능 ID수가 초과되었습니다")
                    return

                await message.channel.send(message.author.mention + "님 해당 ID 등록과 함께 쿠폰 작업을 시작합니다\n보안을 위해 ID가 포함된 메시지는 삭제됩니다")
                irua = True

                dirlohcu = db.reference('lohcu/') #쿠키 리스트 가져오기
                lohcuch = dirlohcu.get()
                lohcuch = list(lohcuch.values())
                coochcu = lohcuch
                get = []
                embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                count = 0

                for inpu in lohcuch:
                    driver.get("https://www.coupon.lordofheroes.com/")
                    driver.implicitly_wait(2)
                    
                    driver.find_element_by_id('comp-k7bccwio').click()
                    driver.find_element_by_id('input_comp-k7bccwio').send_keys(inpu)
                    driver.find_element_by_id('comp-k7bcdh0c').click()
                    driver.find_element_by_id('input_comp-k7bcdh0c').send_keys(trsText)
                                        
                    alertin = ""
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span")))
                        alertin = driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span').get_attribute("innerHTML")
                        driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[3]').click()
                    except:
                        alertin = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/main/div/div/div[2]/div/div/div/div[6]/p/span/span').get_attribute("innerHTML")
                        while alertin == "USER ID 확인을 하고 다시 입력해주세요" or alertin == " ":

                            driver.get("https://www.google.com/")
                            driver.implicitly_wait(10)
                            print("오류로 초기화")
                            
                            driver.get("https://www.coupon.lordofheroes.com/")
                            driver.implicitly_wait(2)
                            
                            driver.find_element_by_id('comp-k7bccwio').click()
                            driver.find_element_by_id('input_comp-k7bccwio').send_keys(inpu)
                            driver.find_element_by_id('comp-k7bcdh0c').click()
                            driver.find_element_by_id('input_comp-k7bcdh0c').send_keys(trsText)
                            driver.find_element_by_xpath("//*[@id='comp-k7bces4d']/button").click()

                            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span")))
                            alertin = driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span').get_attribute("innerHTML")
                            driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[3]').click()
                                
                    embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value=alertin, inline=False)

                    if alertin == "USER ID 오류":
                        embed.add_field(name="ID 확인요청", value="ID를 다시 확인하여 주세요", inline=False)
                        await message.channel.send(embed=embed)
                        return
                    elif alertin == "쿠폰 사용 기간 오류":
                        get.append(inpu)

                    count += 1
                    if count == 20:
                        embed.add_field(name="쿠폰 지급 중간 안내", value="안내된 계정은 지급이 완료 되었으며 남은 계정에 지급 신청을 계속합니다", inline=False)
                        await message.channel.send(embed=embed)
                        embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                        count = 0

                    if irua:
                        dirloh.update({str(len(lohch)):trsText})
                        irua = False

                if len(get) > 0:
                    dirlohcu.delete()
                    for delin in get:
                        coochcu.remove(delin)

                    if len(coochcu) == 0:
                        coochcu.append('LOH1BDAY')

                    dirlohcu.update({'00':coochcu[0]})
                    count = 1

                    if len(coochcu) > 1:
                        for inin in coochcu[1:]:
                            dirlohcu.update({count:inin})
                            count += 1
                
                dirlohcou.update({send:idput})

                dirlohsend = db.reference('lohinlist/' + send) #쿠키 리스트 가져오기
                lohsend = dirlohsend.get()
                
                if lohsend == None:
                    lohsend = 00
                else:
                    lohsend = len(lohsend)

                dirlohsend.update({str(lohsend):trsText})
                
                embed.add_field(name="ID를 정상적으로 등록하였습니다",value="앞으로 누군가 쿠폰을 최초 등록하면 이 계정에 쿠폰이 자동 수령됩니다", inline=False)
                await message.channel.send(embed=embed)

        if message.content.startswith("!!쿠폰등록"): #로오히 ID 리스트에 사용자 등록
            if iruain == False:
                await message.channel.send("해당명령어는 다른분이 사용중 입니다 잠시 후 다시 시도해주세요")
                return
                     
            await message.channel.send("쿠폰 등록을 실행합니다 잠시만 기다려 주세요\n시간이 다소 걸리니 처리 완료까지 기다려주세요")
            trsText = str(message.content.split(" ")[1])

            dirlohcu = db.reference('lohcu/') #로오히 쿠폰 리스트 가져오기
            lohcuch = dirlohcu.get()
            lohcuch = list(lohcuch.values())

            if trsText not in lohcuch: #해당 쿠폰이 없다면 실행
                dirloh = db.reference('loh/') #ID 리스트 가져오기
                lohch = dirloh.get()
                lohch = list(lohch.values())

                embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                count = 0

                for inpu in lohch:
                    driver.get("https://www.coupon.lordofheroes.com/")
                    driver.implicitly_wait(2)
                    
                    driver.find_element_by_id('comp-k7bccwio').click()
                    driver.find_element_by_id('input_comp-k7bccwio').send_keys(inpu)
                    driver.find_element_by_id('comp-k7bcdh0c').click()
                    driver.find_element_by_id('input_comp-k7bcdh0c').send_keys(trsText)
                    driver.find_element_by_xpath("//*[@id='comp-k7bces4d']/button").click()
                    
                    alertin = ""
                    try:
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span")))
                        alertin = driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span').get_attribute("innerHTML")
                        driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[3]').click()
                    except:
                        alertin = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/main/div/div/div[2]/div/div/div/div[6]/p/span/span').get_attribute("innerHTML")
                        while alertin == "USER ID 확인을 하고 다시 입력해주세요" or alertin == "​ " or alertin == "​쿠폰 번호 오류" or alertin == "쿠폰 사용 기간 오류":

                            driver.get("https://www.google.com/")
                            driver.implicitly_wait(10)
                            print("오류로 초기화")
                            
                            driver.get("https://www.coupon.lordofheroes.com/")
                            driver.implicitly_wait(2)
                            
                            driver.find_element_by_id('comp-k7bccwio').click()
                            driver.find_element_by_id('input_comp-k7bccwio').send_keys(inpu)
                            driver.find_element_by_id('comp-k7bcdh0c').click()
                            driver.find_element_by_id('input_comp-k7bcdh0c').send_keys(trsText)
                            driver.find_element_by_xpath("//*[@id='comp-k7bces4d']/button").click()

                            try:
                                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span")))
                                alertin = driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/p/span/span/span/span/span').get_attribute("innerHTML")
                                driver.find_element_by_xpath('/html/body/div/div/div[4]/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[3]').click()
                            except:
                                print("오류 코드 : " + alertin)
       
                    embed.add_field(name=inpu[:2] + "----- 님에게 " + trsText + " 지급 신청", value=alertin, inline=False)

                    if alertin == "쿠폰 번호 오류":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        await message.channel.send(embed=embed)
                        iruain = True
                        return
                    elif alertin == "쿠폰 사용 기간 오류":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        await message.channel.send(embed=embed)
                        iruain = True
                        return

                    if iruain:
                        iruain = False
                        dirlohcu.update({str(len(lohcuch)):trsText})

                    count += 1
                    if count == 20:
                        embed.add_field(name="쿠폰 지급 중간 안내", value="안내된 계정은 지급이 완료 되었으며 남은 계정에 지급 신청을 계속합니다", inline=False)
                        await message.channel.send(embed=embed)
                        embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                        count = 0
 
                embed.add_field(name= "@everyone" + "쿠폰 지급 최종 안내", value=str(len(lohch)) + "명 계정에 새로 등록된 쿠폰 지급 신청을 완료하였습니다", inline=False)
                await message.channel.send(embed=embed)

                channel = client.get_channel(836612578444181504)
                await channel.send("@everyone 새로운 " + trsText + " 쿠폰이 등록되어 쿠폰을 일괄 지급하였습니다 확인하여주세요\n쿠폰을 입력해주신 " + message.author.mention + "님 감사합니다\n 귀하의 입력에 " + str(len(lohch)) + "분이 자동 수령을 받으셨습니다")

                iruain = True
            else:
                await message.channel.send("이미 등록된 쿠폰입니다")
    except:
        iruain = True
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")
        await message.delete()

client.run(token)