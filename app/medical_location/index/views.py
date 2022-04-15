import time

from django.shortcuts import render
from django.db.models import Q
from geopy.geocoders import Nominatim
from .models import Town, Speciality, WorckPlace, Doctor, Category, Service, ImageWorckPlace
from django.db.models import Count
from django.conf import settings
from datetime import datetime
from django.db import DataError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import os

loc = [["Title 1", 36.85763435526387, 30.787827068383148],
       ["Title 2", 36.85600890226297, 30.77399174315743],
       ["Title 3", 36.852655138822854, 30.760993366403905],
       ["Title 4", 36.88663785589302, 30.70453925749659],
       ["Title 5", 36.89167145806146, 30.67446170167133],
       ["Title 6", 36.89783504541357, 30.62472483824644],
       ["Title 7", 36.90040290178947, 30.80171178134303],
       ["Shool<br><b>emir</b>", 36.866839116212496, 30.785225850852516],
       ]


# Create your views here.

def index(request):
    speciality_list = Speciality.objects.all()
    category_list = Category.objects.all()
    service_count_list = []
    for category_item in category_list:
        service_count = Service.objects.filter(category=category_item).count()
        service_count_list.append(service_count)
    context = {
        "category": category_list,
        "speciality": speciality_list,
        "service_count": service_count_list,
    }
    return render(request, 'index/index.html', context=context)


def search(request):
    search = request.GET.get('search')
    search_doctor = request.GET.get('docktor')
    search_medical = request.GET.get('medical_center')
    select = request.GET.get('select')
    for_child = request.GET.get('for_child')
    all_town = Town.objects.all()
    # if select:
    #     get_town = Town.objects.get(name=select)

    serch_list = []


    if search:

        doctors = Doctor.objects.filter(Q(name__icontains=search) | Q(description__icontains=search) )
        w_place = WorckPlace.objects.filter(Q(name__icontains=search) | Q(description__icontains=search) )
    elif select:
        get_town = Town.objects.get(name=select)
        doctors = Doctor.objects.filter(Q(town=get_town)).filter(Q(For_child=for_child))
        w_place = WorckPlace.objects.filter(Q(town=get_town))
    else:
        doctors = None
        w_place = None

    # if search_doctor:
    #     if select:
    #         get_town = Town.objects.get(name=select)
    #         serch_town = Q(town=get_town)
    #         serch_list.append(serch_town)
    #     if for_child:
    #         serch_for_child = Q(For_child=for_child)
    #         serch_list.append(serch_for_child)
    #     doctors = Doctor.objects.filter(serch_list)

    if search_medical:
        pass
   #if for_child:
    #   get_for_child =

    context = {
        "Serch_enter": search,
        'doctors': doctors,
        'w_place': w_place,
        'checkbox': for_child,
        'towns': all_town,
        'select': select,
    }
    return render(request, "bace/search.html", context=context)


def category_list(request, id):
    get_category = Category.objects.get(pk=id)
    get_service_list = Service.objects.filter(category=get_category)
    context = {
        'id': id,
        'service_list': get_service_list,
    }
    return render(request, 'index/category-list.html', context=context)


# pass

def speciality_list(request, id):
    get_speciality = Speciality.objects.get(pk=id)
    get_doctor_list = Doctor.objects.filter(speciality=get_speciality)
    context = {
        'id': id,
        'doctor_list': get_doctor_list,
    }
    return render(request, 'index/speciality-list.html', context=context)


def docktorList(request):
    city_list = Town.objects.all()
    contant_list = Doctor.objects.all()
    paginator = Paginator(contant_list, 20)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        "loc": loc,
        "Doctor": page_obj,
        "paging": paginator,
        "citys": city_list,
    }
    return render(request, 'index/DocktorList.html', context=context)


def wplaceList(request):
    wplace_list = WorckPlace.objects.all()
    paginator = Paginator(wplace_list, 20)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = {
        "name": "Worck places list",
        "wplace_list": wplace_list,
        "Wplace": page_obj,
        "paging": paginator,
    }
    return render(request, "index/worckPlaces-list.html", context=context)


def doctor_detail(request, id):
    singel_doctor = Doctor.objects.get(id=id)
    context = {
        "page_name": "Doctor detail",
        "singel_doctor": singel_doctor,
        "id": id,
    }
    return render(request, "index/detail_doctor.html", context=context)


