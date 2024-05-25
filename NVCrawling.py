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

def NVCrawling(driver, query, df, mark_nv):

    query2 = re.sub(r'[^\w\s]', '', query)
    webtoon_name: list[str] = []
    webtoon_platform: list[str] = []
    webtoon_author: list[str] = []
    webtoon_drawing: list[str] = []
    webtoon_genre: list[str] = []
    webtoon_state: list[str] = []
    webtoon_week: list[str] = []
    # webtoon_watched: list[str] = []
    webtoon_liked: list[str] = []
    webtoon_star: list[str] = []
    webtoon_num: list[int] = []
    webtoon_free: list[int] = []
    # webtoon_rotation: list[str] = []
    # webtoon_keyword: list[str] = []
    webtoon_plot: list[str] = []
    webtoon_link: list[str] = []
    cur_time = int(datetime.datetime.now().timestamp()) + 4
    random.seed(cur_time)
    time.sleep(random.randint(1, 2))
    try:
        check = mark_nv['체크'].tolist()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ac_input1"]')))
        driver.find_element(By.XPATH, '//*[@id="ac_input1"]').send_keys(query)
        driver.find_element(By.XPATH, '//*[@id="ac_form1"]/fieldset/button').send_keys(Keys.ENTER)
        # 만화탭 클릭
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[1]/a[3]')))
        driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/a[3]').click()
        # 맨 앞에 나온 만화(일치율이 높음) 클릭 >> 만약 만화가 없다면 Exception
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[3]/ul/li')))
        driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/ul/li/div/h3/a').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/h2')))
        name = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/h2').text.replace(' ', '')
        name = re.sub(r'[^\w\s]', '', name).lower()
        query2 = query2.replace(' ', '').lower()
        name1 = query2+'독점'
        name2 = query2+'단행본'
        name3 = 'HD'+query2
        name4 = '19'+query2
        name5 = query2 + '컬러연재'

        if name == query2 or name == name1 or name == name2 or name == name3 or name == name4 or name == name5:
            webtoon_name, webtoon_platform, webtoon_author, webtoon_drawing, webtoon_genre,\
            webtoon_state, webtoon_week, webtoon_liked, webtoon_star, webtoon_num,\
            webtoon_free, webtoon_plot, webtoon_link = \
                NVPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_author, webtoon_drawing, webtoon_genre,
                               webtoon_state, webtoon_week, webtoon_liked, webtoon_star, webtoon_num,
                               webtoon_free, webtoon_plot, webtoon_link)
            df_nv = pd.DataFrame()
            df_nv['이름'] = webtoon_name
            df_nv['플랫폼'] = webtoon_platform
            df_nv['작가'] = webtoon_author
            df_nv['그림'] = webtoon_drawing
            df_nv['장르'] = webtoon_genre
            df_nv['상태'] = webtoon_state
            df_nv['요일'] = webtoon_week
            # df_nv['조회수'] = webtoon_watched
            df_nv['좋아요'] = webtoon_liked
            df_nv['별점'] = webtoon_star
            df_nv['총화수'] = webtoon_num
            df_nv['무료'] = webtoon_free
            # df_nv['무료주기'] = webtoon_rotation
            # df_nv['키워드'] = webtoon_keyword
            df_nv['줄거리'] = webtoon_plot
            df_nv['첫화링크'] = webtoon_link
            new_nv = pd.concat([df, df_nv], ignore_index=True)
            new_nv.to_csv('src/file/search_nv.csv', index=False)
        else:
            new_mark = pd.DataFrame()
            check.append(query+'|'+name)
            new_mark['체크'] = check
            print(f"다른 웹툰! (네이버) {name}")
            new_mark.to_csv('src/file/mark_nv.csv', index=False)
        # TEST
    except Exception as e:
        print(f"{query} not in NV")
        # 만약
        driver.find_element(By.XPATH, '//*[@id="ac_input1"]').clear()
        time.sleep(0.5)
