#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Project: chanzhi2discuz(https://github.com/wjsaya/chanzhi2discuz)
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:26 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-10 11:54:26 
 
import hashlib

def cz_encrypt(passwd, username):
#逻辑:  md5(md5(明文) . $account)      cz
#cz_admin	2371465bb4c9dc7f2db7ae263bfb13dd
    re = hashlib.md5(passwd.encode('ascii')).hexdigest()
    re = re + username
    re = hashlib.md5(re.encode('ascii'))
    print(re.hexdigest())

def discuz_encrypt(passwd, salt):
#逻辑:  MD5(MD5(明文)+salt)            discuz
#admin	4cc1b7e93037f5fb654fe31d776f3529    7505f6  123qwe
    re = hashlib.md5(passwd.encode('ascii')).hexdigest()
    re = re + salt
    re = hashlib.md5(re.encode('ascii'))
    print(re.hexdigest())


def cz_decrypt(passwd, username):
#逻辑:  md5(md5(明文) . $account)      cz
#cz_admin	2371465bb4c9dc7f2db7ae263bfb13dd
    re = hashlib.md5(passwd.encode('ascii')).hexdigest()
    re = re + username
    re = hashlib.md5(re.encode('ascii'))
    print(re.hexdigest())

def discuz_decrypt(passwd, salt):
#逻辑:  MD5(MD5(明文)+salt)            discuz
#admin	4cc1b7e93037f5fb654fe31d776f3529    7505f6  123qwe
    re = hashlib.md5(passwd.encode('ascii')).hexdigest()
    re = re + salt
    re = hashlib.md5(re.encode('ascii'))
    print(re.hexdigest())


username = 'cz_admin'
salt = '7505f6'
passwd = '123qwe'

cz_encrypt(passwd=passwd, username=username)
discuz_encrypt(passwd=passwd, salt=salt)

