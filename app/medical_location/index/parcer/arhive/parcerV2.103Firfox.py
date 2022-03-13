from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnknownMethodException
from proxy_auth_data import login, password
import requests
import re
import json

import time

y = 200
p = 1
s = Service('/app/medical_location/index/driverfirfox/geckodriver')
options = webdriver.FirefoxOptions()

headers = "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

options.add_argument(headers)

url = ["https://www.103.ua/list/bolnicy/kiev",
       "https://www.103.ua/list/bolnicy/kiev/?page=2",
       "https://www.103.ua/list/bolnicy/dnepr",
       "https://www.103.ua/list/bolnicy/lvov",
       "https://www.103.ua/list/bolnicy/odessa",
       "https://www.103.ua/list/bolnicy/kharkov",
       "https://www.103.ua/list/bolnicy/kharkov/?page=2",
       ]

driver = webdriver.Firefox(
    service=s,
    options=options)

browser = webdriver.Firefox(
    service=s,
    options=options,
)
all_iteams = {
    "tilte": "",
    "address": "",
    "working_hours": "",
    "info": "",
    "phone_numb": [],
    "phone_title": [],
    "contact_title": [],
    "contact_link": [],
    "description_title": [],
    "description_info": [],
    "category_title": [],
    "category_price_title": [],
    "category_price": [],
    "completeName": [],
}

