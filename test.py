from django.test import TestCase
from django.test.client import Client
import simplejson

import os
import django
import json
#django.setup()

class ViewTest(TestCase):
    def test_addcontacts(self):
        json_string = u'{"emailfrom" : "wy", "emailto" : "yw", "extratext" : "0"}'
        response = self.client.post('/addcontacts', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_addcontacts2(self):
        json_string = u'{"emailfrom" : "wy", "emailto" : "yw", "extratext" : "0"}'
        response = self.client.post('/addcontacts', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_updatecontacts(self):
        json_string = u'{"emailfrom" : "wy", "emailto" : "yw"}'
        response = self.client.post('/updatecontacts', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_getunsolvedcontacts(self):
        json_string = u'{"email" : "wy"}'
        response = self.client.post('/getunsolvedcontacts', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_getcontacts(self):
        json_string = u'{"email" : "wy"}'
        response = self.client.post('/getunsolvedcontacts', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_rejectcontacts(self):
        json_string = u'{"emailfrom" : "wy", "emailto" : "yw"}'
        response = self.client.post('/rejectcontacts', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_removecontacts(self):
        json_string = u'{"emailfrom" : "wy", "emailto" : "yw"}'
        response = self.client.post('/removecontact', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_postchat(self):
        json_string = u'{"emailfrom" : "wy", "emailto" : "yw", "recordtext" : "0"}'
        response = self.client.post('/postchat', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_getchat(self):
        json_string = u'{"emailfrom" : "wy", "emailto" : "yw", "timestamp" : "0"}'
        response = self.client.post('/getchat', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_getunread(self):
        json_string = u'{"email" : "wy", "emailfrom" : "wy", "emailto" : "yw", "timestamp" : "0"}'
        response = self.client.post('/getunread', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_getunread2(self):
        json_string = u'{"email" : "wy", "emailfrom" : "wy", "emailto" : "yw", "timestamp" : "1"}'
        response = self.client.post('/getunread', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
    def test_searchbyname(self):
        json_string = u'{"email" : "wy"}'
        response = self.client.post('/searchbyname', json_string, content_type='application/json') 
        self.failUnlessEqual(200, response.status_code)
