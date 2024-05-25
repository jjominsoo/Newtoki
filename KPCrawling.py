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

def KPCrawling(driver, query, df, mark_kp):

    query2 = re.sub(r'[^\w\s]', '', query)
    webtoon_name: list[str] = []
    webtoon_platform: list[str] = []
    webtoon_author: list[str] = []
    webtoon_drawing: list[str] = []
    webtoon_genre: list[str] = []
    webtoon_state: list[str] = []
    webtoon_week: list[str] = []
    webtoon_watched: list[str] = []
    # webtoon_liked: list[str] = []
    webtoon_star: list[str] = []
    webtoon_num: list[int] = []
    webtoon_free: list[int] = []
    webtoon_rotation: list[str] = []
    webtoon_keyword: list[str] = []
    webtoon_plot: list[str] = []
    webtoon_link: list[str] = []

    cur_time = int(datetime.datetime.now().timestamp()) + 2
    random.seed(cur_time)
    time.sleep(random.randint(0, 1))
    try:
        check = mark_kp['체크'].tolist()
        time.sleep(random.randint(1, 2))
        driver.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/div[1]/input').send_keys(query)
        driver.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/a').click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div/div/div[2]/a/div/div/span')))
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div/div/div[2]/a/div/div/span').click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[3]/div/div[1]/div/a')))
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[3]/div/div[1]/div/a').click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/span[1]')))
        name = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/span[1]').text.replace(' ', '')
        name = re.sub(r'[^\w\s]', '', name).lower()
        query2 = query2.replace(' ', '').lower()
        name1 = query2 + '완결'
        if name == query2 or name == name1:
            webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, \
             webtoon_num, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, \
             webtoon_keyword, webtoon_plot, webtoon_star, webtoon_author, webtoon_drawing = \
                KPPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched,
                               webtoon_num, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation,
                               webtoon_keyword, webtoon_plot, webtoon_star, webtoon_author, webtoon_drawing)
            df_kp = pd.DataFrame()
            # print(len(webtoon_name), len(webtoon_platform), len(webtoon_author), len(webtoon_link), len(webtoon_genre), len(webtoon_watched), len(webtoon_liked), len(webtoon_free), len(webtoon_plot), len(webtoon_keyword), len(webtoon_state), len(webtoon_week),len(webtoon_rotation))
            df_kp['이름'] = webtoon_name
            df_kp['플랫폼'] = webtoon_platform
            df_kp['작가'] = webtoon_author
            df_kp['그림'] = webtoon_drawing
            df_kp['장르'] = webtoon_genre
            df_kp['상태'] = webtoon_state
            df_kp['요일'] = webtoon_week
            df_kp['조회수'] = webtoon_watched
            # df_kp['좋아요'] = webtoon_liked
            df_kp['별점'] = webtoon_star
            df_kp['총화수'] = webtoon_num
            df_kp['무료'] = webtoon_free
            df_kp['무료주기'] = webtoon_rotation
            df_kp['키워드'] = webtoon_keyword
            df_kp['줄거리'] = webtoon_plot
            df_kp['첫화링크'] = webtoon_link

            new_kp = pd.concat([df, df_kp], ignore_index=True)
            new_kp.to_csv('src/file/search_kp.csv', index=False)
        else:
            new_mark = pd.DataFrame()
            check.append(query+'|'+name)
            new_mark['체크'] = check
            print(f"다른 웹툰! (카페) {name}")
            new_mark.to_csv('src/file/mark_kp.csv', index=False)
        # TEST
    except Exception as e:
        print(f"{query} not in KP")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pc-search-modal-root-id"]/div[1]/input')))
        driver.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/div[1]/input').clear()
        time.sleep(0.5)

def KPPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched,
                   webtoon_num, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation,
                   webtoon_keyword, webtoon_plot, webtoon_star, webtoon_author, webtoon_drawing):
    # name platform link genre watched free state(업데이트 마지막 날짜) week rotation author+drawing+원작 keyword plot star
    try:
        # name
        webtoon_name.append(query)
        # platform
        webtoon_platform.append('kakaopage')
        # link
        webtoon_link.append(driver.current_url)
        # genre
        genre = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/div[1]/div[1]/div/span[2]').text
        webtoon_genre.append(genre)
        # watched
        watched = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/div[1]/div[2]/span').text
        webtoon_watched.append(watched)
        # week
        week = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/div[2]/span').text
        if '연재' in week:
            webtoon_week.append(week[0])
        else:
            webtoon_week.append(week)
        # rotation
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[3]/div[1]/span[1]')))
            rotation = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[3]/div[1]/span[1]').text.split(' ')[0]
            # rotation = rotation_text.text.split('"')[1]
        except:
            rotation = ''
        webtoon_rotation.append(rotation)

        # 최신화 정렬
        try:
            wait = WebDriverWait(driver, 5)
            latest_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='최신 순' or text()='첫화부터']")))
            # 요소 클릭
            latest_span.click()
        except:
            print('엉뚱한 웹툰 클릭 or 버튼 위치 이상함 or 쿠폰 등장')
            k = input()
            wait = WebDriverWait(driver, 5)
            latest_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='최신 순' or text()='첫화부터']")))
            # 요소 클릭
            latest_span.click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div[1]/div[3]/div[2]')))
        driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[1]/div[3]/div[2]').click()
        # 모든 화수 확인
        while True:
            try:
                # 버튼을 찾아 클릭
                button = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]')))
                button.click()
                time.sleep(0.5)
            except Exception:
                break
        # num
        num = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/span').text.split(' ')[1]
        num = num.replace(',', '')
        webtoon_num.append(int(num))
        # free
        free = driver.find_elements(By.XPATH, "//*[contains(text(), '무료')]")
        webtoon_free.append(len(free))
        # state
        # week 구한 곳에서 상태를 알려주지만, 시즌완결같은 경운 연재라고 뜸 (쥐뿔도 없는 회귀 : 금 연재, 수라전설 독룡 : 휴재, 나 혼자만 레벨업 : 완결)
        last_date_text = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/ul/li[1]/div/div/a/div/div[2]/div[2]/span[1]').text
        try:
            last_date = datetime.datetime.strptime(last_date_text, '%y.%m.%d')
        except:
            # !! ~일후 무료 경우 ~일을 7로 나눠서 그만큼 내려가서 날짜 받는 방법도 있다
            last_date = datetime.datetime.now()
        diff = abs(datetime.datetime.now() - last_date).days
        if '연재' in week:
            if diff < 7:
                webtoon_state.append('연재중')
            elif diff < 28:
                # 한달까지는 휴재를 할 수 있다고 생각.
                webtoon_state.append('일시적 휴재')
            else:
                # 한달 이상 연재하지 않는다면 시즌 휴재라고 판단
                webtoon_state.append('시즌 휴재')
        else:
            #
            webtoon_state.append(week)
        # star
        try:
            star = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/div[1]/div[3]/span').text
        except:
            star = 0
        webtoon_star.append(star)
        # 정보 탭 이동
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/a/div/div/span').click()
        time.sleep(random.randint(0, 2))
        # plot
        while True:
            try:
                plot_button = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div[2]')))
                plot_button.click()
            except:
                WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,
                                                                                '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/span')))
                break
        plot = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div/span').text
        cleaned_plot = re.sub(r'[\n\r!\.]', '', plot)
        webtoon_plot.append(cleaned_plot)
        # keyword
        keywords = driver.find_elements(By.CSS_SELECTOR, 'a.mb-8pxr.mr-8pxr > div > span')
        keyword = ''
        for i in keywords:
            keyword += i.text[1:] + ','
        webtoon_keyword.append(keyword[:-1])
        # author & drawing
        # !!독보소요 같은 건 글,그림 작가가 없고 해당 XPATH 에는 원작 이름이 나와있다 >> 앞의 글자가 '글' '그림' '분류' 인것들만 모아서 확인해봐야한다
        author_drawing_info = driver.find_elements(By.CLASS_NAME, 'pt-6pxr')
        author = ''
        drawing = ''
        for i in author_drawing_info:
            info = i.find_element(By.XPATH, './span[1]').text
            # author
            if '글' in info:
                author = i.find_element(By.XPATH, './span[2]').text
            # drawing
            if '그림' in info:
                drawing = i.find_element(By.XPATH, './span[2]').text
        webtoon_author.append(author)
        webtoon_drawing.append(drawing)
    except:
        again = pd.read_csv('src/file/again_kp.csv')
        again_list = again['체크'].tolist()
        again_kp = pd.DataFrame()
        again_list.append(query)
        again_kp['체크'] = again_list
        again_kp.to_csv('src/file/again_kp.csv', index=False)
        print('Error at KP')
        traceback.print_exc()
        k = input()
        KPPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched,
                       webtoon_num, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation,
                       webtoon_keyword, webtoon_plot, webtoon_star, webtoon_author, webtoon_drawing)
    return webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, \
        webtoon_num, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, \
        webtoon_keyword, webtoon_plot, webtoon_star, webtoon_author, webtoon_drawing

