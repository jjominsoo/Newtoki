from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import CreateFile
import AllCrawling


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('user-agent=' + user_agent)
service = Service(executable_path=ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get('https://page.kakao.com/')

query = '이미테이션'
driver.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/div[1]/input').send_keys(query)
driver.find_element(By.XPATH, '//*[@id="pc-search-modal-root-id"]/a').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div/div/div[2]/a/div/div/span')))
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[1]/div/div/div[2]/a/div/div/span').click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[3]/div/div[1]/div/a')))
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[3]/div/div[1]/div/a').click()

driver.quit()