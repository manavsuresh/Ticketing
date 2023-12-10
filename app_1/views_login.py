from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Credentials, todo
from . import views
from . import views_ticketing
import logging
from django.core.mail import send_mail
from django.conf import settings


logger = logging.getLogger(__file__)

message = {}

usr = None
nme = None
unt = None
details = {}

def dets():
    return details

def login(request):
    global message

    logger.info(views.get_ip(request))
   
    template = loader.get_template('login.html')
    try:
        message1 = message[views.get_ip(request)]
    except KeyError:
        message1 = ''
    mess = {
        'message' : message1,
    }
    return HttpResponse(template.render(mess,request))

def login_check(request):
    global usr,nme,details,message,unt
    a = request.POST['UID']
    b = request.POST['password']
    login_vals = Credentials.objects.all().filter(status='Active').values()
    for i in login_vals:
        if i['u_id'] == a and i['password'] == b:
            usr = i['dept']
            nme = i['name']
            unt = i['unit']
            eid = i['emp_id']
            phone = i['phone']
            ip = views.get_ip(request)    
            details[ip] = [usr,nme,unt,eid,phone]
            detail = [ip,usr,nme,eid,unt]
            logger.info(detail)
            message[views.get_ip(request)] = ''
            if usr.lower() ==  'admin':
                if nme.lower() == 'manav':
                    send_mail(subject='Login of superuser',message=f'From {ip}',recipient_list=['manavsuresh.04@gmail.com'],fail_silently=True,from_email=settings.EMAIL_HOST_USER)

            return HttpResponseRedirect('/index/todo/')
    message[views.get_ip(request)] = 'Wrong Credentials!!'
    return HttpResponseRedirect('/')

def logout(request):
    global usr,nme,details,message,unt
    usr = None
    nme = None
    unt = None
    try:
        del details[views.get_ip(request)]
    except KeyError:
        pass
    message[views.get_ip(request)] = 'Logged out successfully!!'
    logger.info(views.get_ip(request))
    return HttpResponseRedirect('/')
    
def register(request):
    template = loader.get_template('register.html')
    return HttpResponse(template.render({},request))

def process_register(request):
    global message
    a = request.POST['Name']
    b = request.POST['UID']
    h = request.POST['EID']
    e = request.POST['Email']
    g = request.POST['Phoneno']
    c = request.POST['password']
    d = request.POST['department']
    f = request.POST['unit']
    creds = Credentials(name=a,u_id=b,emp_id=h,password=c,dept=d,email=e,phone=g,unit=f)
    creds.save()
    logger.info(views.get_ip(request))
    # message[views.get_ip(request)] = 'Registered Sucessfully!!'
    
    # return HttpResponseRedirect('/')
    return HttpResponseRedirect('/index/todo/')

def edit_register(request,u_id):
    template = loader.get_template('register_edit.html')
    acc = Credentials.objects.get(u_id=u_id)
    content = {
        'Acc':acc,
    }
    return HttpResponse(template.render(content,request))

def edit_register_process(request,u_id):
    acc = Credentials.objects.get(u_id=u_id)
    a = request.POST['Name']
    b = request.POST['UID']
    h = request.POST['EID']
    e = request.POST['Email']
    g = request.POST['Phoneno']
    c = request.POST['password']
    d = request.POST['department']
    f = request.POST['unit']
    i = request.POST['status']

    acc.name= a
    acc.u_id= b
    acc.emp_id= h
    acc.email= e
    acc.phone= g
    acc.password= c
    acc.unit= f
    acc.dept= d
    acc.status= i

    acc.save()
    logger.info(views.get_ip(request))
    return HttpResponseRedirect('/index/todo')

'''
def deletecreds(request,name):
    creds = Credentials.objects.get(name=name)
    creds.delete()
    return HttpResponseRedirect('/index/todo')
'''

def adduser(request):
    return HttpResponseRedirect('/register/')
