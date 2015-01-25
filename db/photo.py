import base64
from django.shortcuts import render
import time
import traceback
import MySQLdb.cursors
from models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson
import MySQLdb
import datetime

f=open(r'/home/wangyan/myproject/data/1.jpg','rb')
ls_f=base64.b64encode(f.read()) 
p = UserPhoto(imagetext = ls_f)
p.save()
print ls_f
f.close()
