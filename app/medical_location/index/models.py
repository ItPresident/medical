from django.db import models


# from django_postgres_extensions.models.fields import ArrayField


# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True, null=False)

    def __str__(self):
        return '{}'.format(self.name)


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)


class Town(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, null=True)
    latitude = models.FloatField(help_text="Широта", null=True)
    longitude = models.FloatField(help_text="Долгота", null=True)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return '{}'.format(self.name)


class MroInfo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, null=True)
    text = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title


class Speciality(models.Model):
    id = models.AutoField(primary_key=True, )
    name = models.CharField(max_length=60, unique=True, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class ImageWorckPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, unique=True)
    image = models.ImageField(upload_to='medical_photo/%Y/%m/%d/', null=True,  max_length=255)

    def __str__(self):
        return self.name


class WorckPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, unique=True)
    slug = models.SlugField(null=True, max_length=100)
    logo = models.ImageField(upload_to="medical_logo/%Y/%m/%d/", max_length=255, null=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    street = models.CharField(max_length=255, default="Ukraine")
    worck_time = models.JSONField(null=True)
    description = models.TextField(max_length=4000, null=True)
    phone = models.JSONField(null=True, max_length=255)
    branch = models.CharField(max_length=60, null=True)
    photo = models.ManyToManyField(ImageWorckPlace)
    # price = models.C

    def __str__(self):
        return '{}'.format(self.name)


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, null=True, unique=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    speciality = models.ManyToManyField(Speciality)
    info = models.JSONField()
    description = models.TextField(max_length=4000)
    phone = models.JSONField()
    more_info = models.JSONField()
    price = models.IntegerField(help_text="цена консультации", null=True, default=1)
    photo = models.ImageField(upload_to="doctor_photo/%Y/%m/%d/", max_length=255)
    worck_place = models.ManyToManyField(WorckPlace)
    For_child = models.BooleanField(null=True)

    # info = models.ArrayField(models.CharField(max_length=15), null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)
