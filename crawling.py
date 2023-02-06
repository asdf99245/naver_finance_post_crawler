from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument('headless')
options.add_argument('no-sandbox')
options.add_argument("disable-infobars")
options.add_argument("disable-dev-shm-usage")
options.add_argument("disable-browser-side-navigation")
options.add_argument("disable-gpu")
options.add_argument("lang=ko_KR")
options.add_argument('--blink-settings=imagesEnabled=false')

now = datetime.now()
TIME_LIMIT = 3
headers = {'User-Agent': user_agent}


def generate_excel(df, path):
    date_string = datetime.today().strftime("%Y%m%d_%H_%M_%S")
    df.to_excel(excel_writer=path + date_string + ".xlsx", index=False)


def get_time_diff(date):
    target = datetime.strptime(date, "%Y.%m.%d")
    diff = now - target

    return diff.days


def crawler(name, code, keyword):
    result_df = pd.DataFrame([])

    driver = webdriver.Chrome(options=options,
                              executable_path='C:/Users/정윤규/AppData/Local/Programs/Python/chromedriver.exe')
    driver.get('https://finance.naver.com/item/board.naver?code=%s&page=1' % code)
    driver.implicitly_wait(1)

    search_bar = driver.find_element(by=By.XPATH, value='/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/table[3]/tbody/tr/td/input[2]')
    search_bar.clear()
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.ENTER)

    search_url = driver.current_url

    driver.close()
    page = 0
    while True:
        page += 1

        url = search_url + '&page=%s' % (str(page))

        html = requests.get(url, headers=headers).content
        soup = BeautifulSoup(html.decode('euc-kr', 'replace'), 'html.parser')
        table = soup.find('table', {'class': 'type2'})
        rows = table.select('tbody > tr')

        flag = False

        for i in range(2, len(rows)):
            if len(rows[i].select('td > span')) > 0:
                flag = True

                date = rows[i].select('td > span')[0].text
                title = rows[i].select('td.title > a')[0]['title']
                link = rows[i].select('td.title > a')[0]['href']

                if keyword not in title:
                    continue

                if get_time_diff(date[0:10]) > TIME_LIMIT:
                    return result_df

                table = pd.DataFrame({'종목명': [name], '날짜': [date], '제목': [title], '링크': [link]})
                result_df = result_df.append(table)

        if not flag:
            break

    return result_df


def crawling_all(keyword, path):
    result_df = pd.DataFrame([])

    for page in range(1, 2):
        url = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page=%s' % (str(page))
        html = requests.get(url, headers=headers).content
        soup = BeautifulSoup(html.decode('euc-kr', 'replace'), 'html.parser')
        table = soup.find('table', {'class': 'type_2'})
        rows = table.select('tbody > tr')

        for i in range(0, 2):
            td = rows[i].select('td.center > a')
            if len(td) > 0:
                title = rows[i].select('td > a')[0].text
                link = td[0]['href']
                code = link.split('code=')[1]

                print(title + ' 종목 토론방 크롤링')
                print('====================== 크롤링 시작 ======================')
                result_df = result_df.append(crawler(title, code, keyword))
                print('====================== 크롤링 종료 ======================')

    generate_excel(result_df, path)
    # print(result_df)