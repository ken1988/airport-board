# -*- coding: utf_8 -*-
'''
Created on 2015/09/07
@author: ken
'''
from google.appengine.ext import db
from datetime import time

class airport(db.Model):
    portname = db.StringProperty(multiline=False)
    location = db.StringProperty(multiline=False)
    location_key =db.StringProperty(multiline=False)

    def create(self,arg):
        try:
            self.portname = arg['portname']
            self.location = arg['location']
            rescd = 0
        except ValueError:
            rescd = 1
        finally:
            return rescd

class airline(db.Model):
    company_name = db.StringProperty(multiline=False)
    company_abb  = db.StringProperty(multiline=False)
    company_logo = db.BlobProperty()
    origin_country = db.StringProperty(multiline=False)
    origin_key = db.StringProperty(multiline=False)

    def create(self,arg):
        try:
            self.company_name = arg['companyname']
            self.company_abb = arg['companyabb']
            self.origin_country = arg['country']
            self.company_logo = arg['company_logo']

            rescd = 0
        except ValueError:
            rescd = 1
        finally:
            return rescd

class air_route(db.Model):
    route_code = db.StringProperty(multiline=False)
    depart_port = db.StringProperty(multiline=False)
    arrival_port= db.StringProperty(multiline=False)
    airports  = db.ListProperty(item_type=str)
    airline  = db.ListProperty(item_type=str)
    str_airline = db.ListProperty(item_type=str)
    Numbers = db.IntegerProperty()
    Distance = db.IntegerProperty()
    Plane = db.StringProperty(multiline=False)
    Dept_time = db.TimeProperty()
    Arrv_time = db.TimeProperty()

    def create(self,arg):
        try:
            self.depart_port = arg['departure']
            self.arrival_port = arg['arrival']
            self.airports = [arg['departure'],arg['arrival']]
            self.airline = [arg['airline']]
            self.str_airline = [arg['str_airline']]
            self.route_code = arg['code']
            self.Numbers = int(arg['Numbers'])
            self.Distance = int(arg['Distance'])
            self.Plane = arg['Plane']
            self.Dept_time = arg['dept_time']
            rescd = 0

        except Exception:
            rescd = 1

        finally:
            return rescd

class user(db.Model):
    email = db.EmailProperty()
    password = db.StringProperty(multiline=False)
    country_name = db.StringProperty(multiline=False)
