from django.db import models

# Create your models here.

class Userdet(models.Model):
    userid = models.AutoField(primary_key=True, unique=True,db_column='iduserdet')
    username = models.CharField(max_length=100,db_column='userdetnme')
    useremail = models.CharField(max_length=100,db_column='userdeteml')
    userpass = models.CharField(max_length=100,db_column='userdetpas')
    usermob = models.CharField(max_length=100,db_column='userdetmob')
    ustats=models.CharField(max_length=40, default='inactive',db_column='userdetstat')
    
    class Meta:
        managed = False
        db_table = 'userdet'
        
        
class Expdet(models.Model):
    expid = models.AutoField(primary_key=True, unique=True,db_column='idexpdet')
    idreport = models.CharField(max_length=100,db_column='idrep')
    expuname = models.CharField(max_length=100,db_column='expdetuname')
    expcat = models.CharField(max_length=100,db_column='expdetcat')
    expdes = models.CharField(max_length=100,db_column='expdetdes')
    expdate = models.DateField(db_column='expdetdate')
    expamt = models.IntegerField(db_column='expdetamt')
    empl = models.ForeignKey(Userdet, on_delete=models.CASCADE, db_column='expdetudat')
    
    
    class Meta:
        managed = False
        db_table = 'expdet'
    
    
    
    