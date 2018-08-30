#date:2018/8/29

import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from utils.connectdb import DbConnect


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('user_id')


class LoginHandler(BaseHandler):
    def get(self):
        msg = ''
        self.render('login.html',msg=msg)

    def post(self):
        username = self.get_argument('username')
        passwd = self.get_argument('passwd')
        db_conn = DbConnect()
        cursor = db_conn.connect()
        sql = 'select user_id,username,passwd,status from user_info where username=%s and passwd=%s'
        cursor.execute(sql,[username,passwd])
        result = cursor.fetchone()
        print(result)
        db_conn.close()
        if result:
            self.set_secure_cookie('user_id',result['user_id'],expires_days=None)
            self.set_secure_cookie('user_name',username,expires_days=None)
            self.redirect('index.html')
        else:
            msg = '用户名或密码错误'
            self.render('login.html',msg=msg)