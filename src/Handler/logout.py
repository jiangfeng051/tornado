#date:2018/8/30

import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from utils.connectdb import DbConnect


class LogoutHandler(tornado.web.RequestHandler):
    #清除cookie，并且跳转到登录页面
    def get(self):
        self.clear_cookie('user_id')
        self.clear_cookie('user_name')
        self.redirect('/login')