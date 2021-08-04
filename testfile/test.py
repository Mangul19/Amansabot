import discord
import asyncio
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random
import math
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import HTTPError
from urllib.request import Request
from urllib.parse import quote
import json
import time
import urllib
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")
import code

#clinet
client = discord.Client()
#discord bot tokken
token = code.token
#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")

#메세지 수신시
@client.event
async def on_message(message):
    if message.author.id == 265725373843636224:
        channel = client.get_channel(872397048983453716)
        mes = 265725373843636224
        await channel.send("<@!" + str(mes) + ">")
        await channel.send("<@" + str(mes) + ">")

    if message.content.startswith("@"):
        channel = client.get_channel(872397048983453716)

client.run(token)