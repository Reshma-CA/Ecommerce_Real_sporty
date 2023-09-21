from django.contrib import admin
from django.contrib.admin import ModelAdmin
from . models import *
# Register your models here.

class CustomersUser(admin.ModelAdmin):
    list_display = ("username","name","phonenumber","email")

class CategoryUser(admin.ModelAdmin):
    list_display = ("name","No_of_items")

class ProductsUser(admin.ModelAdmin):
    list_display=("name","price","quantity","category")

admin.site.register(Customers,CustomersUser)
admin.site.register(Category,CategoryUser)
admin.site.register(Products,ProductsUser)

