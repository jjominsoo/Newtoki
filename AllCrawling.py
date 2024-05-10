from typing import List, Any

import Captcha
import CreateFile

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import requests
import shutil
import re
import time

from tqdm import tqdm

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

def PageCrawling(url, week, toon_name, toon_genre, toon_week):
    soup = GetSoup(url)

    if week == '열흘':
        webtoon_list = soup.find_all('li', {'data-weekday': week})
    else:
        webtoon_list = soup.find_all('li', {'data-weekday': week + '요일'})
    for i, webtoon in enumerate(webtoon_list):
        # TEST ####
        # if i == 5:
        #     break
        toon_name.append(webtoon['date-title'])
        toon_genre.append(webtoon['data-genre'])
        toon_week.append(week)
    return toon_name, toon_genre, toon_week

def DetailCrawling(name, url, cookie,  driver, webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_update, webtoon_recommend, webtoon_plot):
    # 매 사이트를 접속할 때마다 세션을 새로 설정해야함
    # 세션을 독립적으로 운용하여 요청간 상태가 분리되고 서로 영향을 미치지 않음
    # print("=============================================================================")
    print(f"\n{name} Detail Crawling Start!")
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    session.headers.update(headers)
    session.cookies.update(cookie)
    response = session.get(url, headers={'User-agent': user_agent})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    update_flag = 0

    # 이미지(다운로드)
    webtoon_name_strip = re.sub(r'[^\w\s]+|\s+', '', name)
    try:
        images = soup.find('div', {'class': 'view-img'})
        image = images.find('img').attrs['src']
        img = requests.get(image)
        with open(f'src/img/{webtoon_name_strip}.png', 'wb') as outfile:
            outfile.write(img.content)
        webtoon_img.append(f'src/img/{webtoon_name_strip}.png')
    except Exception as e:
        print(f"Error at Image\n{e}")
        temp_img = "src/file/no_image.png"
        img = f'src/img/{webtoon_name_strip}.png'
        shutil.copyfile(temp_img, img)
        webtoon_img.append(f'src/img/{webtoon_name_strip}.png')

    # 총화수(int)
    try:
        nums = len(soup.find_all('li', {'class': 'list-item'}))
        webtoon_num.append(nums)
    except Exception as e:
        print(f"Error at Webtoon Num\n{e}")
        nums = 0
        webtoon_num.append(nums)

    # 댓글(list)
    reply_flag = 0
    star_reply = ""
    try:
        reply_section = soup.find('div', {'id': 'viewcomment'})
        best_replys_list = reply_section.find('section', {'id': 'bo_vcb'})
        best_replys = best_replys_list.find_all('div', {'class': 'media-content'})
        best_replys_stars = best_replys_list.find_all('div', {'class': 'media-heading'})
        for br, brs in zip(best_replys, best_replys_stars):
            b_star = len(brs.find_all('i', {'class': 'fa fa-star fa-lg crimson'}))
            if b_star >= 1:
                b_reply = re.sub(r'[\r\n]+', '', br.text.strip())
                star_reply = ''.join([star_reply, str(b_star), b_reply])+"|"

        replys_list = reply_section.find('section', {'id': 'bo_vc'})
        replys = replys_list.find_all('div', {'class': 'media-content'})
        replys_stars = replys_list.find_all('div', {'class': 'media-heading'})
        for r, rs in zip(replys, replys_stars):
            star = len(rs.find_all('i', {'class': 'fa fa-star fa-lg crimson'}))
            if star >= 1:
                reply = re.sub(r'[\r\n]+', '', r.text.strip())
                star_reply = ''.join([star_reply + '|' + str(star), reply])
        reply_flag = 1

        reply_pages = reply_section.find('div', {'class': 'text-center'}).select('ul > li')
        for rp in range(len(reply_pages)-5):
            # 다음페이지 클릭
            driver.find_element(By.XPATH, f'//*[@id="viewcomment"]/div[2]/ul/li[{rp+2}]/a').click()
            reply_response = session.get(url, headers={'User-agent': user_agent})
            reply_html = reply_response.text
            reply_soup = BeautifulSoup(reply_html, 'html.parser')

            reply_section = reply_soup.find('div', {'id': 'viewcomment'})
            replys_list = reply_section.find('section', {'id': 'bo_vc'})
            replys_star = replys_list.find_all('div', {'class': 'media-heading'})
            replys = replys_list.find_all('div', {'class': 'media-content'})

            for r, rs in zip(replys, replys_star):
                star = len(rs.find_all('i', {'class': 'fa fa-star fa-lg crimson'}))
                if star >= 1:
                    reply = re.sub(r'[\r\n]+', '', r.text.strip())
                    star_reply = ''.join([star_reply+'|'+str(star), reply])

        webtoon_reply.append(star_reply)
    except Exception as e:
        print(f"Error at Reply\n{e}")
        if reply_flag:
            webtoon_reply.append(star_reply)
        else:
            webtoon_reply.append('')

    # 별점(화수)(list)
    star1_first_date = ''
    star1_last_date = ''
    try:
        star1_temp = []
        star1_lists = soup.find('div', {'class': 'serial-list'}).select('ul > li')
        for index, star1 in enumerate(star1_lists):
            if index == 0:
                star1_first_date = star1.find('div', {'class': 'wr-date'}).text.strip()
            if index == len(star1_lists) - 1:
                star1_last_date = star1.find('div', {'class': 'wr-date'}).text.strip()
            star1_rating = star1.find('div', {'class': 'wr-star'}).text.strip().split('(')[-1].split(')')[0]
            star1_temp.append(float(star1_rating))
        star1_temp.sort(reverse=True)
        star1 = ','.join(map(str, star1_temp))
        webtoon_star1.append(star1)

        update = ','.join([star1_first_date, star1_last_date])
        print(update)
        webtoon_update.append(update)
    except Exception as e:
        print(f"Error at Star1 or Update\n{e}")
        if update_flag == 0:
            webtoon_update.append('')

    # 별점(총)(float)
    try:
        star2_lists = soup.find('div', {'class': 'view-comment'}).text.strip().split()
        star2_rating = star2_lists[2]
        star2_count = star2_lists[-1]
        star2 = ','.join([star2_rating, star2_count])
        webtoon_star2.append(star2)
    except Exception as e:
        print(f"Error at Star2\n{e}")

    # 추천수(int)
    try:
        webtoon_recommend_temp = str(soup.find('b', {'id': 'wr_good'}).text)
        webtoon_recommend.append(int(webtoon_recommend_temp.replace(",", "")))
    except Exception as e:
        print(f"Error at Recommend\n{e}")
        webtoon_recommend_temp = 0
        webtoon_recommend.append(webtoon_recommend_temp)

    # 줄거리
    try:
        plot = soup.find('div', {'class': 'col-sm-8'}).find_all('div')[1].text.strip()
        webtoon_plot.append(plot)
    except Exception as e:
        print(f"Error at Plot\n{e}")
        webtoon_plot.append('')

    return webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update

