from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import todo
from .models import Credentials as cred
from .serializers import todoSerializer,credsSerializer
from rest_framework import viewsets
from . import views
from . import views_login
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__file__)
fil={}

def superuser(request):
    global fil
    template = loader.get_template('to-do_index_admin_superuser.html')
    ip = views.get_ip(request)  
    try:
        user = views_login.dets()[ip][0]
        name = views_login.dets()[ip][1]
    except KeyError:
        return HttpResponseRedirect('/')
    if user.lower() != 'admin'  or name.lower() != 'manav':
        return HttpResponseRedirect('/')
    
    tasks_master = todo.objects.all().filter(closed = 'False').values()
    tasks_master2 = todo.objects.all().filter(closed = 'True').values()
    creds_master = cred.objects.all().filter(status = 'Active').values()
    creds_master2 = cred.objects.all().filter(status='Inactive').values()
    Pending_today = todo.objects.all().filter(date=date.today()).values()
    Pending_today = Pending_today.filter(progress='False')
    Pending_today = Pending_today.count()

    creds = creds_master.order_by('dept')
    creds2 = creds_master2.order_by('dept')
    tasks = tasks_master.order_by('-date')
    tasks2 = tasks_master2.order_by('-date')
    
    now_date = date.today()

    content = {
                'creds' : creds,
                'creds2' : creds2,
                'tasks' : tasks,
                'closedtasks' : tasks2,
                'count_Admin' : todo.objects.all().filter(department='Admin').filter(progress='False').count(),
                'count_IT' : todo.objects.all().filter(department='IT').filter(progress='False').count(),
                'count_Accounts' : todo.objects.all().filter(department='Accounts').filter(progress='False').count(),
                'count_Civil' : todo.objects.all().filter(department='Civil').filter(progress='False').count(),
                'count_Electrical' : todo.objects.all().filter(department='Electrical').filter(progress='False').count(),
                'count_Transport' : todo.objects.all().filter(department='Transport').filter(progress='False').count(),
                'count_Workshop' : todo.objects.all().filter(department='Workshop').filter(progress='False').count(),
                'Total_complaints' : todo.objects.all().count(),
                'Pending' : todo.objects.all().filter(progress='False').count(),
                'Pending_today' : Pending_today,
                'date' : now_date.strftime("%d-%m-%y"),
        
            }
    
    details = [ip,user,name]
    logger.info(details)
    return content,template





def todo_(request):
    global fil
    template = loader.get_template('to-do_index.html')
    ip = views.get_ip(request)  
    try:
        user = views_login.dets()[ip][0]
        name_ = views_login.dets()[ip][1]
    except KeyError:
        return HttpResponseRedirect('/')
    if user == None or name_ == None:
        return HttpResponseRedirect('/')
    
    tasks_master = todo.objects.all().filter(closed = 'False').values()
    if user.lower() ==  'admin':
            if name_.lower() == 'manav':
                content,template = superuser(request)
                return HttpResponse(template.render(content,request))

            tasks = tasks_master.order_by('-date')
            # tasks_0 = tasks.filter()      # Your personal complaints
            tasks_1 = tasks.filter(progress = 'False').order_by('-date')
            tasks_2 = tasks.filter(progress = 'True').order_by('-date')
            # tasks = tasks.order_by('department')
            try:
                if fil[ip] == '' or fil[ip] == 'None':
                    pass
                else:
                    tasks = tasks.filter(department=fil[ip])
                    fil[ip] = ''
            except KeyError:
                pass
            template = loader.get_template('to-do_index_admin.html')
            Pending_today = todo.objects.all().filter(date=date.today()).values()
            Pending_today = Pending_today.filter(progress='False')
            Pending_today = Pending_today.count()
            content = {
                'tasks' : tasks_1,
                'tasks2' : tasks_2,
                'count_Admin' : todo.objects.all().filter(department='Admin').filter(progress='False').count(),
                'count_IT' : todo.objects.all().filter(department='IT').filter(progress='False').count(),
                'count_Accounts' : todo.objects.all().filter(department='Accounts').filter(progress='False').count(),
                'count_Civil' : todo.objects.all().filter(department='Civil').filter(progress='False').count(),
                'count_Electrical' : todo.objects.all().filter(department='Electrical').filter(progress='False').count(),
                'count_Transport' : todo.objects.all().filter(department='Transport').filter(progress='False').count(),
                'count_Workshop' : todo.objects.all().filter(department='Workshop').filter(progress='False').count(),
                'Total_complaints' : todo.objects.all().count(),
                'Pending' : todo.objects.all().filter(progress='False').count(),
                'Pending_today' : Pending_today,
            }
    elif user.lower() == 'client': 
        tasks = tasks_master.filter(name=name_).order_by('progress')
        template = loader.get_template('to-do_index_client.html')
        content = {
                'tasks' : tasks,
                'Pending' : todo.objects.all().filter(progress='False').count(),
        }
    else:
        if views_login.dets()[views.get_ip(request)][2] == '-':
            tasks = tasks_master.filter(department=user)
        else:
            tasks = tasks_master.filter(department=user).filter(progress='False').filter(unit=views_login.dets()[views.get_ip(request)][2])      
        tasks2 = tasks_master.filter(name=name_)
        tasks2 = tasks2.order_by('-date')
        tasks2 = tasks2.order_by('progress')
        tasks = tasks.order_by('-date')
        tasks = tasks.order_by('progress')
        content = {
                'tasks' : tasks,
                'mytask' : tasks2,
        }
    
    details = [ip,user,name_]
    logger.info(details)
    return HttpResponse(template.render(content,request))

