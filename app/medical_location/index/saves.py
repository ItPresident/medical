completeName = os.path.join('media/data/', "licarni_town.json")
with open(completeName, "r") as file:
    town_list = json.load(file)

towns = town_list.keys()

geolocator = Nominatim(user_agent='Max')
for town in towns:
    m_Town = Town()
    location = geolocator.geocode(town)
    latitude = location.latitude
    longitude = location.longitude
    m_Town.name = town
    m_Town.latitude = latitude
    m_Town.longitude = longitude
    m_Town.save()