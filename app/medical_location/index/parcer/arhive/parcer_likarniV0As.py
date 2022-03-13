from bs4 import BeautifulSoup
from progress.bar import ChargingBar
import json
import requests
import time
from datetime import datetime
import traceback
import os
import asyncio
import aiohttp

start_time = time.time()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}  # заголовки для доступа на сайт

main_url = "https://likarni.com"


def get_index_page():
    responce = requests.get(url=main_url, headers=headers)
    result = responce.text
    soup = BeautifulSoup(result, 'lxml')
    return soup


def get_town():
    dict_town = {

    }
    page = get_index_page()
    city_list = page.find(class_="city_list").find_all("li")
    for city in city_list:
        dict_town[city.a.text] = {}
        city_link = city.a.get("href")
        if city_link != "#":
            dict_town[city.a.text].update({
                "link": main_url + city.a.get("href")
            }
            )
        else:
            dict_town[city.a.text].update({
                "link": main_url + city.a.get("data-href")
            }
            )
    with open('../../../media/data/licarni_town.json', 'w', encoding='utf-8') as fp:
        json.dump(dict_town, fp, ensure_ascii=False)
    return "Finish"


def get_categories_doctor():
    town_list = get_town()
    dict_categories = {
        "categories_name": "",
    }
    page = get_index_page()
    categories_kliniki = page.find(class_='categories_kliniki')
    title = categories_kliniki.find('h2').text
    dict_categories["categories_name"] = title
    all_categories = categories_kliniki.find_all("li")
    for cat_item in all_categories:
        categories_name = cat_item.a.text
        categories_item_link = cat_item.a.get('href')
        link_name = categories_item_link
        categories_min_price_lable = cat_item.find(class_="consult_specialist_label").text
        categories_min_price_cost = cat_item.find(class_="consult_specialist_cost").text
        dict_categories[categories_name] = {}
        dict_categories[categories_name].update(
            {
                "name": categories_name,
                "link": link_name,
                "mini_price_lable": categories_min_price_lable,
                "mini_price_cost": categories_min_price_cost
            }
        )
    with open('../../data/dataL.json', 'w', encoding='utf-8') as fp:
        json.dump(dict_categories, fp, ensure_ascii=False)
    return "END kliniki"


def get_categories_diagnostic():
    dict_categories = {
        "categories_name": "",
    }
    page = get_index_page()
    categories_kliniki = page.find(class_='categories_diagnostic')
    title = categories_kliniki.find('h2').text
    dict_categories["categories_name"] = title
    all_categories = categories_kliniki.find_all(class_="category_item")
    for cat_box in all_categories:
        category_title = cat_box.find(class_="category_title")
        category_link = category_title.a.get("href")
        cat_box_all_items = cat_box.find_all("li")
        dict_categories[category_title.text] = {"category_link": main_url + category_link, }
        numb = 0
        for cat_item in cat_box_all_items:
            cat_item_title = cat_item.a.get("title")
            cat_item_link = cat_item.a.get("href")

            dict_categories[category_title.text].update({
                "cat_item_title " + str(numb): cat_item_title,
                "cat_item_link " + str(numb): main_url + cat_item_link
            })
            numb += 1

    with open('../../data/dataD.json', 'w', encoding='utf-8') as fp:
        json.dump(dict_categories, fp, ensure_ascii=False)
    return "END diagnostic"


