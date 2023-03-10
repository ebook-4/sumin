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
        if li[i].text != '' :
            categories.append(li[i].text)

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
        contents = driver.find_elements(By.CSS_SELECTOR, '.prodDt_detail')

        # 상세페이지 주소를 통한 isbn
        for link in data :
            detail = link.select_one('strong h3 a').attrs['href']
            driver2.get(detail)
            isbn = driver2.find_elements(By.CSS_SELECTOR, '.prod_pordInfo_box em')[1].text
            isbns.append(isbn)

        # 전체 목록에서 그 외 정보 추출
        for content in contents :
            title = content.find_element(By.CSS_SELECTOR, 'strong h3').text
            author = content.find_element(By.CSS_SELECTOR, '.prodDt_info').text.split(' ')[0]
            price = content.find_element(By.CSS_SELECTOR, '.prodDt_price b').text
            try :
                star = content.find_element(By.CSS_SELECTOR, '.prodDt_review b').text
            except :
                star = "0.0"
            books.append([title, author, price, star, category])

        # 다음 페이지 이동
        driver.find_element(By.CSS_SELECTOR, '.btn_page.next').click()


# 데이터 프레임 생성
df = pd.DataFrame(columns=['ISBN', 'title', 'author', 'price', 'star', 'category'])

for i in range(len(isbns)) :
    df.loc[i] = {
        "ISBN" : isbns[i],
        "title" : books[i][0],
        "author" : books[i][1],
        "price" : books[i][2],
        "star" : books[i][3],
        "category" : books[i][4]
    }

df.to_csv('kyobo.csv', index=False, encoding='cp949')
