#어만사 전용 디스코드 봇

import discord
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
        dirhelplist = db.reference('helplist/')
        helplist = dirhelplist.get()
        helplist = helplist['helplist']