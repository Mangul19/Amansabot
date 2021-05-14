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

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

trsText = "test@gmail.com"

irua = True

dircoocu = db.reference('coocu/') #쿠키 리스트 가져오기
coocuch = dircoocu.get()
coocuch = list(coocuch.values())
coochcu = coocuch
get = []
count = 0

for inpu in coocuch:
  driver.get("https://game.devplay.com/coupon/ck/ko")
  driver.implicitly_wait(60)
  driver.find_element_by_id('email-box').send_keys(trsText)
  driver.find_element_by_id('code-box').send_keys(inpu)
  driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[5]/div").click()
  WebDriverWait(driver, 60).until(EC.alert_is_present())
  alertin = driver.switch_to_alert().text
  if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
    print(trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청" + alertin)
  driver.switch_to_alert().accept()

  if alertin == "DevPlay 계정을 다시 한번 확인해주세요.":
    print("ID 확인요청 ID를 다시 확인하여 주세요")
  elif alertin == "사용 기간이 만료된 쿠폰입니다.":
    get.append(inpu)

  while alertin == "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
    print("데브 사이트 서버 오류 확인 재시작합니다")
    driver.close()
    driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
    driver.get("https://game.devplay.com/coupon/ck/ko")
    driver.implicitly_wait(60)
    driver.find_element_by_id('email-box').send_keys(trsText)
    driver.find_element_by_id('code-box').send_keys(inpu)
    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[5]/div").click()
    WebDriverWait(driver, 60).until(EC.alert_is_present())
    alertin = driver.switch_to_alert().text
    if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
      print(trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청" + alertin)
    driver.switch_to_alert().accept()

  count += 1
  if count == 20:
      print("쿠폰 지급 중간 안내 안내된 계정은 지급이 완료 되었으며 남은 계정에 지급 신청을 계속합니다")
      count = 0

print("ID를 정상적으로 등록하였습니다 앞으로 누군가 쿠폰을 최초 등록하면 이 계정에 쿠폰이 자동 수령됩니다")