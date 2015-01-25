from django.test import TestCase
from models import *
import os


user1 = User(name = 'haha', email = 'dd@163.com', password='pass')
user1.save()
