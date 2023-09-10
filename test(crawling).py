from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import re
import os
import time
import csv
import pandas
from datetime import datetime, timedelta
import requests
import openpyxl
import pyautogui
import pyperclip

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

fpath = r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki4.xlsx'
wb = openpyxl.load_workbook(fpath)
df = pandas.read_csv('src/Newtoki.csv',encoding='UTF8')

wb_siteInfo = wb['Site Information']
wb_webtoon = wb['webtoon']
url = wb_siteInfo['A2'].value
saved_url = wb_siteInfo['A2'].value
update_num = wb_siteInfo['D2'].value
# 프로그램 총 실행시간 체크
temp = "/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0"
url2 = url + temp
url3 = 'https://newtoki307.com/webtoon/27392253?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0'


s_time = time.time()
# driver.implicitly_wait(10)
# driver.get(url3)
# response = requests.get(driver.current_url, headers={
#         'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
# html = response.text
# soup = BeautifulSoup(html, 'html.parser')
# image_src = soup.find('div',{'class' : 'img-item'})
# images = driver.find_elements(By.CSS_SELECTOR,'div.img-item>a>img')
# names = driver.find_elements(By.CSS_SELECTOR,'div.img-item>div>a>span')
# detail_pages = driver.find_elements(By.CSS_SELECTOR, 'div.img-item>a')

# first_story_url = driver.find_element(By.CSS_SELECTOR, 'th.active > button')
# print(str(first_story_url.get_attribute('onclick'))[15:-1])


# urls = driver.find_elements(By.CSS_SELECTOR, 'div#webtoon-list > ul > li')
# print(urls[0].find_element(By.TAG_NAME, 'a').get_attribute('href'))
# print(urls[95].find_element(By.TAG_NAME, 'a').get_attribute('href'))


# for url in urls:
#     a = url.find_element(By.TAG_NAME, 'a').get_attribute('href')
#     print(a)

# webtoon_name = []
# opener = urllib.request.URLopener()
# opener.addheader('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
# for name in names:
#     # print(name.text)
#     new_name = re.sub(r"[^\uAC00-\uD7A30\s]","",name.text)
#     webtoon_name.append(new_name)
# print(webtoon_name)
# print(images[0].get_attribute('src'))

# temp = requests.get(images[0].get_attribute('src'))
# with open(f'src/img/0.png',"wb") as outfile:
#     outfile.write(temp.content)
# for i, image in enumerate(images):
#     img = image.get_attribute('src')
#     # print(img)
#     name = webtoon_name[i]
#     opener.retrieve(img,f'src/img/{webtoon_name[i]}.png')
# print(len(images))

