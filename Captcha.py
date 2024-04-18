from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import matplotlib.image as mat_img
import matplotlib.pyplot as mat_plt
import pyautogui
import pyperclip

import time
# import threading

def Login(driver):
    newtoki_id = 'zxcvcxz'
    newtoki_pw = 'zxcv  '
    driver.find_element(By.XPATH, '//*[@id="basic_outlogin"]/div[1]/button').click()
    id_field = driver.find_element(By.XPATH,'//*[@id="login_id"]')
    pw_field = driver.find_element(By.XPATH,'// *[ @ id = "login_pw"]')
    id_field.send_keys(newtoki_id)
    pw_field.send_keys(newtoki_pw)
    cookies = captcha(driver)
    # driver.find_element(By.XPATH,'//*[@id="content_wrapper"]/div[2]/div/div[2]/div/div/div[2]/form/div[4]/div[2]/button').click()
    driver.find_element(By.XPATH, '//*[@id="hd_pops_2"]/div[2]/button[1]').click()
    driver.find_element(By.XPATH, '//*[@id="navbar-collapse"]/ul/li[1]/a').click()
    return cookies

def captcha(driver):
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    captcha_img = driver.get_screenshot_as_png()
    open('src/file/captcha.png', 'wb').write(captcha_img)
    a = mat_img.imread('src/file/captcha.png')
    mat_plt.imshow(a[555:585, 860:930])
    mat_plt.show()

    # !! plt랑 pyautogui 동시에 나오게 하는법 없나?
    # !! 아님 plt에서 입력받는 법 없나?
    # ~~ Prac.py 활용해보자 < 아직 안함
    captcha_num = pyautogui.prompt("Captcha 입력 >> ")
    captcha_key = driver.find_element(By.ID, 'captcha_key')
    captcha_key.click()
    pyperclip.copy(captcha_num)
    captcha_key.send_keys(Keys.CONTROL, 'v')
    driver.find_element(By.CLASS_NAME, 'btn-color').click()

    for c in driver.get_cookies():
        cookies = {c['name']: c['value']}
    return cookies
