from selenium import webdriver
from pathlib import PurePosixPath


p = PurePosixPath(__file__)
print('*****'*3,'init connection')
chromedriver = str(p.parents[0])+'/chromedriver'

# background 실행
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")
options.add_argument("--disable-gpu")
options.add_argument("lang=ko_KR")

options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")


driver = webdriver.Chrome(chromedriver, options=options)
# driver = webdriver.Chrome(chromedriver)
# driver.implicitly_wait(3) # 전역에서 3초 기다림
print('*****'*3,'connected')
url = 'https://www.yogiyo.co.kr'
driver.get(url)