try:
    for urls in url:
        driver.get(url=urls)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 100)")
        time.sleep(1)
        cards = driver.find_elements(By.CLASS_NAME, "Place")  # нахожу все картачкаи и собираю в список
        for card in cards:
            print("Card number " + str(p))
            title = card.find_element(By.CLASS_NAME, "Place__title").text  # получяю назване больницы
            all_iteams["tilte"] = title
            print(title)
            address = card.find_element(By.CLASS_NAME, "Place__addressText").text  # получаю адресс
            all_iteams["address"] = address
            try:
                working_hours = card.find_element(By.CLASS_NAME, "Place__time").text  # получаю часы работы
                all_iteams["working_hours"] = working_hours
                info = card.find_element(By.CLASS_NAME,
                                         "AdvertMessage__text").text  # собираю доп информацию если она есть
                all_iteams["info"] = info
            except Exception as ex:
                working_hours = None  # если нкту инфорпации присваиваю нон
                all_iteams["working_hours"] = working_hours
                info = None  # если нкту инфорпации присваиваю нон
                all_iteams["info"] = info
            btn = card.find_element(By.CLASS_NAME, "Place__showContacts")
            btn.click()  # нахожу и прокликиваю кнопку для показа номера телефона
            time.sleep(2)
            contact_popup = driver.find_element(By.CLASS_NAME,
                                                "ContactsPopupWrapper")  # нахожу контейнер со всеми номерами
            all_phone = contact_popup.find_elements(By.CLASS_NAME,
                                                    "ContactsPopupPhones__item")  # собираю блоки с номерами в список
            time.sleep(2)
            for phones in all_phone:
                phone_numb = phones.find_element(By.CLASS_NAME,
                                                 "PhoneLink__number").text  # нахожу и получяю номер телефона
                all_iteams["phone_numb"].append(phone_numb)
                time.sleep(1)
                try:
                    phone_title = phones.find_element(By.CLASS_NAME,
                                                      "ContactsPopupPhones__description").text  # получяю подпись номера телефона
                    all_iteams["phone_title"].append(phone_title)
                except Exception as ex:
                    phone_title = None  # если подпись не найдена пишу нон
                    all_iteams["phone_title"].append(phone_title)
                time.sleep(1)
            button = driver.find_element(By.CLASS_NAME, "Popup__close").click()  # закрываю попап
            time.sleep(1)
            title_link = card.find_element(By.CLASS_NAME,
                                           "Place__wholeLink")  # получяю блок ссылкой на страницу карточки (кард детеил)
            try:
                url = title_link.get_attribute("href")  # получяю ссылку на страницу карточки (кард детеил)
                browser.get(url=url)  # открываю в новом окне
                time.sleep(5)
                b_title = browser.find_element(By.CLASS_NAME, "PersonalTitle__text").text
                contacts_link = browser.find_element(By.CLASS_NAME,
                                                     "AdditionalContacts")  # нахожу бдок с контактными ссылками
                contact_link_all = contacts_link.find_elements(By.CLASS_NAME,
                                                               "AdditionalContacts__button")  # собтраю их в список
                try:
                    for item in contact_link_all:
                        contact_title = item.get_attribute("title")  # нахожу название ссылки
                        all_iteams["contact_title"].append(contact_title)
                        contact_link = item.get_attribute("href")  # и саму ссылку
                        all_iteams["contact_link"].append(contact_link)
                except Exception as ex:
                    contact_title = None  # если нету пишу нон
                    all_iteams["contact_title"].append(contact_title)
                    contact_link = None  # если нету пишу нон
                    all_iteams["contact_link"].append(contact_link)

                description_conteiner = browser.find_element(By.CLASS_NAME,
                                                             "Features")  # пооучяю контейнер блока с описанием
                description_conteiner.find_element(By.CLASS_NAME, "ContentBox__footer")
                description_conteiner.find_element(By.CLASS_NAME, "ContentBox__showMore").click()
                time.sleep(1)
                description_all_item = description_conteiner.find_elements(By.CLASS_NAME,
                                                                           "Features__price")  # здесь получяю все элементы
                try:
                    for description_item in description_all_item:
                        all_iteams["its_for_desck"] = "True"
                        description_title = description_item.find_element(By.CLASS_NAME,
                                                                          "Features__itemTitle").text  # получяю название описания
                        all_iteams["description_title"].append(description_title)
                        description_info = description_item.find_element(By.CLASS_NAME,
                                                                         "Features__itemValue").text  # получяю описание
                        all_iteams["description_info"].append(description_info)
                except Exception as ex:
                    print("DESCRIPTION ERROR")

                map_location = browser.find_element(By.CLASS_NAME, "RouteMap__button")  # нахожу кнопку маршрут
                map_href = map_location.get_attribute("href")  # получяю гугл ссылку га раошрут
                all_iteams["map_href"] = map_href
                map_cordinate_date = re.search('=([0-9]?[0-9]\.[0-9]*),([0-9]?[0-9]\.[0-9]*)', map_href,
                                               re.DOTALL)  # ищю гироту и долготу
                latitude = map_cordinate_date.groups()[0]  # получяю долготу
                all_iteams["latitude"] = latitude
                longitude = map_cordinate_date.groups()[1]  # получяю широту
                all_iteams["longitude"] = longitude
                tabs_container = browser.find_element(By.CLASS_NAME, "NowrapList")
                tabs_button_all = tabs_container.find_elements(By.CLASS_NAME,
                                                        "PersonalTabs__item")  # нахожу контейнер с табами
                # проверяю ксли кнопка цены перехожу
                for tabs_button in tabs_button_all:
                    if tabs_button.text == "Цены":
                        tabs_button.click()
                        time.sleep(5)
                        all_price_container = browser.find_element(By.CLASS_NAME,
                                                                   "PersonalBody")  # получяю контейнер с категориями
                        all_price_list = all_price_container.find_elements(By.CLASS_NAME,
                                                                           "OffersAccordion__item")  # получяю список кптегорий
                        # прохожу по списку категорий
                        for price_item in all_price_list:
                            all_iteams["price"] = "True"
                            category_title = price_item.find_element(By.CLASS_NAME,
                                                                     "OffersAccordion__spoilerTitle").text  # получяю название категории
                            all_iteams["category_title"].append(category_title)
                            price_item.find_element(By.CLASS_NAME, "Button").click()  # разворачиваю список
                            time.sleep(5)
                            category_list = price_item.find_elements(By.CLASS_NAME,
                                                                     "PersonalOffers__item")  # и ищу все цены
                            # прохожусь по списку цен
                            for category_item in category_list:
                                category_price_title = category_item.find_element(By.CLASS_NAME,
                                                                                  "PersonalOffers__title ").text  # получяю название цены
                                all_iteams["category_price_title"].append(category_price_title)
                                category_price = category_item.find_element(By.CLASS_NAME,
                                                                            "PersonalOffers__price").text  # получяю саму цкну
                                all_iteams["category_price"].append(category_price)
                    elif tabs_button.text == None:
                        category_title = None
                        all_iteams["category_title"].append(category_title)
                        category_price_title = None
                        all_iteams["category_price_title"].append(category_price_title)
                        category_price = None
                        all_iteams["category_price"].append(category_price)
                # проверяю если кнопка Фотогалерея перехожу
                for tabs_button in tabs_button_all:
                    if tabs_button.text == "Фотогалерея":
                        tabs_button.click()
                        photo_list = browser.find_elements(By.CLASS_NAME,
                                                           "b-photos_items_all-photos_pic")  # получяю все елементы имг
                        for photo_item in photo_list:
                            photo_link = photo_item.get_attribute("src")  # получяю ссылку на картинку
                            photo_title = photo_link.split("/")[-1]  # вытягиваю название картинки
                            town_name = urls.split("/")[-1]
                            if town_name[0] == "?":
                                town_name = urls.split("/")[-2]
                            completeName = 'media/data/uploads/' + town_name + "/" + title + "/" + photo_title  # формирую путь гду будет храниться картинка
                            all_iteams["completeName"].append(completeName)
                            photo_data = requests.get(photo_link, headers=headers).content  # получяю картинку
                            with open(completeName, 'wb') as handler:
                                handler.write(photo_data)  # скамчиваю её
                    elif tabs_button.text == None:
                        photo = None
            except Exception as ex:
                print(ex)
            p += 1
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 200
            cards_lens = len(cards)
            with open('../../data.json', 'w') as fp:
                json.dump(all_iteams, fp)
            time.sleep(5)

            driver.close()
            browser.close()
        # here
        time.sleep(1)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
