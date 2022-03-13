from bs4 import BeautifulSoup
from progress.bar import ChargingBar
import json
import requests
import time
from datetime import datetime
import sys, traceback, os
from multiprocessing.dummy import Pool as ThreadPool

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
    with open('../../media/data/licarni_town.json', 'w', encoding='utf-8') as fp:
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
    with open('../data/dataL.json', 'w', encoding='utf-8') as fp:
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

    with open('../data/dataD.json', 'w', encoding='utf-8') as fp:
        json.dump(dict_categories, fp, ensure_ascii=False)
    return "END diagnostic"


def get_doctor_list():
    start_time = datetime.now()
    with open("../data/dataD.json", "r") as file:
        doctor_categore_data = json.load(file)
    doctor_categore_data_ke = doctor_categore_data.keys()
    doctor_dict = {
        "Main": True,
    }
    for ke in doctor_categore_data_ke:
        # bar = ChargingBar('{+} Startid ', max=len(doctor_categore_data_ke))
        if ke != "categories_name":
            categories_url = main_url + doctor_categore_data[ke]['link']
            try:
                responce = requests.get(url=categories_url, headers=headers)
            except requests.exceptions.ConnectionError:
                print("{+} Conect Error {}".format(responce.url))
            result = responce.text
            soup = BeautifulSoup(result, 'lxml')
            paging_all = soup.find(class_="pagin").find_all(class_="page")
            try:
                page_num = int(paging_all[-1].text) + 1
                pagings = range(1, page_num)
                # bar = ChargingBar('{+} Parsing doctor list ', max=page_num - 1)
                for paging in pagings:
                    if ke != "categories_name":
                        # print("{+} Starting true")
                        categories_url = main_url + doctor_categore_data[ke]['link'] + "/page/" + str(paging)
                        responce = requests.get(url=categories_url, headers=headers)
                        result = responce.text
                        soup = BeautifulSoup(result, 'lxml')
                        time.sleep(.2)
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
                                    doctor_dict[doctor_name]["info"].update(
                                        {"name {}".format(str(info_iter_num)): info_name[0],
                                         "content {}".format(str(info_iter_num)): info_text})
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
                                worck_place_title = "worck_place"
                            doctor_dict[doctor_name][worck_place_title] = {}
                            w_num = 0
                            for w_place in worck_place_box:
                                if w_place != "\n" and w_place is not None and w_place != " ":
                                    worck_all_place = w_place.find(class_="clinic_name")
                                    if worck_all_place is not None:
                                        for places in worck_all_place:
                                            worck_place_name = places.text
                                            doctor_dict[doctor_name][worck_place_title].update(
                                                {"name {}".format(str(w_num)): worck_place_name})
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

                            on_child = soup.find(class_="benefits")
                            if len(on_child) > 1:
                                doctor_dict[doctor_name]["For_child"] = True
                            elif len(on_child) == 1:
                                doctor_dict[doctor_name]["For_child"] = False

                            doctor_photo = soup.find(class_="doctor_logo")
                            photo_link = main_url + doctor_photo.img.get("src")
                            img_data = requests.get(photo_link, headers=headers).content
                            filename = photo_link.split("/")[-1]
                            categories_url_city = doctor_categore_data[ke]['link'].split("/")[-2]
                            completeName = '../../media/doctor_photo/{}'.format(categories_url_city)
                            if os.path.exists(completeName):
                                pass
                            else:
                                os.mkdir('../../media/doctor_photo/{0}'.format(categories_url_city))
                            with open(completeName + "/" + filename, 'wb') as handler:
                                handler.write(img_data)
                            doctor_dict[doctor_name]["Doctor_Photo"] = os.path.abspath(handler.name)
                            doctor_dict[doctor_name]["Town"] = categories_url_city

                            bar.next()
                # bar.next()

            except Exception as e:
                print(e, traceback.format_exc())

        time.sleep(.1)
        # bar.next()
    end_time = datetime.now()
    print('First Duration: {}'.format(end_time - start_time))
    with open("../../media/data/kiev/kiev.json", "w", encoding='utf-8') as file:
        json.dump(doctor_dict, file, ensure_ascii=False)

    # bar.finish()
    print('Duration: {}'.format(end_time - start_time))
    return "finish"


