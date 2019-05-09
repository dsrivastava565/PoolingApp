from django.db import models
from decimal import Decimal
class MyUser(models.Model):
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=1000)
    uniq_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=250,default='KIET123')
    gender = models.CharField(max_length=250,null=True)
    email = models.CharField(max_length=250, null=True)
    mobile = models.CharField(max_length=20,null=True)


class CarDetails(models.Model):
    carname = models.CharField(max_length=100)
    cardetailsId =models.AutoField(primary_key=True)
    carseats = models.IntegerField()
    addedBy = models.ForeignKey(MyUser,null=True,on_delete=models.SET_NULL)
    carNumber = models.CharField(max_length=100,null=True)

class startPooling(models.Model):
    startPoolingId = models.AutoField(primary_key=True)
    carPooled = models.ForeignKey(CarDetails,null=True,on_delete=models.SET_NULL)
    pooledbyid= models.ForeignKey(MyUser,null=True,on_delete=models.SET_NULL)
    time_start = models.CharField(max_length=20,null=True)
    time_end = models.CharField(max_length=20, null=True)
    latitude = models.CharField(max_length=20,null=True)
    longitude = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=100,null=True)
    seats = models.IntegerField(null=True)
    

# class AllPoolers(models.Model):
#     poolid = models.AutoField(primary_key=True)
#     poolerid = models.ForeignKey(MyUser,null=True,on_delete=models.SET_NULL)


class userPooling(models.Model):
    userPoolingId = models.AutoField(primary_key=True)
    userPooled = models.ForeignKey(MyUser,null=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=20,null=True)
    poolingwithid = models.ForeignKey(startPooling,null=True,on_delete=models.SET_NULL)

