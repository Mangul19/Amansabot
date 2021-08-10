from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")

song = "pop.00026"

global driver
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
driver.get("http://mangul.iptime.org/" + song)# 사이트 열람


jang = (driver.find_element_by_xpath('//*[@id="final"]').get_attribute("innerHTML")).split('장르')
ch = (driver.find_element_by_xpath('//*[@id="d"]').get_attribute("innerHTML"))

print(song + "의 장르는 " + jang[0][10:] + " 입니다 비슷한 곡은 " + ch + " 입니다")