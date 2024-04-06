import re
import pandas as pd
import time


# WebtoonInfo.csv   : 모든 웹툰들을 정리한 csv파일
# Mark.csv          : 마지막으로 업데이트한 웹툰 이름을 저장한 csv파일 > 자주 변동되는 url주소를 확인하기 위해 쓰일 것임
def InitCSV():
    df = pd.DataFrame(columns=['이름', '작가/그림', '장르','요일', '추천수', '별점(총)', '별점(화)', '총화수', '댓글', '줄거리', '이미지', '플랫폼', '첫화링크'])
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

def PageCrawling(url,week,df):
    response = requests.get(url,headers={'User-agent':user_agent})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    webtoon_list = soup.find_all('li', {'data-weekday': week+'요일'})

    webtoon_name = []
    webtoon_genre = []
    webtoon_week = []

    for i, webtoon in enumerate(webtoon_list):
        webtoon_name.append(webtoon['date-title'])
        webtoon_genre.append(webtoon['data-genre'])
        webtoon_week.append(week)

    df['이름'].append(webtoon_name)
    df['장르'].append(webtoon_genre)
    df['요일'].append(webtoon_week)
    # detail_pages =