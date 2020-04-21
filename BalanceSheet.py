from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

driver_path = 'C:\ChromeDriver\chromedriver'
driver = webdriver.Chrome(driver_path)
code_data = pd.read_csv('./Code.csv', encoding="utf-8")


def crawling(ticker):
    stock_type = 'Others'
    stock_url = 'https://finance.vietstock.vn/{}/financials.htm?tab=CDKT&languageid=2'.format(ticker)
    driver.get(stock_url)
    time.sleep(3)
    header = driver.find_element_by_xpath('//*[@id="finance-content"]/div/div/div[4]/div/table/thead')
    body = driver.find_element_by_xpath('//*[@id="finance-content"]/div/div/div[4]/div/table/tbody')

    stock_data = []
    tr_header = header.find_element_by_tag_name('tr')
    th_header = tr_header.find_elements_by_tag_name('th')
    stock_data.append([th.text for th in th_header])

    tr_body = body.find_elements_by_tag_name('tr')
    for tr in tr_body:
        tds = tr.find_elements_by_tag_name('td')
        stock_data.append([td.text for td in tds])
    print(pd.DataFrame(stock_data))
    pd.DataFrame(stock_data).to_csv('./Balance/{}/{}.csv'.format(stock_type, ticker), encoding='utf-8-sig')


def load_page(ticker):
    stock_url = 'https://finance.tvsi.com.vn/Enterprises/FinancialStatements?symbol={}'.format(ticker)
    driver.get(stock_url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="a_change_en"]').click()
    time.sleep(3)
    xpaths = {'//*[@id="table_bcdktbank"]/tbody': 'Bank', '//*[@id="table_bcdktck"]/tbody': 'Securities',
              '//*[@id="table_bcdktbh"]/tbody': 'Insurance', '//*[@id="table_bcdkt"]/tbody': 'Others'}

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
            row_data = list()
            for tr in tr_data:
                try:
                    driver.execute_script("arguments[0].setAttribute('class', 'l3 has-child expanded l3-first')", tr)
                except:
                    pass

                rows = tr.find_elements_by_tag_name('td')
                row_text = []
                selections = ['DIV', 'INNER']
                for row in rows:
                    for selection in selections:
                        if not row.text:
                            if selection == 'DIV':
                                try:
                                    label = row.find_element_by_class_name('label').text
                                    row_text.append(label)
                                    break
                                except:
                                    continue
                            elif selection == 'INNER':
                                try:
                                    label = row.find_element_by_class_name('label')
                                    inner_label = label.find_element_by_class_name('label').text
                                    row_text.append(inner_label)
                                    break
                                except:
                                    continue

                    row_text.append(row.text)
                row_data.append(row_text)
            if i <= 1:
                column_drops = [1]
            else:
                column_drops = [0, 1]

            stock_data = pd.concat([stock_data, pd.DataFrame(row_data).drop(columns=column_drops)], axis=1)
            time.sleep(1)
        except:
            continue
    print(stock_data.head(5))
    stock_data.to_csv('./Balance/{}/{}.csv'.format(stock_type, ticker), encoding='utf-8-sig')


next = True
crawled_shit = []
failed = []
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