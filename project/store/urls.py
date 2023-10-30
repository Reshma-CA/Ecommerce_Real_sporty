from django.urls import path
from .import views
from .views import GenerateInvoice
# from .views import WholeProductsListView

urlpatterns = [
    path("",views.index,name="index"),
    path("signup/",views.Register,name = "signup"),
    path("home/",views.home,name = "home"),
    path("contact/",views.contact,name = "contact"),
    path("blog/",views.blog,name = "blog"),
    # path('whole_products/', WholeProductsListView.as_view(), name='whole_products'),
    path('whole_products/', views.whole_products, name='whole_products'),
    path('category_products/<int:id>', views.category_products, name='category_products'), 
    path('single_p_details/<int:id>',views.single_products_details,name = 'single_p_details'),
    path("quantityupdate/",views.quantity_update,name="quantityupdate"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path("delete_cart_item/",views.delete_cart_item,name = "delete_cart_item"),
    path("checkout/",views.checkout,name = "checkout"),
    path("userprofile/",views.userprofile,name = "userprofile"),
    path('edituserdetails/<int:user_id>/', views.edituserdetails, name='edituserdetails'),
    path('addaddress/', views.Add_address, name='addaddress'),
    path('edit_address/<int:myid>/', views.Edit_address, name='edit_address'),
    path('delete_order/<int:myid>/', views.delete_order, name='delete_order'),
    path('order_details/<int:myid>/',views.order_details, name='order_details'),
    path("razorpay_success/",views.razorpay_success,name = "razorpay_success"),
    path("place_order/",views.place_order,name = "place_order"),
    path("wallet/",views.wallet,name = "wallet"),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path("delete_wishlist_item/",views.delete_wishlist_item,name = "delete_wishlist_item"),
    path("wishlist/",views.view_wishlist,name = "wishlist"),
    path("delivered_product/",views.delivered_product,name = "delivered_product"),
    path("delivered_pdt_return/<int:myid>/",views.delivered_pdt_return,name = "delivered_pdt_return"),
    path('login/',views.Login,name = 'login-page'),
    path('logout/',views.logoutuser,name = 'logout'),
    path('otplogin/',views.otplogin,name = 'otp_ph_login'),
    path('otp_verify/',views.otp_verify,name = 'otp_veryfy'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('forgot_password/', views.forg_pass, name='forgot_password'),
    path('forg_verify_otp/', views.forg_verify_otp, name='forg_verify_otp'),
    path('forg_reset_password/', views.forg_reset_password, name='forg_reset_password'),
    path("applycouponajax/",views.applycouponajax,name="applycouponajax"),
    # path('editsubmit/<int:myid>/', views.editsubmit, name='editsubmit'),
     path('generate_invoice/<int:id>', GenerateInvoice.as_view(), name='generate_invoice'),
     path('custom-404/', views.custom_404_test, name='custom_404_test')


    # path("products/",views.category_products,name = "products"),
]   
