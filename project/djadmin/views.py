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

import os
import re


from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
# import xlsxwriter

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
        print(request.POST)
        name = request.POST.get("name",None)
        No_of_items = request.POST.get("No_of_items",None)  # Make sure the 'name' attribute matches your HTML form
        image = request.FILES.get("image",None)
        error = {}
        if name == None or No_of_items == None or image == None:
            error['empty']="Can't submit empty form"
            return render(request, "tadmin/categories/addcategories.html", {"error": error})
        

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
    if request.method=="POST":
        entereddate=request.POST.get("searchitem")
        orderobjs=Orders_details.objects.filter(orderdate__istartswith=entereddate)
        return render(request,"tadmin/orders/orders.html",{"orderobjs":orderobjs})


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


@never_cache
def categoryoffer(request):
    catofferobjs=Categoryoffer.objects.all()
    if request.method=="POST":
            enteredoffer=request.POST.get("searchitem")
            catofferobjs=Categoryoffer.objects.filter(category__name__istartswith= enteredoffer) 
            context={"catofferobjs":catofferobjs}
            return render(request,"tadmin/categoryoffer/categoryoffer.html",context)

    context={"catofferobjs":catofferobjs}
    return render(request,'tadmin/categoryoffer/categoryoffer.html',context)


def addcategoryoffer(request):
    
    categoryobjs=Category.objects.all()
    

    if request.method=="POST":
        categoryname=request.POST["categoryname"]
        offer=request.POST["offer"]
        discount=request.POST["discount"]
       
  
        categoryobj=Category.objects.get(name=categoryname)
        catofferobj=Categoryoffer(category=categoryobj,offer_description=offer,discount=discount)
        catofferobj.save()
        
        
        return redirect('categoryoffer')
    context={"categoryobjs":categoryobjs}
    
    return render(request,"tadmin/categoryoffer/addcategoryoffer.html",context)

def editcategoryoffer(request,myid):
    catofferobj=Categoryoffer.objects.get(id=myid)
    categoryobjs=Category.objects.all()
    if request.method=="POST":

        
        categoryname=request.POST["categoryname"]
        offer_description=request.POST["offer_description"]
        discount=request.POST["discount"]
        categoryobj=Category.objects.get(name=categoryname)

        catofferobj.category=categoryobj
        catofferobj.offer_description=offer_description
        catofferobj.discount=discount
        catofferobj.save()



        return redirect(categoryoffer)
    context={"catofferobj":catofferobj,"categoryobjs":categoryobjs}
    return render(request,"tadmin/categoryoffer/edit_category_offer.html",context)

def deletecategory_offer(request, myid):
    categoryoffer = get_object_or_404(Categoryoffer,id=myid)
    
   
    if request.method == "POST":
        # Delete the product if the request method is POST
        categoryoffer.delete()
        return redirect('categoryoffer')
    context = {
        'content': categoryoffer,
        

    }

    return render(request, "tadmin/categoryoffer/delete_category_offer.html",{'content':categoryoffer})

def productoffer(request):
    pdtofferobjs=Productoffer.objects.all()
    if request.method=="POST":
            enteredoffer=request.POST.get("searchitem")
            pdtofferobjs=Productoffer.objects.filter(product__name__istartswith=enteredoffer)
            context={"pdtofferobjs":pdtofferobjs}
            return render(request,"tadmin/product_offer/product_offer.html",context)

    context={"pdtofferobjs":pdtofferobjs}
    return render(request,"tadmin/product_offer/product_offer.html",context)

def add_product_offer(request):
    
    productobjs=Products.objects.all()
    context={"productobjs":productobjs}

    if request.method=="POST":
        productname=request.POST["productname"]
        offer=request.POST["offer"]
        discount=request.POST["discount"]


        productobj=Products.objects.get(name=productname)
        productofferobj=Productoffer(product=productobj,offer_description=offer,discount=discount)
        productofferobj.save()
        return redirect('productoffer')
    return render(request,"tadmin/product_offer/add_product_offer.html",context)

def edit_product_offer(request,myid):
    pdtofferobj=Productoffer.objects.get(id=myid)
    productobjs=Products.objects.all()
    if request.method=="POST":

        
        productname=request.POST["productname"]
        offer_description=request.POST["offer_description"]
        discount=request.POST["discount"]
        productobj=Products.objects.get(name=productname)

        pdtofferobj.product=productobj
        pdtofferobj.offer_description=offer_description
        pdtofferobj.discount=discount
        pdtofferobj.save()



        return redirect('productoffer')
    context={"pdtofferobj":pdtofferobj,"productobjs":productobjs}
    return render(request,"tadmin/product_offer/edit_product_offer.html",context)
  