def get_categories():
    medical_category_list = {
    }
    medical_service_list = {
    }
    start_time = datetime.now()
    with open("../data/dataD.json", "r") as file:
        categories_data = json.load(file)
    json_data_ke = categories_data.keys()
    for key in json_data_ke:
        if key != "categories_name":
            categories_url = categories_data[key]['category_link']
            print("Now parsing ", categories_url)
            responce = requests.get(url=categories_url, headers=headers)
            result = responce.text
            soup = BeautifulSoup(result, 'lxml')
            paging_all = soup.find(class_="pagin").find_all(class_="page")
            try:
                page_num = int(paging_all[-1].text) + 1
                pagings = range(1, page_num)
                for paging in pagings:
                    categorie_url = categories_url + "/page/" + str(paging)
                    responce = requests.get(url=categorie_url, headers=headers)
                    result = responce.text
                    soup = BeautifulSoup(result, 'lxml')
                    time.sleep(.2)
                    cards_list = soup.find(class_="b-content__list").find_all(class_="c-clinic")
                    print("{+} page num " + str(paging))
                    card_num = 0
                    for card in cards_list:
                        try:
                            if card is not None:
                                madical_smal_url = card.find(class_="title_doc").get('href')
                                madical_url = main_url + madical_smal_url
                                responce = requests.get(url=madical_url, headers=headers)
                                result = responce.text
                                soup = BeautifulSoup(result, 'lxml')
                                time.sleep(.2)
                                print("{+} ststus code ", responce, " ", card_num)
                                card_num += 1
                                price_box = soup.find(class_="price_list")
                                for iteration, price_item in enumerate(price_box):
                                    if price_item != "\n":
                                        try:
                                            if price_item.a is not None:
                                                try:
                                                    medical_category_list[price_item.a.text]
                                                except Exception as ex:
                                                    categore_name = price_item.a.text
                                                    medical_category_list[categore_name] = ""
                                            if price_item.li is not None:
                                                for iteration, service in enumerate(price_item.li):
                                                    if service is not None:
                                                        if service != "\n" and iteration != 3:
                                                            try:
                                                                medical_service_list[service.text]
                                                            except Exception as ex:
                                                                service_name = service.text
                                                                medical_service_list[service_name] = categore_name
                                        except Exception:
                                            pass
                        except Exception:
                            continue
            except Exception as ex:
                print(ex)
    with open('../../media/data/categoreServices/categoreName.json', 'w', encoding='utf-8') as fp:
        json.dump(medical_category_list, fp, ensure_ascii=False)
    with open('../../media/data/categoreServices/servicesName.json', 'w', encoding='utf-8') as fp:
        json.dump(medical_service_list, fp, ensure_ascii=False)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    return "finish"

