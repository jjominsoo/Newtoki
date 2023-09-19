from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import re
import time
from datetime import datetime, timedelta
import requests
import pyautogui
import openpyxl
import csv
import pandas

from openpyxl.drawing.image import Image
import urllib.request
from urllib.request import urlretrieve
import urllib
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
# chrome_options.add_argument('--headless=new')
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# driver.implicitly_wait(5)

# 엑셀파일에 저장된 최근에 접속가능했던 주소를 가져와서 진행한다.
#!! 데이터 처리는 csv파일이 유리하다는데 xlsx파일을 csv로 변형해보자 나중에
fpath = r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki6.xlsx'
c = open('src/Newtoki.csv','w')
wc = csv.writer(c)
wb = openpyxl.load_workbook(fpath)
wb_siteInfo = wb['Site Information']
wb_webtoon = wb['webtoon']
url = wb_siteInfo['A2'].value
saved_url = wb_siteInfo['A2'].value
update_num = wb_siteInfo['D2'].value
#
genre = []
webtoon_name = []
page_time = 0
#
cell_alp = {'판타지':'F','액션':'G','개그':'H','미스터리':'I','로맨스':'J','드라마':'K','무협':'L','스포츠':'M','일상':'N','학원':'O','성인':'P','한국':'Q','중국':'R'}
week = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일','열흘']

# 프로그램 총 실행시간 체크
s_time = time.time()

