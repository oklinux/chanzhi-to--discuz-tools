#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Project: chanzhi2discuz(https://github.com/wjsaya/chanzhi2discuz)
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:30 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-10 11:54:30 
 
import logging

logging.basicConfig(
    filename='./log/cz2discuz.log',
    format='[%(asctime)s][%(name)s][%(levelname)s][%(module)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.INFO)


def run(cz):
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_category'
    DEST_TABLE = cz.DEST_DB + '.pre_forum_forum'

    orignFields =  "id,  parent,    name, 1,      0,            1,           1,           1,            1,                0,         1"
    targetFields = "fid, fup,       name, status, displayorder, allowsmilies, allowbbcode, allowimgcode, allowpostspecial, allowfeed, recyclebin"

    re1 = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)

    if (re1 is True):
        logging.info("论坛板块导入完毕")
    elif isinstance(re1, str):
        logging.error("导入论坛板块报错: " + re1)
        return False

    op = ' set type = "group"'
    WHERE = ' where fup = 0'

    re2 = cz.change(DEST_TABLE, op, WHERE)

    if (re2 is True):
        logging.info("论坛板块层级关系调整完毕")
    elif isinstance(re2, str):
        logging.error("调整板块层级关系报错: " + re2)
        return False


    print("论坛板块导入处理完成")