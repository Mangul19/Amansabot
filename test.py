from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from selenium.webdriver.chrome.options import Options

#firebase
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred,{'databaseURL' : 'https://amansa-bot-default-rtdb.firebaseio.com/'})

options = Options()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)


trsText = "XYOKSPZLLUJYFKJN"
    
dircooking = db.reference('cooking/') #ID 리스트 가져오기
cookingch = dircooking.get()
cookingch = list(cookingch.values())

for inpu in cookingch:
    driver.get("https://game.devplay.com/coupon/ck/ko")
    driver.implicitly_wait(60)
    driver.find_element_by_id('email-box').send_keys(inpu)
    driver.find_element_by_id('code-box').send_keys(trsText)
    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/form/div[4]/div").click()
    WebDriverWait(driver, 9999).until(EC.alert_is_present())
    alertin = driver.switch_to_alert().text
    print(inpu + " : " + alertin)
    driver.switch_to_alert().accept()