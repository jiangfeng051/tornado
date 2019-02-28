#!/usr/bin/python
# -*- coding: UTF-8 -*-
#date:2019/2/21
#Author:jiangfeng

import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.escape import json_decode, json_encode, utf8
from utils.connectdb import DbConnect
import json

class HarborHandler(tornado.web.RequestHandler):
    def post(self):
        data = {'status': 'success', 'error': "", 'message': ''}
        project_name = self.get_argument('project_name')
        project_version = self.get_argument('project_version')
        db_conn = DbConnect()
        cursor = db_conn.connect()
        #获取数据库中录入的项目id和项目名称，匹配上则插入version，匹配不上则返回错误信息
        sql = '''
            select project_id,project_name from k8s_project
        '''
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            for project in result:
                print(project['project_name'],project_name)
                if project['project_name'] == project_name:
                    project_id = project['project_id']
                    sql = '''
                        insert into k8s_project_version (version_id,project_id) value (%s,%s)
                    '''
                    cursor.execute(sql,[project_version,project_id])
                    db_conn.close()
                    data['message'] = 'project {project_name} version {project_version} add is success'.format(project_name=project_name,project_version=project_version)
                    break
                else:
                    data['status'] = 'failed'
                    data['error'] = 'project {project_name} is not exist'.format(project_name=project_name)
        if data['message']:
            data['error'] = ''
        self.write(json_encode(data))