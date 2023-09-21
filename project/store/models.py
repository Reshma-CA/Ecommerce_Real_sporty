from django.db import models
import datetime

# Create your models here.


class Customers(models.Model):
    username=models.CharField(max_length=200,unique=True)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phonenumber=models.IntegerField()
    password=models.CharField(max_length=200)
    repassword=models.CharField(max_length=200)
    isblocked=models.BooleanField(default=False)


class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)
    image=models.ImageField(upload_to='store/categories/', blank=True)
    No_of_items=models.IntegerField()
    isblocked=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Products(models.Model):
    name=models.CharField(max_length=200,unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    image1=models.ImageField(upload_to='store/products/', blank=True)
    image2=models.ImageField(upload_to='store/products/', blank=True)
    image3=models.ImageField(upload_to='store/products/', blank=True)
    image4=models.ImageField(upload_to='store/products/', blank=True)

