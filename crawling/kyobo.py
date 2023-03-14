import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("C:\\Users\\iris8\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver2 = webdriver.Chrome("C:\\Users\\iris8\\Downloads\\chromedriver_win32\\chromedriver.exe")


driver.get("https://ebook.kyobobook.co.kr/dig/pnd/showcase?pageNo=323&cmdt=EBK&clst1=01&clst2=&clst3=&landing=Y")


# 카테고리 추출
driver.find_elements(By.CSS_SELECTOR, '.btn_sub_depth')[1].click()
time.sleep(2)
datas = driver.find_elements(By.CSS_SELECTOR, '.sub_depth_box')


categories = []

for data in datas :
    li = data.find_elements(By.CSS_SELECTOR, '.sub_depth_list a')
    for i in range(len(li)) :
        if li[i].text != '' and li[i].text != '섹슈얼로맨스' and li[i].text != '웹툰':
            categories.append(li[i].text)

# for i in range(len(categories)) :
#     print(categories[i])


isbns = []
books = []

# 카테고리 별
for category in categories :
    driver.find_elements(By.CSS_SELECTOR, '.btn_sub_depth')[1].click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, category).click()


    # 10페이지 씩
    for i in range(2, 11) :
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        data = soup.select('.prodDt_detail')
        contents = driver.find_elements(By.CSS_SELECTOR, '.prodDt')

        # 상세페이지 주소를 통한 isbn
        for link in data :
            try :
                detail = link.select_one('strong h3 a').attrs['href']
                driver2.get(detail)
                isbn = driver2.find_elements(By.CSS_SELECTOR, '.prod_pordInfo_box em')[1].text
                isbns.append(isbn)
            except :
                isbns.append('0000000000000')

        # 전체 목록에서 그 외 정보 추출
        for content in contents :
            img = content.find_element(By.CSS_SELECTOR, '.prodDt_cover img').get_attribute('src')
            title = content.find_element(By.CSS_SELECTOR, '.prodDt_detail strong h3').text
            author = content.find_element(By.CSS_SELECTOR, '.prodDt_detail .prodDt_info').text.split(' ')[0]
            price = content.find_element(By.CSS_SELECTOR, '.prodDt_detail .prodDt_price b').text
            try :
                star = content.find_element(By.CSS_SELECTOR, '.prodDt_detail .prodDt_review b').text
            except :
                star = "0.0"
            books.append([title, author, price, star, category, img])

        # 다음 페이지 이동
        driver.execute_script('window.scrollTo(0,100000000)')
        driver.find_element(By.CSS_SELECTOR, '.btn_page.next').click()


# # 데이터 프레임 생성
# df = pd.DataFrame(columns=['ISBN', 'title', 'author', 'price', 'star', 'category', 'img'])

# for i in range(len(isbns)) :
#     df.loc[i] = {
#         "ISBN" : isbns[i],
#         "title" : books[i][0],
#         "author" : books[i][1],
#         "price" : books[i][2],
#         "star" : books[i][3],
#         "category" : books[i][4],
#         "img" : books[i][5],
#     }

# df.to_csv('kyobo.csv', index=False, encoding='cp949')
