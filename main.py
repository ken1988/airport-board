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
import logging
from datetime import datetime
from datetime import time
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
import json
from inspect import iscode

class MainPage(webapp2.RequestHandler):
    def initial_set(self,depart_port):
        if depart_port == '':
            depart_port = 'フリータウン空港'
            depart_port = depart_port.decode("utf-8")

        countries = models.user.query()
        allroutes = models.air_route.query(models.air_route.depart_port == depart_port).order(models.air_route.Dept_time)
        allroutes_ar = models.air_route.query(models.air_route.arrival_port == depart_port).order(models.air_route.Arrv_time)

        res = {"dept"     :depart_port,
               "allroutes": allroutes,
               "allroutes_ar":allroutes_ar,
               "countries": countries}
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
                           'allroutes':res["allroutes"],
                           'allroutes_ar':res['allroutes_ar'],
                           'countries':res['countries']}

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
                               'email':user.country_name,
                               'point':user.port_point}

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
    def setval(self,user):
        res= {}
        res['disp_link'] = ''
        res['msg'] = ''
        res['rescd'] = 2
        res['airport'] = ''
        res['airline'] = ''
        return res

    def get(self):
        if self.request.get("data-type") == 'json':
            self.prep_json()
            self.get_json()
        else:
            user = self.user_disp()
            res = self.setval(user)
            self.display(res)

    def prep_json(self):
        return

    def get_json(self):
        if self.request.get("mode") == 'uni':
            resp_key = ndb.Key()
            resp_item = resp_key.get()
            resp_dict = resp_item.to_dict()
        else:
            t_country = self.request.get('country')
            resp_dict = self.get_allname(t_country)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(resp_dict))
        return

    def get_allname(self,t_country):
        all_items = ndb.query(models.user.country_name == t_country)
        res = []

        for port in all_items:
            portname = port.portname.encode('utf_8')
            res.append(portname)

        return res

    def user_disp(self):
        client_id = self.request.cookies.get('clid', '')
        if client_id == '':
            self.redirect('/')
        else:
            user_hash = self.request.cookies.get('hash', '')
            user = models.user().get_by_id(user_hash)
        return user

    def display(self,res):
        header_link = './templates/header_menu.html'
        user = self.user_disp()

        template_values = {'login':1,
                            'email':user.country_name,
                            'point':user.port_point}

        path = os.path.join(os.path.dirname(__file__), header_link)
        header_html = template.render(path,template_values)

        disp_link = res['disp_link']

        template_values = {'sys_message':res['msg'],
                           'header':header_html,
                           'remode':res['rescd'],
                           'allcompanies':res['airline'],
                           'allports':res['airport'],
                           'country_name':user.country_name,
                           'origin_key': user.key.id()}
        path = os.path.join(os.path.dirname(__file__),disp_link)
        self.response.out.write(template.render(path, template_values))

    def create(self):
        return

    def update(self):

        return

    def delete(self):
        return

    def basic_validation(self,items):
    #items:validation対象となるデータ群
    #{kind:"アイテムの種類",type:"データタイプ,"item:"対象データ",len:"桁長",lenc:"桁長符号(以上、以下、イコール)",
    # alpha:"英文字",alphac:"英文字の扱い(NG、OK、ONLY)",
    # numer:"数字",numerc:"数字の扱い(NG、OK、ONLY)",code}
        try:
            code = 0
            msg ="エラーなし"
            for item in items:
                if item["item"] == '':
                #入力値チェック
                    msg = item["type"]+"が入力されていません"
                    code = 1
                    break

                else:
                #桁数確認
                    if item["lenc"] == "MT" and len(item["item"]) < item["len"]:
                        msg =item["type"]+"は"+str(item["len"])+"桁以上にしてください"
                        code = 1

                    elif item["lenc"] == "LT" and len(item["item"]) > item["len"]:
                        msg =item["type"]+"は"+str(item["len"])+"桁以下にしてください"
                        code = 1

                    elif item["lenc"] == "EQ" and len(item["item"]) <> item["len"]:
                        msg =item["type"]+"は"+str(item["len"])+"桁にしてください"
                        code = 1

                #数字の扱い

                #英文字の扱い

                #マイナス値の確認
                    if item['item'] < 0:
                        msg = item["kind"] + "がマイナスです"
                        code = 1

                #コード存在の確認
                    if item.has_key('code') and item["code"] == "Y":
                        if item["kind"] == "空港":
                            fetch = models.airport().get_by_id(item["item"])

                        elif item["kind"] == "航空会社":
                            fetch = models.airline().get_by_id(item["item"])

                        elif item["kind"] == "空路":
                            fetch = models.air_route().get_by_id(item["item"])

                        if fetch is not None:
                            msg = item["kind"] + "が登録済みです"
                            code = 1

                    if code == 1:
                        break

        except Exception as e:
            code = 1
            msg = "message:{0}".format(e.message)

        res = {'code':code,'msg':msg}
        return res

