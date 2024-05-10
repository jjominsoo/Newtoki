import Captcha
import AllCrawling

import re
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

def AllCrawling(url, driver):
    # TEST ####
    weeks=['화', '수', '목', '금', '토', '일', '열흘']
    flag = 0
    # weeks = ['월', '화', '수', '목', '금', '토', '일', '열흘']
    df = pd.read_csv('src/WebtoonInfo.csv')
    driver.get(url)
    driver.maximize_window()
    cookie = Captcha.Login(driver)


    # 일주일을 볼껀데
    for week in weeks:
        print(week + '요일 웹툰 크롤링')
        # week_url = url + '&yoil=' + str(week) + '&jaum=&tag=&sst=as_update&sod=desc&stx='
        # response = requests.get(week_url, headers={'User-agent': user_agent})
        WebDriverWait(driver, 2)
        driver.find_element(By.CSS_SELECTOR, f'span[data-value="{week}"]').click()
        driver.find_element(By.XPATH,
                            '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').click()
        WebDriverWait(driver, 2)
        response = requests.get(driver.current_url, headers={'User-agent': user_agent})
        print(driver.current_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find('div', {'class': 'list-page'}).select('ul > li')

        # 각 요일마다 페이지를 클릭하면서 볼꺼다
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
                # week_url = driver.current_url
            else:
                print(f"{week}요일 Crawling Start")
                print(f"{week}요일 1 page")
            webtoon_name, webtoon_genre, webtoon_week = PageCrawling(driver.current_url, week, webtoon_name,
                                                                     webtoon_genre,
                                                                     webtoon_week)
            webtoons = driver.find_elements(By.XPATH, '//*[@id="webtoon-list-all"]/li')

            # 현재 페이지의 웹툰들의 상세페이지에 다 들어감
            # TEST ####
            print(webtoon_name)
            # for j in tqdm(range(5)):
            for j in tqdm(range(len(webtoons))):
                try:
                    WebDriverWait(driver, 5)
                    href = driver.find_element(By.XPATH,
                                               f'//*[@id="webtoon-list-all"]/li[{j + 1}]/div/div/div/div[1]/div/div/a')
                    href.click()
                except:
                    WebDriverWait(driver, 5)
                    href2 = driver.find_element(By.XPATH,
                                                f'//*[@id="webtoon-list-all"]/li[{j + 1}]/div[2]/div/div/div[1]/div/div/a')
                    href2.click()

                # 최초 클릭 (캡챠 진행)
                if flag == 0:
                    WebDriverWait(driver, 2)
                    flag = 1
                    webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update = DetailCrawling2(
                        # TEST ####
                        webtoon_name[j], driver.current_url, cookie, driver, webtoon_img, webtoon_num, webtoon_reply,
                        webtoon_star1, webtoon_star2, webtoon_update, webtoon_recommend, webtoon_plot)
                    # webtoon_name[j], driver.current_url, cookie, driver,webtoon_img,webtoon_num,webtoon_reply,webtoon_star1,webtoon_star2,webtoon_update,webtoon_recommend,webtoon_plot)
                    driver.back()
                    time.sleep(1)
                    WebDriverWait(driver, 2)

                else:
                    webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update = DetailCrawling2(
                        # TEST ####
                        webtoon_name[j], driver.current_url, cookie, driver, webtoon_img, webtoon_num, webtoon_reply,
                        webtoon_star1, webtoon_star2, webtoon_update, webtoon_recommend, webtoon_plot)
                    # webtoon_name[96*i + j], driver.current_url, cookie, driver,webtoon_img,webtoon_num,webtoon_reply,webtoon_star1,webtoon_star2,webtoon_update,webtoon_recommend,webtoon_plot)
                    driver.back()
                    time.sleep(1)
                    WebDriverWait(driver, 2)
            # df = pd.concat([df, name_genre_week], ignore_index=True)
            # (4/8) 월 : 746 화 : 712 수 : 743 목 : 759 금 : 858 토 : 665 일 : 641 열흘 : 116 == 5240개
            # !!만약 크롤링 중에 업데이트가 된다면?
            # ~~다시 처음부터 크롤링하기로 하자 (4/8) < 아직 구현안함
            # name_dic = {'이름':webtoon_name}
            # genre_dic = {'장르':webtoon_genre}
            # week_dic = {'요일':webtoon_week}
            # img_dic = {'이미지': webtoon_img}
            # num_dic = {'총화수': webtoon_num}
            # reply_dic = {'댓글': webtoon_reply}
            # star1_dic = {'별점(화)': webtoon_star1}
            # star2_dic = {'별점(총)': webtoon_star2}
            # recommend_dic = {'추천수': webtoon_recommend}
            # plot_dic = {'줄거리': webtoon_plot}
            # update_dic = {'업데이트' : webtoon_update}
            # merged_df = pd.concat(
            #     [pd.DataFrame(name_dic), pd.DataFrame(genre_dic), pd.DataFrame(week_dic),
            #     pd.DataFrame(img_dic), pd.DataFrame(num_dic), pd.DataFrame(reply_dic),
            #     pd.DataFrame(star1_dic), pd.DataFrame(star2_dic), pd.DataFrame(recommend_dic),
            #     pd.DataFrame(plot_dic), pd.DataFrame(update_dic)],axis=1)

            merged_df2 = pd.DataFrame()
            print(f'이름 : {len(webtoon_name)}, 장르 : {len(webtoon_genre)},요일 : {len(webtoon_week)}, '
                  f'이미지 : {len(webtoon_img)}, 총화수 : {len(webtoon_week)}, 댓글 : {len(webtoon_reply)}, '
                  f'별점화 : {len(webtoon_star1)}, 별점총 : {len(webtoon_star2)}, 추천수 : {len(webtoon_recommend)}, '
                  f'줄거리 : {len(webtoon_plot)}, 업데이트 : {len(webtoon_update)}')
            merged_df2['이름'] = webtoon_name
            merged_df2['장르'] = webtoon_genre
            merged_df2['요일'] = webtoon_week
            merged_df2['이미지'] = webtoon_img
            merged_df2['총화수'] = webtoon_num
            merged_df2['댓글'] = webtoon_reply
            merged_df2['별점(화)'] = webtoon_star1
            merged_df2['별점(총)'] = webtoon_star2
            merged_df2['추천수'] = webtoon_recommend
            merged_df2['줄거리'] = webtoon_plot
            merged_df2['업데이트'] = webtoon_update
            print(merged_df2)
            df = pd.concat([df, merged_df2], ignore_index=True)
            df.to_csv('src/WebtoonInfo.csv', index=False)
            print(f'{week}요일 Page {i + 1} 끝')
            driver.back()
        # Test ####
        # stack_num += len(df)
        # print(f'df = {df}')
        print(f'{week}요일 웹툰 크롤링 끝')

    return df


def PageCrawling(url, week, toon_name, toon_genre, toon_week):
    response = requests.get(url, headers={'User-agent': user_agent})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
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
    # print(webtoon_name,webtoon_genre,webtoon_week)
    # name_dic = {'이름':webtoon_name}
    # genre_dic = {'장르':webtoon_genre}
    # week_dic = {'요일':webtoon_week}
    # merged_df = pd.concat([pd.DataFrame(name_dic), pd.DataFrame(genre_dic), pd.DataFrame(week_dic)], axis=1)

    # print(merged_df)
    # return merged_df, webtoon_name
    return toon_name, toon_genre, toon_week


from selenium.webdriver.common.by import By
import shutil

def DetailCrawling2(name, url,cookie,driver,webtoon_img,webtoon_num,webtoon_reply,webtoon_star1,webtoon_star2,webtoon_update,webtoon_recommend,webtoon_plot):
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

    # # 이름(str)
    # try:
    #     webtoon_name.append(name)
    # except Exception as e:
    #     print(f"Error at Name\n{e}")
    #     webtoon_name.append("None")

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
    # 전체          ( div id='viewcomment' )
    # 최고 추천 댓글 ( > section id='bo_vcb' )
    # 일반 댓글     ( > section id='bo_vc' )
    # 페이지        ( > div class=text-center > ul > li )

    # 일반 댓글 별점 있는걸로 다가만 크롤링
    # 파싱(\n, 맨끝 공백)
    # 리스트식으로 입력하지말고 어차피 str로 바뀌니까 나중에 파싱하게 좋게 점수1,배댓글1,점수2,배댓글2/점수1,댓글1,점수2,댓글2 << 이런식으로 받자
    try:
        reply_flag = 0
        reply_section = soup.find('div', {'id': 'viewcomment'})
        best_replys_list = reply_section.find('section', {'id': 'bo_vcb'})
        best_replys = best_replys_list.find_all('div', {'class': 'media-content'})
        best_replys_stars = best_replys_list.find_all('div', {'class': 'media-heading'})

        star_reply = ""
        for br, brs in zip(best_replys, best_replys_stars):
            b_star = len(brs.find_all('i', {'class': 'fa fa-star fa-lg crimson'}))
            if b_star >= 1:
                b_reply = re.sub(r'[\r\n]+','',br.text.strip())
                star_reply = ''.join([star_reply,str(b_star),b_reply])+"|"

        replys_list = reply_section.find('section', {'id': 'bo_vc'})
        replys = replys_list.find_all('div', {'class': 'media-content'})
        replys_stars = replys_list.find_all('div', {'class': 'media-heading'})
        for r, rs in zip(replys, replys_stars):
            star = len(rs.find_all('i', {'class': 'fa fa-star fa-lg crimson'}))
            if star >= 1:
                reply = re.sub(r'[\r\n]+','',r.text.strip())
                star_reply = ''.join([star_reply + '|' + str(star), reply])
        reply_flag = 1

        reply_pages = reply_section.find('div',{'class':'text-center'}).select('ul > li')
        for rp in range(len(reply_pages)-5):
            # 다음페이지 클릭
            driver.find_element(By.XPATH, f'//*[@id="viewcomment"]/div[2]/ul/li[{rp+2}]/a').click()
            reply_response = session.get(driver.current_url, headers={'User-agent': user_agent})
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
    # !!최고 추천을 가진 화수 > 최고의 화를 찾아라
    # ~~
    # !!마지막날짜 - 처음업데이트날짜 / 7(10) = 총화수 >> 매주 꾸준히 업데이트
    # !! > 총화수 >> 업데이트가 늦다
    # !! < 총화수 >> 한번에 화수를 많이 올렸음       >> 두 개에 대해 인기도는 낮을 것이다.(비정기적 업데이트)
    # !! 한번에 화수를 많이 올렸는데 업데이트도 늦어? 그럼 그냥 아웃
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
        star1 = ','.join(map(str,star1_temp))
        webtoon_star1.append(star1)

        update = ','.join([star1_first_date,star1_last_date])
        print(update)
        webtoon_update.append(update)
    except Exception as e:
        print(f"Error at Star1\n{e}")
        if update_flag == 0:
            webtoon_update.append('')
        # print("Appending update []..")
        # webtoon_update.append(update)
        # print(webtoon_update)

    # 별점(총)(float)
    try:
        # full_star2 = soup.select('button.btn-white > i.fa-star')
        # half_star2 = soup.select('button.btn-white > i.fa-star-half-empty')
        # webtoon_star2.append(len(full_star2) + (len(half_star2) * 0.5))
        star2_lists = soup.find('div', {'class': 'view-comment'}).text.strip().split()
        star2_rating = star2_lists[2]
        star2_count = star2_lists[-1]
        star2 = ','.join([star2_rating,star2_count])
        webtoon_star2.append(star2)
    except Exception as e:
        print(f"Error at Star2\n{e}")
        # webtoon_star2.append(star2_temp)

    # 추천수(int)
    try:
        webtoon_recommend_temp = str(soup.find('b', {'id': 'wr_good'}).text)
        webtoon_recommend.append(int(webtoon_recommend_temp.replace(",", "")))
    except Exception as e:
        print(f"Error at Recommend\n{e}")
        print("Appending recommend 0..")
        # webtoon_recommend.append(0)

    # 줄거리
    try:
        plot = soup.find('div', {'class': 'col-sm-8'}).find_all('div')[1].text.strip()
        webtoon_plot.append(plot)
    except Exception as e:
        print(f"Error at \n{e}")
        print("Appending recommend \"\"")
        # webtoon_plot.append("")

    return webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update


def KakaoCrawling(driver):
    ## 성인 웹툰 >> 로그인? 아님 제외
    ## 어차피
    pd.set_option('display.max_columns',None)

    webtoon = pd.read_csv('src/file/name.csv')
    driver.get('https://webtoon.kakao.com/')
    driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/div[2]/div[2]/div/a[1]').click()
    df = pd.DataFrame()
    webtoon_name = []
    webtoon_platform = []
    webtoon_artist = []
    webtoon_link = []
    for query in webtoon['이름']:
        try:
            flag = 0
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').send_keys(query)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a').click()
            time.sleep(1.5)
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
            flag = 1
            time.sleep(1)
            print(f"{query} 크롤링 시작!")
            webtoon_name.append(query)
            webtoon_platform.append('kakao')
            artist = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[2]').text
            webtoon_artist.append(artist)
            webtoon_link.append(driver.current_url)
            time.sleep(1)
            driver.back()
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
            # k = input()
        except Exception as e:
            print("Not in Kakao")
            ## 에러 종류 2가지 1. 성인 flag = 1 / 2. 없음 flag = 0
            if flag:
                print(driver.get_cookies())
                k = input('계정 로그인중')
                driver.refresh()
                cookies = driver.get_cookies()
                print(cookies)
                driver.add_cookie(cookies)
                driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
                print(f"{query} 크롤링 재시작!")
                webtoon_name.append(query)
                webtoon_platform.append('kakao')
                time.sleep(3)
                artist = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[2]').text
                webtoon_artist.append(artist)
                webtoon_link.append(driver.current_url)
                time.sleep(1)
                driver.back()
                driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
            else:
                driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
                df['이름'] = webtoon_name
                df['플랫폼'] = webtoon_platform
                df['작가/그림'] = webtoon_artist
                df['첫화링크'] = webtoon_link
                # sys.stdout(df['작가/그림'])
                print(df['첫화링크'])
            continue
    df['이름'] = webtoon_name
    df['플랫폼'] = webtoon_platform
    df['작가/그림'] = webtoon_artist
    df['첫화링크'] = webtoon_link
    print(df)
    return df


