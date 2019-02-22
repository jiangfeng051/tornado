#!/usr/bin/python
# -*- coding: UTF-8 -*-
#date:2019/2/22
#Author:jiangfeng

from kubernetes import watch,client,config

class K8sConnect:
    def connect(self):
        config.kube_config.load_kube_config(config_file="kubeconfig.yaml")