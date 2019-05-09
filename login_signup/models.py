from django.db import models

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
    time_start = models.TimeField(blank=True,null=True)
    time_end = models.TimeField(blank=True, null=True)
