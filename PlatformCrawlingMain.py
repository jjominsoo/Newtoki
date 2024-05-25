from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import KPCrawling
import KWCrawling
import NVCrawling
import pandas as pd
import concurrent.futures

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())

driver1 = webdriver.Chrome(service=service, options=chrome_options)
driver2 = webdriver.Chrome(service=service, options=chrome_options)
driver3 = webdriver.Chrome(service=service, options=chrome_options)
driver1.get("https://webtoon.kakao.com/")
driver2.get("https://page.kakao.com/")
driver3.get("https://series.naver.com/comic/home.series")

def crawl_kakao_webtoon(driver1, title, kw, mark_kw):
    KWCrawling.KWCrawling(driver1, title, kw, mark_kw)
    print(f"{title} - 카카오웹툰 크롤링 완료")


def crawl_kakao_page(driver2, title, kp, mark_kp):
    KPCrawling.KPCrawling(driver2, title, kp, mark_kp)
    print(f"{title} - 카카오페이지 크롤링 완료")

def crawl_naver_series(driver3, title, nv, mark_nv):
    NVCrawling.NVCrawling(driver3, title, nv, mark_nv)
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
                k = input()
    return results

import time
from tqdm import tqdm
if __name__ == "__main__":
    count = 0
    df = pd.read_csv('src/file/name2.csv')
    k = input("모든 페이지 로그인 해보자")
    for title in tqdm(df['이름'][5179:]):
        results = crawl_all_platforms(title)
        print("=" * 50)
    print("All Crawling End")
    time.sleep(30)