def AllCrawling(url, driver):
    # TEST ####
    weeks = ['수']
    # weeks = ['월', '화', '수', '목', '금', '토', '일', '열흘']
    driver.get(url)
    driver.maximize_window()
    cookie = Captcha.Login(driver)

    # 일주일을 볼껀데
    for week in weeks:
        print(week + '요일 웹툰 크롤링')
        WebDriverWait(driver, 10)
        driver.refresh()
        print(driver.current_url)
        driver.find_element(By.CSS_SELECTOR, f'span[data-value="{week}"]').click()
        WebDriverWait(driver, 10)
        driver.find_element(By.XPATH,
                            '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').click()
        WebDriverWait(driver, 10)
        soup = GetSoup(driver.current_url)

        # 각 요일마다 페이지를 클릭하면서 볼꺼다
        pages = soup.find('div', {'class': 'list-page'}).select('ul > li')
        for i in range(len(pages) - 4):
            # 전역변수를 매번 초기화 하자
            webtoon_name = []
            webtoon_genre = []
            webtoon_week = []
            webtoon_img = []
            webtoon_num = []
            webtoon_reply = []
            webtoon_star1 = []
            webtoon_star2 = []
            webtoon_recommend = []
            webtoon_plot = []
            webtoon_update = []
            if i != 0:
                print(f"{week}요일 {i + 1} page")
                driver.find_element(By.XPATH, f'//*[@id="fboardlist"]/div[4]/ul/li[{i + 3}]/a').click()
                time.sleep(0.5)
            else:
                print(f"{week}요일 Crawling Start")
                print(f"{week}요일 1 page")

            webtoon_name, webtoon_genre, webtoon_week = PageCrawling(driver.current_url, week, webtoon_name, webtoon_genre, webtoon_week)
            webtoons = driver.find_elements(By.XPATH, '//*[@id="webtoon-list-all"]/li')

            print(webtoon_name)
            # TEST ####
            # for j in tqdm(range(5)):
            for j in tqdm(range(len(webtoons))):
                try:
                    WebDriverWait(driver, 10)
                    driver.find_element(By.XPATH, f'//*[@id="webtoon-list-all"]/li[{j + 1}]/div/div/div/div[1]/div/div/a').click()
                except Exception as e:
                    print(f"Non-valid detail page link\n{e}")
                    WebDriverWait(driver, 10)
                    driver.find_element(By.XPATH, f'//*[@id="webtoon-list-all"]/li[{j + 1}]/div[2]/div/div/div[1]/div/div/a').click()

                webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update = DetailCrawling(
                    webtoon_name[j], driver.current_url, cookie, driver, webtoon_img, webtoon_num, webtoon_reply,
                    webtoon_star1, webtoon_star2, webtoon_update, webtoon_recommend, webtoon_plot)
                driver.back()
                WebDriverWait(driver, 10)
            CreateFile.CreateDF(webtoon_name, webtoon_genre, webtoon_week, webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update)
            print(f'{week}요일 Page {i + 1} 끝')
        print(f'{week}요일 웹툰 크롤링 끝')

