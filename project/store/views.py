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
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from datetime import date
# from PIL import Image
# from io import BytesIO
# from django.core.files.base import ContentFile


# from .utils import generate_otp, send_otp


# Create your views here.

def index(request):

    allcategories=Category.objects.filter(isblocked=False)
    allproducts=Products.objects.all()
    context={"allcategories":allcategories,"allproducts":allproducts}
    return render(request,'index.html',context)

     
    #  pricerange=1000

    #  Category.objects.filter(price_gte=pricerange)
     

def category_products(request,id):
     
     category_s = Category.objects.get(id=id)
     product_s = Products.objects.filter(category=category_s)
     context={"category_s":category_s,"product_s":product_s}
     
     return render(request,'products.html',context)

# def single_products_details(request, id):
#     product = get_object_or_404(ZoomProduct, id=id)
#     return render(request, 'single-product-details.html', {'product': product})

def single_products_details(request,id):
    product = Products.objects.filter(id = id).first()
    context = {'product':product}
    return render(request,'single-product-details.html',context)

# def add_to_cart(request):
#     if request.method == 'POST':
#         if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
#             userobj = Customers.objects.get(username=request.session["username"])
#             product_id = request.POST.get('product_id')

#             try:
#                 product = Products.objects.get(id=product_id)
#             except Products.DoesNotExist:
#                 return redirect('home')  # Redirect to the home page or handle this case as needed

#             # Check if the product is already in the user's cart
#             existing_cart_item = Cart.objects.filter(user=userobj, product=product).first()

#             if existing_cart_item:
#                 existing_cart_item.quantity += 1  # Increment the quantity if it already exists
#                 existing_cart_item.save()
#             else:
#                 # Create a new cart item for the product
#                 cart_item = Cart(user=userobj, product=product, quantity=1, total=product.price)
#                 cart_item.save()

#             messages.success(request, 'Item added to cart')
#             return redirect('home')  # Redirect to the home page or handle this as needed
#         else:
#             return redirect('login-page')
#     else:
#         return redirect('home')  # Redirect to the home page or handle this as needed

def add_to_cart(request):
    if request.method == 'POST':
        if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
            userobj = Customers.objects.get(username=request.session["username"])
            product_id = request.POST.get('product_id')

            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                return redirect('home')  # Redirect to the home page or handle this case as needed

            # Check if the product is already in the user's cart
            existing_cart_item = Cart.objects.filter(user=userobj, product=product).first()

            if existing_cart_item:
                existing_cart_item.quantity += 1  # Increment the quantity if it already exists
                existing_cart_item.total = existing_cart_item.quantity * product.price  # Calculate the new total
                existing_cart_item.save()
               
            else:
                # Create a new cart item for the product
                cart_item = Cart(user=userobj, product=product, quantity=1, total=product.price)
                cart_item.save()

            messages.success(request, 'Item added to cart')
            return redirect('home')  # Redirect to the home page or handle this as needed
        else:
            return redirect('login-page')
    else:
        return redirect('home')  # Redirect to the home page or handle this as needed

    
def view_cart(request):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        userobj = Customers.objects.get(username=request.session["username"])
        cartobjs = Cart.objects.filter(user=userobj)

        # Calculate the total for each cart item
        for item in cartobjs:
            item.total = item.quantity * item.product.price

        totalsum = sum(item.total for item in cartobjs)
        no_of_cart_items = cartobjs.count()
        wishlistobjs = Wishlist.objects.filter(user=userobj)
        no_of_wishlist_items = wishlistobjs.count()

        return render(request, "cart.html", {
            "cartobjs": cartobjs,
            "totalsum": totalsum,
            "no_of_cart_items": no_of_cart_items,
            "no_of_wishlist_items": no_of_wishlist_items
        })
    else:
        return redirect('login-page')


