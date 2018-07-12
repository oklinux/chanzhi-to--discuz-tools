#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Project: chanzhi2discuz(https://github.com/wjsaya/chanzhi2discuz)
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:37 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-12 11:18:40 
 
import logging

logging.basicConfig(
    filename='./log/cz2discuz.log',
    format='[%(asctime)s][%(name)s][%(levelname)s][%(module)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.INFO)


def run(cz):
    fun1(cz)
    fun2(cz)

def fun1(cz):
    #迁移用户信息
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_user'

    DEST_TABLE = cz.DEST_DB + '.pre_ucenter_members'
    orignFields =  'id,  account,  password, email, ip,    UNIX_TIMESTAMP(`join`), UNIX_TIMESTAMP(last),  " ",     0'
    targetFields = "uid, username, password, email, regip, regdate,                lastlogintime       ,  secques, salt"
    re1 = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    DEST_TABLE2 = cz.DEST_DB + '.pre_common_member'
    orignFields2 =  'id,  account,  password, email, UNIX_TIMESTAMP(`join`), score'
    targetFields2 = "uid, username, password, email, regdate,                credits"
    re2 = cz.transfer(ORIGON_TABLE, DEST_TABLE2, orignFields2, targetFields2)

    if (re1 is True and re2 is True):
        logging.info("用户导入完毕,discuz后台更新缓存后生效")

    else:
        if isinstance(re1, str):
            logging.error("插入用户报错: " + re1)

        if isinstance(re2, str):
            logging.error("插入用户报错: " + re1)
    print("用户导入处理完成")


    
def fun2(cz):
    #绑定用户与用户组
    ORIGON_TABLE = cz.DEST_DB + '.pre_common_usergroup as ug'
    DEST_TABLE = cz.DEST_DB + '.pre_common_member as m, ' +  ORIGON_TABLE

    op = 'set m.groupid = ug.groupid'
    WHERE = ' where m.credits between ug.creditshigher and ug.creditslower'

    re = cz.change(DEST_TABLE, op, WHERE)

    if (re is True):
        logging.info("用户组更新完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        logging.error("用户组更新报错: " + re)
    print("用户与用户组绑定处理完毕")
