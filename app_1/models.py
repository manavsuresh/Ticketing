from django.db import models
from datetime import datetime,date
# Create your models here.
    
class Credentials(models.Model):
    # id = models.AutoField(unique=True,blank=False,auto_created=True,primary_key=True)
    name = models.CharField(max_length=255,blank=False)
    emp_id = models.CharField(max_length=20,blank=False,default="Not Given")
    email = models.CharField(max_length=255,default='Not Given')
    phone = models.CharField(max_length=50,default='Not Given',blank=False)
    u_id = models.CharField(max_length=255,unique=True,blank=False,primary_key=True)
    password = models.CharField(max_length=255,default='1234')
    unit = models.CharField(max_length=255,blank=False,default='-')
    dept = models.CharField(max_length=255,default='Client',blank=False)
    status = models.CharField(max_length=50,default='Active',auto_created=True,blank=False)

class todo(models.Model):
    date = models.CharField(max_length=100,default=date.today(), auto_created=True,blank=False)
    name =  models.CharField(max_length=255)
    emp_id = models.CharField(max_length=50,blank=False,default="Not Given")
    unit = models.CharField(max_length=100,blank=False,default='-')
    task_subject = models.CharField(max_length=255)
    task_dets = models.CharField(max_length=2000,default='',auto_created=True)
    progress = models.CharField(max_length=50,default=False,auto_created=True,blank=False)
    department = models.CharField(max_length=255,blank=False,default='Unsorted')
    feedback = models.CharField(max_length=1000,default='',auto_created=True,blank=False)
    remark = models.CharField(max_length=1000,blank=False,default='',auto_created=True)
    phone = models.CharField(max_length=50,default='Not Given',blank=False)
    closed = models.CharField(max_length=100,default='False',auto_created=True,blank=False)
    category = models.CharField(max_length=255,default='Unassigned', auto_created=True,blank=False)