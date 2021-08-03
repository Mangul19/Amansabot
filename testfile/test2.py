from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
options.add_argument("app-version=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
driver = webdriver.Chrome(chrome_options=options, executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')

listin = ["안녕",'무명','샐러드',"잘못된지식","키리이"]

for i in listin:
  try:
    driver.get("https://opendict.korean.go.kr/search/searchResult?focus_name=query&query=" + i + "&dicType=1&wordMatch=Y")# 사이트 열람
    driver.implicitly_wait(3)
    einput = driver.find_element_by_xpath("//*[@id='searchPaging']/div[1]/div[2]/ul[2]/li/div/div[1]/dl/dd[1]/a/span[4]").get_attribute("innerHTML")
    print(einput + "성공")
  except:
    print("없음")