# for detail_page in detail_pages:
#     detail_url = detail_page.get_attribute('href')
# print(detail_url)
#
# for i in range(len(detail_pages)):
#     detail = detail_pages[i].get_attribute('href')
# print(detail)
from urllib.parse import quote_from_bytes
# print(detail_url)
# def detail_page(i):
#     accessing_s_time = time.time()
#     detail_url = wb_webtoon['V%d' %(i+2)].value
#     driver.get(detail_url)
#     accessing_e_time = time.time()
#
#     captcha_s_time = time.time()
#     if i == 0:
#         captcha_num = pyautogui.prompt("Captcha 입력 >> ")
#         captcha = driver.find_element(By.XPATH, '//*[@id="captcha_key"]')
#         captcha.send_keys(captcha_num)
#         driver.find_element(By.XPATH,
#                             '//*[@id="content_wrapper"]/div[2]/div/div[2]/div/div/div[2]/form/div[3]/div[2]/button').send_keys(
#             Keys.ENTER)
#     captcha_e_time = time.time()
#     driver.implicitly_wait(5)
#
#     # 총 회차수
#     total_num_s_time = time.time()
#     total_num = driver.find_element(By.CSS_SELECTOR, 'ul.list-body>li').text
#     print(total_num[0])
#     total_num_e_time = time.time()
#     # 추천수
#     recommend_s_time = time.time()
#     recommend_num = driver.find_element(By.ID, 'wr_good').text
#     print(recommend_num)
#     recommend_e_time = time.time()
#     # 별점
#     star_s_time = time.time()
#     stars = driver.find_elements(By.CSS_SELECTOR, 'button.btn-white > i')
#     star_point = 0
#     for star in stars:
#         if star.get_attribute('class') == 'fa fa-star crimson':
#             star_point += 1
#         elif star.get_attribute('class') == 'fa fa-star-half-empty crimson':
#             star_point += 0.5
#         else:
#             continue
#     print(star_point)
#     star_e_time = time.time()
#
#     print("한 웹툰 url 접근 시간 : " + str(accessing_e_time-accessing_s_time))
#     print("한 웹툰 캡챠 시간 : " + str(captcha_e_time-captcha_s_time))
#     print("한 웹툰 총화 시간 : " + str(total_num_e_time-total_num_s_time))
#     print("한 웹툰 추천 시간 : " + str(recommend_e_time-recommend_s_time))
#     print("한 웹툰 별점 시간 : " + str(star_e_time-star_s_time))
#     print("한 웹툰 총 실행 시간 : " + str(star_e_time-accessing_s_time))
#
# def temp():
#     print(driver.current_url)
#
#
# for i in range(2):
#         detail_page(i)
#         temp()
# detail_url = wb_webtoon['V2'].value
# driver.get(detail_url)
#
# captcha_num = pyautogui.prompt("Captcha 입력 >> ")
# captcha = driver.find_element(By.XPATH,'//*[@id="captcha_key"]')
# captcha.send_keys(captcha_num)
# driver.find_element(By.XPATH,'//*[@id="content_wrapper"]/div[2]/div/div[2]/div/div/div[2]/form/div[3]/div[2]/button').send_keys(Keys.ENTER)
#
#
# driver.implicitly_wait(5)
# # 총 회차수
# total_num = driver.find_element(By.CSS_SELECTOR,'ul.list-body>li').text
# print(total_num[0])
# # 추천수
# recommend_num = driver.find_element(By.ID,'wr_good').text
# print(recommend_num)
# # 별점
# stars = driver.find_elements(By.CSS_SELECTOR,'button.btn-white > i')
# star_point = 0
# for star in stars:
#         if star.get_attribute('class') == 'fa fa-star crimson':
#                 star_point += 1
#         elif star.get_attribute('class') == 'fa fa-star-half-empty crimson':
#                 star_point += 0.5
#         else:
#                 continue
# print(star_point)
# print("===========================")
#
# detail_url = wb_webtoon['V3'].value
# driver.get(detail_url)
#
# driver.implicitly_wait(5)
# # 총 회차수
# total_num = driver.find_element(By.CSS_SELECTOR,'ul.list-body>li').text
# print(total_num[0])
# # 추천수
# recommend_num = driver.find_element(By.ID,'wr_good').text
# print(recommend_num)
# # 별점
# stars = driver.find_elements(By.CSS_SELECTOR,'button.btn-white > i')
# star_point = 0
# for star in stars:
#         if star.get_attribute('class') == 'fa fa-star crimson':
#                 star_point += 1
#         elif star.get_attribute('class') == 'fa fa-star-half-empty crimson':
#                 star_point += 0.5
#         else:
#                 continue
# print(star_point)
#

