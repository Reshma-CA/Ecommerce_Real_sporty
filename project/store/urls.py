from django.urls import path
from .import views

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.Register,name = "signup"),
    path("home/",views.home,name = "home"),
    path('category_products/<int:id>', views.category_products, name='category_products'),
    path('single_p_details/<int:id>',views.single_products_details,name = 'single_p_details'),
    path('login/',views.Login,name = 'login-page'),
    path('logout/',views.logoutuser,name = 'logout'),
    path('otplogin/',views.otplogin,name = 'otp_ph_login'),
    path('otp_verify/',views.otp_verify,name = 'otp_veryfy'),
    # path("products/",views.category_products,name = "products"),
]

