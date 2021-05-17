from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from selenium.webdriver.chrome.options import Options
import sys
sys.path.insert(0, "D:/Desktop/bot-Amansa/noup")

#firebase
cred = credentials.Certificate("D:/Desktop/bot-Amansa/noup/firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})


webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
driver = webdriver.Chrome(executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

trsText = "test@gmail.com"

irua = True

dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
coocuch = dircoocu.get()
coocuch = list(coocuch.values())
coochcu = coocuch
get = []
count = 0


driver.get("https://game.devplay.com/coupon/ck/ko")