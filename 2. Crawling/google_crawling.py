import pandas as pd
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def find_text(col, url):
    try:
        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, url)))
        for element in elements:
            element = element.text
            col.append(element)
    except:
        col.append('정보없음')

# 최종 데이터프레임의 종류
info_df = pd.DataFrame()
review_df = pd.DataFrame()
merged_df = pd.DataFrame()

# 크롬으로 변경
driver = webdriver.Chrome()

# [stpe1] 크롤링 시작
url = f'https://www.google.co.kr/maps/?hl=ko&entry=ttu'
driver.get(url)

time.sleep(random.uniform(2,3))
search_box = driver.find_element(By.XPATH, '//*[@id="searchboxinput"]')
search_box.send_keys("서울특별시 중구 빵")
search_box.send_keys(Keys.ENTER)

i = 3
number = 1
while True:
    time.sleep(random.uniform(3,4))
    click_elements = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{i}]/div/a')))
    for element in click_elements:
        element.click()

    name = []
    rating = []
    review = []
    category = []
    adress = []

    time.sleep(random.uniform(2,3))
    find_text(name, ".DUwDvf.lfPIob")
    find_text(rating, ".F7nice > span:nth-child(1)")
    find_text(review, ".F7nice > span:nth-child(2)")
    find_text(category, ".fontBodyMedium span button.DkEaL")
    find_text(adress, ".rogA2c")

    # 임시 데이터프레임 생성
    time.sleep(random.uniform(2,3))
    tmp = pd.DataFrame()
    tmp['number'] = [number]
    tmp['Store'] = name
    tmp['Review_score'] = rating
    tmp['Review_counts'] = review
    tmp['Category'] = category
    tmp['Address'] = adress[0]

    # 최종 데이터프레임(1)_인포
    time.sleep(random.uniform(2,3))
    info_df = pd.concat([info_df, tmp])
  
    # [step2] 리뷰 크롤링: 에러가 나면 버튼이 없는 것이라 pass한다.
    try:  # 리뷰 경우의 수(1)
        review_elements = WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[3]/div/div/button[2]')))
        for element in review_elements:
            element.click()
    except:
        pass

    try:
        result = []
        time_list = []

        time.sleep(random.uniform(3,4))  # 리뷰 경우의 수(2)
        driver.find_element(By.CSS_SELECTOR, 'div.m6QErb.Pf6ghf.KoSBEe.ecceSd.tLjsW > div.TrU0dc.kdfrQc').click()

        time.sleep(random.uniform(1,3))
        driver.find_element(By.XPATH, '//*[@id="action-menu"]/div[2]').click()

        time.sleep(random.uniform(2,4))  # 스크롤 내리기 시작
        scroll = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]')
        last_height = driver.execute_script("return arguments[0].scrollHeight", scroll)
        num = 0
        while True:
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scroll)
            time.sleep(random.uniform(4, 5))
            new_height = driver.execute_script("return arguments[0].scrollHeight", scroll)
            buttons = driver.find_elements(By.CSS_SELECTOR, ".w8nwRe.kyuRq")
            for button in buttons:  # 더보기 버튼 누르기
                if button.is_displayed():
                    if button.is_enabled():
                        button.click()
                        num+=1
                        time.sleep(random.uniform(1, 2))
                    break
            if new_height == last_height:
                break
            last_height = new_height

        buttons = driver.find_elements(By.CSS_SELECTOR, ".w8nwRe.kyuRq")
        for button in buttons:
            if button.is_displayed():
                if button.is_enabled():
                    button.click()
                    num+=1
                    time.sleep(random.uniform(1, 2))
                    
        # [stpe3] 진행사항 체크(1)
        print(f"자세히 버튼을 {num}번 클릭했습니다.")

        last_review = None
        flag = False
        while not flag:
            reviews = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.wiI7pd')))
            
            if not reviews:  # 리뷰 경우의수(3)
                break

            for review in reviews:  # 리뷰 경우의 수(4)
                review_text = review.text
                if review_text == last_review:
                    break
                if review_text not in result:
                    if review.tag_name.lower() == 'span':
                        result.append(review_text)
                        now = datetime.now().strftime('%Y-%m-%d - %H:%M:%S')
                        time_list.append(now)
                else:
                    flag=True
            
            if len(result) == 1:  # 리뷰 경우의 수(5)
                break
                
            last_review = result[-1] if result else None
        
        if result:
            # 임시 데이터프레임 생성
            tmp2 = pd.DataFrame()
            tmp2['number'] = [number]*len(result)
            tmp2['Store'] = name*len(result)
            tmp2['Review_text'] = result
            tmp2['Time'] = time_list

            # 최종 데이터프레임(2)_리뷰
            time.sleep(random.uniform(1,2))
            review_df = pd.concat([review_df, tmp2])
    except:
        pass

    # [stpe4] 진행사항 체크(2)
    print(f"{number}번째 {name}상점에서 {len(result)}개의 리뷰를 수집했습니다.")

    time.sleep(random.uniform(1,2))
    try:
        i+=2
        number+=1
        next_element = driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{i}]/div/a')
        driver.execute_script("arguments[0].scrollIntoView(true);", next_element)
    except:
        break

# 문제는 에러 없어도 데이터를 봐야한다.
merged_df = pd.merge(info_df, review_df, on=["number"], how="outer")
