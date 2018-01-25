#!/usr/bin/python  
#-*- coding:utf-8 -*-  
__author__ = 'xujian'
############################  
#File Name: a.py
#Author: orangleliu  
#Mail: orangleliu@gmail.com  
#Created Time: 2018-01-25 10:32:13
############################ 
import hashlib
data = '{"id1":"12345","id2":"56789"}'
#timestamp='1516782574865';
import sys
timestamp=sys.argv[1]
appsecret="12345678912345678912345678912345"
newstr = data + timestamp + appsecret

print 'newstr:',newstr
l = list(newstr)
print 'l:',l
print l.sort()
print 'l:',l
s = "".join(l)
print s

sha = hashlib.sha1(s)
encrypts = sha.hexdigest()
print encrypts