class Airline(webapp2.RequestHandler,registration_page):
    def setval(self,user):
        res= {}
        res['disp_link'] = './templates/Airline.html'
        res['msg'] = '航空会社を登録してください'
        res['rescd'] = 2
        all_lines = models.airline.query().filter(models.airline.origin_country == user.country_name)
        res['airport'] = ''
        res['airline'] = all_lines
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
        self.display(res,"")
        return

class Airport(webapp2.RequestHandler,registration_page):
    def setval(self,user):
        res= {}
        res['disp_link'] = './templates/Airport.html'
        res['msg'] = '空港を登録してください'
        res['rescd'] = 2
        allports = models.airport.query().filter(models.airport.country_name == user.country_name)
        res['airport'] = allports
        res['airline'] = ''

        return res

    def post(self):
        if self.request.get("mode") == "u":
            items =[{"item":self.request.get("portname"),"type":"名称","kind":"空港","len":50,"lenc":"LT"},
                    {"item":self.request.get("portcode"),"type":"コード","kind":"空港","len":3,"lenc":"EQ"},
                    {"item":self.request.get("location"),"type":"所在地","kind":"空港","len":100,"lenc":"LT"}]

        else:
            items =[{"item":self.request.get("portname"),"type":"名称","kind":"空港","len":50,"lenc":"LT"},
                    {"item":self.request.get("portcode"),"type":"コード","kind":"空港","len":3,"lenc":"EQ","code":"Y"},
                    {"item":self.request.get("location"),"type":"所在地","kind":"空港","len":100,"lenc":"LT"}]

        valres = self.basic_validation(items)

        user_hash = self.request.cookies.get('hash', '')
        user = models.user().get_by_id(user_hash)

        recd = 0
        if valres['code'] == 1:
            recd = valres['code']
            remsg = valres['msg']
        else:

            equip = []
            for num in xrange(1,5):

                runway = {'number'     : num,
                          'distance'   :0,
                          'degree'     :0,
                          'root_pointX':0,
                          'root_pointY':0,
                          'runwaypoint':0}
                equip.append(runway)

            arg = {'portname': self.request.get("portname"),
                   'portcode': self.request.get("portcode"),
                   'location': self.request.get("location"),
                   'runway'  : equip,
                   'origin_key':user.key,
                   'maxpoint'  :user.port_point}

            if self.request.get("mode") == "u":
                oldpoint = 0
                portid = int(self.request.get("portid"))
                target_port = models.airport().get_by_id(portid)
                oldpoint = target_port.portPoint

                remsg = "空港情報を更新しました"
                rescd = target_port.update(arg)
                portpoint = target_port.portPoint
                respoint = portpoint - oldpoint

            else:
                remsg = "空港情報を登録しました"
                target_port = models.airport()
                rescd = target_port.create(arg)
                respoint = target_port.portPoint

            if rescd['code'] == 0:
                user.port_point -= respoint
                user.put()
                target_port.put()

            else:
                recd  = rescd['code']
                remsg = user.port_point

        res = self.setval(user)
        res['rescd'] = recd
        res['msg'] = remsg
        self.display(res)
        return

