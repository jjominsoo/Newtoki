from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import CreateFile
import AllCrawling


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())



driver = webdriver.Chrome(service=service, options=chrome_options)
## 모든 웹툰 데이터를 크롤링한다.
## 만약 중간에 멈출 수도 있으므로 index를 일단 정해두자.
## 나중에 Update.py에서 활용할 수 도 있다.
## WebtoonInfo_proto.csv   : 모든 웹툰들을 정리한 csv파일
## Mark.csv          : 마지막으로 업데이트한 웹툰 이름을 저장한 csv파일 > 자주 변동되는 url주소를 확인하기 위해 쓰일 것임
CreateFile.InitCSV()

## 비정기적으로 바뀌는 도메인 주소
## 마지막으로 접속 가능했던 도메인 주소에 1씩 더해가면서 접속 가능한 주소를 찾음
## 해당 주소를 업데이트하는 함수
url = CreateFile.CheckURL(driver)

## 전체 크롤링
## 해당 뉴토끼는 요일을 기준 검색을 하면 각 요일마다 모든 웹툰을 크롤링이 가능함
## 따라서 요일 별로 크롤링을 진행함
## !!마나토끼는 양이 많아서 해당 방식으로는 모든 만화를 크롤링할 수 없다.
## ~~
## !!driver랑 같이 쓰는데 request만은 못쓰나?
## ~~
## +
## 상세 크롤링
## 상세는 업데이트에도 필요하므로 중복을 찾는 것이 중요
## 이미지, 총화수, 댓글, 별점(화수) 마지막업데이트날짜 << 없는 경우가 있으니 예외처리를 해야함
AllCrawling.AllCrawling(url, driver)

## 검색 크롤링
## 일단 '카카오웹툰' '네이버웹툰' 을 기준으로 할 거임
## 만약 카카오, 네이버에도 없으면 따로 리스트 정렬해놓자
driver.quit()





## 크롤링 정보
# 1. 전체페이지
#   이름, 장르, 요일
# 2. 상세페이지
#   이름 이미지(다운로드) 총화수(int) 댓글(list(빨간줄)) 별점(화수)(list) 별점(총)(float) 추천수(int) 마지막업데이트날짜(datetime)
# 3. 검색
#   이름 플랫폼(list(3개 정도)) 작가/그림('/'로슬라이싱) 첫화링크(플랫폼의링크)

## 주의점
# 1,2는 이름이 동일하지만 3은 다를 수 있다.
# ex) 더는 못본척 하지 않기로 했다 <> 더는 못 본 척하지 않기로 했다
# 방법1. 문장간 유사도 / 방법2. trim

# ['이름', '작가/그림', '장르','요일', '추천수', '별점(총)', '별점(화)', '총화수', '댓글', '줄거리', '이미지', '플랫폼', '첫화링크'])


# print(df)
# df.to_csv()

# driver.quit()