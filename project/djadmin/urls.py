from django.urls import path
from .import views


urlpatterns = [
    path("",views.adminilogin,name="login"),
    path("adhome/",views.adminhome,name="adminhome"),
    path("apannel/",views.adminpannel,name="adminpannel"),

    # Users pannel

    path("ausers/",views.adminusers,name='ausers'),
    path("blockuser/<int:id>",views.blockuser,name="admin_blockuser"),
    path("unblockuser/<int:id>",views.unblockuser,name="admin_unblockuser"),

    # categories pannel

    path("acategories/",views.adminCategory,name='acategories'),
    path("addcategories/",views.addcategories,name='addcategories'),
    path("editcategories/<int:myid>",views.editcategories,name='editcategories'),
    path("deletecategories/<int:myid>",views.deletecategories,name='deletecategories'),
    path("blockcategories/<int:myid>",views.blockcategories,name='blockcategories'),

    # Product Pannel

    path("aproducts/",views.adminProducts,name='aproducts'),
    path("addproduct/",views.addproducts,name='addproduct'),
    path("editproduct/<int:myid>/",views.editproducts,name='editproduct'),
    path('delete_product/<int:myid>/', views.delete_products, name='delete_product'),


    # Order pannel

    path("orders/",views.orders,name='orders'),
    path("edit_order_status/<int:myid>",views.edit_order_status,name='edit_order_status'),

    # category offer pannel

    path("categoryoffer/",views.categoryoffer,name='categoryoffer'),
    path("addcategoryoffer/",views.addcategoryoffer,name='addcategoryoffer'),
    path("editcategoryoffer/<int:myid>",views.editcategoryoffer,name="editcategoryoffer"),
    path("deletecategory_offer/<int:myid>",views.deletecategory_offer,name="deletecategory_offer"),

    # Product offer pannel

    path("productoffer/",views.productoffer,name='productoffer'),
    path("add_product_offer/",views.add_product_offer,name='add_product_offer'),
    path("edit_product_offer/<int:myid>",views.edit_product_offer,name='edit_product_offer'),
    path("delete_product_offer/<int:myid>",views.delete_product_offer,name='delete_product_offer'),
    
    # Coupon pannel

    path("coupons/",views.coupons,name='coupons'),
    path("add_coupon/",views.add_coupon,name='add_coupon'),
    path("edit_coupon/<int:myid>",views.edit_coupon,name='edit_coupon'),
    path("delete_coupon/<int:myid>",views.delete_coupon,name='delete_coupon'),


    path("salesreport/",views.salesreport,name="salesreport"),
    path("alogout/",views.admin_logout,name='alogout'),
    


]

#add_product_offer ,delete_product_offer
