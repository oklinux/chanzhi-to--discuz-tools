#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Project: PROJECTNAME(PROJECTURL) 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-21 16:45:44 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-21 16:45:44 

import logging

logging.basicConfig(
    filename='./log/cz2discuz.log',
    format='[%(asctime)s][%(name)s][%(levelname)s][%(module)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.INFO)


def run(cz):
    fun1(cz)

def fun1(cz):
    #导入用户uid到pre_common_member_field_forum表

    ORIGON_TABLE = cz.DEST_DB + '.pre_ucenter_members'
    DEST_TABLE = cz.DEST_DB + '.pre_common_member_field_forum'

    orignFields =  'uid, "",        "",         "",         "",     ""'
    targetFields = "uid, medals,    sightml,    groupterms, groups, authstr"
    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    if (re is True):
        logging.info("pre_common_member_field_forum表更新完毕")

    else:
        if isinstance(re, str):
            logging.error("pre_common_member_field_forum表更新失败, 这将会导致用户重置密码失败: " + re)

    print("pre_common_member_field_forum表更新完毕")

