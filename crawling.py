from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

###
### MySQL에 저장된 domain.txt 파일을 읽어서 최근에 접속가능했던 주소를 가져와서 진행한다.
###
import re
# url = "https://newtoki301.com/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0"
url = "https://newtoki301.com/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0&yoil=%EC%9B%94&jaum=&tag=&sst=as_update&sod=desc&stx="
# url - "https://newtoki301.com/"
num = int(re.sub(r'[^0-9]','',url))
driver.get(url)

###
### 뉴토끼는 도메인 주소가 바뀌므로 만약 없는 주소라면 1씩 더해서 탐색한다
###

###
### 일단 상세정보 클릭 전에 받아올 정보들 ( 이미지, 요일, 장르, 제목 ) 받아오자
###
import requests
from bs4 import BeautifulSoup
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')
infos = soup.select('li#data-id')

# infos = driver.find_elements(By.ID,"webtoon-list-all")
print(infos)








###
### 로그인은 굳이 할 필요가 없을 것 같고, 캡챠입력은 수동으로 받도록 하자.
### https://www.youtube.com/watch?v=ZNOiwvrS_dc

### 걍 1화 링크 걸어주자
# captcha =

driver.quit()