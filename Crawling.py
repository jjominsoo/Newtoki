from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# chrome_options.add_argument('--headless=new')
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 모든 웹툰 데이터를 크롤링한다.
# 만약 중간에 멈출 수도 있으므로 index를 일단 정해두자.
# 나중에 Update.py에서 활용할 수 도 있다.


# WebtoonInfo.csv   : 모든 웹툰들을 정리한 csv파일
# Mark.csv          : 마지막으로 업데이트한 웹툰 이름을 저장한 csv파일 > 자주 변동되는 url주소를 확인하기 위해 쓰일 것임
import Newtoki_Functions as func
func.InitCSV()

url = func.CheckURL(driver)
weeks = ['월','화','수','목','금','토','일','열흘']
for week in weeks:
    print(week + '요일 웹툰 크롤링')
    week_url = url+ '&yoil='+str(week)+'&jaum=&tag=&sst=as_update&sod=desc&stx='
    response = requests.get(week_url, headers={'User-agent' : user_agent})
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    pages = soup.find_all('div',{'class':'list-page'})

    for page in pages:
        p = page.select('ul > li')

    df = pd.read_csv('src/WebtoonInfo.csv')
    for p in range(2):
        if p != 0:
            print("Click Event")
            driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[4]/ul/li[%d]/a' % (p + 3)).click()
            week_url = driver.current_url
        func.PageCrawling(week_url,week,df)

    print(week + '요일 웹툰 크롤링 끝')


print(df)
# df.to_csv()

driver.quit()