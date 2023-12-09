from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Credentials, todo
from .serializers import todoSerializer,credsSerializer
from rest_framework import viewsets
from . import views_ticketing
from . import views_login
import logging

#Class is for json output and def is for UI outputs

class credsViewSet(viewsets.ModelViewSet):
   queryset = Credentials.objects.all()
   serializer_class = credsSerializer

class todoViewSet(viewsets.ModelViewSet):
   queryset = todo.objects.all()
   serializer_class = todoSerializer

#To get ip address
def get_ip(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
