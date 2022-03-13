from django.shortcuts import render
import folium
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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
    i = map()
    return render(request, "map/index.html")


def map():
    numb = 0

    mapObj = folium.Map(location=[50.444988857524024, 30.531005859375004], zoom_start=13)

    folium.Circle(radius=10,
                  location=[50.414693806807826, 30.66277622939258],
                  fill=True,
                  popup=folium.Popup("<h2>Городская больница №1</h2></br>Киев, Харьковское шоссе, 121"),
                  ).add_to(mapObj)

    folium.Circle(radius=10,
                  location=[36.85411556303106, 30.807413945074245],
                  fill=True,
                  popup=folium.Popup("<h2>Здесь я живу</h2></br><b>)))</B>"),
                  ).add_to(mapObj)

    for i in loc:
        folium.Circle(radius=100,
                      location=[i[1], i[2]],
                      fill=True,
                      popup=folium.Popup("<h2>" + i[0] + "</h2>"),
                      ).add_to(mapObj)
        numb += 1
    mapObj.save('templates/map/index.html')
