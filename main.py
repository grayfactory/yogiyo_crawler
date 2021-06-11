import pandas as pd
import time
import re
from tqdm import tqdm

from utils.tools import *
from utils.scroll_func import *
from utils.connect import driver

def filtered_by_review_ratio(rest_tag):
    # 리뷰 + 사장님 댓글 text 찾기
    regex = re.compile(r'([리뷰]+\s)([0-9]+).([사장님댓글]+\s)([0-9]+)')
    rest_title = []
    for tag in rest_tag:
        reviews = regex.findall(tag.text)

        if reviews:
            ratio = int(reviews[0][-1]) / int(reviews[0][1])

            # 사장님 댓글이 충분히 달린 title만 저장
            if ratio >= 0.8:
                # title 찾기
                title = re.findall(r'^.+\n',tag.text)
                inservice = re.findall(r'^[현재 요기요]+\n',tag.text)
                # 서비스중인곳만
                if len(inservice)==0:
                    rest_title.append(title[0].replace('\n',''))
    
    return rest_title


# main function
def review_crawling(locations):
    
    for loc in locations:
        df = pd.DataFrame(columns=['restaurant','review','answer',
                                       'total','taste','quantity','delivery','location'])
        
        try :
            set_location(loc)
        except Exception as e:
            print(f'{loc} 위치설정 오류',e)
            continue

        try :
            rest_tag = scroll_to_end() # 끝까지 스크롤 & element return
            # rest_tag = scroll_to_end_test()
        except Exception as e:
            print(f'{loc} 스크롤 내리기 오류',e)
            go_back_page()
            continue
            
        rest_titles = filtered_by_review_ratio(rest_tag) # 리뷰&응답 비율로 filter
        print(f'{loc} - {len(rest_titles)}개 음식점 filtered\n')

        # in Loc, 개별 식당 iteration
        for title in tqdm(rest_titles): # test

            try :
                search_restaurant(title)
            except Exception as e:
                print(f'{loc} {title} 검색오류',e)
                go_back_page() # 이전 page, 다음 음식점 검색
                continue
            
            try :
                open_review_page()
                review_tags = open_review_page_to_end()
            except Exception as e:
                print(f'{loc} {title} 리뷰페이지 open 오류',e)
                continue
                
            # in 식당, review iteration
            for tag in review_tags[1:]: # 0번째는 넘겨야함
                try :
                    df.loc[len(df)] = {
                          'restaurant' : title
                        , 'review'     : tag.find_element_by_tag_name('p').text
                        , 'total'      : len(tag.find_element_by_css_selector('div > span.total').text)
                        , 'taste'      : tag.find_element_by_css_selector('div > span.category > span:nth-child(3)').text
                        , 'quantity'   : tag.find_element_by_css_selector('div > span.category > span:nth-child(6)').text
                        , 'delivery'   : tag.find_element_by_css_selector('div > span.category > span:nth-child(9)').text
                        , 'answer'     : get_review_answer(tag)
                        , 'location'   : loc
                    }
                except Exception as e:
                    # print(f'{loc} {title} 리뷰 저장 오류 ')
                    continue
            
            go_back_page() # 이전 page, 다음 음식점 검색

        save_pickle(loc, df)
        
        go_back_page() # 다음 location: dong

if __name__ == "__main__" :

    gu = '강남구'
    # dong = ['일원동','역삼동']
    # dong = ['삼성동','수서동']
    dong = ['수서동','대치동','신사동']
    # ,'개포동','청담동','삼성동','대치동','신사동','논현동',
                #  '압구정동','세곡동','자곡동','율현동','수서동','도곡동']
    locations = [' '.join([gu, d]) for d in dong]

    review_crawling(locations)

    driver.close()
    driver.quit()

