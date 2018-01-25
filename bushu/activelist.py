#!/usr/bin/python  
#-*- coding:utf-8 -*-  
__author__ = 'xujian'
############################  
#File Name: req.py
#Author: orangleliu  
#Mail: orangleliu@gmail.com  
#Created Time: 2018-01-25 11:14:50
############################ 
import requests
import time
import hashlib
import json

def a_sign(data):
    data = data.replace(" ","")
    print data

    l = list(data)
    l.sort()
    s = "".join(l)
    sha = hashlib.sha1(s)
    encrypts = sha.hexdigest()
    print encrypts
    return encrypts


timestamp = int(time.time())
print timestamp
sign = ''
data={}
data['bundle'] = 'com.yq.dota'
data['platform'] = '0'
data['resource_type'] = ['0','4']
appsecret="12345678912345678912345678912345"
data_str = json.dumps(data).replace(" ","")
data_str = ''
print data_str
sign = a_sign(data_str + str(timestamp) + appsecret)
url = 'http://127.0.0.1:8888/game/promote/active/list'
para = {}
para['timestamp'] = timestamp 
para['sign'] = sign
print para
r = requests.post(url,params=para,data=data_str)
print r.status_code
print r.content
