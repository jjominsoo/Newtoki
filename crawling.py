from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(5)

###
### MySQL에 저장된 domain.txt 파일을 읽어서 최근에 접속가능했던 주소를 가져와서 진행한다.
###
import re
import time
s_time = time.time()
url = "https://newtoki301.com"
###
### 뉴토끼는 도메인 주소가 바뀌므로 만약 없는 주소라면 1씩 더해서 탐색한다

###
num = int(re.sub(r'[^0-9]','',url))
url += "/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0"
driver.get(url)
driver.find_element(By.XPATH,'//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[2]/td/span[2]').click()
driver.find_element(By.XPATH,'//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').send_keys(Keys.ENTER)
###
### 일단 상세정보 클릭 전에 받아올 정보들 ( 이미지, 요일, 장르, 제목 ) 받아오자
import requests
from bs4 import BeautifulSoup

url2 = driver.current_url
response = requests.get(url2,headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'} )
html = response.text
soup = BeautifulSoup(html,'html.parser')
# print(soup)
webtoon_list = soup.find_all('li',{'data-weekday': '월요일' })
print(webtoon_list)
for webtoon in webtoon_list:
    print(webtoon['data-initial'])
    print(webtoon['data-genre'])
    print(webtoon['date-title'])
    print("+++++++++++++++++++++++")
# webtoon_page = soup.select('div.list-page text-center > li')
# for page in webtoon_page:
#     print(page.text)








###
### 로그인은 굳이 할 필요가 없을 것 같고, 캡챠입력은 수동으로 받도록 하자.
### https://www.youtube.com/watch?v=ZNOiwvrS_dc

### 걍 1화 링크 걸어주자
# captcha =

driver.quit()
e_time = time.time()
print("총 실행시간 : " + str(e_time-s_time))