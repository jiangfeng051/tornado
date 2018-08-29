#date:2018/8/29

import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')