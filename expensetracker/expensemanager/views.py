from collections import defaultdict
import datetime
import os
import random
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Expdet, Userdet
from django.db.models import Sum
import matplotlib.pyplot as plt
from collections import defaultdict





# Create your views here.
def home(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Userdet.objects.filter(username=username,userpass=password).exists():
            status=Userdet.objects.filter(username=username).update(ustats='active')
            stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
        
        # if user is not None:
        #     login(request,user)
            request.session['username'] = username
            messages.success(request, "Logged in")
            
            return render(request, 'hmain.html', {'stat':stat})
        
        else:
            messages.success(request,"There was an error, pls try again")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

# def login_user(request):
#     pass



def logout_user(request):
    username=request.session.get('username')
    logout(request)
    status=Userdet.objects.filter(username=username).update(ustats='active')
    
    messages.success(request, "You have been logged out")
    return redirect('home')




def signup(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        useremail=request.POST.get('emailid')
        password = request.POST.get('password')
        contnum = request.POST.get('phnum')
        print(username,useremail,password)
        userdetails=Userdet.objects.create(username=username,useremail=useremail,userpass=password,usermob=contnum)
        return redirect('home')
        
    else:
        return render(request, 'register.html', {})
    
    


def homemain(request):
    username=request.session.get('username')
    stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
    return render(request, 'hmain.html', {'stat':stat})
    
    
    
def dashboard(request):
    username=request.session.get('username')
    stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
    expdetail=Expdet.objects.filter(expuname=username)
    total = Expdet.objects.filter(expuname=username).aggregate(total_amount=Sum('expamt'))['total_amount'] or 0
    category_totals = Expdet.objects.filter(expuname=username).values('expcat').annotate(total_amount=Sum('expamt'))
    
    return render(request, 'dashboard.html', {'stat':stat,'expdetail':expdetail,'total':total,'categorytotals':category_totals})


def addexp(request):
    username=request.session.get('username')
    stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
    if 'requestid' in request.session:
            requestid = request.session['requestid']
            print("ifrequestid")
    else:
        date = datetime.datetime.now()
        id_prefix = "EXPDAT" + date.strftime("%Y%m%d")
        id_suffix = str(random.randint(1000, 9999))
        requestid=id_prefix+'-'+id_suffix
        request.session['requestid'] = requestid
        
    if request.method == 'POST' :
        repid = request.POST.get('repid')
        uname=request.POST.get('username')
        category = request.POST.get('category')
        desc = request.POST.get('desc')
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        print(repid,uname,category,desc,date,amount)
        expdetails=Expdet.objects.create(idreport=repid,expuname=uname,expcat=category,expdes=desc,expdate=date,expamt=amount)
        return redirect('dashboard')
        
    return render(request, 'addexpform.html', {'username':username,'stat':stat,'requestid':requestid})




def reportgen(request):
    username=request.session.get('username')
    stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
    
    
    return render(request, 'reportgen.html', {'username':username,'stat':stat})
    
    
    
def totaldata(request):
    username=request.session.get('username')
    stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
    expdetail=Expdet.objects.filter(expuname=username)
    total = Expdet.objects.filter(expuname=username).aggregate(total_amount=Sum('expamt'))['total_amount'] or 0
    
    return render(request, 'totaldata.html', {'username':username,'stat':stat,'expdetail':expdetail,'total':total})




def daterange(request):
    username=request.session.get('username')
    stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
    if request.method == 'POST' :
        fdate = request.POST.get('fdate')
        tdate = request.POST.get('tdate')
        expenses = Expdet.objects.filter(expuname=username,expdate__range=[fdate, tdate])
        return render(request, 'daterange.html', {'stat':stat,'expenses':expenses})
    else:
        return render(request, 'daterange.html', {'stat':stat})




def categorydata(request):
    username=request.session.get('username')
    stat=Userdet.objects.filter(username=username).values('ustats')[0]['ustats']
    expenses = Expdet.objects.filter(expuname=username)
    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense.expcat] += float(expense.expamt)

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    category_totals = Expdet.objects.filter(expuname=username).values('expcat').annotate(total_amount=Sum('expamt'))
    context = {'categories': categories, 'amounts': amounts,'stat':stat,'categorytotals':category_totals}
    
    
    return render(request, 'categorydata.html', context)
    

    