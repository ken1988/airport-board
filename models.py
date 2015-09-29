# -*- coding: utf_8 -*-
'''
Created on 2015/09/07
@author: ken
'''
from google.appengine.ext import ndb

class airport(ndb.Model):
    portname = ndb.StringProperty()
    portcode = ndb.StringProperty()
    country_name = ndb.StringProperty()
    location = ndb.StringProperty()

    def create(self,arg):
        try:
            self.portname = arg['portname']
            self.portcode = arg['portcode']
            self.location = arg['location']
            self.country_name = arg['country_name']
            rescd = {'code':0,'msg':'登録成功'}

        except ValueError:
            rescd = {'code':1,'msg':'登録時にエラー発生'}

        finally:
            return rescd

class airline(ndb.Model):
    company_name   = ndb.StringProperty()
    company_abb    = ndb.StringProperty()
    company_logo   = ndb.BlobProperty()
    origin_country = ndb.StringProperty()
    origin_key     = ndb.KeyProperty(kind='user')

    def create(self,arg):
        try:
            self.company_name = arg['companyname']
            self.company_abb = arg['companyabb']
            self.origin_country = arg['country']
            self.company_logo = arg['company_logo']
            rescd = {'code':0,'msg':'登録成功'}

        except ValueError:
            rescd = {'code':1,'msg':'登録時にエラー発生'}

        finally:
            return rescd

class air_route(ndb.Model):
    route_code = ndb.StringProperty()
    depart_port = ndb.StringProperty()
    dept_location = ndb.StringProperty()
    arrival_port= ndb.StringProperty()
    arriv_location = ndb.StringProperty()
    airports  = ndb.StringProperty(repeated=True)
    airline  = ndb.StringProperty(repeated=True)
    str_airline = ndb.StringProperty(repeated=True)
    Numbers = ndb.IntegerProperty()
    Distance = ndb.IntegerProperty()
    Plane = ndb.StringProperty()
    Dept_time = ndb.TimeProperty()
    Arrv_time = ndb.TimeProperty()

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
            self.Arrv_time = arg['arrv_time']

            rescd = {'code':0,'msg':'登録成功'}

        except ValueError:
            rescd = {'code':1,'msg':'登録時にエラー発生'}

        finally:
            return rescd

class user(ndb.Model):
    email        = ndb.StringProperty()
    password     = ndb.StringProperty()
    country_name = ndb.StringProperty()