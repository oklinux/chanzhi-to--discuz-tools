#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Project: chanzhi2discuz(https://github.com/wjsaya/chanzhi2discuz)
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-11 9:44:31 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-11 13:56:31 
 
import logging

logging.basicConfig(
    filename='./log/cz2discuz.log',
    format='[%(asctime)s][%(name)s][%(levelname)s][%(module)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.INFO)

def run(cz):
    fun1(cz)
    fun2(cz)
    fun3(cz)
    fun4(cz)
    fun5(cz)
    fun6(cz)
    print("文章迁移完毕")

def fun1(cz):
    #添加分类

    ORIGON_TABLE = cz.ORIGON_DB + '.eps_category'
    DEST_TABLE = cz.DEST_DB + '.pre_portal_category'

    orignFields = 'id,     "0",  name,    "1",                 "1",               "1", "dz_admin", UNIX_TIMESTAMP(postedDate), "0",    "1",     "",          "",       "",      "./template/default:portal/list",  "./template/default:portal/view", "0",                 "20",     "1000"'
    targetFields = "catid,  upid, catname, notinheritedarticle, notinheritedblock, uid, username,   dateline,                   closed, shownav, description, seotitle, keyword, primaltplname,                     articleprimaltplname,             notshowarticlesummay, perpage, maxpages"
    WHERE = 'where type not in ("slide", "forum")'

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields, WHERE)

    if (re is True):
        logging.info("文章分类导入完毕, 后台更新缓存后生效")

    elif isinstance(re, str):
            logging.error("导入文章分类报错: " + re)

def fun2(cz):
    #把分类放到首页
    ORIGON_TABLE = cz.DEST_DB + '.pre_portal_category'
    DEST_TABLE = cz.DEST_DB + '.pre_common_nav'

    orignFields = 'catname,   "",    concat("portal.php?mod=list&catid=", catid), "",      "1",  "1",       "4",          "",   "",      "",     ""'
    targetFields = "name,     title, url,                                         identifier, type, available, displayorder, icon, subname, suburl, logo"
    #uid稍后更新, 暂时填0

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    if (re is True):
        logging.info("文章分类已加入首页导航栏,刷新前台界面生效")

    else:
        if isinstance(re, str):
            logging.error("文章分类加入首页导航栏出错: " + re)


def fun3(cz):
    #写入文章标题表
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_article'
    DEST_TABLE = cz.DEST_DB + '.pre_portal_article_title'

    orignFields =  "id,  title, author, author,   0,      0,       source, copyURL, copyURL, summary, '1',      '1',          UNIX_TIMESTAMP(addedDate)"
    targetFields = "aid, title, author, username, preaid, nextaid, `from`,   fromurl, url,     summary, contents, allowcomment, dateline"

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    if (re is True):
        logging.info("文章标题导入完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        logging.error("文章标题导入报错: " + re)
    

def fun4(cz):
    #绑定文章id与文章栏目
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_relation as r'
    DEST_TABLE = cz.DEST_DB + '.pre_portal_article_title as t, ' +  ORIGON_TABLE

    op = 'set t.catid = r.category, t.bid = r.category '
    WHERE = ' where t.aid = r.id'

    re = cz.change(DEST_TABLE, op, WHERE)

    if (re is True):
        logging.info("文章与栏目关联完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        logging.error("文章与栏目关联报错: " + re)
    
def fun5(cz):
    #更新username对应id
    TABLE = cz.DEST_DB + '.pre_portal_article_title as t, ' + cz.DEST_DB + '.pre_ucenter_members as m'

    op = 'set t.uid = m.uid '
    WHERE = ' where t.username = m.username'

    re = cz.change(TABLE, op, WHERE)

    if (re is True):
        logging.info("文章发布者id更新完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        logging.error("文章发布者id更新报错: " + re)
    
def fun6(cz):
    #迁移正文
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_article'
    DEST_TABLE = cz.DEST_DB + '.pre_portal_article_content'

    orignFields =  "id,  id,  title, content, UNIX_TIMESTAMP(addedDate), '1'"
    targetFields = "aid, cid, title, content, dateline ,                 pageorder"

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    if (re is True):
        logging.info("文章正文导入完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        logging.error("文章正文导入报错: " + re)
    

