from django.urls import path
from .import views

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.Register,name = "signup"),
    path("home/",views.home,name = "home"),
    path('category_products/<int:id>', views.category_products, name='category_products'),
    path('single_p_details/<int:id>',views.single_products_details,name = 'single_p_details'),
    path("cart/",views.cart,name = "cart"),
    path("checkout/",views.checkout,name = "checkout"),
    path("userprofile/",views.userprofile,name = "userprofile"),
    path("orderplaced/",views.orderplaced,name = "orderplaced"),
    path("wallet/",views.wallet,name = "wallet"),
    path("deliveredproduct/",views.deliveredproduct,name = "deliveredproduct"),
    path('login/',views.Login,name = 'login-page'),
    path('logout/',views.logoutuser,name = 'logout'),
    path('otplogin/',views.otplogin,name = 'otp_ph_login'),
    path('otp_verify/',views.otp_verify,name = 'otp_veryfy'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_password/', views.forg_pass, name='forgot_password'),
    path('forg_verify_otp/', views.forg_verify_otp, name='forg_verify_otp'),
    path('forg_reset_password/', views.forg_reset_password, name='forg_reset_password'),


    # path("products/",views.category_products,name = "products"),
]   
