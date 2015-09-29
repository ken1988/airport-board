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
from datetime import datetime
from datetime import time
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from pickle import EXT1

class MainPage(webapp2.RequestHandler):
    def initial_set(self,depart_port):
        if depart_port == '':
            depart_port = 'フリータウン空港'
            depart_port = depart_port.decode("utf-8")

        allports = models.airport.query()
        allroutes = models.air_route.query(models.air_route.depart_port == depart_port).order(models.air_route.Dept_time)
        allroutes_ar = models.air_route.query(models.air_route.arrival_port == depart_port).order(models.air_route.Arrv_time)

        res = {"dept"     :depart_port,
               "allports" :allports,
               "allroutes": allroutes,
               "allroutes_ar":allroutes_ar}
        return res

    def get(self):
        #メインページ表示
        self.display()

    def post(self):
        self.display()

    def display(self):
        header_html = self.get_header()
        depart_port = self.request.get("airport")
        res = self.initial_set(depart_port)

        template_values = {'sys_message':'メッセージはありません',
                           'header':header_html,
                           'depart_port':res["dept"],
                           'allports': res["allports"],
                           'allroutes':res["allroutes"],
                           'allroutes_ar':res['allroutes_ar']}
        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))

    def get_header(self):
        client_id = self.request.cookies.get('clid', '')
        if client_id == '':
            template_values = {}

        else:
            user_hash = self.request.cookies.get('hash', '')
            user = models.user().get_by_id(user_hash)

            template_values = {'login':1,
                               'email':user.country_name}

        path = os.path.join(os.path.dirname(__file__), './templates/header_menu.html')
        header_html = template.render(path,template_values)

        return header_html

class Get_image(webapp2.RequestHandler):
    def get(self):
        try:
            tar_comp = models.airline.get_by_id(self.request.get('key'))

            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(tar_comp.company_logo)
        except:
            self.response.out.write('No Image')
        return

class registration_page():
    def setval(self):
        res= {}
        res['disp_link'] = ''
        res['msg'] = ''
        res['rescd'] = 2
        res['airport'] = ''
        res['airline'] = ''
        return res

    def get(self):
        res = self.setval()
        self.display(res)

    def display(self,res):
        header_link = './templates/header_menu.html'
        client_id = self.request.cookies.get('clid', '')
        if client_id == '':
            self.redirect('/')
        else:
            user_hash = self.request.cookies.get('hash', '')
            user = models.user().get_by_id(user_hash)

            template_values = {'login':1,
                               'email':user.country_name}

        path = os.path.join(os.path.dirname(__file__), header_link)
        header_html = template.render(path,template_values)

        template_values = {'sys_message':res['msg'],
                           'header':header_html,
                           'remode':res['rescd'],
                           'allcompanies':res['airline'],
                           'allports':res['airport']}
        path = os.path.join(os.path.dirname(__file__),res['disp_link'])
        self.response.out.write(template.render(path, template_values))


class Airline(webapp2.RequestHandler,registration_page):
    def setval(self):
        res= {}
        res['disp_link'] = './templates/Airline.html'
        res['msg'] = '航空会社を登録してください'
        res['rescd'] = 2
        res['airport'] = ''
        res['airline'] = ''
        return res

    def post(self):
        arg = {'companyname':self.request.get("company_name"),
               'companyabb':self.request.get("company_abb"),
               'country':self.request.get("country"),
               'company_logo':self.request.get("file_data")}

        abb = self.request.get("company_abb")
        ndate = datetime.now()
        str_t=ndate.strftime('%Y%m%d')
        abbs = str(abb) + str_t

        newline = models.airline(key_name = abbs)
        rescd = newline.create(arg)

        if rescd['code'] == 0:
            newline.put()

        res = self.setval()
        res['rescd'] = rescd['code']
        res['msg'] = rescd['msg']
        self.display(res)
        return

class Airport(webapp2.RequestHandler,registration_page):
    def setval(self):
        res= {}
        res['disp_link'] = './templates/Airport.html'
        res['msg'] = '空港を登録してください'
        res['rescd'] = 2
        res['airport'] = ''
        res['airline'] = ''
        return res

    def post(self):
        user_hash = self.request.cookies.get('hash', '')
        user = models.user().get_by_id(user_hash)

        arg = {'portname': self.request.get("portname"),
               'location': self.request.get("location"),
               'country_name':user.country_name}
        newport = models.airport()
        rescd = newport.create(arg)

        if rescd['code'] == 0:
            newport.put()

        res = self.setval()
        res['rescd'] = rescd['code']
        res['msg'] = rescd['msg']
        self.display(rescd)
        return

