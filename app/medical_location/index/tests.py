import time
from bs4 import BeautifulSoup
import requests
import json
import os
from datetime import datetime
from geopy.geocoders import Nominatim

start_time = datetime.now()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}

main_url = "https://likarni.com"


def one():
    medical_category_list = {

    }
    medical_service_list = {
    }
    categories_url = "https://likarni.com/clinics/kyev/ehogisterosalypingografija-ehogsg"
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
            # print(cards_list)
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
                        for iteration, p in enumerate(price_box):
                            # print("{+} check pric pobx ", p)
                            if p != "\n":
                                try:
                                    if p.a is not None:
                                        # print("{+} iteration ", iteration)
                                        try:
                                            medical_category_list[p.a.text]
                                        except Exception as ex:
                                            categore_name = p.a.text
                                            medical_category_list[categore_name] = ""
                                    if p.li is not None:
                                        # print("{+} iteration ", iteration)
                                        for iteration, service in enumerate(p.li):
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
    context = {

    }
    with open('../media/data/categoreServices/categoreName.json', 'w', encoding='utf-8') as fp:
        json.dump(medical_category_list, fp, ensure_ascii=False)
    with open('../media/data/categoreServices/servicesName.json', 'w', encoding='utf-8') as fp:
        json.dump(medical_service_list, fp, ensure_ascii=False)
    return context


def twoo():
    with open("../media/data/categoreServices/servicesName.json", "r") as file:
        json_data = json.load(file)
    json_data_ke = json_data.keys()
    for i in json_data_ke:
        print(i)
    return "Finish"


def three():
    w_place_list = {
        'clinick_name': {},
    }
    categories_url = "https://likarni.com/clinic/medicinskij-centr-smart"
    print("Now parsing ", categories_url)
    responce = requests.get(url=categories_url, headers=headers)
    result = responce.text
    soup = BeautifulSoup(result, 'lxml')
    clinik_info_box = soup.find(class_="clinic_info")
    worck_time_all = clinik_info_box.find(class_="time_data").find_all("span")
    print("{+} W LEN ", len(worck_time_all))
    if len(worck_time_all) > 1:
        for worck_time in worck_time_all:
            if len(worck_time.get("class")) > 1:
                w_place_list["clinick_name"] = {
                    worck_time.get("class")[0] + " " + worck_time.get("class")[1]: worck_time.text
                }
            else:
                w_place_list["clinick_name"] = {
                    worck_time.get("class")[0]: worck_time.text
                }
    else:

        w_place_list["clinick_name"] = {
            worck_time_all[0].get("class")[0] + " " + worck_time_all[0].get("class")[1]: worck_time_all[0].text}
    print(w_place_list)
    return "Finihs"


def medical_save_test():
    with open("../media/data/medical_center/medical_center_facilities.json", "r") as file:
        json_data = json.load(file)
    json_data_ke = json_data.keys()
    count = 0
    for i in json_data_ke:
        print("{+} Medical num ", count)
        medical_name = i
        logo = json_data[i]["logo"]
        town = json_data[i]["medical_city"].split(',')[0]
        print(town)
        street = json_data[i]["medical_street"]
        worck_time = json_data[i]["worck_time"]
        description = json_data[i]["description"]
        slug = json_data[i]["slug"]
        description_img_all = json_data[i]["description img"]
        if description_img_all != False:
            for description_img in description_img_all:
                description_img_link = description_img
                description_img_name = slug + "-" + description_img_link.split("/")[-1].split('.')[0]
        phone = json_data[i]["phone numbers"]
        branch = json_data[i]["branch"]
        count += 1
        time.sleep(10)
    return "Finish"


def desk_img():
    with open("../media/data/medical_center/medical_center_facilities.json", "r") as file:
        json_data = json.load(file)
    json_data_ke = json_data.keys()
    for i in json_data_ke:
        try:

            description_img_all = json_data[i]["description-img"]
            slug = json_data[i]["slug"]
            if description_img_all != False:
                for description_img in description_img_all:
                    print(description_img)
            print("_" * 20)
        except Exception:
            pass

end_time = datetime.now()


def main():
    print(desk_img())
    print('First Duration: {}'.format(end_time - start_time))


if __name__ == "__main__":
    main()

# 0:00:00.485947