#
def NVPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_author, webtoon_drawing, webtoon_genre,
                   webtoon_state, webtoon_week, webtoon_liked, webtoon_star, webtoon_num,
                   webtoon_free, webtoon_plot, webtoon_link):
    try:
        # name
        webtoon_name.append(query)
        # platform
        webtoon_platform.append('naverseries')
        # author & drawing
        author = ''
        drawing = ''
        author_drawing_info = driver.find_element(By.CLASS_NAME, 'info_lst').find_element(By.TAG_NAME, 'ul').find_elements(By.TAG_NAME, 'li')
        for i in author_drawing_info:
            try:
                info = i.find_element(By.TAG_NAME, 'span').text
            except:
                continue
            if '글' in info:
                author = i.find_element(By.TAG_NAME, 'a').text
            # drawing
            if '그림' in info:
                drawing = i.find_element(By.TAG_NAME, 'a').text
        webtoon_author.append(author)
        webtoon_drawing.append(drawing)

        # genre
        try:
            genre = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li/ul/li[2]/span/a').text
        except:
            genre = ''
        webtoon_genre.append(genre)
        # 최신순 정렬 + 최신 날짜 받기
        driver.find_element(By.XPATH, '//*[@id="content"]/table/thead/tr/th[1]/div/button').click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="volumeList"]/tr[1]/td[1]/em')))
        last_date_text = driver.find_element(By.XPATH, '//*[@id="volumeList"]/tr[1]/td[1]/em').text
        last_date = datetime.datetime.strptime(last_date_text, '(%Y.%m.%d.)')
        # state
        # !!연재중, 완결 2개는 확실히 있는데 카카오페이지처럼 '휴재' 상태는 있는지 모르겠다.
        state = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li/ul/li[1]/span').text
        if '연재' in state:
            diff = abs(datetime.datetime.now() - last_date).days
            if diff < 7:
                webtoon_state.append('연재중')
            elif diff < 28:
                # 한달까지는 휴재를 할 수 있다고 생각.
                webtoon_state.append('일시적 휴재')
            else:
                # 한달 이상 연재하지 않는다면 시즌 휴재라고 판단
                webtoon_state.append('시즌 휴재')
        else:
            webtoon_state.append(state)
        # week
        weeks = ['월', '화', '수', '목', '금', '토', '일']
        second_last_date_text = driver.find_element(By.XPATH, '//*[@id="volumeList"]/tr[2]/td[1]/em').text
        second_last_date = datetime.datetime.strptime(second_last_date_text, '(%Y.%m.%d.)')
        if (last_date - second_last_date).days == 0 or (last_date - second_last_date).days == 7:
            week = weeks[last_date.weekday()]
        else:
            week = f'{(last_date - second_last_date).days}일'
        webtoon_week.append(week)
        # liked
        liked = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[2]/ul/li[2]/div/a/em').text.replace(',', '')
        webtoon_liked.append(liked)
        # star
        star = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[1]/em').text
        webtoon_star.append(star)
        # num
        try:
            num = driver.find_element(By.XPATH, '//*[@id="content"]/h5/strong').text
            webtoon_num.append(int(num))
        except:
            webtoon_num.append(int(num[:-1]))
        # free
        try:
            free = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]/div/div[1]/strong').text
            webtoon_free.append(free)
        except:
            webtoon_free.append(0)
        # plot
        try:
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/span/a').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[2]')))
            plot = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]').text
        except:
            plot = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div').text
        cleaned_plot = re.sub(r'[\n\r!\.]', '', plot)
        webtoon_plot.append(cleaned_plot)
        # link
        webtoon_link.append(driver.current_url)
        time.sleep(random.randint(2, 4))
    except:
        again = pd.read_csv('src/file/again_nv.csv')
        again_list = again['체크'].tolist()
        again_nv = pd.DataFrame()
        again_list.append(query)
        again_nv['체크'] = again_list
        again_nv.to_csv('src/file/again_nv.csv', index=False)
        print('Error at NV')
        traceback.print_exc()
        k = input()
    return webtoon_name, webtoon_platform, webtoon_author, webtoon_drawing, webtoon_genre, \
           webtoon_state, webtoon_week, webtoon_liked, webtoon_star, webtoon_num,\
           webtoon_free, webtoon_plot, webtoon_link