#date:2018/8/30

import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from utils.connectdb import DbConnect
from src.Handler.login import BaseHandler
from kubernetes import watch,client,config



class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')

