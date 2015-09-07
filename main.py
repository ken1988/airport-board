# -*- coding: utf_8 -*-
'''
Created on 2015/09/07
@author: ken
'''
import webapp2
import os
import models
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    def get(self):
            allports = models.airport.all()
            template_values = {'sys_message':"メッセージはありません",
                               'allports': allports}
            path = os.path.join(os.path.dirname(__file__), './templates/index.html')
            self.response.out.write(template.render(path, template_values))

class Airline(webapp2.RequestHandler):
    def get(self):
        newline = models.airline()
        newline.company_name = "ノイエクルスエアライン"
        newline.company_abb = "LAN"
        newline.put()
        self.redirect('/')
        return

    def post(self):

        return

class Airport(webapp2.RequestHandler):
    def get(self):

        template_values = {'sys_message':"空港を登録してください"}
        path = os.path.join(os.path.dirname(__file__), './templates/Airport.html')
        self.response.out.write(template.render(path, template_values))
        return

    def post(self):

        try:
            newport = models.airport()
            newport.portname = self.request.get("portname")
            newport.location = self.request.get("location")
            newport.put()
            msg = "空港登録完了"

        except ValueError:
            msg = "例外エラー発生"

        finally:
            template_values = {'sys_message':msg}
            path = os.path.join(os.path.dirname(__file__), './templates/index.html')
            self.response.out.write(template.render(path, template_values))

        return
class Route(webapp2.RequestHandler):
    def get(self):
        newroute = models.air_route()
        newroute.airline = ["ノイエクルスエアライン"]
        newroute.airports = ["フリータウン空港","フリータウン空港"]
        newroute.route_code = "LAN1435"
        newroute.put()
        self.redirect('/')
        return

    def post(self):

        return

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/Airline', Airline),
                               ('/Airport', Airport),
                               ('/Route', Route)], debug=True)