from django.db import models

# Create your models here.
class HCA_details(models.Model):
    name=models.CharField(max_length=10,default=None)
    FAD=models.FloatField()
    T_H_In=models.FloatField()
    P_input=models.FloatField()
    Q_input=models.FloatField()

class users(models.Model):
    name=models.CharField(max_length=100,default=None)
    userID=models.CharField(max_length=100,default=None)
    Email=models.EmailField(max_length=100,default=None)
    Phone=models.CharField(max_length=100,default=None)
    DOB=models.DateField()
    password=models.CharField(max_length=200,default=None)

class Registration_Approval(models.Model):
    UserID=models.CharField(max_length=100,default=None)
    Email=models.EmailField(max_length=100,default=None)
    Aprove=models.IntegerField(default=1)

class Reset_password_Approval(models.Model):
    UserID=models.CharField(max_length=100,default=None)
    Email=models.EmailField(max_length=100,default=None)
    Password=models.CharField(max_length=200,default=None)
    Aprove=models.IntegerField(default=0)

class CD26_airend_data(models.Model):
    Model_id=models.CharField(max_length=100,default=None)
    P=models.FloatField()
    p_S1 = models.FloatField()
    p_S2= models.FloatField()
    FAD = models.FloatField()
    Q_sh = models.FloatField()
    Pr_ratio_stg1 = models.FloatField()
    Pr_ratio_stg2 = models.FloatField()
    n_stg1 = models.FloatField()
    n_stg2 = models.FloatField()

class CD26_airend_data_rated(models.Model):
    Model_id=models.CharField(max_length=100,default=None)
    rated_P=models.FloatField()
    Max=models.FloatField(default=0)
    T_W_out=models.FloatField(default=0)