#!! 마찬가지로 지금은 월요일 부터 열흘까지 하지만
#!! 중간에 특정 요일만 크롤링 하고 싶으면 그렇게 하도록 해야하므로
#!! w대신 새로운 변수를 넣어서 그것이 true면 첫페이지를 가져와야하고
#!! 아니라면 다음 요일 클릭하도록 해야한다.
def first_page(url,w):
    # 월요일
    # 유효 url 확인도 겸해야하므로 따로 구분지었다.
    # driver.minimize_window()
    if w == 0:
        accessing_page_s_time = time.time()
        temp = "/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0"
        #!! 네트워크 속도가 빠르면 페이지 인식을 못하는 것 같다. ( 너무빨리 지나가서? )
        #!! 핫스팟으론 되는데 집 와이파이로는 되긴 됐지만 일요일-열흘 이 부분이 안됐다.
        #!! 다시 한번 해봐야 알듯
        #!! https://newtoki306.com/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0
        #~~ 실제로 연결 안되는 url을 셀레니움이 아닌 웹브라우저 크롤로 실행시켰는데 정상 작동했다.
        #~~ 그 이후 url주소가 바뀌었고 그 뒤로는 크롤링이 잘됐다.
        #~~ 아마 url주소가 바뀌는 타이밍에 크롤링 시도하면 안되는거 같다?
        for i in range(1000):
            try:
                url2 = url + temp
                driver.get(url2)
                time.sleep(2)
                driver.implicitly_wait(10)
                driver.find_element(By.XPATH,
                                    '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[2]/td/span[2]').click()
                driver.find_element(By.XPATH,
                                    '//*[@id="content_wrapper"]/div[2]/div/section/div[1]/form/table/tbody/tr[1]/td[2]/button').send_keys(
                    Keys.ENTER)
                break
            except Exception as e:
                time.sleep(1)
                num = int(re.sub(r'[^0-9]', '', url)) + 1
                #!! 여기 좀 수정해야할듯??
                #~~ 지금보면 괜찮은것 같다.
                url = "https://newtoki" + str(num) + ".com"
        accessing_page_e_time = time.time()
        print("첫 웹사이트 접속 시간 : " + str(accessing_page_e_time - accessing_page_s_time))

    # 화요일~열흘
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

    #!! 굳이? 그냥 셀레니움(driver)로 작업해도 되지않나? 부르는게 시간 걸리지않나
    #~~ 완료
    response = requests.get(driver.current_url, headers={
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('div', {'class': 'list-page'})

    for page in pages:
        p = page.select('ul > li')
    # 버튼들까지 합쳐서 (페이지수 + 4)개가 나오므로
    # 밑의 함수에서 가독성을 위해 실제페이지 + 1을 저장한다
    total_page = len(p) - 3

    return total_page

#!! 요소 헷갈리니까 좀 보기 편하게 하자
#!! 목표 = week_num 을 한글로 입력 ( 일요일 ) 하면 일요일 웹툰 하는걸로
# code_temp (1)
def page_crawl(update_num,week_num,p):
    # 첫페이지가 아니면 == 페이지(숫자) 클릭을 해야한다면
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
    #!! 얘네도 그냥 beautiful soup하면 되지 않냐?
    detail_pages = driver.find_elements(By.CSS_SELECTOR,'div#webtoon-list > ul > li')
    # images = driver.find_elements(By.CSS_SELECTOR, 'div.img-item>a>img')
    # names = driver.find_elements(By.CSS_SELECTOR, 'div.img-item>div>a>span')
    setting_e_time = time.time()
    print("사이트 선언 시간 : " + str(setting_e_time-setting_s_time))

    # 이미지 저장
    # code_temp(4) : 웹툰명으로 이미지 저장하려 했으나 나중에 엑셀 추가하려 할 때 정렬이 되버려서 그냥 순서대로 저장했다.
    #!! 지금은 아직 코드 테스트 단계이므로 넘어가지만
    #!! 나중엔 이미지 url 주소도 받아서 이미지 중복 저장하지 않도록 해보자
    #~~ 생각하니까 어차피 웹툰제목으로 중복처리를 할꺼라서 굳이 안해도 될것 같다

    #!! 이미지도 그냥 상세페이지에서 다뤄보자

    # 이름, 장르, 요일, 상세페이지 url 저장
    for i, webtoon in enumerate(webtoon_list):
        # wb_siteInfo[C2]에 나중에 업데이트를 쉽게하기 위해 이름만 저장해놓고
        # wb_webtoon[A2]에 웹툰제목 저장
        wb_siteInfo['C%d' % update_num] = webtoon['date-title']
        wb_webtoon['A%d' % update_num] = webtoon['date-title']
        new_name = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]","",webtoon['date-title'])
        webtoon_name.append(new_name)

        # wb_webtoon[F~R 2]에 장르 저장
        genre = webtoon['data-genre'].split(',')
        for g in genre:
            if g in cell_alp.keys():
                wb_webtoon[cell_alp[g] + '%d' % update_num] = 1

        # wb_webtoon[S2]에 요일 저장
        wb_webtoon['S%d' % update_num] = webtoon['data-weekday']

        # wb_webtoon[U2]에 상세페이지 url 저장
        detail_url = detail_pages[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
        wb_webtoon['U%d'%update_num] = detail_url

        update_num += 1
    one_page_e_time = time.time()

    print("한 페이지 총 실행시간 : " + str(one_page_e_time-setting_s_time))

    wb_siteInfo['D2'] = update_num

    return update_num

# code_temp (2), (3)
# 전체 페이지 파트

if update_num == 2:
    for w in range(len(week)):
        page_num = first_page(url,w)
        for p in range(1,page_num):
            update_num = page_crawl(update_num,w,p)
            # wb_siteInfo['D2'] = update_num
            now = datetime.now()
            print(str(week[w]) + " Page " + str(p) +" End")
            print("현재 시간 : " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) +"초\n")
        # 한 요일 끝나면 저장
        wb.save(fpath)

# 바뀐 주소 저장
k = driver.current_url.find('.com')
new_url = driver.current_url[:k+4]
if saved_url != new_url:
    wb_siteInfo['A2'] = new_url
wb.save(fpath)

import matplotlib.pyplot as mat_plt
import matplotlib.image as mat_img
import pyperclip
import random
import sys
import shutil
# 상세페이즈 파트
# 상세페이지는 페이지 이동같은 상호작용이 필요없고, 무엇보다 모든 웹툰(9월11일기준 4562개)을 셀레니움으로 크롤링하기에는 시간이 오래걸린다.
# 그러므로 처음 셀레니움을 쓸 때(모든 웹툰 크롤링) 상세페이지 url을 저장하고 나중에 한번에 구현하도록 했다.

#!! 전체페이지 크롤링 이후 바로 캡챠 넘어갈때 캡챠 이미지 위치가 안맞는다
def captcha():
    # detail_url = df['url'][i]
    # detail_url = wb_webtoon['U' + str(i + 2)].value
    detail_url = wb_webtoon['U2'].value
    driver.get(detail_url)
    # driver.minimize_window()
        # !! 만약 캡챠 틀렸을때도 고려해야한다

        # !! 캡챠 이미지를 다운 받아서 출력해준다면
        # !! driver를 headless로 해서 속도를 올리려함
        # ~~ 이 작업을 수행하려 하니 IP차단이 먹힘
        # ~~ 화면 캡쳐를 통해 캡챠이미지 추출
        # !! 결국 캡챠가 안뚫린다 어쩌냐
        # ~~ session에 cookie를 업데이트 함으로써 진행

    try:
        captcha_key = driver.find_element(By.ID, 'captcha_key')
    except Exception as e:
        for c in driver.get_cookies():
            cookies = {c['name']: c['value']}
        return cookies

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    captcha_img = driver.get_screenshot_as_png()
    open('captcha.png', 'wb').write(captcha_img)
    a = mat_img.imread('captcha.png')
    mat_plt.imshow(a[370:410, 535:605])
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

    for c in driver.get_cookies():
        cookies = {c['name']: c['value']}

    driver.quit()
    return cookies
#!! 셀레니움은 몰라도 request는 중간에 막힐 수 있으므로
#!! 어디까지 했는지 저장하는것도 좋아보인다
def detail_page(i, cookie):
    try:
        # detail_url = df['url'][i]
        detail_url = wb_webtoon['U' + str(i)].value
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        session.headers.update(headers)
        session.cookies.update(cookie)

        try:
            start_time = time.time()
            # response = requests.get(driver.current_url, headers={
            #         'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
            response = session.get(detail_url, headers={
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
            html = response.text
        # 에러 체크용 (requests가 잘받는지)
        except UnicodeDecodeError as error:
            print("UnicodeDecodeError! Line 282")
            resolved_url = urllib.request.Request(driver.current_url, headers={
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'})
            response = urllib.request.urlopen(resolved_url)
            html = response.read()

        soup = BeautifulSoup(html, 'html.parser')

        # 총 회차수
        # wb_webtoon[E2]
        try:
            # total_num = driver.find_element(By.CSS_SELECTOR, 'ul.list-body>li').get_attribute('data-index')
            total_num = soup.find_all('li', {'class': 'list-item'})
            wb_webtoon['E' + str(int(i))] = len(total_num)
        except Exception as e:
            # 만약 준비된게 없으면 추가하지말자
            print("No webtoons are ready! in " + wb_webtoon['A' + str(int(i))].value +" Line 295")
            return delay_cycle

        # 추천수
        # wb_webtoon[C2]
        # recommend_num = driver.find_element(By.ID, 'wr_good').text
        recommend_num = str(soup.find('b', {'id': 'wr_good'}).text)
        recommend_num = recommend_num.replace(",","")
        wb_webtoon['C' + str(int(i))] = int(recommend_num)


        # 별점
        # wb_webtoon[D2]
        # stars = driver.find_elements(By.CSS_SELECTOR, 'button.btn-white > i')
        # star_point = 0
        # for star in stars:
        #         if star.get_attribute('class') == 'fa fa-star crimson':
        #                 star_point += 1
        #         elif star.get_attribute('class') == 'fa fa-star-half-empty crimson':
        #                 star_point += 0.5
        #         else:
        #                 continue
        full_star2 = soup.select('button.btn-white > i.fa-star')
        half_star2 = soup.select('button.btn-white > i.fa-star-half-empty')

        star_point = len(full_star2) + (len(half_star2) * 0.5)
        wb_webtoon['D' + str(int(i))] = star_point

        # 첫화 링크
        # wb_webtoon[T2]
        # first_story_url = str(driver.find_element(By.CSS_SELECTOR, 'th.active > button').get_attribute('onclick'))[
        #                   15:-1]
        first_story = soup.find('button', attrs={'data-original-title': '첫회보기'})
        first_story_url = str(first_story.attrs['onclick'])[15: -1]
        wb_webtoon['T' + str(int(i))] = first_story_url

        # 이미지 저장
        try:
            images = soup.find('div', {'class': 'view-img'}).find('img').attrs['src']
            img = requests.get(images)
            with open(f'src/img/{i}.png', 'wb') as outfile:
                outfile.write(img.content)
        except Exception as img_error:
            print("No Image! Line 338")
            temp_img = "src/files/no_image.png"
            img = f'src/img/{i}.png'
            shutil.copyfile(temp_img,img)
        end_time = time.time()

        # if i%10 == 0:
        #     print(str(i+1) + "번째 웹툰 완료")
        #     print("한 웹툰 실행 시간 : " + str(end_time-start_time))
        #     # webtoon_num = int(wb_siteInfo['D2'].value) - 2 - (i+1)
        #     # total_time = webtoon_num * (e_e_time-a_s_time)
        #     # hour = int(total_time//3600)
        #     # minute = int(total_time//60)
        #     # second = int(total_time%60)
        #     # now = datetime.now()
        #     # print("예상 완료시간 : " + str(now.hour+hour) + "시 " + str(now.minute+minute) + "분 " + str(now.second+second) + "초")
        #     # print("현재 시간 : " + str(now.hour) + "시 " + str(now.minute) + "분 " + str(now.second) + "초")
        #     print("=========================")
        print(str(i) + "번째 셀("+str(i-1)+"번째 웹툰)에 있는 웹툰 ("+ wb_webtoon['A' + str(i)].value +") 완료")
        print("실행시간 : "+str(end_time-start_time))

        # 20개 웹툰을 할때마다 2~3초 사이의 딜레이를 줘서 ip차단을 막아보자

        #!! 지연 주기 자체도 랜덤성을 주고 싶은데 한번 갱신되기 전까진 같은 값을 유지하고 싶은데 어쩔가
        # if i % 20 == 0:
        #     delay_time = random.uniform(2, 3)
        #     # new_delay_cycle = int(random.uniform(10, 20))
        #
        #     #!! 핫스팟이나 셀레니움 쓰면 굳이 딜레이 줄 필요가 있나??
        #     time.sleep(delay_time)
        #     print("지연 크롤링을 위한 시간 : " + str(delay_time))
        print("=====================")
    except Exception as e:
        print(e,end=" ")
        print("Line 368")
        wb.save(fpath)
        sys.exit()
# 대략 한 웹툰 당 1초정도 소요예정 == (총웹툰 수)초 소요 예정

# 9-17일
last_updated_num = 4551
delay_cycle = int(random.uniform(10,20))

for i in range(last_updated_num+1,update_num-1):
    if i == last_updated_num+1:
        cookie = captcha()
    delay_cycle = detail_page(i, cookie)
    if (i-1)%50 == 0:
        xlsx_save_s_time = time.time()
        wb.save(fpath)
        xlsx_save_e_time = time.time()
        print("엑셀 저장 시간 : " + str(xlsx_save_e_time-xlsx_save_s_time))
wb.save(fpath)
print("모든 웹툰 크롤링 완료")


#!! 나중에 총화수 0인것 그냥 빼버리자




driver.implicitly_wait(3)

e_time = time.time()
print("총 실행시간 : " + str(e_time-s_time))