class Route(webapp2.RequestHandler,registration_page):
    def setval(self):
        res= {}
        res['disp_link'] = './templates/route.html'
        res['msg'] = '空路を設定してください'
        res['rescd'] = 2

        allports = models.airport.query()
        alllines = models.airline.query()

        res['airport'] = allports
        res['airline'] = alllines

        return res

    def post(self):
        valres = self.validate()
        if valres['code'] == 1:
            recd = valres['code']
            remsg = valres['msg']

        else:
            str_airline = models.airline.get_by_id(self.request.get("airline")).company_name
            code = self.request.get("comp_abb")+self.request.get("code")
            times = self.timeset()

            if times['code'] == 1:
                recd = times['code']
                remsg = times['msg']

            else:
                arg = {'departure':self.request.get("departure"),
                        'arrival': self.request.get("arrival"),
                        'airline': self.request.get("airline"),
                        'str_airline':str_airline,
                        'code'   : code,
                        'Distance' : self.request.get("dist"),
                        'Numbers'  : self.request.get("frec"),
                        'Plane'    : self.request.get("plane"),
                        'dept_time': times['dept_time'],
                        'arrv_time': times['arrv_time']}

                newroute = models.air_route()
                rescd = newroute.create(arg)
                recd =  rescd['code']
                remsg = rescd['msg']

                if rescd['code'] == 0:
                    newroute.put()

        res = self.setval()
        res['rescd'] = recd
        res['msg']   = remsg
        self.display(res)

        return

    def timeset(self):
        try:
            h,m = self.request.get("dept_time").split(':')
            dept_time = time(hour=int(h),minute=int(m),second=0)

            h2,m2 = self.request.get("arrv_time").split(':')
            arrv_time = time(hour=int(h2),minute=int(m2),second=0)
            res = {'dept_time':dept_time,'arrv_time':arrv_time,'code':0}

        except Exception:
            res = {'code':1,'msg':'時刻指定が不正です'}

        finally:
            return res

    def validate(self):
        try:
            #入力値確認
            if (self.request.get("dept_time") == '' or
                self.request.get("arrv_time") == '' or
                self.request.get("code") == '' or
                self.request.get("dist") == '' or
                self.request.get("code") == ''):
                msg = "入力されていない項目があります"
                raise ValueError

            #出発空港と到着空港が一致していない事を確認
            if self.request.get("departure") == self.request.get("arrival"):
                msg = "出発地と到着地が同じです"
                raise ValueError

            #所要時間がマイナスじゃないことを確認
            if self.request.get("dist") < 0:
                msg = "所要時間がマイナスです"
                raise ValueError

            #路線コード桁数が４桁以内であることを確認
            if self.request.get("code") > 4:
                msg = "路線コードが４桁を超えています"
                raise ValueError

            res = {'code':0,'msg':'エラーなし'}

        except ValueError:
            res = {'code':1,'msg':msg}

        finally:
            return res

class User(webapp2.RequestHandler):
    def get(self):
        client_id = self.request.cookies.get('clid', '')
        if client_id == '':
            template_values = {}

        else:
            disp_mail = self.request.cookies.get('email', '')
            template_values = {'login':1,
                               'email':disp_mail}

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

        new_user = models.user(id = user_key)
        new_user.email = uid
        new_user.password = password
        new_user.country_name = country_name
        new_user.put()

        self.redirect('/')
        return

class Signin(webapp2.RequestHandler):
    def get(self):
        #cookieを破棄する
        self.response.delete_cookie('clid')
        self.response.delete_cookie('hash')
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

        pr_user = models.user().get_by_id(user_key)
        if pr_user:
            if pr_user.password == passwd:

                client_id = str(uuid.uuid4())
                disp_name = pr_user.country_name
                max_age = 60*120
                pr_list = {'clid':client_id,'hash':user_key,'disp_name':disp_name}
                self.put_cookie(pr_list,max_age)

        self.redirect('/')
        return


    def put_cookie(self,param_list,max_age):
        for key,value in param_list.iteritems():
            keys = key.encode('utf_8')
            values = value.encode('utf_8')
            myCookie = Cookie.SimpleCookie(os.environ.get( 'HTTP_COOKIE', '' ))
            myCookie[keys] = values
            myCookie[keys]["path"] = "/"
            myCookie[keys]["max-age"] = max_age
            self.response.headers.add_header('Set-Cookie', myCookie.output(header=""))
        return

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/Airline', Airline),
                               ('/Airport', Airport),
                               ('/Route', Route),
                               ('/User', User),
                               ('/Signin', Signin),
                               ('/get_img',Get_image)], debug=True)