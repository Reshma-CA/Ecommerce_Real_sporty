from django.urls import path
from .import views


urlpatterns = [
    path("",views.adminilogin,name="login"),
    path("adhome/",views.adminhome,name="adminhome"),
    path("apannel/",views.adminpannel,name="adminpannel"),
    path("ausers/",views.adminusers,name='ausers'),
    path("blockuser/<int:id>",views.blockuser,name="admin_blockuser"),
    path("unblockuser/<int:id>",views.unblockuser,name="admin_unblockuser"),
    path("acategories/",views.adminCategory,name='acategories'),
    path("addcategories/",views.addcategories,name='addcategories'),
    path("orders/",views.orders,name='orders'),
    path("edit_order_status/<int:myid>",views.edit_order_status,name='edit_order_status'),
    path("editcategories/<int:myid>",views.editcategories,name='editcategories'),
    path("deletecategories/<int:myid>",views.deletecategories,name='deletecategories'),
    path("blockcategories/<int:myid>",views.blockcategories,name='blockcategories'),
    path("aproducts/",views.adminProducts,name='aproducts'),
    path("addproduct/",views.addproducts,name='addproduct'),
    path("editproduct/<int:myid>/",views.editproducts,name='editproduct'),
    path('delete_product/<int:myid>/', views.delete_products, name='delete_product'),
    path("alogout/",views.admin_logout,name='alogout'),
    


]

# <int:myid>/
