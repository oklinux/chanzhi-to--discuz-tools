#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:37 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-10 11:54:37 
 
import logging

logging.basicConfig(
    filename='./log/cz2discuz.log',
    format='[%(asctime)s][%(name)s][%(levelname)s][%(module)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.INFO)


def run(cz):
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_user'

    DEST_TABLE = cz.DEST_DB + '.pre_ucenter_members'
    orignFields =  'id,  account,  password, email, ip,    UNIX_TIMESTAMP(`join`), UNIX_TIMESTAMP(last),  " ",     0'
    targetFields = "uid, username, password, email, regip, regdate,                lastlogintime       ,  secques, salt"
    re1 = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    DEST_TABLE2 = cz.DEST_DB + '.pre_common_member'
    orignFields2 =  'id,  account,  password, email, UNIX_TIMESTAMP(`join`), score'
    targetFields2 = "uid, username, password, email, regdate,                credits"
    re2 = cz.transfer(ORIGON_TABLE, DEST_TABLE2, orignFields2, targetFields2)

    if (re1 and re2):
        logging.info("用户导入完毕,discuz后台更新缓存后生效")

    else:
        if isinstance(re1, str):
            logging.error("插入用户报错: " + re1)

        if isinstance(re2, str):
            logging.error("插入用户报错: " + re1)
    print("用户导入处理完成")