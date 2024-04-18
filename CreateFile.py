import pandas as pd
import re

# Web toonInfo.csv   : 모든 웹툰들을 정리한 csv파일
# Mark.csv          : 마지막으로 업데이트한 웹툰 이름을 저장한 csv파일 > 자주 변동되는 url주소를 확인하기 위해 쓰일 것임
def InitCSV():
    df = pd.DataFrame(columns=['이름', '작가/그림', '장르', '요일', '추천수', '별점(총)', '별점(화)', '총화수',
                               '댓글', '줄거리', '이미지', '플랫폼', '링크', '업데이트'])
    df.to_csv('src/WebtoonInfo.csv', index=False)
    init_mark = {'이름': '', '순서': 0, '도메인': 'https://newtoki328.com/'}
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
                print(f'성공! 주소는 {url}입니다.')
                break
        except Exception as e:
            print(f'도메인 주소 변경 중..\n{e}')
            number += 1
            url = url[:a.start()] + str(number) + url[a.end():]
    mark['도메인'] = url
    mark.to_csv('src/Mark.csv', index=False)
    return url

def CreateDF(name, genre, week, img, num, reply, star1, star2, recommend, plot, update):
    df = pd.read_csv('src/WebtoonInfo.csv')
    merged_df2 = pd.DataFrame()
    print(f'이름 : {len(name)}, 장르 : {len(genre)},요일 : {len(week)}, '
          f'이미지 : {len(img)}, 총화수 : {len(num)}, 댓글 : {len(reply)}, '
          f'별점화 : {len(star1)}, 별점총 : {len(star2)}, 추천수 : {len(recommend)}, '
          f'줄거리 : {len(plot)}, 업데이트 : {len(update)}')
    merged_df2['이름'] = name
    merged_df2['장르'] = genre
    merged_df2['요일'] = week
    merged_df2['이미지'] = img
    merged_df2['총화수'] = num
    merged_df2['댓글'] = reply
    merged_df2['별점(화)'] = star1
    merged_df2['별점(총)'] = star2
    merged_df2['추천수'] = recommend
    merged_df2['줄거리'] = plot
    merged_df2['업데이트'] = update
    print(merged_df2)
    df = pd.concat([df, merged_df2], ignore_index=True)
    df.to_csv('src/WebtoonInfo.csv', index=False)
    return df