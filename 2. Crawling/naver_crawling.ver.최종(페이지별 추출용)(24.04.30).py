def switch_left():
    ############## iframe으로 왼쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    #driver.switch_to.default_content()
    iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
    driver.switch_to.frame(iframe)
    
def switch_right():
    ############## iframe으로 오른쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    #driver.switch_to.default_content()
    iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
    driver.switch_to.frame(iframe)

def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    #body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from time import sleep
import random
import re
import pandas as pd

from selenium import webdriver
import sys

numbering = []
store_name_list = []
rating_list = []
visited_review_num_list = []
review_list = []
address_list = []
review_writer_list = []
review_date_list = []

options = Options()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36')
options.add_argument('window-size=1380,850')
driver = webdriver.Chrome(options=options)

# 대기 시간
driver.implicitly_wait(time_to_wait=3)

keyword = input("키워드를 입력하세요 : ")
page_num = input("페이지 번호를 입력하세요 : ")

URL = 'https://map.naver.com/p?c=15.00,0,0,2,dh'
driver.get(url=URL)

search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search.send_keys(keyword)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기
sleep(2)

switch_left()

if page_num == '6':
    driver.find_element(By.XPATH,f'//*[@id="app-root"]/div/div[2]/div[2]/a[{page_num}]').click()
    sleep(2)
    driver.find_element(By.XPATH,f'//*[@id="app-root"]/div/div[2]/div[2]/a[{page_num}]').click()
    sleep(2)

else:
    driver.find_element(By.XPATH,f'//*[@id="app-root"]/div/div[2]/div[2]/a[{page_num}+1]').click()
    sleep(2)

############## 맨 밑까지 스크롤 ##############
scrollable_element = driver.find_element(By.CLASS_NAME, "Ryr1F")

last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

while True:
    # 요소 내에서 아래로 600px 스크롤
    driver.execute_script("arguments[0].scrollTop += 600;", scrollable_element)

    # 페이지 로드를 기다림
    sleep(1)

    # 새 높이 계산
    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

    # 스크롤이 더 이상 늘어나지 않으면 루프 종료
    if new_height == last_height:
        break

    last_height = new_height

elemets = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')

print('현재 ' + '\033[95m' + str(page_num) + '\033[0m' + ' 페이지 / '+ '총 ' + '\033[95m' + str(len(elemets)) + '\033[0m' + '개의 가게를 찾았습니다.\n')

for index, e in enumerate(elemets, start=1):
    final_element = e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span")

    print(str(index) + ". " + final_element.text)

print("-"*50)

switch_left()

sleep(2)

