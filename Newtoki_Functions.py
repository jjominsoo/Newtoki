import re
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

# WebtoonInfo.csv   : 모든 웹툰들을 정리한 csv파일
# Mark.csv          : 마지막으로 업데이트한 웹툰 이름을 저장한 csv파일 > 자주 변동되는 url주소를 확인하기 위해 쓰일 것임
def InitCSV():
    df = pd.DataFrame(columns=['이름', '작가/그림', '장르','요일', '추천수', '별점(총)', '별점(화)', '총화수', '댓글', '줄거리', '이미지', '플랫폼', '첫화링크','업데이트'])
    df.to_csv('src/WebtoonInfo.csv', index=False)
    init_mark = {'이름': '', '순서': 0, '도메인': 'https://newtoki328.com/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0'}
    mark_index = [0]
    mark = pd.DataFrame(init_mark, index=mark_index)
    mark.to_csv('src/Mark.csv', index=False)

def CheckURL(driver):
    pattern = r'\d+'
    mark = pd.read_csv('src/Mark.csv')
    url = mark['도메인'][0]
    a = re.search(pattern, url)
    number = int(a.group())

    for i in range(100):
        try:
            driver.implicitly_wait(10)
            driver.get(url)
            url = driver.current_url
            if driver.current_url == url:
                print('이 주소가 맞습니다.')
                break
        except Exception as e:
            print('도메인 주소 변경 중..')
            number += 1
            url = url[:a.start()] + str(number) + url[a.end():]
    mark['도메인'] = url
    mark.to_csv('src/Mark.csv', index=False)
    return url

import requests
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
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

def PageCrawling(url,week):
    response = requests.get(url,headers={'User-agent':user_agent})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if week == '열흘':
        webtoon_list = soup.find_all('li', {'data-weekday': week})
    else:
        webtoon_list = soup.find_all('li', {'data-weekday': week+'요일'})
    for i, webtoon in enumerate(webtoon_list):
        ### TEST ####
        # if i == 5:
        #     break
        ### TEST ####
        webtoon_name.append(webtoon['date-title'])
        webtoon_genre.append(webtoon['data-genre'])
        webtoon_week.append(week)
    # print(webtoon_name,webtoon_genre,webtoon_week)
    # name_dic = {'이름':webtoon_name}
    # genre_dic = {'장르':webtoon_genre}
    # week_dic = {'요일':webtoon_week}
    # merged_df = pd.concat([pd.DataFrame(name_dic), pd.DataFrame(genre_dic), pd.DataFrame(week_dic)], axis=1)

    # print(merged_df)
    # return merged_df, webtoon_name
    return webtoon_name, webtoon_genre, webtoon_week

from selenium.webdriver.common.by import By

