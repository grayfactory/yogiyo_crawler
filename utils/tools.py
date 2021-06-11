import time
import pickle
from pathlib import PurePosixPath

from utils.connect import driver

# 위치 설정
def set_location(location):
    driver.find_element_by_css_selector('#search > div > form > input').click()
    driver.find_element_by_css_selector('#button_search_address > button.btn-search-location-cancel.btn-search-location.btn.btn-default > span').click()
    driver.find_element_by_css_selector('#search > div > form > input').send_keys(location)
    driver.find_element_by_css_selector('#button_search_address > button.btn.btn-default.ico-pick').click()
    time.sleep(2)
    # location 넣었을 경우 표시되는 주소들 중, 1번째 주소 클릭
    driver.find_element_by_css_selector('#search > div > form > ul.dropdown-menu.ng-scope.am-flip-x.bottom-left > li:nth-child(3) > a').click()
    
    # 로딩 대기 필요
    time.sleep(4)
    print(location+'으로 위치 설정 완료!')

# 이전 page로 돌아가기
def go_back_page():
    try :
        driver.execute_script("window.history.go(-1)")
        time.sleep(5)
    except Exception as e:
        print('페이지 돌아가기 오류',e)

# listed 음식점 검색
def search_restaurant(rest_title):
    # 찾기버튼
    btn = driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a')
    driver.execute_script('arguments[0].click();',btn)

    # fill-in form
    time.sleep(1)
    driver.find_element_by_css_selector('#category > ul > li.main-search > form > div > input').send_keys(rest_title)

    # 입력 버튼 클릭
    click_btn = driver.find_element_by_css_selector('#category_search_button')
    driver.execute_script('arguments[0].click();',click_btn)

    # 1개만 검색되었을 때 [1]는 xpath에 없지만, 넣어도 관계없이 찾아진다.
    time.sleep(3) # 로딩 대기
    # 첫 번째 검색 결과 클릭
    try :
        result = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div[1]/div')
    except :
        result = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div/div')
    finally :
        driver.execute_script('arguments[0].click();',result)

    time.sleep(2) # 클릭 후 로딩 대기

# # 클린리뷰 버튼 클릭
def open_review_page():
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
    time.sleep(2) # 클릭 후 로딩 대기

# 리뷰 more 버튼 클릭
def click_more_btn():
    try :
        driver.find_element_by_class_name('btn-more').click()
    except Exception as e:
        pass

# review, answer text 찾기
def get_review_answer(tag):
    try : 
        return tag.find_element_by_css_selector('div.review-answer.ng-scope > p').text
    except Exception as e:
        return None

# DataFrame 피클로 저장
def save_pickle(location, yogiyo_df):

    p = PurePosixPath(__file__)
    pickle_dir = str(p.parents[1])

    pickle.dump(yogiyo_df, open(f"{pickle_dir}/data/df_{location.replace(' ','_')}.pkl",'wb'))
    print(f'{pickle_dir} {location} pikcle save complete!')