for index, e in enumerate(elemets[:3], start=1):
    switch_left()

    try:
        # 가게명 클릭
        e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a").click()
        sleep(2)

        switch_right()

        # 주소 수집
        address = driver.find_element(By.CLASS_NAME, 'LDgIH').text

        # 리뷰 버튼 클릭
        tabs = driver.find_element(By.CLASS_NAME, 'place_fixed_maintab').find_elements(By.XPATH, './/div/div/div/div/a')       
        if len(tabs) <= 4:
            temp = driver.find_element(By.CLASS_NAME, 'place_fixed_maintab').find_element(By.XPATH, './/div/div/div/div/a[2]/span')
            if temp.text == '메뉴':
                driver.find_element(By.CLASS_NAME, 'place_fixed_maintab').find_element(By.XPATH, './/div/div/div/div/a[3]').click()
                sleep(2)         
            else:
                driver.find_element(By.CLASS_NAME, 'place_fixed_maintab').find_element(By.XPATH, './/div/div/div/div/a[2]').click()
                sleep(2)  

        elif len(tabs) == 5:
            driver.find_element(By.CLASS_NAME, 'place_fixed_maintab').find_element(By.XPATH, './/div/div/div/div/a[3]').click()
            sleep(2)

        elif len(tabs) == 6:
            driver.find_element(By.CLASS_NAME, 'place_fixed_maintab').find_element(By.XPATH, './/div/div/div/div/a[4]').click()
            sleep(2)

        else:
            driver.find_element(By.CLASS_NAME, 'place_fixed_maintab').find_element(By.XPATH, './/div/div/div/div/a[5]').click()
            sleep(2)

        # 우측 프레임 스크롤 다운 & 더보기 버튼 클릭
        more_btns = driver.find_elements(By.CLASS_NAME, 'NSTUp')

        # review_btn이 활성화되지 않았다면, 바로 다음 단계로 넘어갑니다.
        try:
            if len(more_btns) == 0:
                print("review_btn이 활성화되지 않았습니다. 다음 단계로 넘어갑니다.")
            else:
                more_btn = driver.find_element(By.CLASS_NAME, 'NSTUp').find_element(By.XPATH, './/div/a')
                for i in range(3):
                    driver.execute_script("arguments[0].click();", more_btn)
                    sleep(3)

        except Exception as e:  # 구체적인 예외 타입을 지정하는 것이 좋습니다.
            print("오류가 발생했습니다:", e)

    except:
        print('------------ 더보기 오류 발생 ------------')

    ################### 여기부터 크롤링 시작 ##################
    title = driver.find_element(By.XPATH,'//div[@class="zD5Nm undefined"]')
    review = title.find_elements(By.XPATH,'.//div[2]/span')

    # 가게 이름                                      
    store_name = title.find_element(By.XPATH,'.//div[1]/div[1]/span[1]').text

    ###############################

    # 인덱스 변수 값
    _index = 1

    # 리뷰 ROW의 갯수가 3개 이상일 경우 [별점, 방문자 리뷰, 블로그 리뷰]
    if len(review) > 2:
        rating_xpath = f'.//div[2]/span[{_index}]'
        rating_element = title.find_element(By.XPATH, rating_xpath)
        rating = rating_element.text.replace("\n", " ")
        rating = rating[2:]

        _index += 1

        try:
            # 방문자 리뷰
            visited_review = title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text
            visited_review = visited_review[5:]

            # 리뷰 내용
            review_nums = driver.find_elements(By.CLASS_NAME,'owAeM')
            for review_num in review_nums:
                review_writer = review_num.find_element(By.CLASS_NAME, 'RKXdJ').find_element(By.XPATH, './/a[2]/div[1]/span').text
                review_content = review_num.find_element(By.CLASS_NAME,'zPfVt').text
                review_date = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, './/span[1]/time').text
                #visit_num = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div[3]/div[1]/ul/li/div/div[6]/div[2]/span[2]').text
                visit_num = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, './/span[2]').text
                visit_num = visit_num[0]

                numbering.append(index)
                store_name_list.append(store_name)
                rating_list.append(rating)
                visited_review_num_list.append(visited_review)
                review_list.append(review_content)
                address_list.append(address)
                review_writer_list.append(review_writer)
                review_date_list.append(review_date)

        except Exception as e:
            print('------------ 리뷰 없음 1------------', e)

    elif len(review) == 2:
        try:
            # 방문자 리뷰
            visited_review = title.find_element(By.XPATH,f'.//div[2]/span[1]/a').text
            visited_review = visited_review[5:]

            # 리뷰 내용
            review_nums = driver.find_elements(By.CLASS_NAME,'owAeM')
            for review_num in review_nums:
                review_writer = review_num.find_element(By.CLASS_NAME, 'RKXdJ').find_element(By.XPATH, './/a[2]/div[1]/span').text
                review_content = review_num.find_element(By.CLASS_NAME,'zPfVt').text
                review_date = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, './/span[1]/time').text
                #visit_num = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div[3]/div[1]/ul/li/div/div[6]/div[2]/span[2]').text
                visit_num = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, './/span[2]').text
                visit_num = visit_num[0]

                numbering.append(index)
                store_name_list.append(store_name)
                rating_list.append('')
                visited_review_num_list.append(visited_review)
                review_list.append(review_content)
                address_list.append(address)
                review_writer_list.append(review_writer)
                review_date_list.append(review_date)

        except Exception as e:
            print('------------ 리뷰 없음 2------------', e)        

    elif len(review) == 1:
        visited_review = title.find_element(By.XPATH,f'.//div[2]/span/a').text
        visited_review = visited_review[5:]
        if visited_review == '방문자리뷰':
            try:
                # 리뷰 내용
                review_nums = driver.find_elements(By.CLASS_NAME,'owAeM')
                for review_num in review_nums:
                    review_writer = review_num.find_element(By.CLASS_NAME, 'RKXdJ').find_element(By.XPATH, './/a[2]/div[1]/span').text
                    review_content = review_num.find_element(By.CLASS_NAME,'zPfVt').text
                    review_date = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, './/span[1]/time').text
                    visit_num = review_num.find_element(By.CLASS_NAME, 'D40bm').find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div[3]/div[1]/ul/li/div/div[6]/div[2]/span[2]').text
                    visit_num = visit_num[0]

                    numbering.append(index)
                    store_name_list.append(store_name)
                    rating_list.append('')
                    visited_review_num_list.append(visited_review)
                    review_list.append(review_content)
                    address_list.append(address)
                    review_writer_list.append(review_writer)
                    review_date_list.append(review_date)

            except Exception as e:
                print('------------ 리뷰 없음 3------------', e)    

data = {"Number" : numbering, "Store" : store_name_list, "Address" : address_list,\
        "Review_score" : rating_list, "Review_counts" : visited_review_num_list,\
        "ID" : review_writer_list, "Date" : review_date_list,\
            "Review_text" : review_list,\
                }

df = pd.DataFrame(data)

df.to_csv(f"review_crawling_{page_num}page.csv", encoding = "utf-8-sig")