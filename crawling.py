from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://newtoki270.com")
## 뉴토끼는 도메인 주소가 바뀌므로 만약 없는 주소라면 1씩 더해서 탐색한다
## 제일 좋은 방법은 바뀐 주소를 따로 저장하는 것
## 그럼 차라리 파일을 만들어볼까
# Num_in_0804 = 301
# url = "https://www.newtoki" + str(Num_in_0804) + ".com"
# driver.get(url)
