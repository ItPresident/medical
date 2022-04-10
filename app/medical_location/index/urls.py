from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("speciality/<int:id>", views.speciality_list, name="speciality_list"),
    path("category/<int:id>", views.category_list, name="category_list"),
    path('docktor-list', views.docktorList, name='docktor_list'),
    path('wplace-list', views.wplaceList, name='wplace_list'),
    path('search', views.search, name='search'),
    # path('get_town', views.gte_Town, name='get_town'),
    path('save-category', views.save_category, name='save_category'),
    path('save-service', views.save_service, name='save_service'),
    # path('sive-in-db', views.sive_in_DB, name="sive_in_db"),
    # path('save-spec', views.save_spec, name="save_spec"),
    path('save-wplace', views.save_wplace, name="save_wplace"),
    path('save-img', views.save_img, name="save_img"),
    path('doctor-detil/<int:id>', views.doctor_detail, name='doctor_detil'),
]
