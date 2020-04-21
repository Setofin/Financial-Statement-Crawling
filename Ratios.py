from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver_path = 'C:\ChromeDriver\chromedriver'
driver = webdriver.Chrome(driver_path)
code_data = pd.read_csv('./Code.csv', encoding="utf-8")

final = []


def load_page(ticker):
    stock_url = 'https://finance.tvsi.com.vn/Enterprises/FinancialStatements?symbol={}'.format(ticker)
    driver.get(stock_url)
    driver.find_element_by_id('a_change_en').click()
    time.sleep(4)
    driver.find_element_by_xpath('//*[@id="analyze"]/div[4]/ul/li[6]/a').click()
    time.sleep(3)

    stock_data = pd.DataFrame()
    stock_type = 'OTHERS'
    xpaths = {'//*[@id="table_cttcbank"]/tbody': 'BANK', '//*[@id="table_cttc"]/tbody': 'OTHERS'}
    for i in range(1, 11):
        try:
            print('{}, {}'.format(ticker, i))
            driver.find_element_by_xpath('//*[@id="year"]/option[{}]'.format(i)).click()
            time.sleep(4)
            for xpath, type in xpaths.items():
                try:
                    body = driver.find_element_by_xpath(xpath)
                    stock_type = type
                    break
                except:
                    continue

            rows = body.find_elements_by_tag_name('tr')
            time.sleep(4)
            data = list()
            for row in rows:
                td_rows = row.find_elements_by_tag_name('td')
                data.append([td.text for td in td_rows])
            if i <= 1:
                column_drops = [1]
            else:
                column_drops = [0, 1]
            stock_data = pd.concat([stock_data, pd.DataFrame(data).drop(columns=column_drops)], axis=1)
            time.sleep(1)
        except:
            continue

    stock_data = stock_data.set_index(0)
    print(stock_data.head())
    stock_data = stock_data.dropna(how='all')
    stock_data.to_csv('./Ratios/{}/{}.csv'.format(stock_type, ticker))


final_data = pd.DataFrame()

crawled_shit = []
failed = []
next = True
for code in code_data.Ticker.unique():
    if next:
        try:
            load_page(code)
        except:
            failed.append(code)
            print(
                '{} Failed!-------------------------------------------------------------------------------------------'.format(
                    code))
            continue

print('Failure', failed)
