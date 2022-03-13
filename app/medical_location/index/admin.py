from django.contrib import admin
from .models import Town, Doctor, Speciality, WorckPlace, Category, Service, ImageWorckPlace
# Register your models here.
admin.site.register(Town)
admin.site.register(Doctor)
admin.site.register(Speciality)
admin.site.register(WorckPlace)
admin.site.register(ImageWorckPlace)
admin.site.register(Category)
admin.site.register(Service)