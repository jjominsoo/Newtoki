from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import os
import re
import time
from datetime import datetime, timedelta
import requests
import openpyxl
import pyautogui
from openpyxl.drawing.image import Image
import urllib.request
from urllib.request import urlretrieve
import urllib
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.implicitly_wait(5)

# 엑셀파일에 저장된 최근에 접속가능했던 주소를 가져와서 진행한다.
fpath = r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki2.xlsx'
wb = openpyxl.load_workbook(fpath)
wb_siteInfo = wb['Site Information']
wb_webtoon = wb['webtoon']
url = wb_siteInfo['A2'].value
saved_url = wb_siteInfo['A2'].value
update_num = wb_siteInfo['D2'].value
#
genre = []
webtoon_name = []
#
cell_alp = {'판타지':'F','액션':'G','개그':'H','미스터리':'I','로맨스':'J','드라마':'K','무협':'L','스포츠':'M','일상':'N','학원':'O','성인':'P','한국':'Q','중국':'R'}
week = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일','열흘']

# 프로그램 총 실행시간 체크
s_time = time.time()

###
#!! 마찬가지로 지금은 월요일 부터 열흘까지 하지만
#!! 중간에 특정 요일만 크롤링 하고 싶으면 그렇게 하도록 해야하므로
#!! w대신 새로운 변수를 넣어서 그것이 true면 첫페이지를 가져와야하고
#!! 아니라면 다음 요일 클릭하도록 해야한다.
def first_page(url,w):
    if w == 0:
        accessing_page_s_time = time.time()
        temp = "/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0"
        #!! 네트워크 속도가 빠르면 페이지 인식을 못하는 것 같다. ( 너무빨리 지나가서? )
        #!! 핫스팟으론 되는데 집 와이파이로는 되긴 됐지만 일요일-열흘 이 부분이 안됐다.
        #!! 다시 한번 해봐야 알듯
        #!! https://newtoki306.com/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0
        while (1):
            try:
                time.sleep(1)
                url2 = url + temp
                time.sleep(1)
                url3 = 'https://www.naver.com'
                driver.get(url2)
                # time.sleep(3)
                a = input()
                driver.implicitly_wait(10)
                # [월]이란 버튼 클릭
                driver.find_element(By.XPATH,
                                    '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[2]/td/span[2]').click()
                driver.find_element(By.XPATH,
                                    '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').send_keys(
                    Keys.ENTER)
                break
            except Exception as error:
                a = input()

                print(error)
                time.sleep(1)
                num = int(re.sub(r'[^0-9]', '', url)) + 1
                #!! 여기 좀 수정해야할듯??
                url = "https://newtoki" + str(num) + ".com"
                # print(num)

        accessing_page_e_time = time.time()
        print("첫 웹사이트 접속 시간 : " + str(accessing_page_e_time - accessing_page_s_time))
    else:
        other_day_click_s_time = time.time()
        driver.implicitly_wait(5)
        # 다음요일 클릭 [화],[수]...
        driver.find_element(By.XPATH,
                            '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[2]/td/span[%c]' % str(
                                w + 2)).click()
        driver.find_element(By.XPATH,
                            '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').send_keys(
            Keys.ENTER)
        other_day_click_e_time = time.time()
        print("다른 요일 클릭 시간 : " + str(other_day_click_e_time - other_day_click_s_time))

    driver.implicitly_wait(5)
    time.sleep(1)
    response = requests.get(driver.current_url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('div', {'class': 'list-page text-center'})

    for page in pages:
        p = page.select('ul > li')
    # 버튼들까지 합쳐서 (페이지수 + 4)개가 나오므로
    # 밑의 함수에서 가독성을 위해 실제페이지 + 1을 저장한다
    total_page = len(p) - 3

    return total_page

#!! 요소 헷갈리니까 좀 보기 편하게 하자
#!! 목표 = week_num 을 한글로 입력 ( 일요일 ) 하면 일요일 웹툰 하는걸로
# code_temp에 예전 코드 있음 (1)
def page_crawl(update_num,week_num,p):
    # 첫페이지가 아니면
    if p != 1:
        next_page_click_s_time = time.time()
        driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[4]/ul/li[%d]/a' %(p+2)).click()
        next_page_click_e_time = time.time()
        print("다음 페이지 클릭 시간 : " + str(next_page_click_e_time - next_page_click_s_time))

    driver.implicitly_wait(5)
    setting_s_time = time.time()
    response = requests.get(driver.current_url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    webtoon_list = soup.find_all('li', {'data-weekday': week[week_num]})
    detail_pages = driver.find_elements(By.CSS_SELECTOR,'div#webtoon-list > ul > li')
    images = driver.find_elements(By.CSS_SELECTOR, 'div.img-item>a>img')
    names = driver.find_elements(By.CSS_SELECTOR, 'div.img-item>div>a>span')
    setting_e_time = time.time()
    print("사이트 선언 시간 : " + str(setting_e_time-setting_s_time))

    # 이미지 저장
    single_toon_img_s_time = time.time()
    for image, name in zip(images,names):
        new_name = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]","",name.text)
        temp = requests.get(image.get_attribute('src'))
        with open(f'src/img/{new_name}.png', "wb") as outfile:
            outfile.write(temp.content)
    single_toon_img_e_time = time.time()

    # 이름, 장르, 요일, 상세페이지 url 저장
    for i, webtoon in enumerate(webtoon_list):
        # wb_siteInfo[C2]에 나중에 업데이트를 쉽게하기 위해 이름만 저장해놓고
        # wb_webtoon[A2]에 웹툰 제목 저장
        single_toon_name_s_time = time.time()
        wb_siteInfo['C%d' % update_num] = webtoon['date-title']
        wb_webtoon['A%d' % update_num] = webtoon['date-title']
        new_name = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]","",webtoon['date-title'])
        webtoon_name.append(new_name)

        single_toon_name_e_time = time.time()

        # wb_webtoon[F~R 2]에 해당하는거 저장
        single_toon_genre_s_time = time.time()
        genre = webtoon['data-genre'].split(',')
        for g in genre:
            if g in cell_alp.keys():
                wb_webtoon[cell_alp[g] + '%d' % update_num] = 1
        single_toon_genre_e_time = time.time()

        # wb_webtoon[S2]에 저장
        single_toon_day_s_time = time.time()
        wb_webtoon['S%d' % update_num] = webtoon['data-weekday']
        single_toon_day_e_time = time.time()

        # wb_webtoon[V2]에 저장
        single_toon_url_s_time = time.time()
        detail_url = detail_pages[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
        wb_webtoon['V%d'%update_num] = detail_url
        single_toon_url_e_time = time.time()

        update_num += 1

    one_page_e_time = time.time()


    print("한 웹툰 이름 저장시간 : " + str(single_toon_name_e_time-single_toon_name_s_time))
    print("한 웹툰 장르 저장시간 : " + str(single_toon_genre_e_time-single_toon_genre_s_time))
    print("한 웹툰 요일 저장시간 : " + str(single_toon_day_e_time-single_toon_day_s_time))
    print("한 웹툰 이미지 저장시간 : " + str(single_toon_img_e_time-single_toon_img_s_time))
    print("한 웹툰 url 저장시간 : " + str(single_toon_url_e_time-single_toon_url_s_time))
    print("한 페이지 총 실행시간 : " + str(one_page_e_time-setting_s_time))


    return update_num


def detail_page(i):
    detail_url = wb_webtoon['V%d'%i+2].value
    driver.get(detail_url)
    if i == 0:
        captcha_num = pyautogui.prompt("Captcha 입력 >> ")
        captcha = driver.find_element(By.XPATH, '//*[@id="captcha_key"]')
        captcha.send_keys(captcha_num)
        driver.find_element(By.XPATH,
                            '//*[@id="content_wrapper"]/div[2]/div/div[2]/div/div/div[2]/form/div[3]/div[2]/button').send_keys(
            Keys.ENTER)
    driver.implicitly_wait(5)
    # 총 회차수
    total_num = driver.find_element(By.CSS_SELECTOR, 'ul.list-body>li').text
    print(total_num[0])
    # 추천수
    recommend_num = driver.find_element(By.ID, 'wr_good').text
    print(recommend_num)
    # 별점
    stars = driver.find_elements(By.CSS_SELECTOR, 'button.btn-white > i')
    star_point = 0
    for star in stars:
        if star.get_attribute('class') == 'fa fa-star crimson':
            star_point += 1
        elif star.get_attribute('class') == 'fa fa-star-half-empty crimson':
            star_point += 0.5
        else:
            continue


# code_temp (2), (3)
for w in range(len(week)):
    page_num = first_page(url,w)
    wb_siteInfo['D2'] = update_num
    wb.save(fpath)
    for p in range(1,page_num):
        update_num = page_crawl(update_num,w,p)
        wb_siteInfo['D2'] = update_num
        wb.save(fpath)
        now = datetime.now()
        print(str(week[w]) + " Page " + str(p) +" End")
        print("현재 시간 : " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) +"초\n")

## 이제 상세페이지에서 바로 접속 가능한지 찾아보자
# detail_page()
## 아니면 클릭해서 넘어가야한다 일일히 4천 몇개를

# 바뀐 주소 저장
k = driver.current_url.find('.com')
new_url = driver.current_url[:k+4]
if saved_url != new_url:
    wb_siteInfo['A2'] = new_url

wb.save(fpath)
driver.implicitly_wait(3)
driver.quit()

e_time = time.time()
print("총 실행시간 : " + str(e_time-s_time))