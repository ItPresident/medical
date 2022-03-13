from bs4 import BeautifulSoup
from django.shortcuts import render
from progress.bar import ChargingBar
import requests
import os.path
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}  # заголовки для доступа на сайт


def get_page():
    responce = requests.get(
        'https://www.103.ua/list/bolnicy/kiev/?utm_source=google&utm_medium=cpc&utm_campaign=poisk_medicinskie_centri&utm_content=adaptiv_bolnici_obschie_gosudarstvennie_113243956701_497563882507&utm_term=%D0%B1%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D1%8B%20%D0%BA%D0%B8%D0%B5%D0%B2%D0%B0',
        headers=headers)
    result = responce.text
    soup = BeautifulSoup(result, 'lxml')
    return soup


def get_pagenite():
    soup = get_page()
    page_nav_list = []
    page_nav = soup.find(class_='Pagination__listPages').find_all('a')
    for pagenate in page_nav:
        page_nav_list.append(
            "https://www.103.ua/list/bolnicy/kiev/?utm_source=google&utm_medium=cpc&utm_campaign=poisk_medicinskie_centri&utm_content=adaptiv_bolnici_obschie_gosudarstvennie_113243956701_497563882507&utm_term=%D0%B1%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D1%86%D1%8B%20%D0%BA%D0%B8%D0%B5%D0%B2%D0%B0&page=" + pagenate.text)
    return page_nav_list


def get_card():
    title = []
    address = []
    info = []
    img = []
    link = []
    working_hours = []
    all_items = []

    pagenite_urls = get_pagenite()
    bar = ChargingBar('Parce Card ', max=len(pagenite_urls))
    for urels_page in pagenite_urls:
        responce = requests.get(urels_page, headers=headers)
        result = responce.text
        soup_result = BeautifulSoup(result, 'lxml')
        page = soup_result.find(class_="PlaceList")

        find_description = soup_result.find_all(class_="td-excerpt")
        find_date = soup_result.find_all(class_="td-module-meta-info")
        # for item in page:
        #     card = page.find(class_="Place")
        #     title_f = card.find(class_="Place__mainTitle")
        #     title.append(title_f.text)

        #     link.append(item.a.get('href'))
        #     urls = item.img.get('src')
        #     lik_split = str(urls)
        #     img_data = requests.get(urls, headers=headers).content
        #     filename = lik_split.split("/")[-1]
        #     completeName = 'media/data/uploads/news' + filename
        #     with open(completeName, 'wb') as handler:
        #         handler.write(img_data)
        #     # path = completeName
        #     img.append(completeName)
        # for item_d in find_description:
        #     description.append(item_d.text)
        # for item_date in find_date:
        #     date.append(item_date.text)
        #     all_items = [title, link, description, date, img]
        bar.next()
        time.sleep(.1)
    bar.finish()
    return page


print(get_card())
