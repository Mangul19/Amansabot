#어만사 전용 디스코드 봇
import discord
import asyncio
from urllib.parse import quote
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import HTTPError
import json
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

#Naver Open API application ID
client_id = code.client_id
#Naver Open API application token
client_secret = code.client_secret

#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

intents = discord.Intents.all()
#clinet
client = discord.Client(intents=intents)
#discord bot tokken
token = code.token
#API제한 될 시
num = 0

#준비 될 시 시작
@client.event
async def on_ready():
    print("로그인 합니다 : " + str(client.user.name) +
        "\n아래 id로 접속합니다 : " + str(client.user.id) +
        "\n자동번역 시스템을 시작합니다" + 
        "\n==========================================")

#메세지 수신시
@client.event
async def on_message(message):
    #봇일 경우 무시
    if message.author == client.user or str(message.channel.id) != "718436389062180917" and str(message.channel.id) != "875718837373386822":
        return

    #받은 메세지 및 입력자 출력
    print(str(message.author) + str(message.author.mention) + " : " + str(message.content))

    global num
    if str(message.channel.id) == "718436389062180917":
        if len(message.content) == 0:
            channel = client.get_channel(875718837373386822)
            return

        mal = translng("ko", "zh-CN", message)
        if mal == "429":
            for i in range(5):
                channel = client.get_channel(875718837373386822)
                await channel.send(str(num) + " Changed to next papago API Client")
                channel = client.get_channel(718436389062180917)
                await channel.send(str(num) + "번 API가 한도치에 도달하여 새로운 API에 접속하였습니다 [최대 10번까지 있음]")
        elif mal == "ful":
            for i in range(5):
                channel = client.get_channel(875718837373386822)
                await channel.send("All API is restricted Please contact the manager")
                channel = client.get_channel(718436389062180917)
                await channel.send("모든 API가 한도치에 도달했습니다 서비스 이용이 불가합니다")
        else:
            channel = client.get_channel(875718837373386822)
            await channel.send(embed=mal)
    elif str(message.channel.id) == "875718837373386822":
        if len(message.content) == 0:
            channel = client.get_channel(718436389062180917)
            return

        mal = translng("zh-CN", "ko",message)
        if mal == "429":
            for i in range(5):
                channel = client.get_channel(875718837373386822)
                await channel.send(str(num) + " Changed to next papago API Client")
                channel = client.get_channel(718436389062180917)
                await channel.send(str(num) + "번 API가 한도치에 도달하여 새로운 API에 접속하였습니다 [최대 10번까지 있음]")
        elif mal == "ful":
            for i in range(5):
                channel = client.get_channel(875718837373386822)
                await channel.send("All API is restricted Please contact the manager")
                channel = client.get_channel(718436389062180917)
                await channel.send("모든 API가 한도치에 도달했습니다 서비스 이용이 불가합니다")
        else:
            channel = client.get_channel(718436389062180917)
            await channel.send(embed=mal)

def translng(leng1, leng2, word):
    global num

    dirtime = db.reference('apitime/') # 해당일 출석체크 정보 조회
    times = dirtime.get()
    times = times["time"]

    now = datetime.datetime.strptime(str(datetime.datetime.now()).split(" ")[0], "%Y-%m-%d")
    times = datetime.datetime.strptime(times, "%Y-%m-%d")
    if times < now:
        dirtime.update({"time":str(datetime.datetime.now()).split(" ")[0]})
        num = 0

    mainText = word.content
    if len(mainText) > 0: # 번역할 문자이 없을 시
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        # 띄어쓰기 : split처리후 [2:]을 for문으로 붙인다.

        if num == (len(client_id) - 1):
            return "ful"

        #Naver Open API application ID
        clientid = client_id[num]
        #Naver Open API application token
        clientsecret = client_secret[num]

        combineword = mainText
        savedCombineword = combineword.strip()
        combineword = quote(savedCombineword)

        try:
            #언어 설정
            dataParmas = "source=" + leng1 + "&target=" + leng2 + "&text=" + combineword
            request = Request(baseurl)
            request.add_header("X-Naver-Client-Id", clientid)
            request.add_header("X-Naver-Client-Secret", clientsecret)
            response = urlopen(request, data=dataParmas.encode("utf-8"))

            responsedCode = response.getcode()
            if (responsedCode == 200): #오류 구분
                response_body = response.read()
                #디코드 utf-8
                api_callResult = response_body.decode('utf-8')
                api_callResult = json.loads(api_callResult)
                # 수령 값 저장
                translatedText = api_callResult['message']['result']["translatedText"]
                embed = discord.Embed(title="Translate", description= word.author.mention, color=0x5CD1E5)
                embed.add_field(name= translatedText, value="API provided by Naver Open API", inline=False)
                return embed
        except HTTPError as e:
            err = e.read()
            code = e.getcode()
            if (code == 429):
                num += 1
                return "429"

client.run(token)