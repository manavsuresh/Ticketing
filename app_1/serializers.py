# Used to get output in json format
#sample work:

# class <class_name>(serializers.ModelSerializer):
#    class Meta:
#        model = <table name>
#        fields = (<field names>Must match dict keys)


from rest_framework import serializers
from .models import todo,Credentials

class todoSerializer(serializers.ModelSerializer):
   class Meta:
       model = todo
       fields = ('id','date', 'name', 'task','department', 'progress')


class credsSerializer(serializers.ModelSerializer):
   class Meta:
       model = Credentials
       fields = ('name', 'u_id', 'password','dept')