class Route(webapp2.RequestHandler,registration_page):
    def setval(self,user):
        res={}
        res['disp_link'] = './templates/route.html'
        res['msg'] = '空路を設定してください'
        res['rescd'] = 2

        allports = models.airport.query()
        alllines = models.airline.query()

        res['airport'] = allports
        res['airline'] = alllines

        return res

    def post(self):
        code = self.request.get("comp_abb")+self.request.get("code")
        items =[{"item":self.request.get("dist"),"type":"時間","kind":"空路", "len":3,"lenc":"LT"},
                {"item":code,"type":"路線コード","kind":"空路","len":8,"lenc":"LT"}]

        valres = self.basic_validation(items)
        valres2 = self.validate()

        user_hash = self.request.cookies.get('hash', '')
        user = models.user().get_by_id(user_hash)

        if valres['code'] * valres2['code'] == 1:
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
                        'arrv_time': times['arrv_time'],
                        'origin_key':user.key}

                newroute = models.air_route(id = code)
                rescd = newroute.create(arg)
                recd =  rescd['code']
                remsg = rescd['msg']

                if rescd['code'] == 0:
                    newroute.put()

                    tkey = newroute.key

                    arrv_port = models.airport.query(models.airport.portname == self.request.get("arrival")).get()
                    port_list = []
                    port_list = arrv_port.ls_route_arrival
                    port_list.append(tkey)
                    arrv_port.ls_route_arrival = port_list
                    arrv_port.put()

                    dept_port = models.airport.query(models.airport.portname == self.request.get("departure")).get()
                    port_list = []
                    port_list = dept_port.ls_route_departure
                    port_list.append(tkey)
                    dept_port.ls_route_departure = port_list
                    dept_port.put()

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
            #出発空港と到着空港が一致していない事を確認
            if self.request.get("departure") == self.request.get("arrival"):
                msg = "出発地と到着地が同じです"
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
        new_user.port_point = 100
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

class Json_list():
    def get_uni(self,t_kind,t_code):
        t_key = ndb.Key(t_kind,t_code)
        t_obj = t_key.get()

        return  t_obj.to_dict()

    def get_all(self,t_kind,t_country):
        t_objects = ndb.Query(kind = t_kind).filter(models.user.country_name == t_country)
        return t_objects

class Port_list(webapp2.RequestHandler,Json_list):
    def get(self):
        if self.request.get("mode") == 'uni':
            port_code = ''
            port_code = self.request.get('port_id')
            report = self.get_uni("airport", port_code)
        else:
            t_country = self.request.get('country')
            report = self.get_ports(t_country)

        #ヘッダー情報
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(report))
        return

    def get_ports(self, t_country):
        allports = self.get_all("airport", t_country)
        res = []
        res_port = {}

        for port in allports:
            res_port ={"portkey":port.key.id(),
                       "portpoint":port.portPoint,
                       "portcode":port.portcode.encode('utf_8'),
                       "portname":port.portname.encode('utf_8'),
                       "location":port.location.encode('utf_8')}

            res.append(res_port)

        return res

class Airline_list(webapp2.RequestHandler,Json_list):
    def get(self):
        if self.request.get("mode") == 'uni':
            airline_code = ''
            airline_code = self.request.get('company_id')
            report = self.get_uni("airline", airline_code)
            report.pop('company_logo')

            #ヘッダー情報
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(report))

        else:
            t_country = self.request.get('country')
            res = self.get_airlines(t_country)

            #ヘッダー情報
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(res))


    def get_airlines(self, t_country):
        allwings = models.airline.query(models.user.country_name == t_country)
        res = []

        for airline in allwings:
            company_name = airline.company_name.encode('utf_8')
            res.append(company_name)

        return res

class AirRoute_list(webapp2.RequestHandler,Json_list):
    def get(self):
        t_country = self.request.get('country')
        report = self.get_routes(t_country)

        #ヘッダー情報
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(report))
        return

    def get_routes(self,t_country):
        allroutes = self.get_all("air_route", t_country)
        res = []

        for air_route in allroutes:
            route_code = air_route.route_code.encode('utf-8')
            res.append(route_code)

        return res

    def post(self):
        return

class Airport_Designer(webapp2.RequestHandler):
    def get(self):
        port_id = self.request.get('id')

        if port_id.isdigit():
            port = models.airport.get_by_id(int(port_id))
        else:
            port = models.airport.get_by_id(port_id)

        template_values = {'airport':port,
                           'port_id':port_id}

        path = os.path.join(os.path.dirname(__file__), './templates/apdesigner.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/Airline', Airline),
                               ('/Airport', Airport),
                               ('/Route', Route),
                               ('/User', User),
                               ('/Signin', Signin),
                               ('/get_img',Get_image),
                               ('/port_list',Port_list),
                               ('/airline_list',Airline_list),
                               ('/route_list',AirRoute_list),
                               ('/port_designer',Airport_Designer)], debug=True)
