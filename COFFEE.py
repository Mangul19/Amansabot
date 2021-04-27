from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
token = code.coffeetoken
#firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
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
        if CHin != '등록채널' and CHin != '질문채널':
            if message.content != "!!help" and message.content.startswith("!!등록") == False and message.content.startswith("!!쿠폰등록") == False:
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
            embed.add_field(name="!!쿠폰등록 쿠폰번호", value="쿠폰번호를 등록합니다 등록하면 ID 리스트에 등록된 모든 사람들에게 쿠폰 수령을 시도합니다\nEX) !!쿠폰등록 KINGDOMWELOVEYOU", inline=False)
            await message.channel.send( embed=embed)

        if message.content.startswith("!!등록"): #알럽커피 ID 리스트에 사용자 등록
            trsText = message.content.split(" ")[1]
            await message.delete()

            dircoffee = db.reference('coffee/') #ID 리스트 가져오기
            coffeech = dircoffee.get()
            coffeech = list(coffeech.values())

            if trsText in coffeech: #해당 ID가 있다면
                await message.channel.send(message.author.mention + "님은 이미 등록되어있습니다")
            else:# 없다면 리스트로 저장

                
                await message.channel.send(message.author.mention + "님 등록과 함께 쿠폰 작업을 시작합니다\n보안을 위해 ID가 포함된 메시지는 삭제됩니다")

                dircoffeecu = db.reference('coffeecu/') #알럽쿠폰 리스트 가져오기
                coffeecuch = dircoffeecu.get()
                coffeecuch = list(coffeecuch.values())
                coffeechcu = coffeecuch
                get = []
                embed = discord.Embed(title="처리내용", color=0x5CD1E5)

                if len(coffeecuch) > 0:
                    for inpu in coffeecuch:
                        driver.get("https://ilovecoffeen.natris.co.kr/coupon/coupon.html")
                        driver.implicitly_wait(5)
                        driver.find_element_by_id('accountId').send_keys(trsText)
                        driver.find_element_by_id('couponCode').send_keys(inpu)
                        driver.find_element_by_xpath("//*[@id='submitBtn']").click()

                        while True:
                            if driver.find_element_by_xpath('//*[@id="popFail"]').is_displayed():
                                embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value="고객 센터에 연락이 필요합니다.", inline=False)
                                await message.channel.send(embed=embed)
                                return
                            elif driver.find_element_by_xpath('//*[@id="popFail5"]').is_displayed():
                                embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value="만료된 쿠폰입니다", inline=False)
                                get.append(inpu)
                                break
                            elif driver.find_element_by_xpath('//*[@id="popFail7"]').is_displayed():
                                embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value="해당계정은 사용하지 못하는 쿠폰입니다", inline=False)
                                break
                            elif driver.find_element_by_xpath('//*[@id="popFail3"]').is_displayed():
                                embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value="아이디를 다시 확인하여주세요", inline=False)
                                await message.channel.send(embed=embed)
                                return
                            elif driver.find_element_by_xpath('//*[@id="popFail2"]').is_displayed() or driver.find_element_by_xpath('//*[@id="popFail6"]').is_displayed() or driver.find_element_by_xpath('//*[@id="popFail1"]').is_displayed():
                                embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value="이미 사용한 쿠폰입니다", inline=False)
                                break
                            elif driver.find_element_by_xpath('//*[@id="popFail4"]').is_displayed():
                                embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value="쿠폰 번호 오류", inline=False)
                                break
                            elif driver.find_element_by_xpath('//*[@id="popDone"]').is_displayed():
                                embed.add_field(name=trsText[:2] + "----- 님에게 " + inpu + " 지급 신청", value="우편으로 정상적으로 지급되었습니다", inline=False)
                                break

                    if len(get) > 0:
                        dircoffeecu.delete()
                        for delin in get:
                            coffeechcu.remove(delin)

                        if len(coffeecuch) == 0:
                            coffeechcu.append('ILOVECOFFEENDAY')

                        dircoffeecu.update({'00':coffeechcu[0]})
                        count = 1

                        if len(coffeecuch) > 1:
                            for inin in coffeechcu[1:]:
                                dircoffeecu.update({count:inin})
                                count += 1
                
                embed.add_field(name="ID를 정상적으로 등록하였습니다",value="앞으로 누군가 쿠폰을 최초 등록하면 이 계정에 쿠폰이 자동 수령됩니다", inline=False)
                dircoffee.update({str(len(coffeech)):trsText})

                await message.channel.send(embed=embed)

        if message.content.startswith("!!쿠폰등록"): #쿠킹덤 ID 리스트에 사용자 등록
            await message.channel.send("쿠폰 등록을 실행합니다 잠시만 기다려 주세요")
            trsText = message.content.split(" ")[1]

            dircoffeecu = db.reference('coffeecu/') #쿠키 리스트 가져오기
            coffeecuch = dircoffeecu.get()
            coffeecuch = list(coffeecuch.values())

            if trsText not in coffeecuch: #해당 쿠폰이 없다면 실행
                dircoffee = db.reference('coffee/') #ID 리스트 가져오기
                coffeech = dircoffee.get()
                coffeech = list(coffeech.values())

                embed = discord.Embed(title="처리내용", color=0x5CD1E5)

                for inpu in coffeech:
                    driver.get("https://ilovecoffeen.natris.co.kr/coupon/coupon.html")
                    driver.implicitly_wait(5)
                    driver.find_element_by_id('accountId').send_keys(inpu)
                    driver.find_element_by_id('couponCode').send_keys(trsText)
                    driver.find_element_by_xpath("//*[@id='submitBtn']").click()

                    while True:
                        if driver.find_element_by_xpath('//*[@id="popFail"]').is_displayed():
                            embed.add_field(name=inpu[:2] + "----- 님에게 " + trsText + " 지급 신청", value="고객 센터에 연락이 필요합니다.", inline=False)
                            break
                        elif driver.find_element_by_xpath('//*[@id="popFail5"]').is_displayed():
                            embed.add_field(name="쿠폰 번호 확인 요청", value="만료된 쿠폰입니다", inline=False)
                            await message.channel.send(embed=embed)
                            return
                        elif driver.find_element_by_xpath('//*[@id="popFail7"]').is_displayed():
                            embed.add_field(name=inpu[:2] + "----- 님에게 " + trsText + " 지급 신청", value="해당계정은 사용하지 못하는 쿠폰입니다", inline=False)
                            break
                        elif driver.find_element_by_xpath('//*[@id="popFail3"]').is_displayed():
                            embed.add_field(name=inpu[:2] + "----- 님에게 " + trsText + " 지급 신청", value="아이디를 다시 확인하여주세요", inline=False)
                            break
                        elif driver.find_element_by_xpath('//*[@id="popFail2"]').is_displayed() or driver.find_element_by_xpath('//*[@id="popFail6"]').is_displayed() or driver.find_element_by_xpath('//*[@id="popFail1"]').is_displayed():
                            embed.add_field(name=inpu[:2] + "----- 님에게 " + trsText + " 지급 신청", value="이미 사용한 쿠폰입니다", inline=False)
                            break
                        elif driver.find_element_by_xpath('//*[@id="popFail4"]').is_displayed():
                            embed.add_field(name="쿠폰 번호 확인 요청", value="없는 쿠폰입니다", inline=False)
                            await message.channel.send(embed=embed)
                            return
                        elif driver.find_element_by_xpath('//*[@id="popDone"]').is_displayed():
                            embed.add_field(name=inpu[:2] + "----- 님에게 " + trsText + " 지급 신청", value="우편으로 정상적으로 지급되었습니다", inline=False)
                            break
                
                embed.add_field(name="@everyone 쿠폰 지급 안내", value=str(len(coffeecuch)) + "명 계정에 지급 신청을 완료하였습니다", inline=False)

                channel = client.get_channel(836456948555448370)
                await channel.send(embed=embed)

                channel = client.get_channel(836456634196164620)
                await channel.send(embed=embed)

                dircoffeecu.update({str(len(coffeecuch)):trsText})
            else:
                await message.channel.send("이미 등록된 쿠폰입니다")
    except:
        await message.channel.send(message.author.mention + "님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")
        await message.delete()

client.run(token)