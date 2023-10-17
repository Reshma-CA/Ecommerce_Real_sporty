from django.shortcuts import render,redirect
from django.contrib import messages
from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError
import os
import re
from django.shortcuts import get_object_or_404

from django.http import FileResponse
import io
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

# Create your views here.

@login_required(login_url ="")
def  adminhome(request):
     return render(request,'tadmin/adminhome.html')

def  adminpannel(request):
     return render(request,'tadmin/adminpannel.html')

@never_cache
def adminilogin(request):

     if 'username' in request.session:
          return render(request,'tadmin/adminhome.html')  
     
     if request.method=='POST':
        uname=request.POST.get("username")
        pword=request.POST.get("password")
        
     
        res=authenticate(request,username=uname,password=pword)

        if res is not None:
            request.session['username']=uname
            return render(request,'tadmin/adminhome.html')
        
        else:
            # error="Invalid Credentials"
            # return render(request,"adminlogin.html",{"error":error})
            messages.error(request,"Error in login! Invalid Login details!")
            return render(request,"adminlogin.html")
     return render(request,'adminlogin.html')



def admin_logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('login')


def adminusers(request):

    if "username" in request.session:
        datas=Customers.objects.all()

        if request.method=="POST":
            enteredname=request.POST.get("searchitem")
            datas = Customers.objects.filter(username__istartswith=enteredname)
            return render(request,"tadmin/users.html",{"datas":datas})
        
        return render(request,"tadmin/users.html",{"datas":datas})
    else:
        return redirect('login')
    

def blockuser(request,id):
    
    obj=Customers.objects.get(id=id)
    obj.isblocked=True
    obj.save()
    return redirect('ausers')

def unblockuser(request,id):
    print("unblockuser")
    obj=Customers.objects.get(id=id)
    obj.isblocked=False
    obj.save()
    return redirect('ausers')



def addproducts(request):
    categoryobjs = Category.objects.all()
    error = {}

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        category_name = request.POST.get("category")
        description = request.POST.get("description")
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        image3 = request.FILES.get("image3")
        image4 = request.FILES.get("image4")

        try:
            # Check for minimum length requirements
            if len(name) < 4:
                raise ValidationError("Product name should contain a minimum of four characters")

            # Ensure price and quantity are numeric
            if not price.isdigit():
                raise ValidationError("Price must be a numeric value")
            if not quantity.isdigit():
                raise ValidationError("Quantity must be a numeric value")

            # Check if category exists
            categoryobject = Category.objects.get(name=category_name)
        except (ValidationError, Category.DoesNotExist) as e:
            error["general"] = str(e)
        else:
            # Create the product
            product = Products.objects.create(
                name=name,
                category=categoryobject,
                description=description,
                quantity=quantity,
                price=price,
                image1=image1,
                image2=image2,
                image3=image3,
                image4=image4
            )
            return redirect('aproducts')

    return render(request, "tadmin/products/addproducts.html", {"error": error, "categoryobjs": categoryobjs})

def editproducts(request,myid):
    content = Products.objects.get(id=myid)
    categoryobjs = Category.objects.all()
    error = {}

    if request.method == 'POST':
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        category_name = request.POST.get("category")
        description = request.POST.get("description")

        if len(name) < 4:
            error["name"] = "Product name should contain a minimum of four characters"
    
        else:
            content.name = name
            content.description = description
            content.price = price
            content.quantity = quantity

            # Check if new images are provided
            if 'image1' in request.FILES:
                # Delete the existing image1 file
                if content.image1:
                    os.remove(content.image1.path)
                content.image1 = request.FILES.get('image1')

            if 'image2' in request.FILES:
                # Delete the existing image2 file
                if content.image2:
                    os.remove(content.image2.path)
                content.image2 = request.FILES.get('image2')

            if 'image3' in request.FILES:
                # Delete the existing image3 file
                if content.image3:
                    os.remove(content.image3.path)
                content.image3 = request.FILES.get('image3')

            if 'image4' in request.FILES:
                # Delete the existing image4 file
                if content.image4:
                    os.remove(content.image4.path)
                content.image4 = request.FILES.get('image4')

            # Retrieve the category if it exists, otherwise assign a default category
            try:
                categoryobject = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                error["category"] = "Invalid category"
            else:
                content.category = categoryobject
                content.save()
                return redirect('aproducts')

        if error:
            return render(request, "tadmin/products/editproducts.html", {"content": content, "error": error, "categoryobjs": categoryobjs})

    return render(request, "tadmin/products/editproducts.html", {"content": content, "categoryobjs": categoryobjs})
    

