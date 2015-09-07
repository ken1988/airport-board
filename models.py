# -*- coding: utf_8 -*-
'''
Created on 2015/09/07
@author: ken
'''
from google.appengine.ext import db

class airport(db.Model):
    portname = db.StringProperty(multiline=False)
    location = db.StringProperty(multiline=False)

class airline(db.Model):
    company_name = db.StringProperty(multiline=False)
    company_abb  = db.StringProperty(multiline=False)
    company_logo = db.LinkProperty
    origin_country = db.StringProperty(multiline=False)

class air_route(db.Model):
    route_code = db.StringProperty(multiline=False)
    depart_port = db.StringProperty(multiline=False)
    arrival_port= db.StringProperty(multiline=False)
    airports = db.ListProperty(item_type=str)
    airline  = db.ListProperty(item_type=str)
