import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
import urllib.request
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#검색할 키워드
'''구글'''
#keyword = ['한국 여자 연예인 프로필'] #1번부터~100
#keyword = ['여자 연예인 정면'] #101번부터~200
#keyword = ['여자아이돌 레전드'] #201번부터~300
#keyword = ['여자아이돌 정면'] #301번부터~400
#keyword = ['여자 배우 정면'] #401번부터~500
#keyword = ['여자 연예인 얼굴'] #501번부터~600
#keyword = ['여자 아이돌 얼굴'] #601번부터~700
#keyword = ['예쁜 여자 아이돌'] #701번부터~900
#keyword = ['예쁜 여자 배우'] #901번부터~1100
#keyword = ['여자 연예인 리즈'] #1101번부터~1300
keyword = ['여자 연예인 화보'] #1301번부터~1500

numbers = 300 #가져올 이미지 개수

#####selenium 드라이버 설정######
CHROME_DRIVER_PATH = 'C:/Users/yebin/바탕 화면/신경공학 기말/chromedriver.exe' #크롬드라이버 실행파일 설치 경로
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get('https://www.google.com/imghp') #이미지 가져올 주소(구글 이미지 검색)
elem = driver.find_element_by_name('q')
elem.send_keys(keyword)
elem.send_keys(Keys.RETURN)

#####이미지 크롤링######
#로딩 다 되게 스크롤 끝까지 내리기
SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector('.mye4qd').click()
        except:
            break
    last_height = new_height

        
# 이미지 수집 및 저장
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") # 각 이미지들의 class
count = 1
for image in images:
    try:
        image.click()
        time.sleep(1)

        ##이미지 Url 가져오기
        imgUrl = driver.find_element(By.XPATH,
             f'//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]').get_attribute("src")              
        imgUrl = imgUrl.replace('https', 'http') # https로 요청할 경우 보안 문제로 SSL에러가 남

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')] # https://docs.python.org/3/library/urllib.request.html 참고
        urllib.request.install_opener(opener)
        
        ##이미지 저장
        urllib.request.urlretrieve(imgUrl, 'images_google/image_{}.jpg'.format(str(1300+count))) #저장경로
        count = count + 1
        print(f'--{count}번째 이미지 저장 완료--')
        if count == numbers +1:
            break
        
    except Exception as e:
        print('Error : ', e)
        pass

driver.close()

