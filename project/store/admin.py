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

class CartUser(admin.ModelAdmin):
    list_display = ("user","product","quantity")

class WishlistUser(admin.ModelAdmin):
    list_display = ("product","user") 

class AddressUser(admin.ModelAdmin):
    list_display=("customer","country","state","district","locality","house","pincode")

class CategoryofferUser(admin.ModelAdmin):
    list_display=("category","offer_description","discount")

class ProductofferUser(admin.ModelAdmin):
    list_display=("product","offer_description","discount")

class CouponUser(admin.ModelAdmin):
    list_display=("code","discount_percentage","is_available")

class OrdernumberUser(admin.ModelAdmin):
    list_display = ("Slno","user","total_amount","coupon","ordertime")


class OrdersUser(admin.ModelAdmin):
    list_display=("user","product","orderdate")

class WalletUser(admin.ModelAdmin):
    list_display=("user","amount")

admin.site.register(Customers,CustomersUser)
admin.site.register(Category,CategoryUser)
admin.site.register(Products,ProductsUser)
admin.site.register(Cart,CartUser)
admin.site.register(Wishlist,WishlistUser)

# 
admin.site.register(Address,AddressUser)
admin.site.register(Categoryoffer,CategoryofferUser)
admin.site.register(Productoffer,ProductofferUser)
admin.site.register(Coupon,CouponUser)
admin.site.register(Ordernumber,OrdernumberUser)
admin.site.register(Orders,OrdersUser)
admin.site.register(Wallet,WalletUser)