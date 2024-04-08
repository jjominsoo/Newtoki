import re
import pandas as pd
import time


# WebtoonInfo.csv   : 모든 웹툰들을 정리한 csv파일
# Mark.csv          : 마지막으로 업데이트한 웹툰 이름을 저장한 csv파일 > 자주 변동되는 url주소를 확인하기 위해 쓰일 것임
def InitCSV():
    df = pd.DataFrame(columns=['이름', '작가/그림', '장르','요일', '추천수', '별점(총)', '별점(화)', '총화수', '댓글', '줄거리', '이미지', '플랫폼', '첫화링크','마지막업데이트날짜'])
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
def PageCrawling(url,week):
    response = requests.get(url,headers={'User-agent':user_agent})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    if week == '열흘':
        webtoon_list = soup.find_all('li', {'data-weekday': week})
    else:
        webtoon_list = soup.find_all('li', {'data-weekday': week+'요일'})

    webtoon_name = []
    webtoon_genre = []
    webtoon_week = []
    webtoon_detail = []
    for i, webtoon in enumerate(webtoon_list):
        webtoon_name.append(webtoon['date-title'])
        webtoon_genre.append(webtoon['data-genre'])
        webtoon_detail.append(webtoon.find('a')['href'])

    name_dic = {'이름':webtoon_name}
    genre_dic = {'장르':webtoon_genre}
    week_dic = {'요일':webtoon_week}
    detail_dic = {'상세':webtoon_detail}
    merged_df = pd.concat([pd.DataFrame(name_dic), pd.DataFrame(genre_dic), pd.DataFrame(week_dic), pd.DataFrame(detail_dic)], axis=1)

    # print(merged_df)
    return merged_df


from selenium.webdriver.common.by import By
def AllCrawling(url, driver):
    weeks=['열흘']
    # weeks = ['월', '화', '수', '목', '금', '토', '일', '열흘']
    df = pd.read_csv('src/WebtoonInfo.csv')
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
            if i != 0:
                print(f"{week}요일 {i + 1} page")
                driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[4]/ul/li[%d]/a' % (i + 3)).click()
                week_url = driver.current_url
            else:
                print(f"{week}요일 Crawling Start")
            name_genre_week = PageCrawling(week_url, week)
            flag = 0
            webtoons = driver.find_elements(By.XPATH, '//*[@id="webtoon-list-all"]/li')
            # print(len(webtoons))
            for webtoon in webtoons:
                # print(webtoon)
                href = webtoon.find_element(By.TAG_NAME,'a')
                print(href)
                href.click()
                driver.back()
                time.sleep(1)
                # if flag == 0:
                #     # captcha(driver)
                #     captcha2(driver)
                #     flag = 1
                #     print(f"Detail Crawling")
                #     # DetailCrawling()
                #     driver.back()
                #     driver.back()
                # else:
                #     # DetailCrawling()
                #     print(f"Detail Crawling")
                #     driver.back()



            df = pd.concat([df, name_genre_week], ignore_index=True)



        ## (4/8) 월 : 746 화 : 712 수 : 743 목 : 759 금 : 858 토 : 665 일 : 641 열흘 : 116 == 5240개
        # !!만약 크롤링 중에 업데이트가 된다면?
        # ~~다시 처음부터 크롤링하기로 하자 (4/8) < 아직 구현안함
        print(f'{week}요일 웹툰 크롤링 끝')
    df.to_csv('src/WebtoonInfo.csv', index=False)
    return df

