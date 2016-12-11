# -*- coding: utf_8 -*-
'''
Created on 2015/09/07
@author: ken
'''
from google.appengine.ext import ndb
import logging

class runway(ndb.Model):
    number      = ndb.IntegerProperty()
    degree      = ndb.IntegerProperty()
    distance    = ndb.IntegerProperty()
    runwaypoint = ndb.IntegerProperty()
    root_pointX = ndb.IntegerProperty()
    root_pointY = ndb.IntegerProperty()
    def initialize(self):

        if self.distance >= 4000:
            self.runwaypoint = 8

        elif self.distance >= 3000:
            self.runwaypoint = 4

        elif self.runwaypoint >= 2000:
            self.runwaypoint = 2

        else:
            self.runwaypoint = 1

        if self.distance % 1000 == 500:
            self.runwaypoint += 1

        return self.runwaypoint

class airport(ndb.Model):
    portname    = ndb.StringProperty()
    portcode    = ndb.StringProperty()
    country_name= ndb.StringProperty()
    origin_key  = ndb.KeyProperty(kind='user')
    location    = ndb.StringProperty()
    portPoint   = ndb.IntegerProperty()
    portEquip   = ndb.StructuredProperty(runway, repeated = True)
    ls_route_arrival    = ndb.KeyProperty(repeated = True)
    ls_route_departure  = ndb.KeyProperty(repeated = True)
    portPoint   = ndb.IntegerProperty()

    def create(self,arg):
        try:
            self.portname = arg['portname']
            self.portcode = arg['portcode']
            self.location = arg['location']
            self.origin_key=arg['origin_key']
            self.portEquip  = arg['runway']
            self.portPoint  = arg['portpoint']
            self.country_name = arg['country_name']

            self.calc_point(arg['maxpoint'])

            rescd = {'code':0,'msg':'登録成功'}

        except ValueError:
            rescd = {'code':1,'msg':'登録時にエラー発生'}

        finally:
            return rescd

    def update(self,arg):
        try:
            self.portname = arg['portname']
            self.portcode = arg['portcode']
            self.location = arg['location']
            self.origin_key = arg['origin_key']
            self.portEquip  = arg['runway']

            rescd = {'code':0,'msg':'更新成功'}

        except Exception as e:
            rescd = {'code':1,'msg':'更新時にエラー発生'}
            logging.error(e)

        finally:
            chksize = self.calc_point(arg['maxpoint'])
            if chksize['code'] == 1:
                rescd = chksize

            return rescd

    def calc_point(self,maxpoint):
        self.portPoint = 10
        for runway in self.portEquip:
            self.portPoint += runway.runwaypoint

        if self.portPoint > maxpoint:
            rescd = {'code':1,'msg': '有効ポイント：' + str(maxpoint) +'に対して空港規模' + str(self.portPoint) + 'が大きすぎる'}
        else:
            rescd = {'code':0,'msg': self.portPoint}

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
            rescd = {'code':0,'msg':''}

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
    port_point   = ndb.IntegerProperty()