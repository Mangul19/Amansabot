from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
    
driver.get("https://www.weather.go.kr/w/eqk-vol/recent-eqk.do")# 사이트 열람
driver.implicitly_wait(10)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

print(str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(1) > td'))[17:-6])
print(str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(2) > td > strong'))[9:-17])
print(str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(3) > td > strong > font:nth-child(1)'))[22:-8])
print(str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(4) > td:nth-child(4)'))[5:-6])
print(str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(4) > td.td_loc'))[20:-48])
print(str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div.over-scroll.cont-box-eqk > table > tbody > tr:nth-child(5) > td'))[17:-6])
print("https://www.weather.go.kr/" + str(soup.select('#eqk-report > div.cont-box02 > div:nth-child(3) > div:nth-child(3) > div > img'))[32:-4])