#어만사 전용 디스코드 봇

import discord
from discord.enums import _is_descriptor
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import code

#clinet
client = discord.Client()
#discord bot tokken
token = code.token
#firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user:
        return

    #받은 메세지 및 입력자 출력
    print(str(message.author) + str(message.author.mention) + " : " + str(message.content))

    try:
        if str(message.channel.id) == "841693793828470824":
            if message.content == "!!help":
                embed = discord.Embed(title="명령어", color=0x5CD1E5)
                embed.add_field(name="!!쿠킹등록 '닉네임'", value="'닉네임'을 등록합니다\nEX) !!쿠킹등록 한망울", inline=False)
                embed.add_field(name="!!확인", value="등록된 유저를 확인합니다", inline=False)
                embed.add_field(name="!!점수등록 '닉네임' 현재점수", value="현재점수를 입력하여 토벌에 참가하였는지 확인합니다\nEX) !!점수등록 한망울 15682", inline=False)
                embed.add_field(name="!!정산", value="토벌 점수를 초기화합니다", inline=False)
                embed.add_field(name="!!쿠킹삭제 닉네임", value="'닉네임'을 삭제합니다\nEX) !!쿠킹삭제 한망울", inline=False)
                await message.channel.send( embed=embed)
            
            if message.content.startswith("!!쿠킹등록"): #유저 등록
                trsText = message.content.split(" ")[1]
                
                dirteamlist = db.reference('teamlist/')
                teamlist = dirteamlist.get()
                teamlist = list(teamlist.values())
                
                if trsText not in teamlist:
                    dirteamlist.update({str(len(teamlist)):trsText})
                    
                    dirteamsc = db.reference('teamsc/')
                    dirteamsc.update({trsText:0})
                    
                    await message.channel.send(trsText + " 님을 등록하였습니다")
                else:
                    await message.channel.send(trsText + " 님을 이미 등록된 유저입니다")
                    
            if message.content == "!!확인": #유저 확인
                dirteamlist = db.reference('teamlist/')
                teamlist = dirteamlist.get()
                teamlist = list(teamlist.values())
                
                embed = discord.Embed(title="유저 리스트",description=teamlist, color=0x5CD1E5)
                    
                await message.channel.send(embed=embed)
                
            if message.content.startswith("!!점수등록"): #점수 관리
                trsText = message.content.split(" ")[1]
                trssc = int(float(message.content.split(" ")[2]))
                
                dirteamsc = db.reference('teamsc/')
                teamsc = dirteamsc.get()[trsText]
                trsscr = trssc - teamsc
                
                await message.channel.send("점수 처리 결과\n" + trsText + " 님은 " + str(trsscr) + "점을 추가로 획득하셨습니다")
                dirteamsc.update({trsText:trsscr + teamsc})
                
            if message.content == "!!정산": #정산 초기화
                dirteamsc = db.reference('teamsc/')
                teamscr = dirteamsc.get()
                teamsc = list(teamscr.keys())
                
                for inpu in teamsc:
                    if teamscr[inpu] <= 15000:
                        await message.channel.send(inpu + " 님 점수 미달 점수 : " + str(teamscr[inpu]))
                               
                    dirteamsc.update({inpu:0})
                    
                await message.channel.send("점수 초기화 완료")
                
            if message.content.startswith("!!쿠킹삭제"): #유저 삭제
                trsText = message.content.split(" ")[1]
                
                dirteamlist = db.reference('teamlist/')
                teamlist = dirteamlist.get()
                teamlist = list(teamlist.values())

                if trsText in teamlist:
                    dirteamlist.delete()
                    dirteamsc = db.reference('teamsc/' + trsText)
                    dirteamsc.delete()
                    
                    teamlist.remove(trsText)

                    dirteamlist.update({'00':teamlist[0]})
                    count = 1

                    for inin in teamlist[1:]:
                        dirteamlist.update({count:inin})
                        count += 1
                        
                    await message.channel.send(trsText + " 님을 정상 삭제하였습니다")
                else:
                    await message.channel.send(trsText + " 님은 없는 유저입니다")
    except:
        await message.channel.send(message.author.mention + " 님 명령어 실행 중 오류가 발생하였습니다 명령어를 확인하여 주세요")
        
client.run(token)