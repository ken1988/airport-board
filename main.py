# -*- coding: utf_8 -*-
'''
Created on 2015/09/07
@author: ken
'''
import webapp2
import os
import models
import uuid
import Cookie
import hashlib
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
    def get(self):

        allports = models.airport.all()
        allroutes = models.air_route.all()

        #メインページ表示
        template_values = Signin.chk_cookie()
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        header_html = template.render(path,template_values)

        template_values = {'sys_message':"メッセージはありません",
                           'header':header_html,
                           'allports': allports,
                           'allroutes':allroutes}
        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        template_values = Signin.chk_cookie()
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        header_html = template.render(path,template_values)

        depart_port = self.request.get("airport")
        allports = models.airport.all()
        q = models.air_route.all()
        allroutes = q.filter("depart_port =", depart_port)

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
        template_values = Signin.chk_cookie()
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
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
            template_values = Signin.chk_cookie()
            path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
            header_html = template.render(path,template_values)

            template_values = {'sys_message':msg,
                               'header':header_html,
                               'remode': remode}
            path = os.path.join(os.path.dirname(__file__), './templates/Airline.html')
            self.response.out.write(template.render(path, template_values))

        return

class Airport(webapp2.RequestHandler):
    def get(self):
        template_values = Signin.chk_cookie()
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
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
            template_values = Signin.chk_cookie()
            path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
            header_html = template.render(path,template_values)

            template_values = {'sys_message':msg,
                               'header':header_html,
                               'remode': remode}
            path = os.path.join(os.path.dirname(__file__), './templates/Airport.html')
            self.response.out.write(template.render(path, template_values))
        return

class Route(webapp2.RequestHandler):
    def get(self):
        template_values = Signin.chk_cookie()
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
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

            template_values = Signin.chk_cookie()
            path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
            header_html = template.render(path,template_values)

            template_values = {'sys_message':msg,
                               'header':header_html,
                               'allports':allports,
                               'allcompanies':allcompanies,
                               'remode': remode}
            path = os.path.join(os.path.dirname(__file__), './templates/route.html')
            self.response.out.write(template.render(path, template_values))
        return

class User(webapp2.RequestHandler):
    def get(self):
        template_values = Signin.chk_cookie()
        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        header_html = template.render(path,template_values)

        template_values = {'header':header_html}
        path = os.path.join(os.path.dirname(__file__), './templates/User_registration.html')
        self.response.out.write(template.render(path, template_values))
        return

    def post(self):
        uid = self.request.get('userID')
        passstr = self.request.get('password')
        country_name = self.request.get('country_name')

        #パスワードハッシュ値生成
        m = hashlib.md5()
        m.update(passstr)
        password = m.hexdigest()

        #メールアドレスハッシュ値生成
        h = hashlib.md5()
        h.update(uid)
        user_key = h.hexdigest()
        country_key = user_key + "c"

        #country生成、country_key取得
        new_country = models.country(key_name = country_key)
        new_country.country_name = country_name
        new_country.put()

        new_user = models.user(key_name = user_key)
        new_user.email = uid
        new_user.password = password
        new_user.country_key = country_key
        new_user.put()

        self.redirect('/')
        return

class Signin(webapp2.RequestHandler):
    def get(self):
        #メインページに戻す
        self.redirect('/')
        return

    def post(self):
        #Postがあった場合の処理
        uid = self.request.get("userID")
        password = self.request.get('password')

        #ユーザーキー生成
        h = hashlib.md5()
        h.update(uid)
        user_key = h.hexdigest()

        #パスワードハッシュ値生成
        m = hashlib.md5()
        m.update(password)
        passwd = m.hexdigest()

        pr_user = models.user().get_by_key_name(user_key, None)
        if pr_user:
            if pr_user.password == passwd:

                client_id = str(uuid.uuid4())
                pr_list = {'clid':client_id,'mail':pr_user.email}
                self.put_cookie(pr_list)

        self.redirect('/')
        return

    def chk_cookie(self):
        client_id = self.request.cookies.get('clid', '')
        if client_id == '':
            template_values = {}

        else:
            disp_mail = self.request.cookies.get('email', '')
            template_values = {'login':1,
                               'email':disp_mail}
        return template_values

    def put_cookie(self,param_list):
        client_id = self.request.cookies.get('clid', '')
        if client_id == '':
            for key,value in param_list.iteritems():
                keys = key.encode('utf_8')
                values = value.encode('utf_8')
                myCookie = Cookie.SimpleCookie(os.environ.get( 'HTTP_COOKIE', '' ))
                myCookie[keys] = values
                myCookie[keys]["path"] = "/"
                myCookie[keys]["max-age"] = 60*120
                self.response.headers.add_header('Set-Cookie', myCookie.output(header=""))
        return

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/Airline', Airline),
                               ('/Airport', Airport),
                               ('/Route', Route),
                               ('/User', User),
                               ('/Signin', Signin)], debug=True)