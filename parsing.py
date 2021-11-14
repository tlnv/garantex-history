from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from itertools import zip_longest
import os


CHROME_DIR = "C:\\Users\\tlnv\\AppData\\Local\\Google\\Chrome\\User Data\\"
USER_PROFILE = 'Default'


def get_deals(table):
    table_body = table.find("tbody")
    deals = table_body.find_all("tr")
    deals_details = {}
    for deal in deals:
        deal_details = deal.find_all("td")
        deals_details[deal_details[0].text.replace("#", "")] = {
            "datetime": deal_details[1].text,
            "seller": deal_details[2].text,
            "buyer": deal_details[3].text,
            "status": deal_details[4].text,
            "money": deal_details[5].text,
            "payment_method": deal_details[6].text,
            "cost": deal_details[7].text,
            "comission": deal_details[8].text,
            "final_cost": deal_details[9].text
        }
    return deals_details


def clear_history():
    os.remove(f"{CHROME_DIR}\\{USER_PROFILE}\\History")


def observe():
    chrome_options = Options()
    # отдаем Селениуму параметры браузера, в которых вход в garantex уже произведен
    chrome_options.add_argument(f'--user-data-dir={CHROME_DIR}')
    chrome_options.add_argument(f'--profile-directory={USER_PROFILE}')
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)  # запускаем браузер
    driver.get("https://garantex.io")
    try:
        login_button = driver.find_element_by_link_text("Вход")
        login_button.click()
    except:
        pass
    sleep(3)  # ждем пока сайт считает слепок браузера
    driver.get("https://garantex.io/deals")
    html_page = driver.page_source
    driver.close()
    soup = BeautifulSoup(html_page, 'html.parser')
    tables = soup.find_all(
        "table", class_="table table-condensed table-striped")  # читаем таблицы активных, завершеных и отмененных сделок
    statuses = "active", "succeeded", "canceled"
    formed_deals = {}
    for (status, table) in zip_longest(statuses, tables):
        formed_deals[status] = get_deals(table)
    return formed_deals
