import firebase_admin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import code
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")
options.add_argument(":method=OPTIONS")
options.add_argument(':authority=account.devplay.com')
options.add_argument(':path=/v2/coupon/ck')
options.add_argument(':scheme=https')
options.add_argument('accept=*/*')
options.add_argument('accept-encoding=gzip, deflate, br')
options.add_argument('accept-language=ko-KR,ko;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3')
options.add_argument('access-control-request-headers=content-type')
options.add_argument('access-control-request-method=POST')
options.add_argument('dnt=1')
options.add_argument('origin=https://game.devplay.com')
options.add_argument('referer=https://game.devplay.com/')
options.add_argument('sec-fetch-dest=empty')
options.add_argument('sec-fetch-mode=cors')
options.add_argument('sec-fetch-site=-site')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
driver = webdriver.Chrome(chrome_options=options, executable_path='chromedriver.exe')


trsText = "test@gamil.com"

dircooking = db.reference('cooking/') #ID 리스트 가져오기
cookingch = dircooking.get()
cookingch = list(cookingch.values())

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
    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
    WebDriverWait(driver, 60).until(EC.alert_is_present())
    alertin = driver.switch_to_alert().text
    if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
      print(trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청")
    driver.switch_to_alert().accept()

    if alertin == "DevPlay 계정을 다시 한번 확인해주세요.":
      print("ID 확인요청 ID를 다시 확인하여 주세요")
    elif alertin == "사용 기간이 만료된 쿠폰입니다.":
      get.append(inpu)

    while alertin == "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
      driver.close()
      driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
      driver.get("https://game.devplay.com/coupon/ck/ko")
      driver.implicitly_wait(60)
      driver.find_element_by_id('email-box').send_keys(trsText)
      driver.find_element_by_id('code-box').send_keys(inpu)
      driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
      WebDriverWait(driver, 60).until(EC.alert_is_present())
      alertin = driver.switch_to_alert().text
      if alertin != "서버에서 알 수 없는 응답이 발생하였습니다. 잠시후 다시 시도해주세요.":
        print(trsText[:2] + "-----@" + trsText.split('@')[1] + "님에게 " + inpu + " 지급 신청")
      driver.switch_to_alert().accept()

    count += 1
    if count == 20:
      print("쿠폰 지급 중간 안내 안내된 계정은 지급이 완료 되었으며 남은 계정에 지급 신청을 계속합니다")
      count = 0
    
    if irua:
      dircooking.update({str(len(cookingch)):trsText})
      irua = False

if len(get) > 0:
    dircoocu.delete()
    for delin in get:
      coochcu.remove(delin)

    if len(coochcu) == 0:
      coochcu.append('KINGDOMWELOVEYOU')

    dircoocu.update({'00':coochcu[0]})
    count = 1

    if len(coochcu) > 1:
      for inin in coochcu[1:]:
        dircoocu.update({count:inin})
        count += 1

print(name="ID를 정상적으로 등록하였습니다 앞으로 누군가 쿠폰을 최초 등록하면 이 계정에 쿠폰이 자동 수령됩니다")