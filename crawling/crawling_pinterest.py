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
from selenium.webdriver import ActionChains


#검색할 키워드
'''핀터레스트'''
#keyword = ['여자 연예인 정면'] #1번부터~300
#keyword = ['한국 여자 연예인 정면'] #301번부터~600
#keyword = ['여자 연예인 화보'] #601번부터~900
#keyword = ['여자 배우'] #901번부터~1200
#keyword = ['여자 아이돌'] #1201번부터~1500


#####selenium 드라이버 설정######
CHROME_DRIVER_PATH = 'C:/Users/yebin/바탕 화면/신경공학 기말/chromedriver.exe' #크롬드라이버 실행파일 설치 경로
driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.implicitly_wait(1)
driver.get('https://www.pinterest.com/') 
driver.implicitly_wait(1)
time.sleep(2)

# 로그인 버튼 찾아서 클릭
button_login_window = driver.find_element_by_css_selector('#mweb-unauth-container > div > div > div.QLY._he.zI7.iyn.Hsu > div > div.Eqh.KS5.hs0.un8.C9i.TB_ > div.wc1.zI7.iyn.Hsu > button')
button_login_window.click()

# 이메일, 비밀번호 폼 찾기
input_email = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[2]/fieldset/span/div/input')
input_password = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[4]/fieldset/span/div/input')

# 이메일, 비밀번호 입력하기
input_email.send_keys('핀터레스트 아이디')
input_password.send_keys('핀터레스트 비밀번호')


# 로그인 버튼 누르기
button_login = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[4]/form/div[7]/button')
button_login.click()

# 로그인하는데 시간이 좀 걸려서 기다린다
time.sleep(4)
driver.implicitly_wait(2)

image_file_number = 0 #이미지 파일 이름 숫자
for keyword in ['여자 연예인 정면', '한국 여자 연예인 정면', '여자 연예인 화보', '여자 아이돌']: #검색어 리스트
    # 검색어 입력하기
    elem = driver.find_element_by_css_selector('#searchBoxContainer > div > div > div.ujU.zI7.iyn.Hsu > input[type=text]')
    for _ in range(100):
        elem.send_keys(Keys.BACKSPACE) #전부 지우고 검색어 입력
        time.sleep(0.01)
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)
    
    driver.implicitly_wait(1)

    links_saved = set() 

    target_num_images = 300 #검색어 당 가져올 개수
    force_scroll_down = 0
    
    # LOOP
    while True:
        try:
            ##이미지 가져오기
            images = driver.find_elements_by_xpath("//img[@srcset]")

            count_new_images = 0

            for image in images:
                try:
                    links = image.get_property('srcset')
                    imgUrl = list(filter(lambda x: x.startswith('https'), links.split(' ')))[-1]
                    imgUrl = imgUrl.replace('https', 'http') # https로 요청할 경우 보안 문제로 SSL에러가 남
                    
                    if imgUrl not in links_saved: #중복 거름
                        links_saved.add(imgUrl)

                        count_new_images += 1
                        image_file_number +=1
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-Agent', 'Mozilla/5.0')] 
                        urllib.request.install_opener(opener)
        
                        ##이미지 저장
                        urllib.request.urlretrieve(imgUrl, 'images_pinterest/image_{}.jpg'.format(str(image_file_number))) #저장경로 
                        print(f'--{image_file_number}번째 이미지 저장 완료--')
                except Exception as e:
                    pass

            if len(links_saved) > target_num_images:
                break
            
            #스크롤 내리기    
            if count_new_images == 0:
                if force_scroll_down < 5:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    force_scroll_down += 1
                    time.sleep(1)
                    driver.implicitly_wait(1)
                else:
                    print('Force break')
                    break
            elif len(images)>0:
                action = ActionChains(driver)
                action.move_to_element(images[-1]).perform()
                force_scroll_down = 0
            else:
                break
            pass
        except Exception as e:
            pass