def AllCrawling(url, driver):
    #### TEST ####
    # weeks=['열흘','월']
    #### TEST ####
    flag = 0
    weeks = ['월', '화', '수', '목', '금', '토', '일', '열흘']
    df = pd.read_csv('src/WebtoonInfo.csv')
    stack_num = 0
    for week in weeks:
        print(week + '요일 웹툰 크롤링')
        week_url = url + '&yoil=' + str(week) + '&jaum=&tag=&sst=as_update&sod=desc&stx='
        driver.get(week_url)
        response = requests.get(week_url, headers={'User-agent': user_agent})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find_all('div', {'class': 'list-page'})

        for page in pages:
            p = page.select('ul > li')

        for i in range(len(p) - 4):
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
                driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[4]/ul/li[%d]/a' % (i + 3)).click()
                time.sleep(0.5)
                week_url = driver.current_url
            else:
                print(f"{week}요일 Crawling Start")
            # name_genre_week, webtoon_name = PageCrawling(week_url, week)
            webtoon_name,webtoon_genre,webtoon_week = PageCrawling(week_url, week)
            webtoons = driver.find_elements(By.XPATH, '//*[@id="webtoon-list-all"]/li')
            ### TEST ####
            # for j in tqdm(range(5)):
            ### TEST ####
            for j in tqdm(range(len(webtoons))):
                try:
                    WebDriverWait(driver, 5)
                    href = driver.find_element(By.XPATH,f'//*[@id="webtoon-list-all"]/li[{j+1}]/div/div/div/div[1]/div/div/a')
                    # print(href)
                    href.click()
                except:
                    WebDriverWait(driver, 5)
                    href2 = driver.find_element(By.XPATH,f'//*[@id="webtoon-list-all"]/li[{j+1}]/div[2]/div/div/div[1]/div/div/a')
                    href2.click()
                if flag == 0:
                    cookie = captcha2(driver)
                    WebDriverWait(driver, 2)
                    flag = 1
                    webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update = DetailCrawling2(
                        ### TEST ###
                        # webtoon_name[5 * i + j + stack_num], driver.current_url, cookie)
                        ### TEST ###
                        webtoon_name[96 * i + j + stack_num], driver.current_url, cookie)

                    driver.back()
                    WebDriverWait(driver, 2)
                    driver.back()
                    WebDriverWait(driver, 2)
                else:
                    webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_plot, webtoon_update = DetailCrawling2(
                        ### TEST ###
                        # webtoon_name[5*i+j + stack_num], driver.current_url, cookie)
                        ### TEST ###
                        webtoon_name[96 * i + j + stack_num], driver.current_url, cookie)

                    driver.back()
                    WebDriverWait(driver, 2)
            # df = pd.concat([df, name_genre_week], ignore_index=True)
        ## (4/8) 월 : 746 화 : 712 수 : 743 목 : 759 금 : 858 토 : 665 일 : 641 열흘 : 116 == 5240개
        ## !!만약 크롤링 중에 업데이트가 된다면?
        ## ~~다시 처음부터 크롤링하기로 하자 (4/8) < 아직 구현안함
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
        #     [pd.DataFrame(name_dic), pd.DataFrame(genre_dic), pd.DataFrame(week_dic), pd.DataFrame(img_dic), pd.DataFrame(num_dic), pd.DataFrame(reply_dic),
        #     pd.DataFrame(star1_dic), pd.DataFrame(star2_dic), pd.DataFrame(recommend_dic),pd.DataFrame(plot_dic), pd.DataFrame(update_dic)],axis=1)

            merged_df2 = pd.DataFrame()
            print(webtoon_name)
            merged_df2['이름'] = webtoon_name
            print(webtoon_genre)
            merged_df2['장르'] = webtoon_genre
            print(webtoon_week)
            merged_df2['요일'] = webtoon_week
            print(webtoon_img)
            merged_df2['이미지'] = webtoon_img
            print(webtoon_week)
            merged_df2['총화수'] = webtoon_num
            print(webtoon_reply)
            merged_df2['댓글'] = webtoon_reply
            print(webtoon_star1 , len(webtoon_star1))
            merged_df2['별점(화)'] = webtoon_star1
            print(webtoon_star2)
            merged_df2['별점(총)'] = webtoon_star2
            print(webtoon_recommend)
            merged_df2['추천수'] = webtoon_recommend
            print(webtoon_plot)
            merged_df2['줄거리'] = webtoon_plot
            print(webtoon_update)
            merged_df2['업데이트'] =webtoon_update
            # print(f'M1 = {merged_df}')
            # print(f'M2 = {merged_df2}')
            df = pd.concat([df,merged_df2],ignore_index=True)
            df.to_csv('src/WebtoonInfo.csv', index=False)
        stack_num += len(df)
            # print(f'DF = {df}')
        print(f'{week}요일 웹툰 크롤링 끝')

    return df

import shutil
import pyautogui
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as mat_plt
import matplotlib.image as mat_img
import pyperclip
import threading

def captcha2(driver):
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    captcha_img = driver.get_screenshot_as_png()
    open('src/file/captcha.png', 'wb').write(captcha_img)
    a = mat_img.imread('src/file/captcha.png')
    mat_plt.imshow(a[385:425, 535:605])
    mat_plt.show()
    # driver.minimize_window()

    # !! plt랑 pyautogui 동시에 나오게 하는법 없나?
    # !! 아님 plt에서 입력받는 법 없나?
    # ~~ Prac.py 활용해보자 < 아직 안함
    captcha_num = pyautogui.prompt("Captcha 입력 >> ")
    captcha_key = driver.find_element(By.ID, 'captcha_key')
    captcha_key.click()
    pyperclip.copy(captcha_num)
    captcha_key.send_keys(Keys.CONTROL, 'v')
    driver.find_element(By.CLASS_NAME, 'btn-color').click()

    for c in driver.get_cookies():
        cookies = {c['name']: c['value']}
    return cookies

