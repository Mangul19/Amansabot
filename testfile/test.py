from selenium import webdriver

global driver
driver = webdriver.Chrome(executable_path='D:/Desktop/bot-Amansa/chromedriver.exe')
driver.get("https://v1.coronanow.kr/live.html")# 사이트 열람
driver.implicitly_wait(3)

print(driver.find_element_by_xpath("/html/body/div[2]/b/div[5]/div[1]/div/span/p[1]/b").get_attribute("innerHTML"))