def delete_cart_item(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')

        # Assuming you have a Cart model
        cart_item = get_object_or_404(Cart, id=cart_id)

        # Delete the cart item
        cart_item.delete()

        # You can also calculate the new total or do any other necessary actions here

        # Redirect to the cart view or any other page you prefer
        return redirect('cart')  # Redirect to the cart page or any other page

    # Handle other HTTP methods as needed
    return redirect('cart')  # Redirect to the cart page or any other page

def add_to_wishlist(request):
    if request.method == 'POST':
        if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
            userobj = Customers.objects.get(username=request.session["username"])
            product_id = request.POST.get('product_id')
            
        
            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                return redirect('home')  # Redirect to the home page or handle this case as needed

            # Check if the product is already in the user's wishlist
            existing_wishlist_item = Wishlist.objects.filter(user=userobj, product=product).first()

            if existing_wishlist_item:
                messages.info(request, 'Item already in wishlist')
            else:
                # Create a new wishlist item for the product
                wishlist_item = Wishlist(user=userobj, product=product)
                wishlist_item.save()
                messages.success(request, 'Item added to wishlist')

            return redirect('home')  # Redirect to the home page or handle this as needed
        else:
            return redirect('login-page')
    else:
        return redirect('home')  # Redirect to the home page or handle this as needed
    
def view_wishlist(request):
    if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
        userobj = Customers.objects.get(username=request.session["username"])
        wishlistobjs = Wishlist.objects.filter(user=userobj)

        return render(request, "wishlist.html", {
            "wishlistobjs": wishlistobjs,
        })
    else:
        return redirect('login-page')

def delete_wishlist_item(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        # Assuming you have a Cart model
        wishlist_item = get_object_or_404(Wishlist, id=product_id)

        # Delete the cart item
        wishlist_item.delete()

        # You can also calculate the new total or do any other necessary actions here

        # Redirect to the cart view or any other page you prefer
        return redirect('wishlist')  # Redirect to the cart page or any other page

    # Handle other HTTP methods as needed
    return redirect('wishlist')  # Redirect to the cart page or any other page


    
def userprofile(request):
    username = request.session["username"]
    customerobj = Customers.objects.get(username=username)
    orderobjs = Order.objects.filter(user=customerobj)
    addressobjs = Address.objects.filter(customer=customerobj)
    wishlistobjs = Wishlist.objects.filter(user=customerobj)
    cartobjs = Cart.objects.filter(user=customerobj)

    no_of_cart_items = cartobjs.count()
    no_of_wishlist_items = wishlistobjs.count()

    totalsum = 0
    for item in cartobjs:
        totalsum += item.total

    ordernumberobjs = Orders_details.objects.filter(user=customerobj)

    # Get a list of all customer objects
    customerobj_list = Customers.objects.filter(username=username)

    context = {
        "ordernumberobjs": ordernumberobjs,
        "orderobjs": orderobjs,
        "username": username,
        "addressobjs": addressobjs,
        "username": username,
        "addressobjs": addressobjs,
        "customerobj": customerobj,
        "cartobjs": cartobjs,
        "totalsum": totalsum,
        "no_of_cart_items": no_of_cart_items,
        "no_of_wishlist_items": no_of_wishlist_items,
        "customerobj_list": customerobj_list,  # Pass the list of customer objects
    }
    return render(request, "userprofile.html", context)


def edituserdetails(request,user_id):
     # Check if the user has permission to edit the details (you can customize this part)
    # if request.user.id != user_id:
    #     return HttpResponse("You don't have permission to edit this user's details")

    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phonenumber = request.POST["phonenumber"]

        customerobj = Customers.objects.get(id=user_id)
        
        customerobj.name = name
        customerobj.email = email
        customerobj.phonenumber = phonenumber
        customerobj.save()
        return redirect('userprofile')

    customerobj = Customers.objects.get(id=user_id)
    return render(request, 'edituserdetails.html', {'customerobj': customerobj})

##############################error#################################
def Add_address(request):
    if request.method == "POST":
        house = request.POST.get("house")
        locality = request.POST.get("locality")
        district = request.POST.get("district")
        state = request.POST.get("state")
        country = request.POST.get("country")
        pincode = request.POST.get("pincode")
        customer = Customers.objects.get(username=request.session["username"])

        new_address = Address.objects.create(
            house=house,
            locality=locality,
            district=district,
            state=state,
            country=country,
            pincode=pincode,
            customer=customer 
        )

        return redirect('userprofile')

    return render(request, 'add_address.html')
##############################error#################################

def Edit_address(request,myid):
    
    addressobjs = Address.objects.get(id=myid)
 
    house=addressobjs.house
    locality=addressobjs.locality
    state=addressobjs.state
    country=addressobjs.country
    pincode=addressobjs.pincode
    district=addressobjs.district
    # id=addressobjs.id

    if request.method == "POST":
        addressobjs = Address.objects.get(id=myid)
        house = request.POST["house"]
        locality = request.POST["locality"]
        district = request.POST["district"]
        state = request.POST["state"]
        country = request.POST["country"]
        pincode = request.POST["pincode"]

        addressobjs.house=house
        addressobjs.locality=locality
        addressobjs.district=district
        addressobjs.state=state
        addressobjs.country=country
        addressobjs.pincode=pincode

        addressobjs.save()
        return redirect('userprofile')


    return render(request, 'edit_address.html',{"house":house,"locality":locality,"state":state,"country":country,"pincode":pincode,"district":district }) 
    


def checkout(request):
    username = request.session["username"]
    customer = Customers.objects.get(username=username)
    addressobjs = Address.objects.filter(customer=customer)


    cartobj = Cart.objects.filter(user=customer)
    subtotal=0
    for item in cartobj:
        subtotal+=item.total

    
    

    context = {
        'cartobj':cartobj,
        'subtotal':subtotal,
        'addressobjs':addressobjs
    }

    return render(request,'checkout.html',context)
    
def Cash_on_delivery(request):
    if request.method=="POST":

        username = request.session["username"]
        customer = Customers.objects.get(username=username)
        cartobj = Cart.objects.filter(user=customer)
        address_house=request.POST.get("address")
        addressobj=Address.objects.get(house=address_house)

        finalprice = 0
        for item in cartobj:
            finalprice += item.total

        orderobj=Order(user=customer,totalamount=finalprice)
        orderobj.save()



        for item in cartobj:
            order_details=Orders_details(user=customer,product=item.product,address=addressobj,ordertype="Cash on Delivery",orderstatus="Confirmed",quantity=item.quantity,finalprice=item.total,ordernumber=orderobj)
            order_details.save()
            

        
        datevalue=date.today()

        # Fetch the order data for the current user
        # order = Orders.objects.filter(user=customer).last()

        context = {
            'addressobj': addressobj,
            'cartobj': cartobj,
            'finalprice': finalprice,
            "date":datevalue,
            
          
        }

        return render(request, 'orderplaced.html',context)


def order_details(request,myid):


    orderobj=Order.objects.get(id=myid)
    order_details_objs = Orders_details.objects.filter(ordernumber=orderobj)



    context = { 'order_details_objs':order_details_objs
      
  }

    return render(request,'order_details.html',context) 

def delete_order(request,myid):
    # username=request.session["username"]
    # user=Customers.objects.get(username=username)
    # orderobj=Order.objects.get(id=myid)
    order_details_objs = Orders_details.objects.get(id=myid)

    order_details_objs.orderstatus="Cancelled"
    order_details_objs.save()

    return redirect('userprofile')




def wallet(request):
    return render(request,'wallet.html')

def deliveredproduct(request):
    return render(request,"deliveredproduct.html")



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
    try:
        if "username" in request.session and not Customers.objects.get(username=request.session["username"]).isblocked:
            return redirect('home')
    except:
        pass
    if request.method=="POST":
            username=request.POST.get("username")
            password=request.POST.get("password")
            if len(username)<4:
                error="Username should contain minimum four characters"

            else:
                try:
                    customer = Customers.objects.get(username=username, password=password)
                    if not customer.isblocked:
                        request.session["username"] = username
                        return redirect('home')
                    else:
                        context = "Account is blocked"
                except Customers.DoesNotExist:
                    context = "Invalid Credentials"

                return render(request, "login.html", {"context": context})

            if error:
                return render(request,"login.html",{"error":error})
                
    if "cartdict" in request.session:
        cartdict=request.session["cartdict"]
        subtotal=0
        for k,v in cartdict.items():
            subtotal+=v["total"]
        cartcount=len(cartdict)
    else:
        cartdict={}
        subtotal=0
        cartcount=0
    if "wishlistdict" in request.session:
        wishlistdict=request.session["wishlistdict"]
        wishcount=len(wishlistdict) 
    else:
        wishcount=0  
    context={"cartdict":cartdict,"totalsum":subtotal,"cartcount":cartcount,"wishcount":wishcount} 
    return render(request,"login.html",context)

# ############################################################################################################################
    
def home(request):
    allcategories=Category.objects.all()
    allproducts=Products.objects.all()
    context={"allcategories":allcategories,"allproducts":allproducts}
    return render(request,'home.html',context)
     
    
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



    





