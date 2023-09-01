from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import re
import time
from datetime import datetime, timedelta
import requests
import openpyxl
import urllib.request
import urllib
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.implicitly_wait(5)

# 엑셀파일에 저장된 최근에 접속가능했던 주소를 가져와서 진행한다.
fpath = r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki.xlsx'
wb = openpyxl.load_workbook(fpath)
wb_siteInfo = wb['Site Information']
wb_webtoon = wb['webtoon']
url = wb_siteInfo['A2'].value
saved_url = wb_siteInfo['A2'].value
# 프로그램 총 실행시간 체크
s_time = time.time()

# 만약 그 새 주소가 바뀌었다면, 숫자부분에 1씩 더하면서 바뀐 주소를 탐색해본다
while(1):
    try:
        temp = "/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0"
        url2 = url + temp
        driver.implicitly_wait(10)
        driver.get(url2)
        driver.find_element(By.XPATH,'//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[2]/td/span[2]').click()
        driver.find_element(By.XPATH,'//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').send_keys(Keys.ENTER)
        break
    except Exception as error:
        print(error)
        num = int(re.sub(r'[^0-9]', '', url)) + 1
        ### 여기 좀 수정해야할듯??
        url = "https://newtoki" + str(num) + ".com"
        driver.implicitly_wait(1)
        print(num)


###
### 일단 상세정보 클릭 전에 받아올 정보들 ( 이미지, 요일, 장르, 제목 ) 받아오자


# 웹툰 정보를 저장할 리스트 = 2번에 나눠서 append 시킬꺼
# 일단 저장해놓고 추후 가공한자
# 1차 : 이름, 장르, 요일, 이미지

#
update_name = []
genre = []
#
update_num = wb_siteInfo['D2'].value
#
cell_alp = {'판타지':'F','액션':'G','개그':'H','미스터리':'I','로맨스':'J','드라마':'K','무협':'L','스포츠':'M','일상':'N','학원':'O','성인':'P','한국':'Q','중국':'R'}
week = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일','열흘']

###
def click_and_crawl(update_num,week_num):
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[4]/ul/li[%d]/a' %p).click()
    response = requests.get(driver.current_url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    webtoon_list = soup.find_all('li', {'data-weekday': week[week_num]})

    for webtoon in webtoon_list:
        # wb_siteInfo[C2]에 나중에 업데이트를 쉽게하기 위해 이름만 저장해놓고
        # wb_webtoon[A2]에 웹툰 제목 저장
        wb_siteInfo['C%d' %update_num] = webtoon['date-title']
        wb_webtoon['A%d' %update_num] = webtoon['date-title']

        # wb_webtoon[F~R 2]에 해당하는거 저장
        genre = webtoon['data-genre'].split(',')
        for i, g in enumerate(genre):
            if g in cell_alp.keys():
                wb_webtoon[cell_alp[g] + '%d' % update_num] = 1

        # wb_webtoon[S2]에 저장
        wb_webtoon['S%d' % update_num] = webtoon['data-weekday']

        # wb_webtoon[B2]에 저장

        update_num += 1
    return update_num
def first_page_crawl(update_num,week_num):
    driver.implicitly_wait(10)
    response = requests.get(driver.current_url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    webtoon_list = soup.find_all('li', {'data-weekday': week[week_num]})
    pages = soup.find_all('div', {'class': 'list-page text-center'})
    for page in pages:
        p = page.select('ul > li')
    total_page = len(p) - 1

    for webtoon in webtoon_list:
        # wb_siteInfo[C2]에 나중에 업데이트를 쉽게하기 위해 이름만 저장해놓고
        # wb_webtoon[A2]에 웹툰 제목 저장
        wb_siteInfo['C%d' % update_num] = webtoon['date-title']
        wb_webtoon['A%d' % update_num] = webtoon['date-title']

        # wb_webtoon[F~R 2]에 해당하는거 저장
        genre = webtoon['data-genre'].split(',')
        for i, g in enumerate(genre):
            if g in cell_alp.keys():
                wb_webtoon[cell_alp[g] + '%d' % update_num] = 1

        # wb_webtoon[S2]에 저장
        wb_webtoon['S%d' % update_num] = webtoon['data-weekday']

        # wb_webtoon[B2]에 저장

        # print(webtoon['data-initial'])
        # print(webtoon['data-genre'])
        # print(webtoon['date-title'])
        # print("+++++++++++++++++++++++")

        update_num += 1
    return total_page, update_num
###

total_page, update_num = first_page_crawl(update_num,0)
print("월요일 Page 1 End")
for p in range(4,total_page):
    update_num = click_and_crawl(update_num,0)
    print("월요일 Page " + str(p - 2) + " End")

for w in range(1, len(week)):
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH,
                        '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[2]/td/span[%c]' %str(w+2)).click()
    driver.find_element(By.XPATH,
                        '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').send_keys(
        Keys.ENTER)

    total_page, update_num = first_page_crawl(update_num, w)
    print(week[w] + " Page 1 End")
    for p in range(4, total_page):
        update_num = click_and_crawl(update_num, w)
        print(week[w] + " Page " + str(p - 2) + " End")
    wb.save(fpath)
# 웹툰 총 화수 저장
wb_siteInfo['D2'] = update_num


# ## 다음페이지
# driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[4]/ul/li[4]/a').click()
#
# response = requests.get(driver.current_url,headers={'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'} )
# html = response.text
# soup = BeautifulSoup(html,'html.parser')
# webtoon_list = soup.find_all('li',{'data-weekday':"월요일"})
# for webtoon in webtoon_list:
#     print(webtoon['data-initial'])
#     print(webtoon['data-genre'])
#     print(webtoon['date-title'])
#     print("+++++++++++++++++++++++")

## 이제 상세페이지에서 바로 접속 가능한지 찾아보자
## 아니면 클릭해서 넘어가야한다 일일히 4천 몇개를


# 바뀐 주소 저장
# !!주소가 자동으로 최신주소로 바뀌어줘서 driver상 주소는 바뀌지않는다
k = driver.current_url.find('.com')
url3 = url2[:k+4]
if saved_url != url3:
    wb_siteInfo['A2'] = url3


###
### 로그인은 굳이 할 필요가 없을 것 같고, 캡챠입력은 수동으로 받도록 하자.
### https://www.youtube.com/watch?v=ZNOiwvrS_dc

### 걍 1화 링크 걸어주자
wb.save(fpath)
driver.implicitly_wait(3)
driver.quit()

e_time = time.time()
print("총 실행시간 : " + str(e_time-s_time))