def gte_Town(request):
    start_time = datetime.now()
    completeName = os.path.join('media/data/', "licarni_town.json")
    with open(completeName, "r") as file:
        town_list = json.load(file)

    towns = town_list.keys()

    geolocator = Nominatim(user_agent='Max')
    for town in towns:
        m_Town = Town()
        location = geolocator.geocode(town, language="en")
        slug = location.raw["display_name"].split(",")[0]
        latitude = location.latitude
        longitude = location.longitude
        m_Town.name = town
        m_Town.slug = slug
        m_Town.latitude = latitude
        m_Town.longitude = longitude
        m_Town.save()
        end_time = datetime.now()
        context = {
            "Page_name": "Save Towns",
            "time": end_time - start_time,
            "data": None
        }
    return render(request, "index/success.html", context=context)


def sive_in_DB(request):
    start_time = datetime.now()
    with open(settings.MEDIA_ROOT + "data/kiev/kiev.json", "r") as file:
        json_data = json.load(file)
    json_data_ke = json_data.keys()
    count = 0
    for i in json_data_ke:
        try:
            town_t = Town

            WorckPlace_T = WorckPlace
            Doctor_T = Doctor()

            name = i
            speciality = json_data[i]['doctor_speciality']
            info = json_data[i]['info']
            description = json_data[i]['description']
            phone = json_data[i]['phone']
            more_info = json_data[i]['more_info']
            For_child = json_data[i]['For_child']
            Doctor_Photo = json_data[i]['Doctor_Photo']
            price = json_data[i]['price']
            worck_place = json_data[i]["worck_place"]

            Doctor_T.id = count
            Doctor_T.name = name

            Doctor_T.info = info
            Doctor_T.description = description
            Doctor_T.phone = {"number": phone}
            Doctor_T.more_info = more_info
            if price == None:
                Doctor_T.price = 1
            else:
                Doctor_T.price = price
            Doctor_T.photo = Doctor_Photo
            Doctor_T.For_child = For_child
            Doctor_T.town = town_t.objects.get(slug="Kyiv")

            Doctor_T.save()
            for spec in speciality:
                find_spec = Speciality.objects.get(name=spec)
                Doctor_T.speciality.add(find_spec)
            for w_place in worck_place.values():
                find_place = WorckPlace.objects.get(name=w_place)
                Doctor_T.worck_place.add(find_place)

            count += 1
        except Exception as ex:
            print(ex)
            continue
    end_time = datetime.now()
    context = {
        "Page_name": "Save Doctor",
        "time": end_time - start_time,
        "data": None
    }
    return render(request, "index/success.html", context=context)


def save_spec(request):
    start_time = datetime.now()

    # with open(settings.MEDIA_ROOT + "data/kiev/kiev.json", "r") as file:
    #     json_data = json.load(file)
    #
    # json_data_ke = json_data.keys()
    # naumb = 0
    # for ke in json_data_ke:
    #     specialitys = json_data[ke]['doctor_speciality']
    #
    #     for speciality in specialitys:
    #         try:
    #             spec = Speciality()
    #             spec.name = speciality
    #             spec.save()
    #             print(naumb)
    #             naumb += 1
    #         except Exception:
    #             continue

    spec = Speciality.objects.get(name="Невропатолог")
    end_time = datetime.now()
    context = {
        "Page_name": "Save speciality",
        "time": end_time - start_time,
        "spec": spec,
    }
    return render(request, "index/success.html", context=context)