def GetSoup(url):
    response = requests.get(url, headers={'User-agent': user_agent})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

import pandas as pd

# def SearchGoogleCrawling(driver):
#     df = pd.read_csv('src/file/name.csv')
#     driver.get('https://www.google.com')
#     driver.find_element(By.XPATH, '//*[@id="gb"]/div/div[2]/a').click()
#     driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys('hollyshit139@gmail.com')
#     driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
#     time.sleep(7)
#     driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys('shitholly931')
#     driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
#     time.sleep(7)
#     try:
#         print("보안코드 해야함")
#         driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[2]/div/div/button/span').click()
#         driver.find_element(By.XPATH,
#                             '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/section/div/div/div/ul/li[1]/div').click()
#         k = input('스탑!')
#     except Exception as e:
#         print("크롤링진행하자")
#     count = 0
#     for query in df['이름']:
#         # 카카오 웹툰
#         driver.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys(query + ' 웹툰')
#         if count == 0:
#             driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]').click()
#             count = 1
#         else:
#             driver.find_element(By.CLASS_NAME, "Tg7LZd").send_keys(Keys.ENTER)
#         platform = []
#         try:
#             driver.implicitly_wait(10)
#             a = driver.find_elements(By.CSS_SELECTOR, 'span.VuuXrf')
#             temp = []
#             # 플랫폼은 3개만 받을거다 (메이저플랫폼만 받기 위해)
#             # 그리고 모든 플랫폼을 저장할 것이다.
#             # 중복되면 따로 저장은 안한다.
#             for j in range(0, 5, 2):
#                 # 플랫폼 종류 확인
#                 if a[j].text == 'kakao.com' or a[j].text == "kakaocorp.com":
#                     temp_nft = '카카오'
#                 elif a[j].text == 'Naver':
#                     temp_nft = '네이버'
#                 elif a[j].text == 'Lezhin Comics':
#                     temp_nft = '레진'
#                 else:
#                     temp_nft = a[j].text
#                 if temp_nft not in platform:
#                     platform.append(temp_nft)
#                     print(platform)
#                 if temp_nft in temp:
#                     continue
#                 temp.append(temp_nft)
#         except Exception as e:
#             print(f'{e}')
#             k = input('')
#         driver.find_element(By.XPATH, '//*[@id="APjFqb"]').clear()

import traceback
import random
import datetime
from selenium.webdriver.support import expected_conditions as EC







# def LezhinCrawling(driver):
#       # name platform link genre state(업데이트 마지막날짜) week(업데이트 날짜기준) author drawing keyword plot
# def LezhinPageCrawling():