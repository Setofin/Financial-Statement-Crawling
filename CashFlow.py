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
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="a_change_en"]').click()
    time.sleep(3)
    bs_xpaths = {'//*[@id="table_bcdktbank"]/tbody': 'Bank', '//*[@id="table_bcdktck"]/tbody': 'Securities',
                 '//*[@id="table_bcdktbh"]/tbody': 'Insurance', '//*[@id="table_bcdkt"]/tbody': 'Others'}

    for xpath, type in bs_xpaths.items():
        try:
            fin_tr = driver.find_element_by_xpath(xpath)
            stock_type = type
            break
        except:
            continue

    if stock_type == 'Insurance':
        driver.find_element_by_xpath('//*[@id="analyze"]/div[4]/ul/li[3]').click()
    elif stock_type == 'Bank':
        driver.find_element_by_xpath('//*[@id="analyze"]/div[4]/ul/li[3]').click()
    else:
        driver.find_element_by_xpath('//*[@id="analyze"]/div[4]/ul/li[4]').click()
    time.sleep(3)
    cf_xpaths = {'//*[@id="table_lctttructiepbank"]/tbody': 'Bank',
                 '//*[@id="table_lctttgiantiepck"]/tbody': 'Securities',
                 '//*[@id="table_lctttructiepbaohiem"]/tbody': 'Insurance',
                 '//*[@id="table_lctttgiantiep"]/tbody': 'Others'}
    stock_data = pd.DataFrame()
    for i in range(2, 11):
        print('{}, {}'.format(ticker, i))
        try:
            driver.find_element_by_xpath('//*[@id="year"]/option[{}]'.format(i)).click()
            time.sleep(3)
            for xpath, type in cf_xpaths.items():
                try:
                    fin_tr = driver.find_element_by_xpath(xpath)
                    stock_type = type
                    break
                except:
                    continue
            tr_data = fin_tr.find_elements_by_tag_name('tr')
            row_data = list()
            for tr in tr_data:
                try:
                    driver.execute_script("arguments[0].setAttribute('class', 'l3 has-child expanded l3-first')", tr)
                except:
                    pass

                rows = tr.find_elements_by_tag_name('td')
                row_data.append([row.text for row in rows])
            if i <= 2:
                column_drops = [1]
            else:
                column_drops = [0, 1]

            stock_data = pd.concat([stock_data, pd.DataFrame(row_data).drop(columns=column_drops)], axis=1)
            time.sleep(1)
        except:
            continue
    print(stock_data.head(5))
    stock_data.to_csv('./Cashflow/{}/{}.csv'.format(stock_type, ticker), encoding='utf-8-sig')


failed = []
for code in code_data.Ticker.unique():
    try:
        load_page(code)
    except:
        failed.append(code)
        print('Failed', code)
print('Failed', failed)