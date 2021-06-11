import time
import re

from utils.connect import driver
from utils.tools import click_more_btn

def scroll_to_end():
    # 알고리즘 수정 -> 현재 요기요에서 서비스 되지 않는 음식점은 검색이 되지 않음. 굳이 최하단까지 내려갈 필요가 없음
    
    flag = True
    # first 로딩 page 음식점 수
    rest_tag = driver.find_elements_by_class_name("col-sm-6")
    
    while flag :
        # 최하단으로
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3) # 로딩대기

        re_tag = driver.find_elements_by_class_name("col-sm-6")
        
        if len(rest_tag) < len(re_tag):
            flag = True
            rest_tag = re_tag
        else :
            flag = False
            
        title = re.findall(r'^[현재 요기요]+\n',re_tag[-1].text)
        # 현재 요기요 서비스가 제공되지 않습니다 text 매칭 stop
        if title:
            flag = False

    # 마지막 스크롤 지점에서 모든 element return 
    print('*** Scroll reach to end!')
    return rest_tag

def scroll_to_end_test():
    # 알고리즘 수정 -> 현재 요기요에서 서비스 되지 않는 음식점은 검색이 되지 않음. 굳이 최하단까지 내려갈 필요가 없음
    
    # first 로딩 page 음식점 수
    rest_tag = driver.find_elements_by_class_name("col-sm-6")
    
    # 마지막 스크롤 지점에서 모든 element return 
    print('*** Scroll reach to end!')
    return rest_tag
    
# def open_review_page_to_end():
    
#     flag = True
#     while flag:
#         try :
#             driver.find_element_by_class_name('btn-more.ng-hide')
#             print(' findmore'*10)
#         except :
#             click_more_btn()
#             # time.sleep(0.5)
#         else :
#             review_tags = driver.find_elements_by_class_name("list-group-item")
#             flag = False
#             return review_tags

def open_review_page_to_end():
    
    flag = True
    clicker = 0
    print('*** Now loading review pages')
    while flag:

        clicker += 1
        try :
            driver.find_element_by_class_name('btn-more.ng-hide')
        except :
            click_more_btn() # 광클
            time.sleep(0.1)
            # print(' findmore'*10)
            if clicker % 200 == 0:
                print(f'*** {clicker}회 review page  scrolling..')
            if clicker > 10000:
                flag = False
                review_tags = driver.find_elements_by_class_name("list-group-item")
                return review_tags
        else :
            review_tags = driver.find_elements_by_class_name("list-group-item")
            flag = False
            print(f'*** Review page scrolling 완료 ({clicker}회 반복) {len(review_tags)}개 review scrap!')
            return review_tags

            