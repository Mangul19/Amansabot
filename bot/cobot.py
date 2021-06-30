#어만사 전용 디스코드 봇

import discord
from discord import team
from discord.enums import _is_descriptor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import sys
<<<<<<< HEAD
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
=======
sys.path.insert(0, "D:/Desktop/중요파일/bot-Amansa/noup")
>>>>>>> 8e6da7a5f6c543bee85c0fe39074a7e8a29606b3
import code

#clinet
client = discord.Client()
#discord bot tokken
token = code.token
#firebase
<<<<<<< HEAD
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
=======
cred = credentials.Certificate("D:/Desktop/중요파일/bot-Amansa/noup/firebase-adminsdk.json")
>>>>>>> 8e6da7a5f6c543bee85c0fe39074a7e8a29606b3
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n쿠킹덤 관리 시스템을 시작합니다" + 
        "\n==========================================")
    # 이 기능을 이용하여 봇의 상태를 출력
    mssg = discord.Game("!help|Made by Han_MangUl")
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
        if str(message.channel.id) == "842362278014746696":
            if message.content == "!!help":
                embed = discord.Embed(title="명령어", color=0x5CD1E5)
                embed.add_field(name="!!등록 '닉네임'", value="'닉네임'을 등록합니다\nEX) !!등록 한망울", inline=False)
                embed.add_field(name="!!확인", value="등록된 유저를 확인합니다", inline=False)
                embed.add_field(name="!!미달 '닉네임'", value="미달 목록을 작성합니다\nEX) !!미달 한망울", inline=False)
                embed.add_field(name="!!미달해제 '닉네임'", value="미달 목록에서 '닉네임'을 제거합니다\nEX) !!미달해제 한망울", inline=False)
                embed.add_field(name="!!정산", value="토벌 점수를 초기화합니다", inline=False)
                embed.add_field(name="!!삭제 닉네임", value="'닉네임'을 삭제합니다\nEX) !!삭제 한망울", inline=False)
                await message.channel.send( embed=embed)
            
            if message.content.startswith("!!등록"): #유저 등록
                trsText = message.content.split(" ")[1]
                
                dirteamlist = db.reference('teamlist/')
                teamlist = dirteamlist.get()
                teamlist = list(teamlist.values())
                
                if trsText not in teamlist:
                    dirteamlist.update({str(len(teamlist)):trsText})
                    
                    await message.channel.send(trsText + " 님을 등록하였습니다")
                else:
                    await message.channel.send(trsText + " 님을 이미 등록된 유저입니다")
                    
            if message.content == "!!확인": #유저 확인
                dirteamlist = db.reference('teamlist/')
                teamlist = dirteamlist.get()
                teamlist = list(teamlist.values())
                
                bteamlist = ""
                
                for inpu in teamlist:
                    bteamlist += inpu + " , "
                
                embed = discord.Embed(title="유저 리스트",description=bteamlist, color=0x5CD1E5)
                    
                await message.channel.send(embed=embed)
                        
            if message.content.startswith("!!미달해제"): #점수 관리
                trsText = message.content.split(" ")[1]
                
                dirteamscno = db.reference('teamscno/' + trsText)
                teamscno = dirteamscno.get()
                
                if teamscno != None:
                    dirteamscno.delete()
                    await message.channel.send(trsText + " 님 미달을 해제합니다")
            elif message.content.startswith("!!미달"): #점수 관리
                trsText = message.content.split(" ")[1]
                
                dirteamscno = db.reference('teamscno/')
                teamscno = dirteamscno.get()
                
                if teamscno != None:
                    teamchno = teamscno.keys()
                    
                    if trsText not in teamchno:
                        dirteamscno.update({trsText:"Waring"})
                        await message.channel.send(trsText + " 님은 활동을 안 하였습니다 경고 1회 누적합니다")
                    else:
                        await message.channel.send(trsText + " 님은 활동을 안 하였습니다 경고 누적 2회 강제 추방 조치 필요")
                else:
                    dirteamscno.update({trsText:"Waring"})
                    await message.channel.send(trsText + " 님은 활동을 안 하였습니다 경고 1회 누적합니다")      
                
            if message.content == "!!정산": #정산 초기화
                dirteamscno = db.reference('teamscno/')
                dirteamlist.delete()
                    
                await message.channel.send("초기화 완료")
                
            if message.content.startswith("!!삭제"): #유저 삭제
                trsText = message.content.split(" ")[1]
                
                dirteamlist = db.reference('teamlist/')
                teamlist = dirteamlist.get()
                teamlist = list(teamlist.values())

                if trsText in teamlist:
                    dirteamlist.delete()
                    
                    teamlist.remove(trsText)

                    dirteamlist.update({'00':teamlist[0]})
                    count = 1

                    for inin in teamlist[1:]:
                        dirteamlist.update({count:inin})
                        count += 1
                    
                    dirteamscno = db.reference('teamscno/')
                    teamscno = dirteamscno.get()
                    teamchno = teamscno.keys()
                    
                    if trsText in teamchno:
                        dirteamscno = db.reference('teamscno/'  + trsText)
                        dirteamscno.delete()
                        
                    await message.channel.send(trsText + " 님을 정상 삭제하였습니다")
                else:
                    await message.channel.send(trsText + " 님은 없는 유저입니다")
    except:
        await message.channel.send(message.author.mention + " 님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")
        
client.run(token)