def DetailCrawling2(name,url,cookie):
    ## 매 사이트를 접속할 때마다 세션을 새로 설정해야함
    ## 세션을 독립적으로 운용하여 요청간 상태가 분리되고 서로 영향을 미치지 않음
    print("=============================================================================")
    print(f"{name} Detail Crawling Start!")
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    session.headers.update(headers)
    session.cookies.update(cookie)
    response = session.get(url, headers={'User-agent': user_agent})
    html = response.text
    # print(html)
    soup = BeautifulSoup(html,'html.parser')

    # ## 이름(str)
    # try:
    #     webtoon_name.append(name)
    # except Exception as e:
    #     print(f"Error at Name\n{e}")
    #     webtoon_name.append("None")

    ## 이미지(다운로드)
    webtoon_name_strip = re.sub(r'[^\w\s]+|\s+','',name)
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

    ## 총화수(int)
    try:
        nums = len(soup.find_all('li', {'class': 'list-item'}))
        webtoon_num.append(nums)
    except Exception as e:
        print(f"Error at Webtoon Num\n{e}")
        nums = 0
        webtoon_num.append(nums)

    ## 댓글(list)
    try:
        webtoon_reply_list = ['a','b','c']
        webtoon_reply.append(webtoon_reply_list)
    except Exception as e:
        print(f"Error at Reply\n{e}")
        print(soup)
        webtoon_reply.append([])

    ## 별점(화수)(list)
    ## !!최고 추천을 가진 화수 > 최고의 화를 찾아라
    ## ~~
    ## !!마지막날짜 - 처음업데이트날짜 / 7(10) = 총화수 >> 매주 꾸준히 업데이트
    ## !! > 총화수 >> 업데이트가 늦다
    ## !! < 총화수 >> 한번에 화수를 많이 올렸음       >> 두 개에 대해 인기도는 낮을 것이다.(비정기적 업데이트)
    ## !! 한번에 화수를 많이 올렸는데 업데이트도 늦어? 그럼 그냥 아웃
    try:
        star1_temp = []
        update_temp = []
        try:
            star1_lists = soup.find_all('div',{'class':'serial-list'})
        except:
            print("Appending star1 []..")
            star1_lists = []
        for star1_list in star1_lists:
            star1s = star1_list.select('ul > li')

        star1_recommend_temp = []
        for index, star1 in enumerate(star1s):
            try:
                if index == 0:
                    star1_first_date = star1.find('div', {'class': 'wr-date'}).text.strip()
                if index == len(star1s)-1:
                    star1_last_date = star1.find('div', {'class': 'wr-date'}).text.strip()
            except:
                star1_first_date = ['1900-01-01']
                star1_last_date = ['1900-01-01']
            try:
                star1_rating = star1.find('div', {'class':'wr-star'}).text.strip().split('(')[-1].split(')')[0]
                # star1_recommend = star1.find('div', {'class':'wr-good'}).text.strip()
                # star1_recommend_temp.append(int(star1_recommend))
            except:
                star1_rating = 0
            star1_temp.append(float(star1_rating))
        star1_temp.sort(reverse=True)
        webtoon_star1.append(star1_temp)
        update_temp.append(pd.to_datetime(star1_first_date))
        update_temp.append(pd.to_datetime(star1_last_date))
        update_temp.sort(reverse=True)
        webtoon_update.append(update_temp)
    except Exception as e:
        print(f"Error at Star1\n{e}")
        # 에러 위치에 따라
        update_temp = []
        print("Appending update []..")
        webtoon_update.append(update_temp)
        # print(webtoon_update)

    ## 별점(총)(float)
    try:
        # full_star2 = soup.select('button.btn-white > i.fa-star')
        # half_star2 = soup.select('button.btn-white > i.fa-star-half-empty')
        # webtoon_star2.append(len(full_star2) + (len(half_star2) * 0.5))
        star2_temp = []
        star2_lists = soup.find('div',{'class':'view-comment'}).text.strip().split()
        star2_rating = float(star2_lists[2])
        star2_count = int(star2_lists[-1])
        star2_temp.append(star2_rating)
        star2_temp.append(star2_count)
        webtoon_star2.append(star2_temp)
    except Exception as e:
        print(f"Error at Star2\n{e}")
        print("Appending star2 []..")
        webtoon_star2.append([])

    ## 추천수(int)
    try:
        webtoon_recommend_temp = str(soup.find('b', {'id': 'wr_good'}).text)
        webtoon_recommend.append(int(webtoon_recommend_temp.replace(",", "")))
    except Exception as e:
        print(f"Error at Recommend\n{e}")
        print("Appending recommend 0..")
        webtoon_recommend.append(0)

    ## 줄거리
    try:
        plot = soup.find('div',{'class':'col-sm-8'}).find_all('div')[1].text.strip()
        webtoon_plot.append(plot)
    except Exception as e:
        print(f"Error at Recommend\n{e}")
        print("Appending recommend \"\"")
        webtoon_plot.append("")
    return webtoon_img, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2,webtoon_recommend,webtoon_plot,webtoon_update