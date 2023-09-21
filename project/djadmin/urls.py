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
    path("aproducts/",views.adminProducts,name='aproducts'),
    path("alogout/",views.admin_logout,name='alogout'),
    


]