def get_medical_center():
    w_place_list = {}
    clinick_facilities_list = {}
    start_time = datetime.now()
    with open("../data/dataD.json", "r") as file:
        categories_data = json.load(file)
    json_data_ke = categories_data.keys()
    for key in json_data_ke:
        if key != "categories_name":
            categories_url = categories_data[key]['category_link']
            print("Now parsing ", categories_url)
            responce = requests.get(url=categories_url, headers=headers)
            result = responce.text
            soup = BeautifulSoup(result, 'lxml')
            paging_all = soup.find(class_="pagin").find_all(class_="page")
            try:
                page_num = int(paging_all[-1].text) + 1
                pagings = range(1, page_num)
                for paging in pagings:
                    categorie_url = categories_url + "/page/" + str(paging)
                    responce = requests.get(url=categorie_url, headers=headers)
                    result = responce.text
                    soup = BeautifulSoup(result, 'lxml')
                    time.sleep(.2)
                    cards_list = soup.find(class_="b-content__list").find_all(class_="c-clinic")
                    print("{+} page num " + str(paging))
                    card_num = 0
                    for card in cards_list:
                        try:
                            if card is not None:
                                madical_smal_url = card.find(class_="title_doc").get('href')
                                madical_url = main_url + madical_smal_url
                                print("{+} card number ", card_num)
                                responce = requests.get(url=madical_url, headers=headers)
                                result = responce.text
                                soup = BeautifulSoup(result, 'lxml')
                                time.sleep(.2)

                                #parce clinick info
                                clinik_info_box = soup.find(class_="clinic_info")

                                #Finde clinick name
                                clinick_name = clinik_info_box.find(class_="name").text
                                w_place_list[clinick_name] = {}

                                #find clinick img
                                logo_img_link = clinik_info_box.find(class_="clinic_logo").img.get("src")
                                photo_link = main_url + logo_img_link
                                img_data = requests.get(photo_link, headers=headers).content
                                filename = photo_link.split("/")[-1]
                                categories_url_city = categories_data[key]['category_link'].split("/")[-2]
                                completeName = '../../media/medical_logo/{}'.format(categories_url_city)
                                if os.path.exists(completeName):
                                    pass
                                else:
                                    os.mkdir('../../media/medical_logo/{0}'.format(categories_url_city))
                                with open(completeName + "/" + filename, 'wb') as handler:
                                    handler.write(img_data)
                                w_place_list[clinick_name]["logo"] = os.path.abspath(handler.name)
                                #clinick facilities
                                clinic_facilities_list = clinik_info_box.find_all(class_="clinic-services")
                                for facilities in clinic_facilities_list:
                                    try:
                                        clinick_facilities_list[facilities]
                                    except Exception:
                                        facilities_name = facilities.text
                                        clinick_facilities_list[facilities_name] = ''
                                #adress
                                medical_city = clinik_info_box.find(class_='adrss').find(class_="city").text
                                medical_street = clinik_info_box.find(class_='adrss').find(class_="street").text
                                w_place_list[clinick_name]["medical_city"] = medical_city
                                w_place_list[clinick_name]["medical_street"] = medical_street
                                # worck time
                                worck_time_all = clinik_info_box.find(class_="time_data").find_all("span")
                                if len(worck_time_all) > 3:
                                    for worck_time in worck_time_all:
                                        if len(worck_time.get("class")) > 1:
                                            w_place_list[clinick_name]["worck_time"] = {
                                                worck_time.get("class")[0] + " " + worck_time.get("class")[1]: worck_time.text
                                            }
                                        else:
                                            w_place_list[clinick_name]["worck_time"] = {
                                                worck_time.get("class")[0]: worck_time.text
                                            }
                                else:
                                    if len(worck_time_all[0].get("class")) > 1:
                                        w_place_list[clinick_name]["worck_time"] = { worck_time_all[0].get("class")[0] + " " + worck_time_all[0].get("class")[1]: worck_time_all[0].text}
                                    else:
                                        w_place_list[clinick_name]["worck_time"] = { worck_time_all[0].get("class")[0]: worck_time_all[0].text}

                                #description
                                description = clinik_info_box.find(class_="description_text").contents
                                w_place_list[clinick_name]["description"] = str(description)

                                # photo description
                                photo_box = clinik_info_box.find(class_="description_text").find(class_="gallery")
                                if photo_box is not None:
                                    w_place_list[clinick_name]["description img"] = []
                                    for photo_item in photo_box:
                                        if photo_item != "\n":
                                            photo_medickal_link = photo_item.a.img.get("src")
                                            img_data = requests.get(photo_medickal_link, headers=headers).content
                                            filename = photo_medickal_link.split("/")[-1]
                                            folder_name = madical_url.split("/")[-1]
                                            completeName = '../../media/medical_photo_description/{}'.format(folder_name)
                                            if os.path.exists(completeName):
                                                with open(completeName + "/" + filename, 'wb') as handler:
                                                    handler.write(img_data)
                                                w_place_list[clinick_name]["description img"].append(
                                                    os.path.abspath(handler.name))
                                                pass
                                            else:
                                                os.mkdir('../../media/medical_photo_description/{0}'.format(folder_name))
                                                with open(completeName + "/" + filename, 'wb') as handler:
                                                    handler.write(img_data)
                                                w_place_list[clinick_name]["description img"].append(os.path.abspath(handler.name))

                                else:
                                    w_place_list[clinick_name]["description img"] = False

                                # Slug
                                slug = madical_url.split("/")[-1]
                                w_place_list[clinick_name]['slug'] = slug

                                # Phone
                                phone_box = clinik_info_box.find(class_="order_phone_block").find(class_="nembers")
                                w_place_list[clinick_name]['phone numbers'] = []
                                for phone in phone_box:
                                    w_place_list[clinick_name]['phone numbers'].append(phone.text)

                                # branch
                                branch = clinik_info_box.find(class_="clinic_net")
                                if branch is not None:
                                    branch_name = branch.text
                                    w_place_list[clinick_name]['branch'] = branch_name
                                else:
                                    w_place_list[clinick_name]['branch'] = False

                                # price
                                medical_price_list = clinik_info_box.find(class_="price_list").find_all("ul")
                                w_place_list[clinick_name]["price"] = {}
                                for medical_price in medical_price_list:
                                    for li in medical_price:
                                        if li != "\n" and li is not None:
                                            if li.find(class_="left") is not None and li.find(class_="md_price"):
                                                price_name = li.find(class_="left").text
                                                price_count = li.find(class_="md_price").text
                                                w_place_list[clinick_name]["price"].update(
                                                    {
                                                        price_name: price_count
                                                    }
                                                )

                                # Doctor in clinick
                                clinic_doctors_list = clinik_info_box.find(class_="clinic_doctors")

                                if clinic_doctors_list is not None:
                                    doctors_list = clinic_doctors_list.find(class_="doctor_items")
                                    w_place_list[clinick_name]["doctors"] = {}
                                    for doctors_item in doctors_list:
                                        if doctors_item is not None and doctors_item != "\n":
                                            name_box = doctors_item.find("a")
                                            doctor_name = name_box.text
                                            doctor_linck = name_box.get("href")
                                            w_place_list[clinick_name]["doctors"].update(
                                                {
                                                    doctor_name: doctor_linck
                                                }
                                            )
                                else:
                                    w_place_list[clinick_name]["doctors"] = False
                                card_num += 1
                        except Exception as ex:
                            continue
            except Exception:
                continue
    with open('../../media/data/medical_center/medical_center_data.json', 'w', encoding='utf-8') as fp:
        json.dump(w_place_list, fp, ensure_ascii=False)
    with open('../../media/data/medical_center/medical_center_facilities.json', 'w', encoding='utf-8') as fp:
        json.dump(clinick_facilities_list, fp, ensure_ascii=False)
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    return "Finish"

def main():
    print(get_medical_center())
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()

# time Duration: 0:04:29.058263
