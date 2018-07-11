#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:28 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-10 11:54:28 
 
def run(cz):
    fun1(cz)
    fun2(cz)

def fun1(cz):
    ORIGON_TABLE = cz.ORIGON_DB + '.blog'
    DEST_TABLE = cz.DEST_DB + '.pre_home_blog'

    orignFields =  "id,     0,   author,   title,   UNIX_TIMESTAMP(addedDate), views"
    targetFields = "blogid, uid, username, subject, dateline,                  viewnum"
    #####uid稍后更新, 暂时填0
    sqli = "truncate" +  cz.DEST_DB + ".eps_article"

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)
    cz.justdoit(sqli)

    if (re is True):
        print("博客主题导入完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        print("导入博客主题报错: " + re)

def fun2(cz):
    ORIGON_TABLE = cz.ORIGON_DB + '.blog'
    DEST_TABLE = cz.DEST_DB + '.pre_home_blog'

    orignFields =  "id,     0,   author,   title,   UNIX_TIMESTAMP(addedDate), views"
    targetFields = "blogid, uid, username, subject, dateline,                  viewnum"
    #####uid稍后更新, 暂时填0
    sqli = "truncate" +  cz.DEST_DB + ".eps_article"

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)
    cz.justdoit(sqli)

    if (re is True):
        print("博客主题导入完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        print("导入博客主题报错: " + re)