def save_wplace(request):
    start_time = datetime.now()
    with open(settings.MEDIA_ROOT + "data/medical_center/medical_center_facilities.json", "r") as file:
        json_data = json.load(file)

    json_data_ke = json_data.keys()
    count = 2352
    for i in json_data_ke:
        w_place_t = WorckPlace()
        w_place_t_find = WorckPlace
        town_t = Town

        logo = json_data[i]["logo"]
        town = json_data[i]["medical_city"].split(',')[0]
        street = json_data[i]["medical_street"]
        worck_time = json_data[i]["worck_time"]
        description = json_data[i]["description"]
        phone = json_data[i]["phone numbers"]
        try:
            branch = json_data[i]["branch"]
        except Exception:
            continue
        medical_name = i
        slug = json_data[i]["slug"]
        description_img_all = json_data[i]["description-img"]
        if len(w_place_t_find.objects.filter(name=medical_name)) == 1:
            medickal_find = w_place_t_find.objects.get(name=medical_name)
            medickal_find.logo = logo
            medickal_find.slug = slug
            medickal_find.town = town_t.objects.get(name=town)
            medickal_find.street = street
            medickal_find.worck_time = worck_time
            medickal_find.description = description
            if description_img_all != False:
                for description_img in description_img_all:
                    image_t_find = ImageWorckPlace
                    description_img_link = description_img
                    description_img_name = slug + "-" + description_img_link.split("/")[-1].split('.')[0]
                    find_img = image_t_find.objects.get(name=description_img_name).id
                    medickal_find.photo.add(find_img)
            medickal_find.phone = phone
            medickal_find.branch = branch
            medickal_find.save()
        else:
            w_place_t.id = count
            w_place_t.name = medical_name
            w_place_t.logo = logo
            w_place_t.slug = slug
            w_place_t.town = town_t.objects.get(name=town)
            w_place_t.street = street
            w_place_t.description = description
            if description_img_all != False:
                for description_img in description_img_all:
                    image_t_find = ImageWorckPlace
                    description_img_link = description_img
                    description_img_name = slug + "-" + description_img_link.split("/")[-1].split('.')[0]
                    find_img = image_t_find.objects.get(name=description_img_name).id
                    w_place_t.photo.add(find_img)
            w_place_t.phone = phone
            w_place_t.branch = branch

            w_place_t.save()
        count += 1
    # for i in json_data_ke:
    #     worck_place = json_data[i]["worck_place"].values()
    #     for place in worck_place:
    #         # print(place)
    #         wplace_list.append(place)
    # uniqueplace = set(wplace_list)
    # for unique in uniqueplace:
    #     WorckPlace_T = WorckPlace()
    #     WorckPlace_T.name = unique
    #     WorckPlace_T.save()
    # W_palce = WorckPlace.objects.get(name="QRD dental clinic (Къюарди дентал клиник), стоматология")
    end_time = datetime.now()
    context = {
        "Page_name": "Save w_place",
        "time": end_time - start_time,
        "data": "",
    }
    return render(request, "index/success.html", context=context)


def save_img(request):
    start_time = datetime.now()
    with open(settings.MEDIA_ROOT + "data/medical_center/medical_center_facilities.json", "r") as file:
        json_data = json.load(file)

    json_data_ke = json_data.keys()
    count = 0
    for i in json_data_ke:
        try:
            description_img_all = json_data[i]["description-img"]
            slug = json_data[i]["slug"]

            if description_img_all != False:
                for description_img in description_img_all:
                    image_t_save = ImageWorckPlace()
                    description_img_link = description_img
                    description_img_name = slug + "-" + description_img_link.split("/")[-1].split('.')[0]

                    image_t_save.id = count
                    image_t_save.name = description_img_name
                    image_t_save.image = description_img_link
                    image_t_save.save()
                    count += 1

        except Exception:
            continue

    end_time = datetime.now()
    context = {
        "Page_name": "Save w_place",
        "time": end_time - start_time,
        "data": "",
    }
    return render(request, "bace/success.html", context=context)


def save_category(request):
    start_time = datetime.now()
    with open(settings.MEDIA_ROOT + "data/categoreServices/categoreName.json", "r") as file:
        json_data = json.load(file)
    json_data_ke = json_data.keys()
    count = 0
    for i in json_data_ke:
        category_t = Category()
        try:
            category_t.name = i
            category_t.id = count
        except Exception:
            continue
        count += 1
        category_t.save()

    end_time = datetime.now()
    context = {
        "Page_name": "Save categore",
        "time": end_time - start_time,
        "data": "",
    }
    return render(request, "bace/success.html", context=context)


def save_service(request):
    start_time = datetime.now()
    with open(settings.MEDIA_ROOT + "data/categoreServices/servicesName.json", "r") as file:
        json_data = json.load(file)
    json_data_ke = json_data.keys()
    for i in json_data_ke:
        service_t = Service()
        categoty_t = Category
        try:
            service_t.name = i
            service_t.category = categoty_t.objects.get(name=json_data[i])
        except Exception:
            continue
        service_t.save()

    end_time = datetime.now()
    context = {
        "Page_name": "Save categore",
        "time": end_time - start_time,
        "data": "",
    }
    return render(request, "bace/success.html", context=context)


def save_madical_center(request):
    start_time = datetime.now()

    end_time = datetime.now()
    context = {
        "Page_name": "Save categore",
        "time": end_time - start_time,
        "data": "",
    }
    return render(request, "bace/success.html", context=context)