def delete_products(request,myid):
    product = get_object_or_404(Products, id=myid)
    if request.method == 'POST':
        # Delete the product if the request method is POST
        product.delete()
        return redirect('aproducts')  # Redirect to the product list page after deletion
    context = {
        'content': product,
    }

    return render(request, 'tadmin/products/deleteproducts.html', {'content': product})

@never_cache
def adminProducts(request):
   if "username" in request.session:
        datas=Products.objects.all()
        if request.method=="POST":
            enteredproduct=request.POST.get("searchitem")
            datas = Products.objects.filter(name__istartswith=enteredproduct)
            return render(request,"tadmin/products/products.html",{"datas":datas})
        return render(request,"tadmin/products/products.html",{"datas":datas})
   else:
        return redirect('login')
   
@never_cache  
def adminCategory(request):
    # Retrieve all categories from the database
    categories = Category.objects.all()

    if request.method == "POST":
        # Handle the search functionality
        search_item = request.POST.get("searchitem")
        categories = Category.objects.filter(name__istartswith=search_item)

        context = {
        'datas': categories,
    }

    return render(request, "tadmin/categories/categories.html",{'datas':categories})
    
    
    
from django.db import IntegrityError  # Import IntegrityError

def addcategories(request):
    categoryobjs = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        No_of_items = request.POST.get("No_of_items")  # Make sure the 'name' attribute matches your HTML form
        image = request.FILES.get("image")
        error = {}

        if Category.objects.filter(name=name).exists():
            error["name"] = "Same Category name is not allowed"
        elif len(name) > 20:
            error["name"] = "Category name can at most have 20 letters"
        else:
            try:
                added = Category(name=name, No_of_items=No_of_items , image=image)
                added.save()
                return redirect('acategories')
            except IntegrityError:
                error["name"] = "Category with this name already exists"

        return render(request, "tadmin/categories/addcategories.html", {"error": error})

    return render(request, "tadmin/categories/addcategories.html", {"categoryobjs": categoryobjs})



def editcategories(request, myid):
    obj = Category.objects.get(id=myid)
    categoryobjs = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        No_of_items = request.POST.get("No_of_items")  # Use "No_of_items" consistently with your form
        error = {}

        if Category.objects.filter(name=name).exclude(id=myid).exists():
            error["name"] = "Same Category name is not allowed"
        elif len(name) > 20:
            error["name"] = "Category name can have at most 20 letters"
        else:
            obj.name = name
            obj.No_of_items = No_of_items
            if 'image' in request.FILES:
                # Delete the existing image file
                if obj.image:
                    os.remove(obj.image.path)
                obj.image = request.FILES.get('image')
            obj.save()
            return redirect('acategories')
        if error:
            return render(request, "tadmin/categories/editcategories.html", {"obj": obj, "error": error, "categoryobjs": categoryobjs})

    return render(request, "tadmin/categories/editcategories.html", {"obj": obj, "categoryobjs": categoryobjs})

def delete_products(request,myid):
    product = get_object_or_404(Products, id=myid)
    if request.method == 'POST':
        # Delete the product if the request method is POST
        product.delete()
        return redirect('aproducts')  # Redirect to the product list page after deletion
    context = {
        'content': product,
    }

    return render(request, 'tadmin/products/deleteproducts.html', {'content': product})
   
def deletecategories(request, myid):
    category = get_object_or_404(Category,id=myid)
    if request.method == "POST":
        # Delete the product if the request method is POST
        category.delete()
        return redirect('acategories')
    context = {
        'content': category,

    }

    return render(request, "tadmin/categories/deletecategories.html",{'content':category})
  
    
def blockcategories(request,myid):
    content = Category.objects.get(id=myid)
    
    if content.isblocked==True:
        content.isblocked=False
        content.save()
        return redirect('acategories')
    
    elif content.isblocked==False:
        content.isblocked=True
        content.save()
        return redirect('acategories')
    

def orders(request):
    orderobjs=Orders_details.objects.all()
    # if request.method=="POST":
    #     entereddate=request.POST["searchitem"]
    #     orderobjs=Order.objects.filter(orderdate__icontains=entereddate)


    return render(request,"tadmin/orders/orders.html",{"orderobjs":orderobjs})

def edit_order_status(request,myid):
    details = Orders_details.objects.get(id=myid)
    if request.method=="POST":
        orderstatus=request.POST.get("orderstatus")
        details.orderstatus=orderstatus
        details.save()
        return redirect("orders")


    context = {
        'orderobjs':details
    }
    return render(request,'tadmin/orders/edit_order_ststus.html',context)