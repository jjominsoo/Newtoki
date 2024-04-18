import Captcha
import Crawling

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
