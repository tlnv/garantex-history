from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from itertools import zip_longest
from pprint import pprint
import schedule


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


def observe():
    chrome_options = Options()
    chrome_options.add_argument(
        '--user-data-dir=C:\\Users\\tlnv\\AppData\\Local\\Google\\Chrome\\User Data\\')  # отдаем Селениуму параметры браузера, в которых вход в garantex уже произведен
    chrome_options.add_argument('--profile-directory=Profile 1')
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)  # запускаем браузер
    driver.get("https://garantex.io/deals")  # идем на нужню страницу
    sleep(3)  # ждем пока сайт считает слепок браузера
    html_page = driver.page_source
    driver.close()
    soup = BeautifulSoup(html_page, 'html.parser')
    tables = soup.find_all(
        "table", class_="table table-condensed table-striped")
    statuses = "active", "succeeded", "canceled"
    deals = {}
    for (status, table) in zip_longest(statuses, tables):
        deals[status] = get_deals(table)
    pprint(deals)


def main():
    schedule.every(2).minutes.do(observe)
    while True:
        schedule.run_pending()
        sleep(1)


main()
