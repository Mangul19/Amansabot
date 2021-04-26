#공지
import discord
import asyncio
import code

#discord bot tokken
token = code.token
#clinet
client = discord.Client()

#준비 될 시 시작
@client.event
async def on_ready():
    sayin = "금일 PM 12:00 ~ PM 4:00 까지 봇 서비스가 일시 정지합니다"
    channel = client.get_channel(832799360210436107)
    await channel.send(sayin)
    channel = client.get_channel(833629507939467274)
    await channel.send(sayin)

client.run(token)