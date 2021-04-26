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
import code

#clinet
client = discord.Client()
#discord bot tokken
token = code.cotoken
#firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

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
        CHin = str(message.channel)
<<<<<<< HEAD
        if CHin != '등록채널' and CHin != '질문채널':
            if message.content != "!!help" and message.content.startswith("!!등록") == False and message.content.startswith("!!쿠폰등록") == False and message.content.startswith("!!게스트") == False:
                await message.channel.send("대화는 금지!")
                await message.delete()

        if CHin == '질문채널':
            if message.content == "!!help" or message.content.startswith("!!등록") or message.content.startswith("!!쿠폰등록"):
                await message.channel.send("여기는 질문창입니다 명령어는 명령어-입력-채널 에 입력해주세요")
                await message.delete()

        if message.content == "!!help":
            await message.delete()
            embed = discord.Embed(title="명령어", color=0x5CD1E5)
            embed.add_field(name="!!등록 ID", value="'ID'를 등록하고 만료되지 않은 모든 쿠폰 수령을 시도합니다\nEX) !!등록 TEST@gmail.com", inline=False)
            embed.add_field(name="!!게스트 ID", value="ID에 만료되지 않은 모든 쿠폰 수령을 시도합니다\n게스트 아이디 전용\nEX) !!쿠폰등록 KINGDOMWELOVEYOU", inline=False)
            embed.add_field(name="!!쿠폰등록 쿠폰번호", value="쿠폰번호를 등록합니다 등록하면 ID 리스트에 등록된 모든 사람들에게 쿠폰 수령을 시도합니다\n!!게스트 GUEST-123456", inline=False)
            await message.channel.send( embed=embed)

        if message.content.startswith("!!등록"): #쿠킹덤 ID 리스트에 사용자 등록
            trsText = message.content.split(" ")[1]
            await message.delete()

            dircooking = db.reference('cooking/') #ID 리스트 가져오기
            cookingch = dircooking.get()
            cookingch = list(cookingch.values())

            if trsText in cookingch: #해당 ID가 있다면
                await message.channel.send(message.author.mention + "님은 이미 등록되어있습니다")
            else:# 없다면 리스트로 저장
                await message.channel.send(message.author.mention + "님 등록과 함께 쿠폰 작업을 시작합니다\n보안을 위해 ID가 포함된 메시지는 삭제됩니다")

                dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
                coocuch = dircoocu.get()
                coocuch = list(coocuch.values())
                coochcu = coocuch
                get = []

                driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
                embed = discord.Embed(title="처리내용", color=0x5CD1E5)

                for inpu in coocuch:
                    driver.get("https://game.devplay.com/coupon/ck/ko")
                    driver.implicitly_wait(5)
                    driver.find_element_by_id('email-box').send_keys(trsText)
                    driver.find_element_by_id('code-box').send_keys(inpu)
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    alertin = driver.switch_to_alert().text
                    embed.add_field(name=trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청", value=alertin, inline=False)
                    driver.switch_to_alert().accept()

                    if alertin == "DevPlay 계정을 다시 한번 확인해주세요.":
                        embed.add_field(name="ID 확인요청", value="ID를 다시 확인하여 주세요", inline=False)
                        await message.channel.send(embed=embed)
                        return
                    elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                        get.append(inpu)

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
                
                embed.add_field(name="ID를 정상적으로 등록하였습니다",value="앞으로 누군가 쿠폰을 최초 등록하면 이 계정에 쿠폰이 자동 수령됩니다", inline=False)
                dircooking.update({str(len(cookingch)):trsText})

                await message.channel.send(embed=embed)
                driver.close()
       
        if message.content.startswith("!!쿠폰등록"): #쿠킹덤 ID 리스트에 사용자 등록
            await message.channel.send("쿠폰 등록을 실행합니다 잠시만 기다려 주세요")
            trsText = message.content.split(" ")[1]

            dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
            coocuch = dircoocu.get()
            coocuch = list(coocuch.values())

            if trsText not in coocuch: #해당 쿠폰이 없다면 실행
                driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

                dircooking = db.reference('cooking/') #ID 리스트 가져오기
                cookingch = dircooking.get()
                cookingch = list(cookingch.values())

                embed = discord.Embed(title="처리내용", color=0x5CD1E5)

                for inpu in cookingch:
                    driver.get("https://game.devplay.com/coupon/ck/ko")
                    driver.implicitly_wait(5)
                    driver.find_element_by_id('email-box').send_keys(inpu)
                    driver.find_element_by_id('code-box').send_keys(trsText)
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    alertin = driver.switch_to_alert().text
                    embed.add_field(name=inpu[:2] + "-----@" + inpu.split('@')[1] + "님에게 " + trsText + " 지급 신청", value=alertin, inline=False)
                    driver.switch_to_alert().accept()

                    if alertin == "쿠폰번호는 16자리입니다. 다시 한 번 확인해 주세요.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        channel = client.get_channel(836171133966483492)
                        await channel.send(embed=embed)

                        channel = client.get_channel(836183313253007380)
                        await channel.send(embed=embed)
                        return
                    elif alertin == "쿠폰번호를 다시 한번 확인해주세요.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        channel = client.get_channel(836171133966483492)
                        await channel.send(embed=embed)

                        channel = client.get_channel(836183313253007380)
                        await channel.send(embed=embed)
                        return
                    elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        channel = client.get_channel(836171133966483492)
                        await channel.send(embed=embed)

                        channel = client.get_channel(836183313253007380)
                        await channel.send(embed=embed)
                        return
                
                channel = client.get_channel(836171133966483492)
                await channel.send(embed=embed)

                channel = client.get_channel(836183313253007380)
                await channel.send(embed=embed)
                driver.close()

                dircoocu.update({str(len(coocuch)):trsText})
            else:
                channel = client.get_channel(836171133966483492)
                await channel.send("이미 등록된 쿠폰입니다")

                channel = client.get_channel(836183313253007380)
                await channel.send("이미 등록된 쿠폰입니다")
        
        if message.content.startswith("!!게스트"): #게스트 아이디 사용
            trsText = message.content.split(" ")[1]
            await message.delete()

            await message.channel.send(message.author.mention + "님 쿠폰 작업을 시작합니다\n보안을 위해 ID가 포함된 메시지는 삭제됩니다\n게스트 계정을 1회성으로 ID 등록이 되진 않습니다")

            if trsText.split('-')[0] != "GUEST":
                await message.channel.send("해당명령어는 게스트 계정을 위한 1회용 일괄 수령 시스템입니다 정규 계정은 다른 명령어를 이용해주세요")

            dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
            coocuch = dircoocu.get()
            coocuch = list(coocuch.values())
            coochcu = coocuch
            get = []

            driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
            embed = discord.Embed(title="처리내용", color=0x5CD1E5)

            for inpu in coocuch:
                driver.get("https://game.devplay.com/coupon/ck/ko")
                driver.implicitly_wait(5)
                driver.find_element_by_id('email-box').send_keys(trsText)
                driver.find_element_by_id('code-box').send_keys(inpu)
                driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alertin = driver.switch_to_alert().text
                embed.add_field(name=trsText.split('-')[0]  + "-"  + trsText.split('-')[1][:2]+ "님에게 " + inpu + " 지급 신청", value=alertin, inline=False)
                driver.switch_to_alert().accept()

                if alertin == "DevPlay 계정을 다시 한번 확인해주세요.":
                    embed.add_field(name="ID 확인요청", value="ID를 다시 확인하여 주세요", inline=False)
                    await message.channel.send(embed=embed)
                    return
                elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                    get.append(inpu)

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
            driver.close()
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")
        await message.delete()

client.run(token)
=======
        if CHin != '등록채널' and CHin != '대화채널':
            if message.content != "!!help" and message.content.startswith("!!등록") == False and message.content.startswith("!!쿠폰등록") == False:
                await message.channel.send("대화는 금지!")
                await message.delete()

        if message.content == "!!help":
            await message.delete()
            embed = discord.Embed(title="명령어", color=0x5CD1E5)
            embed.add_field(name="!!등록 ID", value="'ID'를 등록하고 만료되지 않은 모든 쿠폰 수령을 시도합니다", inline=False)
            embed.add_field(name="!!쿠폰등록 쿠폰번호", value="쿠폰번호를 등록합니다 등록하면 ID 리스트에 등록된 모든 사람들에게 쿠폰 수령을 시도합니다", inline=False)
            await message.channel.send( embed=embed)

        if message.content.startswith("!!등록"): #쿠킹덤 ID 리스트에 사용자 등록
            trsText = message.content.split(" ")[1]
            await message.delete()

            dircooking = db.reference('cooking/') #ID 리스트 가져오기
            cookingch = dircooking.get()
            cookingch = list(cookingch.values())

            if trsText in cookingch: #해당 ID가 있다면
                await message.channel.send(message.author.mention + "님은 이미 등록되어있습니다")
            else:# 없다면 리스트로 저장
                await message.channel.send(message.author.mention + "님 등록과 함께 쿠폰 작업을 시작합니다\n보안을 위해 ID가 포함된 메시지는 삭제됩니다")

                dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
                coocuch = dircoocu.get()
                coocuch = list(coocuch.values())
                coochcu = coocuch
                get = []

                driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
                embed = discord.Embed(title="처리내용", color=0x5CD1E5)

                for inpu in coocuch:
                    driver.get("https://game.devplay.com/coupon/ck/ko")
                    driver.implicitly_wait(5)
                    driver.find_element_by_id('email-box').send_keys(trsText)
                    driver.find_element_by_id('code-box').send_keys(inpu)
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    alertin = driver.switch_to_alert().text
                    embed.add_field(name=trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청", value=alertin, inline=False)
                    driver.switch_to_alert().accept()

                    if alertin == "DevPlay 계정을 다시 한번 확인해주세요.":
                        embed.add_field(name="ID 확인요청", value="ID를 다시 확인하여 주세요", inline=False)
                        await message.channel.send(embed=embed)
                        return
                    elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                        get.append(inpu)

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
                
                dircooking.update({str(len(cookingch)):trsText})

                await message.channel.send(embed=embed)
                driver.close()
       
        if message.content.startswith("!!쿠폰등록"): #쿠킹덤 ID 리스트에 사용자 등록
            await message.channel.send("쿠폰 등록을 실행합니다 잠시만 기다려 주세요")
            trsText = message.content.split(" ")[1]

            dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
            coocuch = dircoocu.get()
            coocuch = list(coocuch.values())

            if trsText not in coocuch: #해당 쿠폰이 없다면 실행
                driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

                dircooking = db.reference('cooking/') #ID 리스트 가져오기
                cookingch = dircooking.get()
                cookingch = list(cookingch.values())

                embed = discord.Embed(title="처리내용", color=0x5CD1E5)

                for inpu in cookingch:
                    driver.get("https://game.devplay.com/coupon/ck/ko")
                    driver.implicitly_wait(5)
                    driver.find_element_by_id('email-box').send_keys(inpu)
                    driver.find_element_by_id('code-box').send_keys(trsText)
                    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    alertin = driver.switch_to_alert().text
                    embed.add_field(name=inpu[:2] + "-----@" + inpu.split('@')[1] + "님에게 " + trsText + " 지급 신청", value=alertin, inline=False)
                    driver.switch_to_alert().accept()

                    if alertin == "쿠폰번호는 16자리입니다. 다시 한 번 확인해 주세요.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        channel = client.get_channel(836171133966483492)
                        await channel.send(embed=embed)

                        channel = client.get_channel(836183313253007380)
                        await channel.send(embed=embed)
                        return
                    elif alertin == "쿠폰번호를 다시 한번 확인해주세요.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        channel = client.get_channel(836171133966483492)
                        await channel.send(embed=embed)

                        channel = client.get_channel(836183313253007380)
                        await channel.send(embed=embed)
                        return
                    elif alertin == "사용 기간이 만료된 쿠폰입니다.":
                        embed.add_field(name="쿠폰 번호 확인 요청", value="쿠폰 번호를 다시 확인하여주세요", inline=False)
                        channel = client.get_channel(836171133966483492)
                        await channel.send(embed=embed)

                        channel = client.get_channel(836183313253007380)
                        await channel.send(embed=embed)
                        return
                
                channel = client.get_channel(836171133966483492)
                await channel.send(embed=embed)

                channel = client.get_channel(836183313253007380)
                await channel.send(embed=embed)
                driver.close()

                dircoocu.update({str(len(coocuch)):trsText})
            else:
                channel = client.get_channel(836171133966483492)
                await channel.send("이미 등록된 쿠폰입니다")

                channel = client.get_channel(836183313253007380)
                await channel.send("이미 등록된 쿠폰입니다")
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")

client.run(token)
>>>>>>> 43543b488cc479d6ff7275aa72aa7734c4a12daf
