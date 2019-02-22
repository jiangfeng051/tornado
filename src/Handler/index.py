#date:2018/8/30

import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from utils.connectdb import DbConnect
from tornado.escape import json_decode, json_encode, utf8
from utils.connectk8s import K8sConnect
from src.Handler.login import BaseHandler
from kubernetes import watch,client,config


k8s_conn = K8sConnect()
k8s_conn.connect()

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')


class K8sRollbackHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        namespace=[]
        v1 = client.CoreV1Api()
        for ns in v1.list_namespace().items:
            print(ns.metadata.name)
            namespace.append(ns.metadata.name)