def delete_product_offer(request, myid):
    productoffer = get_object_or_404(Productoffer,id=myid)
    
   
    if request.method == "POST":
        # Delete the product if the request method is POST
        productoffer.delete()
        return redirect('productoffer')
    context = {
        'content': productoffer,
        

    }

    return render(request, "tadmin/product_offer/delete_product_offer.html",{'content':productoffer})

def coupons(request):  
    couponobjs=Coupon.objects.all()
    if request.method=="POST":
            enteredcoupon=request.POST.get("searchitem")
            couponobjs=Coupon.objects.filter(code__icontains=enteredcoupon)
            return render(request,"tadmin/coupons/coupons.html",{"couponobjs":couponobjs})
    return render(request,"tadmin/coupons/coupons.html",{"couponobjs":couponobjs})

def add_coupon(request):

    if request.method=="POST":

        code=request.POST["code"]
        discount_percent=request.POST["discount_percent"]
        minprice=request.POST["minprice"]
        maxprice=request.POST["maxprice"]
        is_available=request.POST["is_available"]
        
        if is_available == "Yes":
            is_available=True
        else:
            is_available=False
        coup=Coupon(code=code,discount_percentage=discount_percent,minprice=minprice,maxprice=maxprice,is_available=is_available)
        coup.save()
        return redirect('coupons')
    return render(request,"tadmin/coupons/add_coupon.html")

def edit_coupon(request,myid):
    couponobj=Coupon.objects.get(id=myid)
    
    if request.method=="POST":

        
        code=request.POST["code"]
        discount_percentage=request.POST["discount_percentage"]
        minprice=request.POST["minprice"]
        maxprice=request.POST["maxprice"]
        is_available=request.POST["is_available"]
        if is_available=="Yes":
            is_available=True
        else:
            is_available=False
        

        couponobj.code=code
        couponobj.discount_percentage=discount_percentage
        couponobj.minprice=minprice
        couponobj.maxprice=maxprice
        couponobj.is_available=is_available
        couponobj.save()



        return redirect('coupons')
    context={"couponobj":couponobj}
    return render(request,"tadmin/coupons/edit_coupons.html",context)

def delete_coupon(request, myid):
    coupon_offer = get_object_or_404(Coupon,id=myid)
    
   
    if request.method == "POST":
        # Delete the product if the request method is POST
        coupon_offer.delete()
        return redirect('coupons')
    context = {
        'content': coupon_offer,
        

    }

    return render(request, "tadmin/coupons/delete_coupons.html",{'content':coupon_offer})




def salesreport(request):
    if request.method=="POST":
        if "show" in request.POST:
            start_date=request.POST.get("start_date")
            end_date=request.POST.get("end_date")
            orderobjs = Orders_details.objects.filter(orderdate__range=[start_date, end_date])
            if orderobjs.count()==0:
                message="Sorry! No orders in this particular date range"
                context={"orderobjs":orderobjs,"message":message}
            else:

                context={"orderobjs":orderobjs}
            return render(request,"tadmin/sales_report.html",context)
        elif "download" in request.POST:
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter)
            elements = []

            # Add heading
            styles = getSampleStyleSheet()
            heading_style = styles['Heading1']
            heading = "Sales Report"
            heading_paragraph = Paragraph(heading, heading_style)
            elements.append(heading_paragraph)
            elements.append(Spacer(1, 12))  # Add space after heading

            ords = Orders_details.objects.filter(orderdate__range=[start_date, end_date])
            

            if ords:
                data = [['Sl.No.', 'Name', 'Product', 'House', 'Order Date', 'Order Status', 'Quantity']]
                slno = 0
                for ord in ords:
                    slno += 1
                    row = [slno, ord.user.name, ord.product.name, ord.address.house, ord.orderdate, ord.orderstatus, ord.quantity]
                    data.append(row)

                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))

                elements.append(table)
            else:
                elements.append(Paragraph("No orders", styles['Normal']))
            if elements:

                doc.build(elements)
                buf.seek(0)
                return FileResponse(buf, as_attachment=True, filename='Orders.pdf')
            
    return render(request,"tadmin/sales_report.html")