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
import requests
# from .utils import generate_otp, send_otp


# Create your views here.

def index(request):

    allcategories=Category.objects.all()
    allproducts=Products.objects.all()
    context={"allcategories":allcategories,"allproducts":allproducts}
    return render(request,'index.html',context)

     
    #  pricerange=1000

    #  Category.objects.filter(price_gte=pricerange)
     


    
    

def Register(request):
      if 'username' in request.session:
            return redirect('home')
      if request.method=="POST":
        error={}
        username=request.POST.get("username")
        name=request.POST.get("name")
        email=request.POST.get("email")
        phonenumber=request.POST.get("phonenumber")
        password=request.POST.get("password")
        repassword=request.POST.get("repassword")
        

        already_presentuser = None
        try:
            already_presentuser = Customers.objects.get(username = username)
            
        except:
            pass

        

        if not username.isalpha():
           error["username"]="Name can't have numbers"

        elif len(username)<4:
           
            error["username"]="Username should contain minimum four characters"

        elif not name.isalpha() :
            
            error["name"]="Name can't have numbers"
            
        elif already_presentuser:
            
            error["username"]="Username already taken.Please choose any other"
            
        elif len(username)>10:
            
            error["username"]="Username can only have upto 10 characters"
            
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            
            error["email"]="Invalid Email"

        elif phonenumber.isalpha()==True:
            
            error["phonenumber"]="Phonenumber can't have letters"

        elif not re.match(r"^\d{10}$",phonenumber):
            
            error["phonenumber"]="Invalid Phone number"

        elif Customers.objects.filter(email=email):
            
            error["email"]="Email already exists! Please Use a different email"

        elif len(password)<6:
            
            error["password"]="Password must atleast contain 6 characters"

        elif len(password)>12:
            
            error["password"]="Password can only have upto 12 characters"
            
        elif password!=repassword:
            
            error["repassword"]="Passwords doesn't match to Confirm password!" 

        

        elif len(phonenumber)!=10:
            
            error["phonenumber"]="Invalid Phonennumber"

        elif phonenumber[0]==0:
            
            error["phonenumber"]="Invalid Phone number"

        elif int(phonenumber)<0:
            
            error["phonenumber"]="Phone number can't be negative value" 

        elif Customers.objects.filter(phonenumber=phonenumber):
            
            error["phonenumber"]="Phone number already exists! Please Use a differnet number"
        
        else:
            request.session["contactno"] = phonenumber
            res=Customers(username=username,email=email,password=password,repassword=repassword,phonenumber=phonenumber,name=name)
            res.save()
            
            msg="Signup Successfull"
            return redirect('otp_ph_login')
        
        datas={"error":error,"username":username,"name":name,"email":email,"phonenumber":phonenumber,"password":password,"repassword":repassword,}
        
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
    #     return redirect('home')
     
    if request.method=="POST":
        phonenumber=request.POST["phonenumber"]
        cust=Customers.objects.filter(phonenumber=phonenumber).count()
        if cust==0:
            error="Phonenumber not registered"
            return render(request,"otp_ph_login.html",{"error":error})
        else:
            
            otp = generate_otp()
            
            request.session['U_otp'] = otp
            request.session['U_phone'] = phonenumber
            
            send_otp(phonenumber, otp)
            return redirect('otp_veryfy')
            
    return render(request,"otp_ph_login.html")
           
        
def send_otp(phonenumber, otp):
    # url = ' https://www.fast2sms.com/dev/bulkV2'
    # payload = f'sender_id=TXTIND&message={otp}&route=v3&language=english&numbers={phonenumber}'
    # headers = {
    #     'authorization': "1SYNLFJ7EK6H5YFAa4o6xbIf2A1Zjgr07Wci1XoHedRgK1SPny4i09DlUqjC",
    #     'Content-Type': "application/x-www-form-urlencoded"
    # }
    # response = requests.request("POST", url, data=payload, headers=headers)
    # print(response.text)
        

        url = "https://www.fast2sms.com/dev/bulkV2"

        querystring = {"authorization":"1SYNLFJ7EK6H5YFAa4o6xbIf2A1Zjgr07Wci1XoHedRgK1SPny4i09DlUqjC","variables_values":otp,"route":"otp","numbers":phonenumber}

        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

