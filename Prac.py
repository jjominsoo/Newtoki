# import matplotlib.pyplot as plt
# import pyautogui
# import threading
#
#
# # 그래프 표시 함수
# def show_plot():
#     x = [1, 2, 3, 4, 5]
#     y = [2, 3, 5, 7, 11]
#
#     plt.plot(x, y)
#     plt.xlabel('X-axis')
#     plt.ylabel('Y-axis')
#     plt.title('Sample Plot')
#     plt.subplots_adjust(right=10)
#
#     plt.show()
#
#
# # 입력 받고 확인하는 함수
# def input_confirmation():
#     # 그래프가 보이는 곳에서 멀리 떨어진 위치에 GUI 생성
#     # pyautogui.alert(text='Enter a number:', title='Input', button='OK')
#     pyautogui.moveTo(800, 400)
#
#     # 값을 입력 받음
#     value = pyautogui.prompt(text='Enter a number:', title='Input', default='')
#
#     if value is not None:  # 취소 버튼이 아닌 경우
#         plt.close()
#
#
# # 그래프 표시
# show_plot_thread = threading.Thread(target=show_plot)
# show_plot_thread.start()
#
# # 입력 받고 확인
# input_confirmation_thread = threading.Thread(target=input_confirmation)
# input_confirmation_thread.start()
#
# # 두 쓰레드가 모두 종료될 때까지 대기
# show_plot_thread.join()
# input_confirmation_thread.join()
#
# print("Plot closed.")

# from queue import Queue
# import threading
#
# # 웹툰 제목 리스트
# webtoon_titles = ["웹툰1", "웹툰2", "웹툰3", "웹툰4", "웹툰5", "웹툰6", "웹툰7", "웹툰8", "웹툰9", "웹툰10", "웹툰11", "웹툰12", "웹툰13", "웹툰14", "웹툰15", "웹툰16", "웹툰17", "웹툰18", "웹툰19", "웹툰20"]
#
# # 큐 생성
# first_queue = Queue()
# second_queue = Queue()
# third_queue = Queue()
# fourth_queue = Queue()
#
# # 웹툰 제목을 첫 번째 큐에 추가
# for title in webtoon_titles:
#     first_queue.put(title)
#
#
# def crawl_kakao_webtoon(title):
#     print(f"kakowebtoon : {title}")
#
# # 카카오웹툰 크롤링 코드
# # ...
#
# def crawl_kakao_page(title):
#     print(f"kakopage : {title}")
#
#
# # 카카오페이지 크롤링 코드
# # ...
#
# def crawl_naver_series(title):
#     print(f"naver : {title}")
#
#
# # 네이버시리즈 크롤링 코드
# # ...
#
# def crawl_lezhin_comics(title):
#     print(f"lezhin : {title}")
#
#
# # 레진코믹스 크롤링 코드
# # ...
#
# def worker(queue, next_queue):
#     while not queue.empty():
#         title = queue.get()
#         if crawl_kakao_webtoon(title):
#             continue
#         elif crawl_kakao_page(title):
#             continue
#         elif crawl_naver_series(title):
#             continue
#         elif crawl_lezhin_comics(title):
#             continue
#         else:
#             next_queue.put(title)
#
#         queue.task_done()
#
#
# # 쓰레드 생성 및 시작
# threads = []
# queues = [(first_queue, second_queue), (second_queue, third_queue), (third_queue, fourth_queue)]
#
# for queue, next_queue in queues:
#     thread = threading.Thread(target=worker, args=(queue, next_queue))
#     thread.start()
#     threads.append(thread)
#
# # 첫 번째 큐의 작업이 완료될 때까지 대기
# for thread in threads:
#     thread.join()
#
# print("크롤링 완료!")

