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
        WebDriverWait(driver, 2)
        driver.refresh()
        print(driver.current_url)
        driver.find_element(By.CSS_SELECTOR, f'span[data-value="{week}"]').click()
        WebDriverWait(driver, 2)
        driver.find_element(By.XPATH,
                            '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').click()
        WebDriverWait(driver, 2)
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
                    WebDriverWait(driver, 5)
                    driver.find_element(By.XPATH, f'//*[@id="webtoon-list-all"]/li[{j + 1}]/div/div/div/div[1]/div/div/a').click()
                except Exception as e:
                    print(f"Non-valid detail page link\n{e}")
                    WebDriverWait(driver, 5)
                    driver.find_element(By.XPATH, f'//*[@id="webtoon-list-all"]/li[{j + 1}]/div[2]/div/div/div[1]/div/div/a').click()

                webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update = DetailCrawling(
                    webtoon_name[j], driver.current_url, cookie, driver, webtoon_img, webtoon_num, webtoon_reply,
                    webtoon_star1, webtoon_star2, webtoon_update, webtoon_recommend, webtoon_plot)
                driver.back()
                WebDriverWait(driver, 2)
            CreateFile.CreateDF(webtoon_name, webtoon_genre, webtoon_week, webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update)
            print(f'{week}요일 Page {i + 1} 끝')
        print(f'{week}요일 웹툰 크롤링 끝')

def GetSoup(url):
    response = requests.get(url, headers={'User-agent': user_agent})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

import pandas as pd
from selenium.webdriver.common.keys import Keys

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
from selenium.common.exceptions import TimeoutException

def KakaoCrawling(driver):
    webtoon = pd.read_csv('src/file/name.csv')
    df = pd.read_csv('src/file/search.csv')
    # TEST
    # df = pd.read_csv('src/file/search2.csv')
    mark = pd.read_csv('src/file/mark2.csv')
    num = int(mark['마지막번호'][0])
    driver.get('https://webtoon.kakao.com/')
    # 인증을 하고 가자
    k = input("인증 필요.. 인증 후 아무 문자 입력")
    print('인증 완료')
    driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/div[2]/div[2]/div/a[1]').click()
    webtoon_name: list[str] = []
    webtoon_platform: list[str] = []
    webtoon_author: list[str] = []
    webtoon_drawing: list[str] = []
    webtoon_link: list[str] = []
    webtoon_genre: list[str] = []
    webtoon_watched: list[str] = []
    webtoon_liked: list[str] = []
    webtoon_free: list[int] = []
    webtoon_plot: list[str] = []
    webtoon_keyword: list[str] = []
    webtoon_state: list[str] = []
    webtoon_week: list[str] = []
    webtoon_rotation: list[str] = []

    for index, query in tqdm(enumerate(webtoon['이름'][num:])):
        cur_time = int(datetime.datetime.now().timestamp())
        random.seed(cur_time)
        time.sleep(random.randint(1,2))
        try:
            mark['마지막번호'] = [num + index]
            mark.to_csv('src/file/mark2.csv', index=False)
            check = str(mark['체크'][0])
            time.sleep(random.randint(0, 1))
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
            time.sleep(random.randint(1, 2))
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').send_keys(query)
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a')))
            if driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li[1]/a/p').text.replace(' ', '') != query.replace(' ', ''):
                print(f"이 웹툰 체크해봐라(1) {query}")
                mark['체크'] = [check + ',' + query]
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a').click()
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a')))
            if driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li[1]/div/a/div/div/div[2]/picture/img').get_attribute('alt').replace(' ', '') != query.replace(' ', ''):
                print(f"이 웹툰 체크해봐라(2) {query}")
                mark['체크'] = [check + ',' + query]
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
            time.sleep(random.randint(1, 2))
            print(f"\n{query} 크롤링 시작!")
            ## 여기부터 에러
            webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot = \
                KakaoPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot)
            df_kakaoW = pd.DataFrame()
            # print(len(webtoon_name), len(webtoon_platform), len(webtoon_author), len(webtoon_link), len(webtoon_genre), len(webtoon_watched), len(webtoon_liked), len(webtoon_free), len(webtoon_plot), len(webtoon_keyword), len(webtoon_state), len(webtoon_week),len(webtoon_rotation))
            df_kakaoW['이름'] = webtoon_name
            df_kakaoW['플랫폼'] = webtoon_platform
            df_kakaoW['작가'] = webtoon_author
            df_kakaoW['첫화링크'] = webtoon_link
            df_kakaoW['장르'] = webtoon_genre
            df_kakaoW['조회수'] = webtoon_watched
            df_kakaoW['좋아요'] = webtoon_liked
            df_kakaoW['무료'] = webtoon_free
            df_kakaoW['줄거리'] = webtoon_plot
            df_kakaoW['키워드'] = webtoon_keyword
            df_kakaoW['상태'] = webtoon_state
            df_kakaoW['요일'] = webtoon_week
            df_kakaoW['무료주기'] = webtoon_rotation
            new_df = pd.concat([df, df_kakaoW], ignore_index=True)
            # new_df.to_csv('src/file/search.csv', index=False)
            # TEST
            new_df.to_csv('src/file/search3.csv', index=False)
        except Exception as e:
            print(f"\n{query} is not in Kakao")
            WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
        if index % 50 == 0:
            mark['마지막번호'] = [num + index]
            mark.to_csv('src/file/mark.csv', index=False)
        time.sleep(0.5)
    df_kakaoW['이름'] = webtoon_name
    df_kakaoW['플랫폼'] = webtoon_platform
    df_kakaoW['작가'] = webtoon_author
    df_kakaoW['그림'] = webtoon_drawing
    df_kakaoW['첫화링크'] = webtoon_link
    df_kakaoW['장르'] = webtoon_genre
    df_kakaoW['조회수'] = webtoon_watched
    df_kakaoW['좋아요'] = webtoon_liked
    df_kakaoW['무료'] = webtoon_free
    df_kakaoW['줄거리'] = webtoon_plot
    df_kakaoW['키워드'] = webtoon_keyword
    df_kakaoW['상태'] = webtoon_state
    df_kakaoW['요일'] = webtoon_week
    df_kakaoW['무료주기'] = webtoon_rotation
    new_df = pd.concat([df, df_kakaoW], ignore_index=True)
    new_df.to_csv('src/file/search_end.csv', index=False)

def KakaoPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre,
                      webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week,
                      webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot):
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[1]')))
    webtoon_name.append(query)
    webtoon_platform.append('kakao')
    webtoon_link.append(driver.current_url)
    genre = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[1]').text
    webtoon_genre.append(genre)
    watched = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[2]').text
    webtoon_watched.append(watched)
    liked = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[3]').text
    webtoon_liked.append(liked)

    prev_h = driver.execute_script("return document.body.scrollHeight")
    while (1):
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(0.5)
        curr_h = driver.execute_script("return document.body.scrollHeight")
        if curr_h == prev_h:
            break
        prev_h = curr_h
    free = driver.find_elements(By.XPATH, "//*[contains(text(), '무료')]")
    webtoon_free.append(len(free))

    # 정보 탭으로 이동 (줄거리, 키워드 받기)
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/main/div/div/div[5]/div[2]/div[1]/div[1]/div/div[2]/ul/li[2]/p').click()
    time.sleep(random.randint(1, 3))
    state = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/div/p[1]').text
    webtoon_state.append(state)
    try:
        week = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/div/p[2]').text
    except:
        week = ''
    webtoon_week.append(week)
    try:
        rotation = driver.find_element(By.XPATH, "//*[contains(text(), '마다 무료')]").text
    except:
        rotation = '전편 무료'
    webtoon_rotation.append(rotation)
    author = driver.find_element(By.XPATH,
                                 '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/dl/div[1]/dd').text
    webtoon_author.append(author)
    drawing = driver.find_element(By.XPATH,
                                  '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/dl/div[2]/dd').text
    webtoon_drawing.append(drawing)
    plot = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[2]/div/p').text
    cleaned_plot = re.sub(r'[\n\r!\.]', '', plot)
    webtoon_plot.append(cleaned_plot)
    # h-30을 클래스로 가진 a 태그 밑의 p태그의 text값 [1:] 을 str로 변환해서 , 구분자로 쓰자
    keywords = driver.find_elements(By.CLASS_NAME, 'h-30')
    keyword = ""
    for i in keywords:
        keyword += i.text[1:].replace(' ', '') + ','
    webtoon_keyword.append(keyword[:-1])
    # print(f'{genre}  {watched}  {liked}  {len(free)}  {keyword[:-1]}  {state}  {week}  {author}  {drawing}  {rotation}')
    driver.back()
    WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
    driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
    return webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot

# def NaverCrawling(driver):
#       # name platform link genre star liked free state week(업데이트날짜기준) author drawing plot
#
# def NaverPageCrawling():
#
# def KakaopageCrawling(driver):
#       # name platform link genre watched star free state(업데이트 마지막 날짜) week rotation author+drawing+원작 keyword plot
# def KakaopagePageCrawling():
#
# def LezhinCrawling(driver):
#       # name platform link genre state(업데이트 마지막날짜) week(업데이트 날짜기준) author drawing keyword plot
# def LezhinPageCrawling():