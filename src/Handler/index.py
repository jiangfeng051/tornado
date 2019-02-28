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
import json


k8s_conn = K8sConnect()
k8s_conn.connect()

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')


class RollbackHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        namespace=[]
        v1 = client.CoreV1Api()
        for ns in v1.list_namespace().items:
            namespace.append(ns.metadata.name)


class ListDeployHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        namespace = []
        v1 = client.CoreV1Api()
        for ns in v1.list_namespace().items:
            namespace.append(ns.metadata.name)
        self.render('rollback.html',namespace_list=namespace)
    @tornado.web.authenticated
    def post(self):
        # arg_list = self.request.body()
        # print(json.load(arg_list))
        namespace = self.get_argument('namespace')
        keyword = self.get_argument('keyword')
        print(namespace,keyword)
        data = {'status': True, 'error': "", 'message': '','data': ''}
        deploy_list=[]
        #根据namespace和keyword获取对应的deploy，如keyword为空，则获取当前namespace下的所有deploy，
        v2 = client.AppsV1Api()
        api_response = v2.list_namespaced_deployment(namespace)
        db_conn = DbConnect()
        cursor = db_conn.connect()
        for deploy in api_response.items:
            if keyword in deploy.metadata.name:
                deploy_dict = {}
                deploy_dict['deploy'] = deploy.metadata.name
                deploy_dict['image'] = deploy.spec.template.spec.containers[0].image
                deploy_dict['replicas'] = deploy.status.replicas
                deploy_dict['available'] = deploy.status.available_replicas
                if not deploy_dict['available']:
                    deploy_dict['available'] = 0
                #根据deploy_dict['deploy']获取当前deploy前5的version号
                sql='''
                    select k8s_project.project_name,k8s_project_version.version_id from 
                    k8s_project,k8s_project_version 
                    where k8s_project.project_id = k8s_project_version.project_id 
                    and k8s_project.project_name=%s order by k8s_project_version.gmt_create desc limit 3
                '''
                cursor.execute(sql,[deploy_dict['deploy']])
                result=cursor.fetchall()
                deploy_dict['version'] = result
                deploy_list.append(deploy_dict)
        print(deploy_list)
        data['data'] = deploy_list
        self.write(json.dumps(data))
