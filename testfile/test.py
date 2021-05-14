import firebase_admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

dircooking = db.reference('cooking/') #ID 리스트 가져오기
cookingch = dircooking.get()
cookingch = list(cookingch.values())

get = ""

f = open("새파일.txt", 'w')
for inpu in cookingch:
  get += "\"" + inpu + "\","
  
f.write(get)