def otp_verify(request):
    msg1="OTP sent. "
    msg2="Please enter the OTP received in your phone below."
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        if 'U_otp' in request.session and 'U_phone' in request.session:
            exact_otp = request.session['U_otp']
            phonenumber = request.session['U_phone']
            if exact_otp == user_otp:
                try:
                    
                    user = Customers.objects.get(phonenumber=phonenumber)
                    
                    if user is not None:

                        request.session['username'] = user.username 
                        request.session['phonenumber'] = phonenumber
                        # messages.success(request, "Login completed successfully")
                        return redirect('login-page')
                except Customers.DoesNotExist:
                    messages.error(request, "This User doesn't Exist")
            else:
                # messages.error(request, "Invalid OTP. Please try again.")
                error="Otp doesn't match!"
                return render(request,"otp_veryfy.html",{"msg1":msg1,"msg2":msg2,"error":error})
    return render(request,"otp_veryfy.html",{"msg1":msg1,"msg2":msg2})


    

def resend_otp(request):
    msg1="OTP sent. "
    msg2="Please enter the OTP received in your phone below."
    
    Uphonenumber = request.session.get('U_phone')
    phonenumber=None
    if 'phonenumber' in request.session:
            phonenumber = request.session['phonenumber']
            
    print(Uphonenumber,phonenumber)
    if Uphonenumber or phonenumber:

        new_otp = generate_otp()
        if phonenumber is not None:
            send_otp(phonenumber, new_otp)
        else:
            send_otp(Uphonenumber,new_otp)

        request.session['U_otp'] = new_otp
        request.session['otp'] = new_otp
        messages.success(request, "OTP resent successfully. Please check your phone.")

        if 'phonenumber' in request.session:
            print('phone number in session sendotp')
            return redirect('forg_verify_otp')
        
        return redirect('otp_veryfy')
    
            
    return render(request, "otp_veryfy.html", {"msg1": msg1, "msg2": msg2})               

    

# def forgot_password(request):
    
#     return render(request,"forgot_pass.html")


def category_products(request,id):
     
     category_s = Category.objects.get(id=id)
     product_s = Products.objects.filter(category=category_s)
     context={"category_s":category_s,"product_s":product_s}
     
     return render(request,'products.html',context)

def single_products_details(request,id):

    product = Products.objects.filter(id = id).first()
    context = {'product':product}
    return render(request,'single-product-details.html',context)


def forg_pass(request):
    if request.method == "POST":
        
        phonenumber=request.POST["phonenumber"]
        user = Customers.objects.filter(phonenumber=phonenumber).count()
        if user == 0:
            error="Phonenumber not registered"
            return render(request,"forgot_pass.html",{"error":error})
        
        else :

            # Generate and send OTP (you should implement send_otp)
            otp = generate_otp()

            # Store the OTP in the session for verification later
            request.session['otp'] = otp
            request.session['phonenumber'] = phonenumber

            send_otp(phonenumber, otp)
            return redirect('forg_verify_otp')
        
    return render(request, "forgot_pass.html")



# from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
# from django.contrib import messages
# import random     

def forg_verify_otp(request):
   

    if request.method == "POST":
        user_otp = request.POST.get("otp")
        print(user_otp,'otp')
        stored_otp = request.session.get('otp')
        print(stored_otp,'session otp')
        phonenumber = request.session.get('phonenumber')
        print(phonenumber,'phone')
        
        if user_otp == stored_otp:
            # If OTP is correct, allow the user to reset their password
            return render(request, "forgot_reset_pass.html", {"phonenumber": phonenumber})
        else:
            error = "Incorrect OTP. Please try again."
            request.session['otp']= generate_otp()
            send_otp(phonenumber,request.session['otp'])
            p_session=request.session['phonenumber']=phonenumber
            p_usession=request.session['U_phone']=phonenumber
            print(p_session,p_usession)
            
            return render(request, "forgot_verify.html", {"error": error})

    return render(request, "forgot_verify.html")

def forg_reset_password(request):
    if request.method == "POST":
        phonenumber = request.POST.get("phonenumber")
        print(phonenumber)
        password = request.POST.get("password")
        print(password)
        confirm_password = request.POST.get("confirm_password")
        print(confirm_password)

        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render(request, "forgot_reset_pass.html", {"error": error})

        try:
            user = Customers.objects.get(phonenumber=phonenumber)
            print(user)
        except Customers.DoesNotExist:
            error = "User's phone number does not exist in the database."
            return render(request, "forgot_reset_pass.html", {"error": error})

        # Update the user's password (you should hash the password before saving it)
        user.password = confirm_password
        user.save()

        messages.success(request, "Password reset successfully. You can now log in with your new password.")
        return redirect("login-page")  # Redirect to your login page

    return render(request, "forgot_reset_pass.html")