async def get_doctor_list():
    start_time = datetime.now()
    with open("../../data/dataL.json", "r") as file:
        doctor_categore_data = json.load(file)
    doctor_categore_data_ke = doctor_categore_data.keys()
    doctor_dict = {
        "Main": True,
    }
    for ke in doctor_categore_data_ke:
        bar = ChargingBar('{+} Startid', max=len(doctor_categore_data_ke))
        if ke != "categories_name":
            categories_url = main_url + doctor_categore_data[ke]['link']
            try:
                async with aiohttp.ClientSession() as session:
                    responce = await requests.get(url=categories_url, headers=headers)
            except requests.exceptions.ConnectionError:
                print("{+} Conect Error " + responce.url)
            result = responce.text
            soup = BeautifulSoup(await result, 'lxml')
            paging_all = soup.find(class_="pagin").find_all(class_="page")
            try:
                page_num = int(paging_all[-1].text) + 1
                pagings = range(1, page_num)
                bar = ChargingBar('{+} Parsing doctor list ', max=page_num - 1)
                for paging in pagings:
                    if ke != "categories_name":
                        # print("{+} Starting true")
                        categories_url = main_url + doctor_categore_data[ke]['link'] + "/page/" + str(paging)
                        responce = requests.get(url=categories_url, headers=headers)
                        result = responce.text
                        soup = BeautifulSoup(result, 'lxml')
                        time.sleep(2)
                        cards_list = soup.find(class_="result_list").find(class_="row")
                        for card in cards_list:
                            bar = ChargingBar('{+} Parsing doctor card ', max=len(cards_list))
                            try:
                                doctor_name = card.find(class_="name").a.text
                            except Exception:
                                continue
                            doctor_dict[doctor_name] = {
                                "doctor_speciality": [],
                                "info": {},
                                "description": "",
                                "phone": [],
                                "more_info": {},
                                "For_child": "",
                                "Doctor_Photo": "",
                            }
                            try:
                                doctor_link = card.find(class_="name").a.get("href")
                            except Exception:
                                continue
                            categories_url = main_url + doctor_link
                            responce = requests.get(url=categories_url, headers=headers)
                            result = responce.text
                            soup = BeautifulSoup(result, 'lxml')
                            doctor_speciality = soup.find(class_="specialization").text
                            doctor_dict[doctor_name]["doctor_speciality"] = doctor_speciality.split(",")
                            doctor_info = soup.find(class_="undernameBlock")
                            info_iter_num = 0
                            for info in doctor_info:
                                if info != "\n" and info.get("class")[0] != "who":
                                    info_name = info.get("class")
                                    info_text = info.text
                                    doctor_dict[doctor_name]["info"].update({"name " + str(info_iter_num): info_name[0],
                                                                             "content " + str(
                                                                                 info_iter_num): info_text})
                                    info_iter_num += 1
                            price_count = soup.find(class_="price")
                            if price_count is not None:
                                price_count = price_count.text
                            try:
                                price = price_count.split(" ")
                                for price_i in price:
                                    if price_i.isnumeric():
                                        price = price_i
                            except Exception as ex:
                                price = price_count
                            doctor_dict[doctor_name]["price"] = price
                            description = soup.find(class_="description").text
                            doctor_dict[doctor_name]["description"] = description
                            phone_list = soup.find(class_="nembers")
                            for phone in phone_list:
                                if phone != "\n":
                                    phone_number = phone.text
                                    doctor_dict[doctor_name]["phone"].append(phone_number)
                            worck_place_box = soup.find(class_="doctor_clinic")
                            if worck_place_box is not None:
                                worck_place_title = worck_place_box.find(class_="label")
                            if worck_place_title is not None:
                                worck_place_title = worck_place_title.text
                            doctor_dict[doctor_name][worck_place_title] = {}
                            w_num = 0
                            for w_place in worck_place_box:
                                if w_place != "\n" and w_place is not None and w_place != " ":
                                    worck_all_place = w_place.find(class_="clinic_name")
                                    if worck_all_place is not None:
                                        for places in worck_all_place:
                                            worck_place_name = places.text
                                            doctor_dict[doctor_name][worck_place_title].update(
                                                {"name " + str(w_num): worck_place_name})
                                            w_num += 1
                            doctor_more_info = soup.find(class_="doctor_body")
                            numb_title = 0
                            numb_text = 1
                            more_info_list = []
                            for more_info in doctor_more_info:
                                if more_info != "\n" and more_info != " ":
                                    more_info_list.append(more_info.text)
                                    if len(more_info_list) % 2 != 2:
                                        try:
                                            doctor_dict[doctor_name]["more_info"][str(more_info_list[numb_title])] = {}
                                            bore_info_dict_title = more_info_list[numb_title]
                                            doctor_dict[doctor_name]["more_info"][str(bore_info_dict_title)] = {
                                                "name": str(more_info_list[numb_text])}
                                            numb_title += 2
                                            numb_text += 2
                                        except Exception as ex:
                                            continue
                            doctor_photo = soup.find(class_="doctor_logo")
                            photo_link = main_url + doctor_photo.img.get("src")
                            img_data = requests.get(photo_link, headers=headers).content
                            filename = photo_link.split("/")[-1]
                            completeName = '../media/doctor_photo/' + filename
                            with open(completeName, 'wb') as handler:
                                handler.write(img_data)
                            doctor_dict[doctor_name]["Doctor_Photo"] = os.path.abspath(handler.name)
                            on_child = soup.find(class_="benefits")
                            if len(on_child) > 1:
                                doctor_dict[doctor_name]["For_child"] = True
                            elif len(on_child) == 1:
                                doctor_dict[doctor_name]["For_child"] = False

                        bar.next()
                bar.next()

            except Exception as e:
                print(e, traceback.format_exc())

        time.sleep(.1)
        bar.next()
    end_time = datetime.now()
    print('First Duration: {}'.format(end_time - start_time))
    with open("../../../media/data/kiev/kiev.json", "w", encoding='utf-8') as file:
        json.dump(doctor_dict, file, ensure_ascii=False)

    bar.finish()
    print('Duration: {}'.format(end_time - start_time))
    return "finish"


def main():
    print(get_doctor_list())
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
