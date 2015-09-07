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
            allroutes = models.air_route.all()

            path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
            template_values = {}
            header_html = template.render(path,template_values)

            template_values = {'sys_message':"メッセージはありません",
                               'header':header_html,
                               'allports': allports,
                               'allroutes':allroutes}
            path = os.path.join(os.path.dirname(__file__), './templates/index.html')
            self.response.out.write(template.render(path, template_values))

    def post(self):
        depart_port = self.request.get("airport")
        allports = models.airport.all()
        q = models.air_route.all()
        allroutes = q.filter("depart_port =", depart_port)

        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        template_values = {}
        header_html = template.render(path,template_values)

        template_values = {'sys_message':"メッセージはありません",
                           'header':header_html,
                           'depart_port':depart_port,
                           'allports': allports,
                           'allroutes':allroutes}
        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))

        return

class Airline(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        template_values = {}
        header_html = template.render(path,template_values)

        template_values = {'sys_message':"航空会社を登録してください",
                           'header':header_html}
        path = os.path.join(os.path.dirname(__file__), './templates/Airline.html')
        self.response.out.write(template.render(path, template_values))
        return

    def post(self):

        try:
            newline = models.airline()
            newline.company_name = self.request.get("company_name")
            newline.company_abb = self.request.get("company_abb")
            newline.origin_country = self.request.get("country")
            newline.put()
            msg = "航空会社登録完了"
            remode = 1

        except ValueError:
            msg = "例外エラー発生"

        finally:
            path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
            template_values = {}
            header_html = template.render(path,template_values)

            template_values = {'sys_message':msg,
                               'header':header_html,
                               'remode': remode}
            path = os.path.join(os.path.dirname(__file__), './templates/Airline.html')
            self.response.out.write(template.render(path, template_values))

        return

class Airport(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        template_values = {}
        header_html = template.render(path,template_values)

        template_values = {'sys_message':"航空会社を登録してください",
                           'header':header_html}
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
            remode = 1

        except ValueError:
            msg = "例外エラー発生"

        finally:
            path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
            template_values = {}
            header_html = template.render(path,template_values)

            template_values = {'sys_message':msg,
                               'header':header_html,
                               'remode': remode}
            path = os.path.join(os.path.dirname(__file__), './templates/Airport.html')
            self.response.out.write(template.render(path, template_values))
        return
class Route(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        template_values = {}
        header_html = template.render(path,template_values)

        allports = models.airport.all()
        allcompanies = models.airline.all()

        template_values = {'sys_message':"空路を設定してください",
                           'header':header_html,
                           'allports':allports,
                           'allcompanies':allcompanies}
        path = os.path.join(os.path.dirname(__file__), './templates/route.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

        try:
            newroute = models.air_route()
            newroute.depart_port = self.request.get("departure")
            newroute.arrival_port = self.request.get("arrival")
            newroute.airports = [self.request.get("departure"),self.request.get("arrival")]
            newroute.airline = [self.request.get("airline")]
            newroute.route_code = self.request.get("code")
            newroute.put()
            msg = "空路登録完了"
            remode = 1

        except ValueError:
            msg = "例外エラー発生"

        finally:
            allports = models.airport.all()
            allcompanies = models.airline.all()

            path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
            template_values = {}
            header_html = template.render(path,template_values)

            template_values = {'sys_message':msg,
                               'header':header_html,
                               'allports':allports,
                               'allcompanies':allcompanies,
                               'remode': remode}
            path = os.path.join(os.path.dirname(__file__), './templates/route.html')
            self.response.out.write(template.render(path, template_values))
        return

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/Airline', Airline),
                               ('/Airport', Airport),
                               ('/Route', Route)], debug=True)