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

class Order_detailsUser(admin.ModelAdmin):
    list_display=("user","product","address","orderdate","orderstatus","ordertype","quantity","finalprice","ordernumber")
    

class OrderUser(admin.ModelAdmin):
    list_display = ("user","totalamount","coupon","ordertime")


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
admin.site.register(Orders_details,Order_detailsUser)
admin.site.register(Order,OrderUser)
admin.site.register(Wallet,WalletUser)