import json

with open("../../../media/data/kiev/kiev.json", "r") as file:
    json_data = json.load(file)

json_data_ke = json_data.keys()

# for i in data_ke:
#     print(i)
#     print(data_db[i]['info'])
#     print("_" * 20)
i = "Бартеньев Сергей Григорьевич"
name = i
doctor_speciality = json_data[i]['doctor_speciality']
info = json_data[i]['info']
description = json_data[i]['description']
phone = json_data[i]['phone']
more_info = json_data[i]['more_info']
For_child = json_data[i]['For_child']
Doctor_Photo = json_data[i]['Doctor_Photo']
price = json_data[i]['price']
worck_place = json_data[i]["worck_place"]



# for m in more_info.keys():
#     print("Mor info title ", m)
#     print("Mor info text ", json_data[i]['more_info'][m]["name"])
#     print("_" * 20)

# print("Nmae: ", name)
for i in doctor_speciality:
    print(i)
print("doctor_speciality: ", doctor_speciality)
# print("Info: ", info)
# print("description: ", description)
# print("phone: ", phone)
# print("more_info: ", more_info)
# print("For_child: ", For_child)
# print("Doctor_Photo: ", Doctor_Photo)
# print("price: ", price)
# print("worck_place: ", worck_place)

