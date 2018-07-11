#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:32 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-10 11:54:32 
 
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
    print("跟帖导入处理完成")

def fun1(cz):
    #主贴
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_thread'
    DEST_TABLE = cz.DEST_DB + '.pre_forum_post'
    orignFields =   "id,  id,  1,     board, author, content, UNIX_TIMESTAMP(addedDate)"
    targetFields  = "tid, pid, first, fid,   author, message, dateline"
    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)
    
    if (re is True):
        logging.info("帖子内容迁移完毕")
    elif isinstance(re, str):
        logging.error("迁移帖子内容报错: " + re)

def fun2(cz):
    #跟帖
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_reply'
    DEST_TABLE = cz.DEST_DB + '.pre_forum_post'

    sqli = "select max(tid) from " + cz.DEST_DB + ".pre_forum_thread"
    status, re = cz.get(sqli)

    if not (status):
        logging.error("获取跟帖数量失败: " + re)
        return False

    orignFields = "id+" + str(re) + ", thread, 0,     author, content, UNIX_TIMESTAMP(addedDate)"
    #       蝉知主题贴和跟帖分表,所以thread id和跟帖的pid分离,可重复
    #       discuz中,主题贴和跟帖都在pre_forum_post中,因此两个id会冲突
    #       由于是先导入的主题帖,因此只能在将跟帖pid全部加上主题帖的最大id,防止冲突
    targetFields  = "pid,  tid,    first, author, message, dateline"
    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)
    if (re is True):
        logging.info("论坛帖子跟帖迁移完毕, 刷新前台页面生效")
    elif isinstance(re, str):
        logging.error("迁移跟帖内容报错: " + re)

def fun3(cz):
    #   更新pre_forum_thread中字段
    sqli1 = "select count(1) from " + cz.DEST_DB + ".pre_forum_thread" 
    sqli2 = "select count(1) from " + cz.DEST_DB + ".pre_forum_post_tableid" 
    status1, re1 = cz.get(sqli1)
    status2, re2 = cz.get(sqli2)
    
    if not (status1):
        logging.error("获取帖子数量失败")
        return False

    elif not (status2):
        logging.error("获取跟帖数量失败")
        return False

    else:
        num = re2 - re1
        conn = cz.getDBH()
        cur = conn.cursor()

        #主题id已经加入pre_forum_thread, 此时加入比主题id大的跟帖id即可.
        for i in range(num):
            sqli3 = 'insert into discuz.pre_forum_post_tableid values();'
            cur.execute(sqli3)
        conn.commit()
        cur.close()

def fun4(cz):
    #   更新评论中用户id
    sqli = "update " + cz.DEST_DB + ".pre_forum_post t, " + cz.DEST_DB + ".pre_ucenter_members as m  \
        set t.authorid = m.uid  \
        where t.author = m.username"

    re = cz.justdoit(sqli)

    if isinstance(re, str):
        logging.error("跟帖用户id更新出错: " + re)
        return False
    else:
        logging.info("跟帖用户id更新完毕")

def fun5(cz):
    sqli1 = "CREATE view " + cz.DEST_DB + ".temp_postcount as  \
            select count(1) as num, fid from " + cz.DEST_DB + ".pre_forum_post group by fid;"

    TABLE = cz.DEST_DB + ".pre_forum_forum, " + cz.DEST_DB + ".temp_postcount"
    op = "set " + cz.DEST_DB + ".pre_forum_forum.posts = " + cz.DEST_DB + ".temp_postcount.num"
    WHERE = "where " + cz.DEST_DB + ".pre_forum_forum.fid = " + cz.DEST_DB + ".temp_postcount.fid"

    sqli3 = "drop view " + cz.DEST_DB + ".temp_postcount;"

    re1 = cz.justdoit(sqli1)
    re2 = cz.change(TABLE, op, WHERE)
    re3 = cz.justdoit(sqli3)

    if isinstance(re1, str):
        logging.error(re1)
    if isinstance(re3, str):
        logging.error(re3)
    
    if (re2 is True):
        logging.info("帖子数量计数器更新完毕")
    elif isinstance(re2, str):
        logging.error("帖子数量计数器更新出错: " + re2)
