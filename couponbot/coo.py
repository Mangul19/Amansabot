from selenium import webdriver
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

#clinet
client = discord.Client()
#discord bot tokken
token = code.cotoken
#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

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

    #받은 메세지 및 입력자 출력
    print(str(message.author) + str(message.author.mention) + " : " + str(message.content))

    global driver

    try:
        CHin = str(message.channel)
        if CHin != '질문채널' and CHin != '도움채널':
            if message.content != "!!help" and message.content.startswith("!!등록") == False and message.content.startswith("!!쿠폰등록") == False and message.content.startswith("!!게스트") == False and message.content.startswith("!!쿠폰리스트") == False and message.content.startswith("!!당첨확인") == False:
                await message.channel.send("대화는 금지!")
                await message.delete()
                return

        if CHin == '질문채널':
            if message.content == "!!help" or message.content.startswith("!!등록") or message.content.startswith("!!쿠폰등록") or message.content.startswith("!!게스트") or message.content.startswith("!!쿠폰리스트") or message.content.startswith("!!당첨확인"):
                await message.channel.send("여기는 질문창입니다 명령어는 명령어-입력-채널 에 입력해주세요")
                await message.delete()
                return

        if message.content == "!!help":
            await message.delete()
            embed = discord.Embed(title="명령어", color=0x5CD1E5)
            embed.add_field(name="!!등록 ID", value="'ID'를 등록하고 만료되지 않은 모든 쿠폰 수령을 시도합니다\nEX) !!등록 TEST@gmail.com", inline=False)
            embed.add_field(name="!!게스트 ID", value="ID에 만료되지 않은 모든 쿠폰 수령을 시도합니다\n게스트 아이디 전용\nEX) !!게스트 GUEST-123456", inline=False)
            embed.add_field(name="!!쿠폰등록 쿠폰번호", value="쿠폰번호를 등록합니다 등록하면 ID 리스트에 등록된 모든 사람들에게 쿠폰 수령을 시도합니다\nEX) !!쿠폰등록 KINGDOMWELOVEYOU", inline=False)
            embed.add_field(name="!!쿠폰리스트", value="쿠폰번호를 리스트를 안내해드립니다", inline=False)
            embed.add_field(name="<이벤트 종료>!!당첨확인 MID", value="10억 감사제 당첨 내역을 조회해드립니다\n주의사항 : 계정 ID가 아닌 MID를 입력하여야합니다\nMID는 게임 접속 후 계정 ID 아래에 위치해있습니다", inline=False)
            await message.channel.send( embed=embed)

        if message.content.startswith("!!등록"): #쿠킹덤 ID 리스트에 사용자 등록
            trsText = message.content.split(" ")[1]
            await message.delete()

            dircooking = db.reference('cooking/') #ID 리스트 가져오기
            cookingch = dircooking.get()
            cookingch = list(cookingch.values())

            if trsText in cookingch: #해당 ID가 있다면
                await message.channel.send(message.author.mention + "님 해당 아이디는 이미 등록되어있습니다")
            else:# 없다면 리스트로 저장
                dircookingcou = db.reference('cookingcou/') #ID 리스트 가져오기
                cookingcou = dircookingcou.get()
                cookingcouch = list(cookingcou.keys())

                send = str(message.author)
                send = send.split("#")
                send = send[0] + "*" + send[1] # 송출자 ID 설정
                idput = 0
                if send in cookingcouch: #해당 ID가 있다면
                    idput = cookingcou[send] + 1
                else:
                    print("새로운 유저입니다")

                if idput >= 3:
                    await message.channel.send(message.author.mention + "님 등록 가능 ID수가 초과되었습니다")
                    return

                await message.channel.send(message.author.mention + "님 등록과 함께 쿠폰 작업을 시작합니다\n보안을 위해 ID가 포함된 메시지는 삭제됩니다")
                irua = True
                
                dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
                coocuch = dircoocu.get()
                coocuch = list(coocuch.values())
                coochcu = coocuch
                get = []
                embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                count = 0

                for inpu in coocuch:
                    driver.get("https://game.devplay.com/coupon/ck/ko")
                    driver.implicitly_wait(3)
                    driver.find_element_by_id('email-box').send_keys(trsText)
                    driver.find_element_by_id('code-box').send_keys(inpu)
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                    WebDriverWait(driver, 1).until(EC.alert_is_present())
                    alertin = driver.switch_to_alert().text
                    if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                        embed.add_field(name=trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청", value=alertin, inline=False)
                    driver.switch_to_alert().accept()

                    if alertin == "DevPlay 계정을 다시 한번 확인해주세요.":
                        embed.add_field(name="ID 확인요청", value="ID를 다시 확인하여 주세요", inline=False)
                        await message.channel.send(embed=embed)
                        return
                    elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                        get.append(inpu)

                    while alertin == "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                        await message.channel.send("데브 사이트 서버 오류 확인 재시작합니다")
                        driver.close()
                        driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
                        driver.get("https://game.devplay.com/coupon/ck/ko")
                        driver.implicitly_wait(3)
                        driver.find_element_by_id('email-box').send_keys(trsText)
                        driver.find_element_by_id('code-box').send_keys(inpu)
                        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                        WebDriverWait(driver, 1).until(EC.alert_is_present())
                        alertin = driver.switch_to_alert().text
                        if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                            embed.add_field(name=trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청", value=alertin, inline=False)
                        driver.switch_to_alert().accept()

                    count += 1
                    if count == 20:
                        embed.add_field(name="쿠폰 지급 중간 안내", value="안내된 계정은 지급이 완료 되었으며 남은 계정에 지급 신청을 계속합니다", inline=False)
                        await message.channel.send(embed=embed)
                        embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                        count = 0
                    
                    if irua:
                        dircooking.update({str(len(cookingch)):trsText})
                        irua = False

                if len(get) > 0:
                    dircoocu.delete()
                    for delin in get:
                        coochcu.remove(delin)

                    if len(coochcu) == 0:
                        coochcu.append('KINGDOMWELOVEYOU')

                    dircoocu.update({'00':coochcu[0]})
                    count = 1

                    if len(coochcu) > 1:
                        for inin in coochcu[1:]:
                            dircoocu.update({count:inin})
                            count += 1

                dircookingcou.update({send:idput})

                dircoosend = db.reference('cooinlist/' + send) #쿠키 리스트 가져오기
                coosend = dircoosend.get()
                
                if coosend == None:
                    coosend = 00
                else:
                    coosend = len(coosend)

                dircoosend.update({str(coosend):trsText})

                embed.add_field(name="ID를 정상적으로 등록하였습니다",value="앞으로 누군가 쿠폰을 최초 등록하면 이 계정에 쿠폰이 자동 수령됩니다", inline=False)
                await message.channel.send(embed=embed)

        if message.content.startswith("!!쿠폰등록"): #쿠킹덤 ID 리스트에 사용자 등록
            await message.channel.send("쿠폰 등록을 실행합니다 잠시만 기다려 주세요\n시간이 다소 걸리니 처리 완료까지 기다려주세요")
            trsText = message.content.split(" ")[1].upper()

            dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
            coocuch = dircoocu.get()
            coocuch = list(coocuch.values())

            if trsText not in coocuch: #해당 쿠폰이 없다면 실행
                irua = True
                
                dircooking = db.reference('cooking/') #ID 리스트 가져오기
                cookingch = dircooking.get()
                cookingch = list(cookingch.values())

                embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                count = 0

                for inpu in cookingch:
                    driver.get("https://game.devplay.com/coupon/ck/ko")
                    driver.implicitly_wait(3)
                    driver.find_element_by_id('email-box').send_keys(inpu)
                    driver.find_element_by_id('code-box').send_keys(trsText)
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                    WebDriverWait(driver, 1).until(EC.alert_is_present())
                    alertin = driver.switch_to_alert().text
                    if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                        embed.add_field(name=inpu[:2] + "-----@" + inpu.split('@')[1] + "님에게 " + trsText + " 지급 신청", value=alertin, inline=False)
                    driver.switch_to_alert().accept()

                    if alertin == "쿠폰번호는 16자리입니다. 다시 한 번 확인해 주세요.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        await message.channel.send(embed=embed)
                        return
                    elif alertin == "쿠폰번호를 다시 한번 확인해주세요.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        await message.channel.send(embed=embed)
                        return
                    elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        await message.channel.send(embed=embed)
                        return
                    
                    while alertin == "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                        await message.channel.send("데브 사이트 서버 오류 확인 재시작합니다")
                        driver.close()
                        driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
                        driver.get("https://game.devplay.com/coupon/ck/ko")
                        driver.implicitly_wait(3)
                        driver.find_element_by_id('email-box').send_keys(inpu)
                        driver.find_element_by_id('code-box').send_keys(trsText)
                        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                        WebDriverWait(driver, 1).until(EC.alert_is_present())
                        alertin = driver.switch_to_alert().text
                        if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                            embed.add_field(name=inpu[:2] + "-----@" + inpu.split('@')[1] + "님에게 " + trsText + " 지급 신청", value=alertin, inline=False)
                        driver.switch_to_alert().accept()

                    count += 1
                    if count == 20:
                        embed.add_field(name="쿠폰 지급 중간 안내", value="안내된 계정은 지급이 완료 되었으며 남은 계정에 지급 신청을 계속합니다", inline=False)
                        await message.channel.send(embed=embed)
                        embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                        count = 0
                    
                    if irua:
                        dircoocu.update({str(len(coocuch)):trsText})
                        irua = False
                
                embed.add_field(name= "쿠폰 지급 최종 안내", value=str(len(cookingch)) + "명 계정에 새로 등록된 쿠폰 지급 신청을 완료하였습니다", inline=False)
                await message.channel.send(embed=embed)

                channel = client.get_channel(865421064398045184)
                await channel.send("@everyone 새로운 " + trsText + " 쿠폰이 등록되어 쿠폰을 일괄 지급하였습니다 확인하여주세요\n쿠폰을 입력해주신 " + message.author.mention + "님 감사합니다\n 귀하의 입력에 " + str(len(cookingch)) + "분이 자동 수령을 받으셨습니다")
            else:
                await message.channel.send(message.author.mention + "님 해당 쿠폰은 이미 등록된 쿠폰입니다")
        
        if message.content.startswith("!!게스트"): #게스트 아이디 사용
            trsText = message.content.split(" ")[1]
            await message.delete()

            await message.channel.send(message.author.mention + "님 쿠폰 작업을 시작합니다\n보안을 위해 ID가 포함된 메시지는 삭제됩니다\n게스트 계정 쿠폰 수령은 1회성으로 ID 등록이 되진 않습니다")

            if trsText.split('-')[0] != "GUEST" and trsText.split('-')[0] != "guest":
                await message.channel.send("해당명령어는 게스트 계정을 위한 1회용 일괄 수령 시스템입니다 정규 계정은 다른 명령어를 이용해주세요")
                return

            dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
            coocuch = dircoocu.get()
            coocuch = list(coocuch.values())
            coochcu = coocuch
            get = []

            embed = discord.Embed(title="처리내용", color=0x5CD1E5)
            count = 0

            for inpu in coocuch:
                driver.get("https://game.devplay.com/coupon/ck/ko")
                driver.implicitly_wait(3)
                driver.find_element_by_id('email-box').send_keys(trsText)
                driver.find_element_by_id('code-box').send_keys(inpu)
                driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                WebDriverWait(driver, 1).until(EC.alert_is_present())
                alertin = driver.switch_to_alert().text
                if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                    embed.add_field(name=trsText.split('-')[0]  + " 아이디 인식, 번호 : "  + trsText.split('-')[1][:2]+ "-----" + "님에게 " + inpu + " 지급 신청", value=alertin, inline=False)
                driver.switch_to_alert().accept()

                if alertin == "DevPlay 계정을 다시 한번 확인해주세요.":
                    embed.add_field(name="ID 확인요청", value="ID를 다시 확인하여 주세요", inline=False)
                    await message.channel.send(embed=embed)
                    return
                elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                    get.append(inpu)

                while alertin == "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                    await message.channel.send("데브 사이트 서버 오류 확인 재시작합니다")
                    driver.close()
                    driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
                    driver.get("https://game.devplay.com/coupon/ck/ko")
                    driver.implicitly_wait(3)
                    driver.find_element_by_id('email-box').send_keys(trsText)
                    driver.find_element_by_id('code-box').send_keys(inpu)
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                    WebDriverWait(driver, 1).until(EC.alert_is_present())
                    alertin = driver.switch_to_alert().text
                    if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
                        embed.add_field(name=trsText.split('-')[0]  + " 아이디 인식, 번호 : "  + trsText.split('-')[1][:2]+ "-----" + "님에게 " + inpu + " 지급 신청", value=alertin, inline=False)
                    driver.switch_to_alert().accept()

                count += 1
                if count == 20:
                    embed.add_field(name="쿠폰 지급 중간 안내", value="안내된 계정은 지급이 완료 되었으며 남은 계정에 지급 신청을 계속합니다", inline=False)
                    await message.channel.send(embed=embed)
                    embed = discord.Embed(title="처리내용", color=0x5CD1E5)
                    count = 0

            if len(get) > 0:
                dircoocu.delete()
                for delin in get:
                    coochcu.remove(delin)
                    print(coocuch)

                dircoocu.update({'00':coochcu[0]})
                count = 1

                for inin in coochcu[1:]:
                    dircoocu.update({count:inin})
                    count += 1

            await message.channel.send(embed=embed)

        if message.content == "!!쿠폰리스트": #쿠킹덤 ID 리스트에 사용자 등록
            await message.channel.send("쿠폰 리스트를 불러옵니다")

            dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
            coocuch = dircoocu.get()
            coocuch = list(coocuch.values())

            embed = discord.Embed(title="쿠폰 리스트", color=0x5CD1E5)
            count = 0
            incount = 1

            for inpu in coocuch:
                embed.add_field(name=str(incount) + "번 쿠폰", value=inpu, inline=False)

                count += 1
                incount += 1
                if count == 20:
                    embed.add_field(name="쿠폰 리스트 중간 안내", value="남은 쿠폰리스트를 계속 불러옵니다", inline=False)
                    await message.channel.send(embed=embed)
                    embed = discord.Embed(title="쿠폰 리스트", color=0x5CD1E5)
                    count = 0
            
            await message.channel.send(embed=embed)
            
        if message.content.startswith("!!당첨확인"): #당첨확인
            await message.channel.send(message.author.mention + "님의 해당이벤트는 현재 종료되었습니다")
            return


            trsText = message.content.split(" ")[1]
            await message.delete()
            
            embed = discord.Embed(title="처리내용", color=0x5CD1E5)
             
            driver.get("https://thanks10m.cookierun-kingdom.com/ko/")
            driver.implicitly_wait(3)
            driver.find_element_by_xpath('//*[@id="top"]/div[3]/form/input').send_keys(trsText)
            driver.find_element_by_xpath('//*[@id="btn-mid-check"]').click()
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alertin = driver.switch_to_alert().text
            driver.switch_to_alert().accept()
            
            embed.add_field(name=trsText[:2] + "-----" + "님의 당첨 조회 결과 입니다", value=alertin, inline=False)
            await message.channel.send(embed=embed)
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")
        await message.delete()

async def background(): #자동 공지
    await client.wait_until_ready()
    await asyncio.sleep(60*60*6)

    while True:
        try:
            embed = discord.Embed(title="자동 안내", description="여러가지 문의 및 기능 추가 요청 등의 사항은 언제나 받고 있으니 자유로이 말씀해주시기 바랍니다\n" +
                "제 시스템을 이용해주셔서 감사합니다\n" +
                "새로 오신분들 필독 꼭! 확인해주세요\n" +
                "이 디코는 기본적으로 멘션 @ 태그로만 알림이 가도록 설정되어있으니 참고하여 주세요\n" +
                "새 쿠폰이 인식되었을때 자동 수령을 받기 위해서는 ID 등록을 최초 한번 하셔야합니다\n" +
                "오류나 기타 문의시에는 @Han_MangUl 로 관리자를 호출해주세요\n", color=0x5CD1E5)
            embed.set_footer(text="12시간 주기로 자동 안내됩니다")

            channel = client.get_channel(836191919935324170)
            await channel.send(embed=embed)
        except:
            print("오류 발생 다음에 다시 시도합니다")

        await asyncio.sleep(60*60*12)

#client.loop.create_task(background())
client.run(token)