# from queue import Queue
# import threading
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# # 웹툰 제목 리스트
# webtoon_titles = ["웹툰1", "웹툰2", "웹툰3", "웹툰4", "웹툰5", "웹툰6", "웹툰7", "웹툰8", "웹툰9", "웹툰10", "웹툰11", "웹툰12", "웹툰13", "웹툰14", "웹툰15", "웹툰16", "웹툰17", "웹툰18", "웹툰19", "웹툰20"]
#
# # 큐 생성
# kakao_webtoon_queue = Queue()
# kakao_page_queue = Queue()
# naver_series_queue = Queue()
# lezhin_comics_queue = Queue()
# nothing_queue = Queue()
# webtoon_queue = Queue()
# # 웹툰 제목을 첫 번째 큐에 추가
# for title in webtoon_titles:
#     kakao_webtoon_queue.put(title)
#
# def crawl_kakao_webtoon(title):
#     kakao_webtoon_list = ['웹툰1','웹툰3','웹툰6','웹툰13','웹툰19']
#     # 카카오웹툰에서 웹툰을 찾을 수 있는지 확인하는 로직
#     if title in kakao_webtoon_list:
#         print(f"{title} - 카카오웹툰에서 정보를 가져옵니다.")
#         kakao_page_queue.put(title)
#     else:
#         kakao_page_queue.put(title)
#
#
# def crawl_kakao_page(title):
#     kakao_page_list = ['웹툰1','웹툰4','웹툰5','웹툰10','웹툰15','웹툰16']
#     if title in kakao_page_list:
#         print(f"{title} - 카카오페이지에서 정보를 가져옵니다.")
#         naver_series_queue.put(title)
#     else:
#         naver_series_queue.put(title)
#
#
# def crawl_naver_series(title):
#     naver_list = ['웹툰9','웹툰11','웹툰17','웹툰18']
#     # 네이버시리즈에서 웹툰을 찾을 수 있는지 확인하는 로직
#     if title in naver_list:
#         print(f"{title} - 네이버시리즈에서 정보를 가져옵니다.")
#         lezhin_comics_queue.put(title)
#     else:
#         lezhin_comics_queue.put(title)
#
#
# def crawl_lezhin_comics(title):
#     lezhin_list = ['웹툰8','웹툰12','웹툰14','웹툰20']
#     # 레진코믹스에서 웹툰을 찾을 수 있는지 확인하는 로직
#     if title in lezhin_list:
#         print(f"{title} - 레진코믹스에서 정보를 가져옵니다.")
#     else:
#         nothing_queue.put(title)
#
# def nothing(title):
#     print(f"{title} - 기타 플랫폼에 있습니다. (추가정보를 가져올 수 없습니다)")
#
#
# def worker(queue, crawler):
#     while not queue.empty():
#         title = queue.get()
#         crawler(title)
#         # queue.task_done()
#
# for title in webtoon_titles:
#     webtoon_queue.put(title)
# # 쓰레드 생성 및 시작
# threads = [
#     threading.Thread(target=worker, args=(webtoon_queue, crawl_kakao_webtoon)),
#     threading.Thread(target=worker, args=(webtoon_queue, crawl_kakao_page)),
#     threading.Thread(target=worker, args=(webtoon_queue, crawl_naver_series)),
#     threading.Thread(target=worker, args=(webtoon_queue, crawl_lezhin_comics)),  # 마지막 크롤링은 다음 큐가 없음
#     # threading.Thread(target=worker, args=(nothing_queue, None, nothing))  # 마지막 크롤링은 다음 큐가 없음
# ]
#
# k = input()
# # 쓰레드 시작
# for thread in threads:
#     thread.start()
#     thread.join()
#
#
# # 모든 작업이 완료될 때까지 대기
# # for thread in threads:
# #     thread.join()
#
# print("크롤링 완료!")
#

import AllCrawling
import KPCrawling
import KWCrawling
import NVCrawling

import pandas as pd
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('user-agent=' + user_agent)
# chrome_options.add_argument('--headless=new')
service = Service(executable_path=ChromeDriverManager().install())
driver1 = webdriver.Chrome(service=service, options=chrome_options)
driver2 = webdriver.Chrome(service=service, options=chrome_options)
driver3 = webdriver.Chrome(service=service, options=chrome_options)
driver1.get("https://webtoon.kakao.com/")
driver2.get("https://page.kakao.com/")
driver3.get("https://series.naver.com/comic/home.series")

def crawl_kakao_webtoon(driver1, title, kw, mark_kw):
    AllCrawling.KWCrawling(driver1, title, kw, mark_kw)
    print(f"{title} - 카카오웹툰 크롤링 완료")


def crawl_kakao_page(driver2, title, kp, mark_kp):
    KPCrawling.KPCrawling(driver2, title, kp, mark_kp)
    print(f"{title} - 카카오페이지 크롤링 완료")

def crawl_naver_series(driver3, title, nv, mark_nv):
    AllCrawling.NVCrawling(driver3, title, nv, mark_nv)
    print(f"{title} - 네이버시리즈 크롤링 완료")



def crawl_all_platforms(title):
    results = {}
    kw = pd.read_csv('src/file/search_kw.csv')
    kp = pd.read_csv('src/file/search_kp.csv')
    nv = pd.read_csv('src/file/search_nv.csv')
    mark_kw = pd.read_csv('src/file/mark_kw.csv')
    mark_kp = pd.read_csv('src/file/mark_kp.csv')
    mark_nv = pd.read_csv('src/file/mark_nv.csv')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(crawl_kakao_webtoon, driver1, title, kw, mark_kw): "카카오웹툰",
            executor.submit(crawl_kakao_page, driver2, title, kp, mark_kp): "카카오페이지",
            executor.submit(crawl_naver_series, driver3, title, nv, mark_nv): "네이버시리즈",
        }

        for future in concurrent.futures.as_completed(futures):
            platform = futures[future]
            try:
                data = future.result()
                results[platform] = data
            except Exception as e:
                print(f"{platform} 크롤링 중 에러 발생: {e}")
    return results

import time
from tqdm import tqdm
if __name__ == "__main__":
    count = 0
    df = pd.read_csv('src/file/name2.csv')
    k = input("모든 페이지 로그인 해보자")
    for title in tqdm(df['이름'][420:]):
        results = crawl_all_platforms(title)
        print("=" * 50)
    print("All Crawling End")
    time.sleep(30)