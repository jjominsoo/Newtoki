import traceback
import datetime
import random
import time
import pandas as pd
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def KWCrawling(driver, query, df, mark):
    # df = pd.read_csv('src/file/search_kw.csv')
    # TEST
    query2 = re.sub(r'[^\w\s]', '', query)
    webtoon_name: list[str] = []
    webtoon_platform: list[str] = []
    webtoon_author: list[str] = []
    webtoon_drawing: list[str] = []
    webtoon_genre: list[str] = []
    webtoon_state: list[str] = []
    webtoon_week: list[str] = []
    webtoon_watched: list[str] = []
    webtoon_liked: list[str] = []
    # webtoon_star: list[str] = []
    webtoon_num: list[int] = []
    webtoon_free: list[int] = []
    webtoon_rotation: list[str] = []
    webtoon_keyword: list[str] = []
    webtoon_plot: list[str] = []
    webtoon_link: list[str] = []

    cur_time = int(datetime.datetime.now().timestamp())
    random.seed(cur_time)
    time.sleep(random.randint(0, 2))
    try:
        check = mark['체크'].tolist()
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').send_keys(query)
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a')))
        name1 = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li[1]/a/p').text.replace(' ', '')
        name1 = re.sub(r'[^\w\s]', '', name1).lower()
        query2 = query2.replace(' ', '').lower()
        if query2 == name1:
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a').click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a')))
            name2 = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li[1]/div/a/div/div/div[2]/picture/img').get_attribute(
                    'alt').replace(' ', '')
            name2 = re.sub(r'[^\w\s]', '', name2).lower()
            if query2 == name2:
                driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
                time.sleep(random.randint(1, 2))
                webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, \
                    webtoon_liked, webtoon_num, webtoon_free, webtoon_state, webtoon_week, \
                    webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot = \
                        KWPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched,
                                       webtoon_num, webtoon_liked, webtoon_free, webtoon_state, webtoon_week,
                                       webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot)
                df_kw = pd.DataFrame()
                # print(len(webtoon_name), len(webtoon_platform), len(webtoon_author), len(webtoon_link), len(webtoon_genre), len(webtoon_watched), len(webtoon_liked), len(webtoon_free), len(webtoon_plot), len(webtoon_keyword), len(webtoon_state), len(webtoon_week),len(webtoon_rotation))
                df_kw['이름'] = webtoon_name
                df_kw['플랫폼'] = webtoon_platform
                df_kw['작가'] = webtoon_author
                df_kw['그림'] = webtoon_drawing
                df_kw['장르'] = webtoon_genre
                df_kw['상태'] = webtoon_state
                df_kw['요일'] = webtoon_week
                df_kw['조회수'] = webtoon_watched
                df_kw['좋아요'] = webtoon_liked
                # df_kw['별점'] = webtoon_star
                df_kw['총화수'] = webtoon_num
                df_kw['무료'] = webtoon_free
                df_kw['무료주기'] = webtoon_rotation
                df_kw['키워드'] = webtoon_keyword
                df_kw['줄거리'] = webtoon_plot
                df_kw['첫화링크'] = webtoon_link

                new_df = pd.concat([df, df_kw], ignore_index=True)
                new_df.to_csv('src/file/search_kw.csv', index=False)
            else:
                new_mark = pd.DataFrame()
                check.append(query+'|'+name2)
                new_mark['체크'] = check
                print("다른 웹툰(2)! (카웹)")
                new_mark.to_csv('src/file/mark_kw.csv', index=False)
        else:
            new_mark = pd.DataFrame()
            check.append(query+'|'+name1)
            new_mark['체크'] = check
            print("다른 웹툰(1)! (카웹)")
            new_mark.to_csv('src/file/mark_kw.csv', index=False)
            raise Exception
    except Exception as e:
        print(f"{query} not in KW")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
        time.sleep(0.5)


def KWPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched,
                   webtoon_liked, webtoon_num, webtoon_free, webtoon_state, webtoon_week,
                   webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[1]')))
        # name
        webtoon_name.append(query)
        # platform
        webtoon_platform.append('kakaowebtoon')
        # link
        webtoon_link.append(driver.current_url)
        # genre
        genre = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[1]').text
        webtoon_genre.append(genre)
        # watched
        watched = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[2]').text
        webtoon_watched.append(watched)
        # liked
        liked = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[3]').text
        webtoon_liked.append(liked)

        prev_h = driver.execute_script("return document.body.scrollHeight")
        while (1):
            time.sleep(1)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            curr_h = driver.execute_script("return document.body.scrollHeight")
            if curr_h == prev_h:
                break
            prev_h = curr_h
        # num
        num = driver.find_elements(By.CSS_SELECTOR, "li[class*='w-full']")
        webtoon_num.append(len(num))
        # free
        free = driver.find_elements(By.XPATH, "//*[contains(text(), '무료')]")
        webtoon_free.append(len(free))
        # week temp
        week_temp = driver.find_element(By.XPATH, f'//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/ul/li[{len(num)}]/a/div[2]/div/p').text
        # 정보 탭으로 이동 (줄거리, 키워드 받기)
        driver.find_element(By.XPATH,
                            '//*[@id="root"]/main/div/div/div[5]/div[2]/div[1]/div[1]/div/div[2]/ul/li[2]/p').click()
        time.sleep(random.randint(1, 3))
        # state
        state = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/div/p[1]').text
        webtoon_state.append(state)
        # week
        weeks = ['월', '화', '수', '목', '금', '토', '일']
        try:
            week = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/div/p[2]').text
        except:
            week1 = datetime.datetime.strptime(week_temp, '%y.%m.%d')
            week = weeks[week1.weekday()]
        webtoon_week.append(week)

        # rotation
        try:
            rotation = driver.find_element(By.XPATH, "//*[contains(text(), '마다 무료')]").text
        except:
            rotation = '연재 무료'
        webtoon_rotation.append(rotation)

        # author & drawing
        author = ''
        drawing = ''
        author_drawing_info = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/dl').find_elements(By.TAG_NAME, 'div')
        for i in author_drawing_info:
            info = i.find_element(By.XPATH, './dt').text
            if '글' in info:
                author = i.find_element(By.XPATH, './dd').text
            if '그림' in info:
                drawing = i.find_element(By.XPATH, './dd').text
        webtoon_author.append(author)
        webtoon_drawing.append(drawing)
        # author = driver.find_element(By.XPATH,
        #                              '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/dl/div[1]/dd').text
        # webtoon_author.append(author)
        # drawing = driver.find_element(By.XPATH,
        #                               '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/dl/div[2]/dd').text
        # webtoon_drawing.append(drawing)

        # plot
        plot = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[2]/div/p').text
        cleaned_plot = re.sub(r'[\n\r!\.]', '', plot)
        webtoon_plot.append(cleaned_plot)
        # keyword
        # h-30을 클래스로 가진 a 태그 밑의 p태그의 text값 [1:] 을 str로 변환해서 , 구분자로 쓰자
        keywords = driver.find_elements(By.CLASS_NAME, 'h-30')
        keyword = ""
        for i in keywords:
            keyword += i.text[1:].replace(' ', '') + ','
        webtoon_keyword.append(keyword[:-1])
        # print(f'{genre}  {watched}  {liked}  {len(free)}  {keyword[:-1]}  {state}  {week}  {author}  {drawing}  {rotation}')
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
    except Exception as e:
        again = pd.read_csv('src/file/again_kw.csv')
        again_list = again['체크'].tolist()
        again_kw = pd.DataFrame()
        again_list.append(query)
        again_kw['체크'] = again_list
        again_kw.to_csv('src/file/again_kw.csv', index=False)
        print('Error at KW')
        traceback.print_exc()
        k = input()
    return webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched,\
        webtoon_liked, webtoon_num, webtoon_free, webtoon_state, webtoon_week,\
        webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot
