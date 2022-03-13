from bs4 import BeautifulSoup
from progress.bar import ChargingBar
from django.shortcuts import render
from app.medical_location.index.models import News
from PIL import Image
import requests
import os.path
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'}  # заголовки для доступа на сайт


# получаем данные с первой страници
def get_page():
    responce = requests.get('https://hub.packtpub.com/tag/python/', headers=headers)
    result = responce.text
    soup = BeautifulSoup(result, 'lxml')
    return soup


# находим блок пагинации и формеруем список всех странниц
def get_pagenite():
    soup = get_page()
    page_nav_list = []
    urels_page = []
    page_nav = soup.find(class_='page-nav td-pb-padding-side').find_all('a')
    for page_nav_item in page_nav:
        page_nav_list.append(page_nav_item.get('title'))
    page_number = int(page_nav_list[-2]) + 1
    bar = ChargingBar('Get pagenite ', max=page_number - 1)
    for page_number in range(1, page_number):
        urels = f'https://hub.packtpub.com/tag/python/page/{page_number}/'
        urels_page.append(urels)
        time.sleep(.1)
    bar.finish()
    return urels_page


# print(news_card())

# проходим по каждой странице и парсим нужные нам данные и добавляем их в список
def get_news():
    title = []
    date = []
    description = []
    img = []
    link = []
    all_items = []
    pagenite_urls = get_pagenite()
    bar = ChargingBar('Parce News ', max=len(pagenite_urls))
    for urels_page in pagenite_urls:
        responce = requests.get(urels_page, headers=headers)
        result = responce.text
        soup_result = BeautifulSoup(result, 'lxml')
        page = soup_result.find_all(class_="td-block-span6")
        find_description = soup_result.find_all(class_="td-excerpt")
        find_date = soup_result.find_all(class_="td-module-meta-info")
        for item in page:
            title.append(item.h3.text)
            link.append(item.a.get('href'))
            urls = item.img.get('src')
            lik_split = str(urls)
            img_data = requests.get(urls, headers=headers).content
            filename = lik_split.split("/")[-1]
            completeName = 'media/data/uploads/news' + filename
            with open(completeName, 'wb') as handler:
                handler.write(img_data)
            # path = completeName
            img.append(completeName)
        for item_d in find_description:
            description.append(item_d.text)
        for item_date in find_date:
            date.append(item_date.text)
            all_items = [title, link, description, date, img]
        bar.next()
        time.sleep(.1)
    bar.finish()
    return all_items


def save_news(request):
    news = get_news()
    print("Len News", len(news))
    print("Len title", len(news[0]))
    bar = ChargingBar('Save in db ', max=len(news[0]))
    iter_it = range(0, len(news[0]))
    title = news[0]
    date = news[3]
    desc = news[2]
    img = news[4]
    link = news[1]
    count = 0
    for i in iter_it:
        news_model = News()
        news_model.title = title[count]
        news_model.post_date = date[count]
        news_model.description = desc[count]
        news_model.image = img[count]
        news_model.news_link = link[count]
        news_model.save()
        bar.next()
        time.sleep(.1)
        count += 1
    bar.finish()

    return render(request, "news/parce-sucses.html", )
# render(request, "news/parce-sucses.html")
# скачиваем изображения и добавляем путь к изображению в список
# def image_path():
#     url_img = get_news()
#     image_links = []
#     bar = ChargingBar('Download img ', max=len(url_img[4]))
#     for urls in url_img[4]:
#         lik_split = str(urls)
#         img_data = requests.get(urls, headers=headers).content
#         filename = lik_split.split("/")[-1]
#         completeName = os.path.join('../image/uploads/news', filename)
#         news_model.image = img_data
#
#         # with open(completeName, 'wb') as handler:
#         #     handler.write(img_data)
#         path = os.path.abspath(completeName)
#         # image_links.append(path)
#         time.sleep(.1)
#
#     bar.finish()
#     return image_links
#
#
# page_info = image_path()
