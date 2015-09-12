# -*- coding: utf_8 -*-
'''
Created on 2015/09/07
@author: ken
'''
from google.appengine.ext import db

class airport(db.Model):
    portname = db.StringProperty(multiline=False)
    location = db.StringProperty(multiline=False)

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
    company_logo = db.LinkProperty
    origin_country = db.StringProperty(multiline=False)

    def create(self,arg):
        try:
            self.company_name = arg['companyname']
            self.company_abb = arg['companyabb']
            self.origin_country = arg['country']
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
    def create(self,arg):
        try:
            self.depart_port = arg['departure']
            self.arrival_port = arg['arrival']
            self.airports = [arg['departure'],arg['arrival']]
            self.airline = [arg['airline']]
            self.route_code = arg['code']
            rescd = 0
        except ValueError:
            rescd = 1
        finally:
            return rescd

class user(db.Model):
    email = db.EmailProperty()
    password = db.StringProperty(multiline=False)
    country_key = db.StringProperty(multiline=False)

class country(db.Model):
    country_name = db.StringProperty(multiline=False)
