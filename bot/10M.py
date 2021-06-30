from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#ptions.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")

global driver
<<<<<<< HEAD
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
=======
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/중요파일/bot-Amansa/chromedriver.exe')
>>>>>>> 8e6da7a5f6c543bee85c0fe39074a7e8a29606b3

driver.get("https://www.youtube.com/watch?v=0ZVLvRenGl8")# 사이트 열람
driver.implicitly_wait(3)

driver.find_element_by_xpath('//*[@id="buttons"]/ytd-button-renderer').click()
driver.find_element_by_name('identifier').send_keys('mulmangul19@gmail.com')
driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button').click()
time.sleep(60*12*24)

while(True):
    try:
        driver.get("https://www.youtube.com/watch?v=0ZVLvRenGl8")# 사이트 열람
        driver.implicitly_wait(3)
    except:
        print("오류 발생 다음에 다시 시도합니다")

    time.sleep(60*12*24)