import matplotlib.pyplot as mat_plt
import matplotlib.image as mat_img
# i = 0~(update_num-2)
def detail_page(i):
        a_s_time = time.time()
        # detail_url = wb_webtoon['U' + str(int(i)+2)].value
        detail_url = df['url'][i]
        # print(detail_url)
        driver.get(detail_url)
        #!! 만약 캡챠 틀렸을때도 고려해야한다
        if i == 0:
                #!! 캡챠 이미지를 다운 받아서 출력해준다면
                #!! driver를 headless로 해서 속도를 올리려함
                #~~ 이 작업을 수행하려 하니 IP차단이 먹힘
                #~~ 화면 캡쳐를 통해 캡챠이미지 추출
                #!! 결국 캡챠가 안뚫린다 어쩌냐
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                captcha = driver.get_screenshot_as_png()
                open('captcha.png','wb').write(captcha)
                a = mat_img.imread('captcha.png')
                print(driver.current_url)
                mat_plt.imshow(a[375:410, 540:600])
                mat_plt.show()
                captcha_num = pyautogui.prompt("Captcha 입력 >> ")
                captcha = driver.find_element(By.ID, 'captcha_key')
                captcha.click()
                pyperclip.copy(captcha_num)
                captcha.send_keys(Keys.CONTROL,'v')

                # captcha.send_keys(captcha_num)
                time.sleep(3)

                # driver.find_element(By.CLASS_NAME,'btn btn-color pull-right').send_keys(
                #         Keys.ENTER)
                driver.find_element(By.CLASS_NAME, 'btn-color').click()
                # time.sleep(10)

                driver.implicitly_wait(10)
        # detail_url2 = wb_webtoon['U' + str(int(i+3))].value
        # driver.get(detail_url2)
        # detail_url2 = df['url'][i+1]
        # driver.get(detail_url2)
        driver.refresh()
        driver.implicitly_wait(10)
        print(driver.current_url)
        try:
                response = requests.get(driver.current_url, headers={
                        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
                html = response.text
        except UnicodeDecodeError as error:
                print(error)
                resolved_url = urllib.request.Request(driver.current_url, headers={
                        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
                response = urllib.request.urlopen(resolved_url)
                html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
        a_e_time = time.time()
        # a = input()

        # 총 회차수
        # wb_webtoon[E2]
        try:
                b_s_time = time.time()
                # total_num = driver.find_element(By.CSS_SELECTOR, 'ul.list-body>li').get_attribute('data-index')
                total_num = soup.find_all('li',{'class':'list-item'})

                print("total num start")
                print(total_num)
                print("total num end")
                a = input()
                # wb_webtoon['E' + str(int(i) + 2)] = int(total_num)
                b_e_time = time.time()
        except Exception as e:
                print(e)
                wb_webtoon['E' + str(int(i) + 2)] = 0
        # print(int(total_num))


        # 추천수
        # wb_webtoon[C2]
        c_s_time = time.time()
        recommend_num = driver.find_element(By.ID, 'wr_good').text
        recommend_num2 = soup.find('b',{'id':'wr_good'}).text
        wb_webtoon['C' + str(int(i)+2)] = int(recommend_num)
        print(recommend_num2)
        c_e_time = time.time()

        # 별점
        # wb_webtoon[D2]
        d_s_time = time.time()
        stars = driver.find_elements(By.CSS_SELECTOR, 'button.btn-white > i')
        star_point = 0
        for star in stars:
                if star.get_attribute('class') == 'fa fa-star crimson':
                        star_point += 1
                elif star.get_attribute('class') == 'fa fa-star-half-empty crimson':
                        star_point += 0.5
                else:
                        continue

        # star_temp = soup.find_all('i')
        # full_star = soup.find_all('i',{'class':'fa fa-star crimson'})
        # half_star = soup.find_all('i',{'class':'fa fa-star-half-empty crimson'})
        # no_star = soup.find_all('i',{'class':'fa fa-star-o crimson'})
        # print(len(full_star), len(half_star), len(no_star))
        # print(star_temp)
        # star_point = full_star +

        wb_webtoon['D' + str(int(i)+2)] = star_point
        # print(star_point)
        d_e_time = time.time()


        # wb_webtoon[T2]
        e_s_time = time.time()
        first_story_url = str(driver.find_element(By.CSS_SELECTOR, 'th.active > button').get_attribute('onclick'))[
                          15:-1]
        # first_story_url = str(soup.find(attrs={'data-original-title':'첫회보기'}))[15:-1]
        wb_webtoon['T' + str(int(i)+2)] = first_story_url
        # print(first_story_url)
        e_e_time = time.time()


        print("한 웹툰 접속 시간 : " + str(a_e_time-a_s_time))
        print("한 웹툰 총 화수 저장 시간 : " + str(b_e_time-b_s_time))
        print("한 웹툰 추천 저장 시간 : " + str(c_e_time-c_s_time))
        print("한 웹툰 별점 저장 시간 : " + str(d_e_time-d_s_time))
        print("한 웹툰 첫화 링크 저장 시간 : " + str(e_e_time-e_s_time))
        print("한 웹툰 총 실행 시간 : " + str(e_e_time-a_s_time))
        now = datetime.now()
        print("현재 시간 : " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) +"초")
        print("=========================")

for i in range(3):
        detail_page(i)
        wb.save(fpath)

driver.implicitly_wait(3)
driver.quit()
e_time = time.time()
print("총 실행시간 : " + str(e_time-s_time))
