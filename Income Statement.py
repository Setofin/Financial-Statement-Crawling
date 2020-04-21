from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver_path = 'C:\ChromeDriver\chromedriver'
driver = webdriver.Chrome(driver_path)
code_data = pd.read_csv('./Code.csv', encoding="utf-8")


def load_page(ticker):
    stock_url = 'https://finance.tvsi.com.vn/Enterprises/FinancialStatements?symbol={}'.format(ticker)
    driver.get(stock_url)
    driver.find_element_by_id('a_change_en').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="analyze"]/div[4]/ul/li[2]').click()
    time.sleep(3)
    xpaths = {'//*[@id="table_bckqkdbank"]/tbody': 'Bank', '//*[@id="table_bckqkdck"]/tbody': 'Securities',
              '//*[@id="table_bckqkdbh"]/tbody': 'Insurance', '//*[@id="table_bckqkd"]/tbody': 'Others'}

    stock_data = pd.DataFrame()
    stock_type = 'Others'
    for i in range(1, 11):
        print('{}, {}'.format(ticker, i))
        try:
            driver.find_element_by_xpath('//*[@id="year"]/option[{}]'.format(i)).click()
            time.sleep(3)

            for xpath, type in xpaths.items():
                try:
                    fin_tr = driver.find_element_by_xpath(xpath)
                    stock_type = type
                    break
                except:
                    continue

            tr_data = fin_tr.find_elements_by_tag_name('tr')
            row_data = []
            if i <= 1:
                column_drops = [1]
            else:
                column_drops = [0, 1]
            for tr in tr_data:
                rows = tr.find_elements_by_tag_name('td')
                row_data.append([row.text for row in rows])
            stock_data = pd.concat([stock_data, pd.DataFrame(row_data).drop(columns=column_drops)], axis=1)
            time.sleep(1)
        except:
            continue
    stock_data.to_csv('./Income/{}/{}.csv'.format(stock_type, ticker), encoding='utf-8-sig')


next = True
failed = []
for code in code_data.Ticker.unique():
    if next:
        try:
            load_page(code)
        except:
            print(
                '{} Failed!-------------------------------------------------------------------------------------------'.format(
                    code))
            failed.append(code)
            continue
print('Failed', failed)