def KakaoCrawling(driver):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    webtoon = pd.read_csv('src/file/name.csv')
    driver.get('https://webtoon.kakao.com/')
    # driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/div[2]/div[2]/div/a[2]').click()
    # driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/div[2]/div[3]/a').click()
    # driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div[2]/div/div/button').click()
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

    for query in tqdm(webtoon['이름']):
        cur_time = int(datetime.datetime.now().timestamp())
        random.seed(cur_time)
        time.sleep(random.randint(1, 3))
        try:
            flag = 0
            WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
            time.sleep(random.randint(1, 2))
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').send_keys(query)
            WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a')))
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a').click()
            WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a')))
            driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
            time.sleep(random.randint(1, 2))
            flag = 1
            print(f"\n{query} 크롤링 시작!")
            ## 여기부터 에러
            webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot = \
                KakaoPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre,
                                  webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week,
                                  webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot)
            # WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
            # driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
            # k = input()
        except Exception as e:
            ## 에러 종류 2가지 1. 성인 flag = 1 / 2. 없음 flag = 0
            ## 성인인증 하자
            if flag:
                traceback.print_exc()
                k = input("인증 필요.. 인증 후 아무 문자 입력")
                print('인증 완료')
                time.sleep(random.randint(1, 3))
                WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a')))
                driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
                WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[2]')))
                webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot = \
                    KakaoPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre,
                                      webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week,
                                      webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot)
                driver.refresh()
                time.sleep(1)
            else:
                print(f"\n{query} is not in Kakao")

            # time.sleep(1)
            # WebDriverWaitdd(driver, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
            # driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
            # print('cleared')
            df3 = pd.DataFrame()
            # print(len(webtoon_name), len(webtoon_platform), len(webtoon_author), len(webtoon_link), len(webtoon_genre), len(webtoon_watched), len(webtoon_liked), len(webtoon_free), len(webtoon_plot), len(webtoon_keyword), len(webtoon_state), len(webtoon_week),len(webtoon_rotation))
            df3['이름'] = webtoon_name
            df3['플랫폼'] = webtoon_platform
            df3['작가'] = webtoon_author
            df3['첫화링크'] = webtoon_link
            df3['장르'] = webtoon_genre
            df3['조회수'] = webtoon_watched
            df3['좋아요'] = webtoon_liked
            df3['무료'] = webtoon_free
            df3['줄거리'] = webtoon_plot
            df3['키워드'] = webtoon_keyword
            df3['상태'] = webtoon_state
            df3['요일'] = webtoon_week
            df3['무료주기'] = webtoon_rotation
            df3.to_csv('src/file/search.csv', index=False)
            # k = input("Saved.. press any key to continue..")
            print("Saved.. continue..")
            continue
    df3['이름'] = webtoon_name
    df3['플랫폼'] = webtoon_platform
    df3['작가'] = webtoon_author
    df3['첫화링크'] = webtoon_link
    df3['장르'] = webtoon_genre
    df3['조회수'] = webtoon_watched
    df3['좋아요'] = webtoon_liked
    df3['무료'] = webtoon_free
    df3['줄거리'] = webtoon_plot
    df3['키워드'] = webtoon_keyword
    df3['상태'] = webtoon_state
    df3['요일'] = webtoon_week
    df3['무료주기'] = webtoon_rotation
    df3.to_csv('src/file/search.csv', index=False)
    print(df3)
    return df3


def KakaoPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre,
                      webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week,
                      webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot):
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[1]')))
    webtoon_name.append(query)
    webtoon_platform.append('kakao')
    webtoon_link.append(driver.current_url)
    genre = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[1]').text
    webtoon_genre.append(genre)
    watched = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[2]').text
    webtoon_watched.append(watched)
    liked = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/div/p[3]').text
    webtoon_liked.append(liked)
    ## 동적으로 스크롤 끝까지 내려야한다.
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
    week = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[5]/div[2]/div[2]/div/div[1]/div/p[2]').text
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
    print(f'{genre}  {watched}  {liked}  {len(free)}  {keyword[:-1]}  {state}  {week}  {author}  {drawing}  {rotation}')
    driver.back()
    return webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot

# ===================================================================================
# 동시에 돌리기 위해 쿼리를 따로 집어넣을 것이므로 필요없어진 기능들이 생김
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


    try:
        check = str(mark['체크'][0])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').send_keys(query)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a')))
        if driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li[1]/a/p').text.replace(' ', '') != query.replace(' ', ''):
            mark['체크'] = [check + ',' + query]
            print("다른 웹툰(1)! (카웹)")
            mark.to_csv('src/file/mark_kw.csv', index=False)
            raise Exception
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a').click()
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a')))
        if driver.find_element(By.XPATH,'//*[@id="root"]/main/div/div/div[2]/ul/li[1]/div/a/div/div/div[2]/picture/img').get_attribute(
                'alt').replace(' ', '') != query.replace(' ', ''):
            mark['체크'] = [check + ',' + query]
            print("다른 웹툰(2)! (카웹)")
            mark.to_csv('src/file/mark_kw.csv', index=False)
            raise Exception
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
        time.sleep(random.randint(1, 2))
        ## 여기부터 에러
        webtoon_name, webtoon_platform, webtoon_link, webtoon_genre, webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week, webtoon_rotation, webtoon_author, webtoon_drawing, webtoon_keyword, webtoon_plot = \
            KWPageCrawling(driver, query, webtoon_name, webtoon_platform, webtoon_link, webtoon_genre,
                              webtoon_watched, webtoon_liked, webtoon_free, webtoon_state, webtoon_week,
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
        df_kw['무료'] = webtoon_free
        df_kw['무료주기'] = webtoon_rotation
        df_kw['키워드'] = webtoon_keyword
        df_kw['줄거리'] = webtoon_plot
        df_kw['첫화링크'] = webtoon_link

        new_df = pd.concat([df, df_kw], ignore_index=True)
        # new_df.to_csv('src/file/search.csv', index=False)
        # TEST
        new_df.to_csv('src/file/search_kw.csv', index=False)
    except Exception as e:
        print(f"{query} is not in kw")
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div/div/input')))
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div/div/input').clear()
        time.sleep(0.5)

def crawl_lezhin_comics(driver4, title, lz, mark_lz):
    # 레진코믹스 크롤링 로직
    # 예시로 로그만 출력
    # 줄거리
    # mark_lz = pd.read_csv('src/file/mark_lz.csv')
    check_lz = str(mark_lz['체크'][0])
    plot_temp = pd.DataFrame()
    driver4.find_element(By.XPATH, '/html/body/div[2]/div[2]/button[1]').click()
    WebDriverWait(driver4, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-input"]')))
    driver4.find_element(By.XPATH, '//*[@id="search-input"]').send_keys(title)
    try:
        WebDriverWait(driver4, 4).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div/div/section/ul/li/a')))
        driver4.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div/section/ul/li/a').click()
        WebDriverWait(driver4, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="comic-info"]/div/h2')))
        name = driver4.find_element(By.XPATH, '//*[@id="comic-info"]/div/h2').text.replace(' ', '')
        if title.replace(' ', '') == name:
            plot_temp['이름'] = [title]
            plot_temp['줄거리'] = [name]
            new_lz = pd.concat([lz, plot_temp], ignore_index=True)
            new_lz.to_csv('src/file/search_lz.csv', index=False)
        else:
            print(f"다른 웹툰! (레진) {name}")
            mark_lz['체크'] = [check_lz + ',' + title]
            mark_lz.to_csv('src/file/mark_lz.csv', index=False)
        driver4.back()
    except:
        driver4.refresh()
    print(f"{title} - 레진코믹스 크롤링 완료")

## ~ prac > crawling main
def crawl_kakao_webtoon(driver1, title, kw, mark_kw):
    # 카카오웹툰 크롤링 로직
    # 예시로 로그만 출력
    # 장르
    # driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/div[2]/div[2]/div/a[1]').click()
    AllCrawling.KWCrawling(driver1, title, kw, mark_kw)

    # genre_temp = pd.DataFrame()
    # genre_temp['이름'] = [title]
    # # driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/div[2]/div[2]/div/a[1]').click()
    # WebDriverWait(driver1, 5).until( EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[1]/div/input')))
    # driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[1]/div/input').send_keys(title)
    # try:
    #     WebDriverWait(driver1, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a')))
    #     driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div/ul/li/a').click()
    #     WebDriverWait(driver1, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a')))
    #     driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/ul/li/div/a').send_keys(Keys.ENTER)
    #     WebDriverWait(driver1, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[1]')))
    #     genre_temp['장르'] = [driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[4]/div[2]/p[1]').text]
    #     driver1.back()
    #     WebDriverWait(driver1, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/main/div/div/div[1]/div/input')))
    #     driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[1]/div/input').clear()
    # except:
    #     driver1.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[1]/div/input').clear()
    #     genre_temp['장르'] = ['nope']
    # new_kw = pd.concat([kw, genre_temp], ignore_index=True)
    # new_kw.to_csv('src/file/prac1.csv', index=False)
    print(f"{title} - 카카오웹툰 크롤링 완료")


def crawl_kakao_page(driver2, title, kp, mark_kp):
    # 카카오페이지 크롤링 로직
    # 예시로 로그만 출력
    # 요일
    # mark_kp = pd.read_csv('src/file/mark_kp.csv')

    KPCrawling.KPCrawling(driver2, title, kp, mark_kp)
    # check_kp = str(mark_kp['체크'][0])
    # week_temp = pd.DataFrame()
    # driver2.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/div[1]/input').send_keys(title)
    # driver2.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/a').click()
    # WebDriverWait(driver2, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div/div/div[2]/a/div/div/span')))
    # driver2.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div/div/div[2]/a/div/div/span').click()
    # try:
    #     WebDriverWait(driver2, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[3]/div/div[1]/div/a')))
    #     driver2.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[3]/div/div[1]/div/a').click()
    #     WebDriverWait(driver2, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/span[1]')))
    #     name = driver2.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/a/div/span[1]').text.replace(' ', '')
    #     if title.replace(' ', '') == name:
    #         week_temp['이름'] = [title]
    #         week_temp['요일'] = [name]
    #         new_kp = pd.concat([kp, week_temp], ignore_index=True)
    #         new_kp.to_csv('src/file/search_kp.csv', index=False)
    #     else:
    #         print(f"다른 웹툰! (카페) {name}")
    #         mark_kp['체크'] = [check_kp + ',' + title]
    #         mark_kp.to_csv('src/file/mark_kp.csv', index=False)
    # except:
    #     driver2.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/div[1]/input').clear()
    print(f"{title} - 카카오페이지 크롤링 완료")

def crawl_naver_series(driver3, title, nv, mark_nv):
    # 네이버시리즈 크롤링 로직
    # 예시로 로그만 출력
    # 키워드
    # mark_nv = pd.read_csv('src/file/mark_nv.csv')

    AllCrawling.NVCrawling(driver3, title, nv, mark_nv)
    # check_nv = str(mark_nv['체크'][0])
    # keyword_temp = pd.DataFrame()
    # WebDriverWait(driver3, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ac_input1"]')))
    # driver3.find_element(By.XPATH, '//*[@id="ac_input1"]').send_keys(title)
    # driver3.find_element(By.XPATH, '//*[@id="ac_form1"]/fieldset/button').send_keys(Keys.ENTER)
    # # 만화탭 클릭
    # WebDriverWait(driver3, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[1]/a[3]')))
    # driver3.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/a[3]').click()
    # try:
    #     # 첫번째 만화 클릭
    #     WebDriverWait(driver3, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[3]/ul/li/div/h3/a')))
    #     driver3.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/ul/li/div/h3/a').click()
    #     WebDriverWait(driver3, 4).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/h2')))
    #     name = driver3.find_element(By.XPATH, '//*[@id="content"]/div[1]/h2').text.replace(' ', '')
    #     if title.replace(' ', '') == name:
    #         keyword_temp['이름'] = [title]
    #         keyword_temp['키워드'] = [name]
    #         new_nv = pd.concat([nv, keyword_temp], ignore_index=True)
    #         new_nv.to_csv('src/file/search_nv.csv', index=False)
    #     else:
    #         print(f"다른 웹툰! (네이버) {name}")
    #         mark_nv['체크'] = [check_nv + ',' + title]
    #         mark_nv.to_csv('src/file/mark_nv.csv', index=False)
    # except:
    #     driver3.find_element(By.XPATH, '//*[@id="ac_input1"]').clear()
    print(f"{title} - 네이버시리즈 크롤링 완료")