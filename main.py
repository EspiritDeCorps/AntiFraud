from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import csv

chrome_options = Options()
driver = webdriver.Chrome(executable_path='drivers/chromedriver', options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(5)

"""
Заходим на сайт и по XPATH ищем кнопку и переходим по ней
Cookie файлы удалятся, что бы сервер не блокировал запросы
"""
driver.get("https://www.nseindia.com/")
link = driver.find_element_by_xpath('//*[@id="main_navbar"]/ul/li[3]/div/div[1]/div/div[1]/ul/li[1]/a').get_attribute(
    "href")
driver.delete_all_cookies()
driver.get(link)

"""
Ждём когда загрузится  таблица, после берем данные и записываем их в файл
"""


table = driver.find_element_by_xpath('//*[@id="livePreTable"]/tbody')
time.sleep(3)
with open("market.csv", "w") as file:
    writer = csv.writer(file, delimiter=";")

    for row in table.find_elements_by_xpath('./tr'):
        row = row.text.split()
        writer.writerow([row[0], row[2]])

"""
Возвращаемся на главную находим координаты графика и JS кодом спускаемся до него
"""
driver.delete_all_cookies()
driver.get("https://www.nseindia.com/")

schedule = driver.find_element_by_xpath('//*[@id="nse-indices"]/div[2]/div/div/nav')
driver.execute_script("window.scrollTo(0, {})".format(schedule.location["y"] - 150))

"""
Выбираем график "NIFTY BANK"
"""
button = driver.find_element_by_xpath('//*[@id="nse-indices"]/div[2]/div/div/nav/div/div/a[4]')
driver.execute_script("arguments[0].click();", button)
"""
Находим кнопку "View all" и переходим по ней
"""
button = driver.find_element_by_xpath('//*[@id="tab4_gainers_loosers"]/div[3]/a')
driver.delete_all_cookies()
driver.execute_script("arguments[0].click();", button)
"""
Ожидаем загрузку select'а и похже выбираем в нём требуемый пункт
"""

selectBank = driver.find_element_by_xpath('//*[@id="equitieStockSelect"]')
select = Select(selectBank)
select.select_by_visible_text("NIFTY ALPHA 50")
