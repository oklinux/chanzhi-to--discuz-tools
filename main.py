#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Project: chanzhi2discuz(https://github.com/wjsaya/chanzhi2discuz)
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:03 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-12 11:21:05 
 
import logging

from conf import config
from lib import (process_article, process_forum, process_reply,
                 process_resetpassword, process_thread, process_user)
from lib.chanzhi_class import chanzhi

logging.basicConfig(
    filename='./log/cz2discuz.log',
    format='[%(asctime)s][%(name)s][%(levelname)s][%(module)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.INFO)

if __name__ == '__main__':
    cz = chanzhi()
    logging.info("开始迁移数据, 从{" + cz.ORIGON_DB + "} 到 {" + cz.DEST_DB + "}")
    process_user.run(cz)
    process_forum.run(cz)
    process_thread.run(cz)
    process_reply.run(cz)
    process_article.run(cz)
    process_resetpassword.run(cz)