import shutil
def DetailCrawling(name,url,driver,cookie):
    ## 매 사이트를 접속할 때마다 세션을 새로 설정해야함
    ## 세션을 독립적으로 운용하여 요청간 상태가 분리되고 서로 영향을 미치지 않음
    print("Detail Crawling Start!")
    requests.get(url)
    session = requests.Session()
    session.headers.update({'User-Agent':user_agent})
    session.cookies.update(cookie)
    response = session.get(url,headers={'User-agent':user_agent})
    html = response.text
    print(html)
    soup = BeautifulSoup(html,'html.parser')

    ## 이름(str)
    try:
        webtoon_name = name
    except Exception as e:
        print(f"Error at Name\n{e}")

    ## 이미지(다운로드)
    try:
        images = soup.find('div', {'class': 'view-img'})
        print(f"images = {images}")
        image = images.find('img').attrs['src']
        print(f"image = {image}")
        img = requests.get(image)
        print(f"img = {img}")
        with open(f'src/img/{webtoon_name}.png', 'wb') as outfile:
            outfile.write(img.content)
    except Exception as e:
        print(f"Error at Image\n{e}")
        temp_img = "src/img/no_image.png"
        img = f'src/img/{webtoon_name}.png'
        shutil.copyfile(temp_img, img)

    ## 총화수(int)
    try:
        webtoon_num = len(soup.find_all('li', {'class': 'list-item'}))
    except Exception as e:
        print(f"Error at Webtoon Num\n{e}")
        webtoon_num = 0

    ## 댓글(list)
    try:
        webtoon_reply = 0
    except Exception as e:
        print(f"Error at Reply\n{e}")
        webtoon_reply = []

    ## 별점(화수)(list)
    try:
        webtoon_star1 = 0
    except Exception as e:
        print(f"Error at Star1\n{e}")
        webtoon_star1 = []

    ## 별점(총)(float)
    try:
        full_star2 = soup.select('button.btn-white > i.fa-star')
        half_star2 = soup.select('button.btn-white > i.fa-star-half-empty')
        webtoon_star2 = len(full_star2) + (len(half_star2) * 0.5)
    except Exception as e:
        print(f"Error at Star2\n{e}")
        webtoon_star2 = 0

    ## 추천수(int)
    try:
        webtoon_recommend = str(soup.find('b', {'id': 'wr_good'}).text)
        webtoon_recommend = int(webtoon_recommend.replace(",", ""))
    except Exception as e:
        print(f"Error at Recommend\n{e}")
        webtoon_recommend = 0

    ## 마지막업데이트날짜(datetime)
    try:
        webtoon_updatedate = 0
    except Exception as e:
        print(f"Error at Update date\n{e}")
        webtoon_updatedate = 0

    print(webtoon_name, webtoon_num, webtoon_reply, webtoon_star1, webtoon_star2, webtoon_recommend, webtoon_updatedate)

import pyautogui
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as mat_plt
import matplotlib.image as mat_img
import pyperclip
import threading
def captcha(driver):
    # detail_url = df['url'][i]
    # detail_url = wb_webtoon['U' + str(i + 2)].value

    # driver.get('https://newtoki332.com/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0')
    # driver.find_element(By.XPATH,
    #                     '//*[@id="webtoon-list-all"]/li[1]/div/div/div/div[1]/div/a').click()
    # driver.minimize_window()
    #     !! 만약 캡챠 틀렸을때도 고려해야한다
    #     ~~
    #     !! 캡챠 이미지를 다운 받아서 출력해준다면
    #     !! driver를 headless로 해서 속도를 올리려함
    #     ~~ 이 작업을 수행하려 하니 IP차단이 먹힘
    #     ~~ 화면 캡쳐를 통해 캡챠이미지 추출
    #     !! 결국 캡챠가 안뚫린다 어쩌냐
    #     ~~ session에 cookie를 업데이트 함으로써 진행

    # try:
    #     captcha_key = driver.find_element(By.ID, 'captcha_key')
    # except Exception as e:
    #     for C in driver.get_cookies():
    #         cookies = {C['name']: C['value']}
    #     return cookies

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    captcha_img = driver.get_screenshot_as_png()
    open('src/img/captcha.png', 'wb').write(captcha_img)
    a = mat_img.imread('src/img/captcha.png')
    mat_plt.imshow(a[385:425, 535:605])
    mat_plt.show()
    driver.minimize_window()

    # !! plt랑 pyautogui 동시에 나오게 하는법 없나?
    # !! 아님 plt에서 입력받는 법 없나?
    captcha_num = pyautogui.prompt("Captcha 입력 >> ")
    captcha_key = driver.find_element(By.ID, 'captcha_key')
    captcha_key.click()
    pyperclip.copy(captcha_num)
    captcha_key.send_keys(Keys.CONTROL, 'v')
    driver.find_element(By.CLASS_NAME, 'btn-color').click()

    ct = time.time()
    for c in driver.get_cookies():
        cookies = {c['name']: c['value']}
    cct = time.time()
    print(f'Setting Cookie : {cct-ct}')
    driver.quit()
    return cookies

def captcha2(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    captcha_img = driver.get_screenshot_as_png()
    open('src/img/captcha.png', 'wb').write(captcha_img)
    a = mat_img.imread('src/img/captcha.png')
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