def Filter(request):
    global fil
    a = request.POST['Filter']
    ip = views.get_ip(request)   
    fil[ip] = a
    return HttpResponseRedirect('/index/todo/')


def todo_mark(request, id):
    task = todo.objects.get(id=id)
    task.progress = True
    task.task_dets = f'Solved by {views_login.dets()[views.get_ip(request)][1]} on {date.today()}'
    task.save()
    return HttpResponseRedirect('/index/todo/')

def todo_add(request):
    ip = views.get_ip(request)  
    try:
        user = views_login.dets()[ip][0]
    except KeyError:
        return HttpResponseRedirect('/')
    if user == None:
        return HttpResponseRedirect('/')
    template = loader.get_template('todo_add.html')
    logger.info(views.get_ip(request))
    return HttpResponse(template.render({},request))


def todo_addtask(request):
    a = date.today()
    b = views_login.dets()[views.get_ip(request)][1]
    c = request.POST['task']
    d = request.POST['department']
    e = 'False'
    f = request.POST['unit']
    g = views_login.dets()[views.get_ip(request)][3]
    h = views_login.dets()[views.get_ip(request)][4]
    task1 = todo(date=a,name=b,unit=f,task_subject=c,task_dets='',department=d,progress=e,remark='',phone=h,emp_id=g)
    task1.save()
    
    return HttpResponseRedirect('/index/todo') 


def todo_update(request,id):
    ip = views.get_ip(request)  
    try:
        user = views_login.dets()[ip][0]
        name = views_login.dets()[ip][1]
    except KeyError:
        return HttpResponseRedirect('/')
    if user == None:
        return HttpResponseRedirect('/')
    task = todo.objects.get(id=id)
    if user.lower() ==  'admin' or user.lower() == 'client' or task.name.lower() == name.lower():
        template = loader.get_template('todo_update.html')
    else:
        template = loader.get_template('todo_update_dept.html')
    context = {
        'Task':task,
    }
    return HttpResponse(template.render(context,request))

def todo_update_task(request,id):
    Task1 = todo.objects.get(id=id)
    ip = views.get_ip(request)  
    user = views_login.dets()[ip][0]
    name = views_login.dets()[ip][1]
    if user.lower() == 'admin' or user.lower() == 'client' or Task1.name.lower() == name.lower():
        f = request.POST['unit']
        c=request.POST['task']
        e = request.POST['department']
        d = 'False'
        Task1.unit = f
        Task1.task_subject = c
        Task1.department = e
    else:
        d=request.POST['progress']
        if d.lower() == 'true':
            e=request.POST['feedback']
            Task1.task_dets = f'Solved by {views_login.dets()[views.get_ip(request)][1]} on {date.today()}'
            Task1.feedback = e
        Task1.progress = d

    Task1.save()
    return HttpResponseRedirect('/index/todo')

#Remarks - POST Solving
def todo_remark(request,id):
    ip = views.get_ip(request)  
    try:
        user = views_login.dets()[ip][0]
        name = views_login.dets()[ip][1]
    except KeyError:
        return HttpResponseRedirect('/')
    task = todo.objects.get(id=id)
    if user.lower() == 'client' or user.lower() == 'admin' or task.name.lower() == name.lower():
        template = loader.get_template('todo_remark.html')
    else:
        template = loader.get_template('todo_remark_view.html')
    context = {
        'Task':task,
    }
    return HttpResponse(template.render(context,request))

def todo_remark_task(request,id):
    Task1 = todo.objects.get(id=id)
    ip = views.get_ip(request)  
    try:
        user = views_login.dets()[ip][0]
        name = views_login.dets()[ip][1]
    except KeyError:
        return HttpResponseRedirect('/')
    if user.lower() == 'client' or user.lower() == 'admin' or Task1.name.lower() == name.lower():
        b=request.POST['remark']
        d=request.POST['progress']
        Task1.closed = d
        Task1.remark = b
        Task1.progress = d
        Task1.save()
    else:
        pass
    return HttpResponseRedirect('/index/todo')