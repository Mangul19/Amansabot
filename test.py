from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
driver.get("https://v1.coronanow.kr/live.html")# 사이트 열람
driver.implicitly_wait(10)

html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')

einput1 = str(soup.select("body > div.cona_main > div:nth-child(6) > a > p"))[29:-5]

if einput1 != " ":
    print("비어있지 않음")
    print(einput1)
elif einput1 == " ":
    print("불러오기 오류 다음에 다시 시도합니다") 
    print(einput1)