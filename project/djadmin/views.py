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

from django.http import FileResponse
import io

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
            datas = Customers.objects.filter(username__icontains=enteredname)
            return render(request,"tadmin/users.html",{"datas":datas})
        
        return render(request,"tadmin/users.html",{"datas":datas})
    else:
        return redirect('login')
    

def adminCategory(request):
    return render(request,"tadmin/categories/categories.html")

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

@never_cache
def adminProducts(request):
   if "username" in request.session:
        datas=Products.objects.all()
        if request.method=="POST":
            enteredproduct=request.POST.get("searchitem")
            datas=Products.objects.filter(name__icontains=enteredproduct)
            return render(request,"tadmin/products/products.html",{"datas":datas})
        return render(request,"tadmin/products/products.html",{"datas":datas})
   else:
        return render(request,"tadmin/products/products.html")

    