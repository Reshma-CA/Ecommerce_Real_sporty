from django.shortcuts import render,redirect
from django.http.response import HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
from store.models import Customers
from django.contrib.auth.decorators import login_required
import re
import random
from twilio.rest import Client



# Create your views here.

def index(request):

    allcategories=Category.objects.all()
    allproducts=Products.objects.all()
    context={"allcategories":allcategories,"allproducts":allproducts}
    return render(request,'index.html',context)

     
    #  pricerange=1000

    #  Category.objects.filter(price_gte=pricerange)
     


    
    

def Register(request):
      if 'cusername' in request.session:
            return redirect('index')
      if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        repassword=request.POST.get("repassword")
        phonenumber=request.POST.get("phonenumber")
        name=request.POST.get("name")

        msg1 = None

        if not username.isalpha():
            msg1="Name should not contain numbers"

        elif len(username)<4:
            msg1="Name should have atleast 4 characters"
            
        elif len(username)>10:
            msg1="Username can only have at the most 10 characters"
        
        elif not isinstance(email, str):
            msg1 = "Invalid Email: Email must be a string"
            
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            msg1 = "Invalid Email"

        elif len(password)<6:
            msg1="Password must altleast contain 6 characters"
            
        elif password!=repassword:
            msg1="Passwords doesn't match to Confirm password!" 

        elif phonenumber.isalpha():
            msg1="Please enter a valid phone number" 

        elif len(phonenumber)!=10:
            msg1="Phone number should have ten digits" 

        elif not name.isalpha():
            msg1="Name should only contain alphabets"

        if msg1:

            return render(request,"signup.html",{"msg1":msg1})


        res=Customers(username=username,email=email,password=password,repassword=repassword,phonenumber=phonenumber,name=name)
        res.save()
        msg="Signup Successfull"
        return render(request,"login.html",{"msg":msg})
        
      return render(request,"signup.html")
      

def Login(request):
    if 'cusername' in request.session:
        myuser=request.session["cusername"]
        contents=Customers.objects.filter(username=myuser)
        return render(request,"home.html",{"contents":contents})
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        count=Customers.objects.filter(username=username,password=password).count()
        if count==1:
            request.session["cusername"]=username
            contents=Customers.objects.filter(username = username)# require only our details
            return render(request,"home.html",{"contents":contents})
        else:
            return render(request,"login.html",{"cerror":"Sorry Invalid Credentials!"})
        
    return render(request,"login.html")

def home(request):
     return render(request,'home.html',{})

def logoutuser(request):
    logout(request)
    return redirect ('index')

def generate_otp():
    return str(random.randint(1000, 9999))

def otplogin(request):
    # if "username" in request.session:
    #     return redirect(loggedin)
    
    if request.method=="POST":
        phonenumber=request.POST["phonenumber"]
        cust=Customers.objects.filter(phonenumber=phonenumber).count()
        if cust==0:
            error="Phonenumber not registered"
            return render(request,"store/otplogin.html",{"error":error})
        else:
            
            otp = generate_otp()
            
            request.session['U_otp'] = otp
            request.session['U_phone'] = phonenumber
            
            send_otp(phonenumber, otp)
            
            return redirect('otp_veryfy')
        

    return render(request,"otp_ph_login.html")

    



def otp_verify(request):
    return render(request,"otp_veryfy.html")


def category_products(request,id):
     
     category_s = Category.objects.get(id=id)
     product_s = Products.objects.filter(category=category_s)
     context={"category_s":category_s,"product_s":product_s}
     
     return render(request,'products.html',context)

def single_products_details(request,id):

    product = Products.objects.filter(id = id).first()
    context = {'product':product}
    return render(request,'single-product-details.html',context)