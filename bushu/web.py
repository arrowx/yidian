#!/usr/bin/python  #-*- coding:utf-8 -*-  
__author__ = 'xujian'
############################  
#File Name: web.py
#Author: orangleliu  
#Mail: orangleliu@gmail.com  
#Created Time: 2018-01-25 10:37:45
############################ 
import tornado.ioloop
import tornado.web
from tornado.options import options, define
from tornado import gen
import hashlib
import json
import logging
from tornado.ioloop import IOLoop

define("port", default=9888, help="TCP port to listen on")
logger = logging.getLogger(__name__)

appsecret="12345678912345678912345678912345"

def check_sign(sign,data):
    l = list(data)
    l.sort()
    s = "".join(l)

    sha = hashlib.sha1(s)
    encrypts = sha.hexdigest()
    logger.info("old sign:%s",sign)
    logger.info("new sign:%s",encrypts)
    if sign == encrypts:
        return True
    else:
        return False
msg = {
        '0000':'',
        '0008':'Invalid request.',
        '0009':'Unsupport params.',
        '2001':'The identifier does not exist.',
        '2002':'The resource type is not specified.'
        }

class ExampleHandler(tornado.web.RequestHandler):
    def post(self):
        result = {}
        logger.info('body:%s',self.request.body)
        logging.info('body:')
	try:
		timestamp = self.get_argument("timestamp")
		sign = self.get_argument("sign")
                logger.info('timestamp:%s',timestamp)
                logger.info('sign:%s',sign)
		if not sign or not timestamp:
                    code = "0008"
                else:
                    data =  self.request.body + timestamp + appsecret
                    if not check_sign(sign,data):
                        code = "0008"
                    else:
                        code = "0000"
	except Exception as e:
                code = "0008"
		logger.error('error :%s',str(e))

        result['code'] = code
        result['msg'] = msg[code]
        self.write(json.dumps(result))
        self.finish()
    def get(self):
        self.post()

class ActiveListHandler(tornado.web.RequestHandler):
    def post(self):
        result = {}
        logger.info('body:%s',self.request.body)
        logging.info('body:')
	try:
		timestamp = self.get_argument("timestamp")
		sign = self.get_argument("sign")
                logger.info('timestamp:%s',timestamp)
                logger.info('sign:%s',sign)
		if not sign or not timestamp:
                    code = "0008"
                data =  self.request.body + timestamp + appsecret
                if not check_sign(sign,data):
                    code = "0008"
                else:
                    code = "0000"

                    datajson = json.loads(self.request.body)
                    logger.info('datajson :%s',datajson)
                    logger.info('datajson bundle:%s',datajson['bundle'])

                    if 'bundle' in datajson:
                        if datajson['bundle'] == 'com.yq.dota':
                            code = '0000'
                            resource_type = datajson['resource_type']
                            if len(resource_type) == 0:
                                code = '2002'
                            else:
                                with open('./activelist.json','r') as fp:
                                    webdata = json.load(fp, encoding="utf-8")
                                result['inner_games'] = webdata['inner_games']
                        else:
                            code = '2001'
                    else:
                        code = '0008'
	except Exception as e:
                code = "0008"
		logger.error('error :%s',str(e))
                with open('./activelist.json','r') as fp:
                    webdata = json.load(fp, encoding="utf-8")
                result['inner_games'] = webdata['inner_games']

        result['code'] = code
        result['msg'] = msg[code]
        self.write(json.dumps(result,indent = 4,ensure_ascii=False))
        self.finish()

    def get(self):
        self.post()

class InActiveListHandler(tornado.web.RequestHandler):
    def post(self):
        result = {}
        logger.info('body:%s',self.request.body)
        logging.info('body:')
	try:
		timestamp = self.get_argument("timestamp")
		sign = self.get_argument("sign")
                logger.info('timestamp:%s',timestamp)
                logger.info('sign:%s',sign)
		if not sign or not timestamp:
                    code = "0008"
                data =  self.request.body + timestamp + appsecret
                if not check_sign(sign,data):
                    code = "0008"
                else:
                    code = "0000"

                    datajson = json.loads(self.request.body)
                    logger.info('datajson :%s',datajson)
                    logger.info('datajson bundle:%s',datajson['bundle'])

                    if 'bundle' in datajson:
                        if datajson['bundle'] == 'com.yq.dota':
                            code = '0000'
                            resource_type = datajson['resource_type']
                            if len(resource_type) == 0:
                                code = '2002'
                            else:
                                with open('./activelist.json','r') as fp:
                                    webdata = json.load(fp, encoding="utf-8")
                                result['inner_games'] = webdata['inner_games']
                        else:
                            code = '2001'
                    else:
                        code = '0008'
	except Exception as e:
                code = "0008"
		logger.error('error :%s',str(e))
                with open('./activelist.json','r') as fp:
                    webdata = json.load(fp, encoding="utf-8")
                result['inner_games'] = webdata['inner_games']

        result['code'] = code
        result['msg'] = msg[code]
        self.write(json.dumps(result,indent = 4,ensure_ascii=False))
        self.finish()

    def get(self):
        self.post()

class PromoteHandler(tornado.web.RequestHandler):
    enable = '1'
    def post(self):
        result = {}
        logger.info('body:%s',self.request.body)
        logging.info('body:')
	try:
		timestamp = self.get_argument("timestamp")
		sign = self.get_argument("sign")
                logger.info('timestamp:%s',timestamp)
                logger.info('sign:%s',sign)
		if not sign or not timestamp:
                    code = "0008"
                data =  self.request.body + timestamp + appsecret
                if not check_sign(sign,data):
                    code = "0008"
                else:
                    code = "0000"

                    #logger.info('datajson :%s',datajson)
                    datajson = json.loads(self.request.body)
                    logger.info('datajson :%s',datajson)
                    logger.info('datajson bundle:%s',datajson['bundle'])
                    if 'bundle' in datajson:
                        if datajson['bundle'] == 'com.yq.dota':
                            code = '0000'
                            if self.enable == '1':
                                result['enable_promote'] = '0'
                                self.enable = '0'
                            else:
                                result['enable_promote'] = '1'
                                self.enable = '1'
                        else:
                            code = '2001'
                    else:
                        code = '0008'
	except Exception as e:
                code = "0008"
		logger.error('error :%s',str(e))

        result['code'] = code
        result['msg'] = msg[code]
        self.write(json.dumps(result))
        self.finish()

    def get(self):
        self.post()
	

def make_app():
    return tornado.web.Application([
        (r"^/game/example", ExampleHandler),
        (r"^/game/promote/enable", PromoteHandler),
        (r"^/game/promote/active/list", ActiveListHandler),
        (r"^/game/promote/inactive/list", InActiveListHandler),
    ])

if __name__ == "__main__":
    options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
