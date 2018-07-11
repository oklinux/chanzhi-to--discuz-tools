#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-11 9:44:31 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-11 13:56:31 
 
def run(cz):
#    fun1(cz)
    fun2(cz)

def fun1(cz):
    #添加分类
    DEST_TABLE = cz.DEST_DB + '.pre_portal_category'

    orignFields1 = '"1001", "0", "社区学院", "1",                "1",              "1", "dz_admin", "1531151988", "0",    "1",      "",          "",      "",       "./template/default:portal/list", "./template/default:portal/view", "0",                 "20",    "1000"'
    targetFields = "catid,  upid, catname, notinheritedarticle, notinheritedblock, uid, username, dateline,      closed, shownav, description, seotitle, keyword, primaltplname,                     articleprimaltplname,            notshowarticlesummay, perpage, maxpages"
    orignFields2 = '"1002", "1",  "技术角", "1",                 "1",              "1",   "dz_admin", "1531151988", "0",    "1",      "",          "",      "",       "./template/default:portal/list", "./template/default:portal/view", "0",                  "20",   "1000"'
    #uid稍后更新, 暂时填0
    #####稍后更改, 添加字段应该从eps_category里筛选出来, 条件为type="article"
    sqli = "insert into %s (%s) values(%s)"
    re1 = cz.justdoit(sqli % (DEST_TABLE, targetFields, orignFields1))
    re2 = cz.justdoit(sqli % (DEST_TABLE, targetFields, orignFields2))

    if (re1 is True and re2 is True):
        print("文章分类导入完毕, 后台更新缓存后生效")

    else:
        if isinstance(re1, str):
            print("导入文章分类报错: " + re1)
        if isinstance(re2, str):
            print("导入文章分类报错: " + re2)

def fun2(cz):
    #把分类放到首页
    
    ORIGON_TABLE = cz.DEST_DB + '.pre_portal_category'
    DEST_TABLE = cz.DEST_DB + '.pre_common_nav'

    orignFields = 'catname,   "",    concat("portal.php?mod=list&catid=", catid), "",      "1",  "1",       "4",          "",   "",      "",     ""'
    targetFields = "name,     title, url,                                         identifier, type, available, displayorder, icon, subname, suburl, logo"
    #uid稍后更新, 暂时填0

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    if (re is True):
        print("文章分类已加入首页导航栏,刷新前台界面生效")

    else:
        if isinstance(re, str):
            print("文章分类加入首页导航栏出错: " + re)



def fun3(cz):
    ORIGON_TABLE = cz.ORIGON_DB + '.blog'
    DEST_TABLE = cz.DEST_DB + '.pre_home_blog'

    orignFields =  "id,     0,   author,   title,   UNIX_TIMESTAMP(addedDate), views"
    targetFields = "blogid, uid, username, subject, dateline,                  viewnum"
    #uid稍后更新, 暂时填0
    sqli = "truncate" +  cz.DEST_DB + ".eps_article"

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)
    cz.justdoit(sqli)

    if (re):
        print("博客主题导入完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        print("导入博客主题报错: " + re)