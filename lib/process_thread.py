#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:34 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-10 11:54:34 
 
import logging

logging.basicConfig(
    filename='./log/cz2discuz.log',
    format='[%(asctime)s][%(name)s][%(levelname)s][%(module)s]:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.INFO)

'''
    第一步：向 主题表 pre_forum_thread 中插入版块ID、用户ID、用户名、帖子标题、发帖时间等信息。
    第二步：获取第一步插入表 pre_forum_thread 的数据ID，作为主题ID,即 tid 
    第三步：向 post 分表协调表 pre_forum_post_tableid 插入一条数据，这张表中只有一个自增字段 pid 
    第四步：获取 第三步 插入表 pre_forum_post_tableid 的数据ID，作为 pid 
    第五步：向帖子表 pre_forum_post 中插入帖子相关信息，这里需要注意的是： pid为第四部的pid值，tid为第二步的tid值 
    第六步：更新版块 pre_forum_forum 相关主题、帖子数量信息 
    第七步：更新用户 pre_common_member_count 帖子数量信息 
'''
def run(cz):
    do1(cz)
    do2(cz)
    do6(cz)
    do7(cz)
    print("论坛帖子导入处理完成")
    

def do1(cz):
    #    第一步：向 主题表 pre_forum_thread 中插入版块ID、用户ID、用户名、帖子标题、发帖时间等信息。
    ORIGON_TABLE = cz.ORIGON_DB + '.eps_thread'
    DEST_TABLE = cz.DEST_DB + '.pre_forum_thread '

    orignFields =   "id,  board, title,   color,   author, UNIX_TIMESTAMP(addedDate), views, replies, repliedBy,  UNIX_TIMESTAMP(repliedDate)"
    targetFields  = "tid, fid,   subject, bgcolor, author, dateline,                  views, replies, lastposter, lastpost"

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields)
    
    if (re):
        logging.info("帖子信息导入完毕")
    elif isinstance(re, str):
        logging.error("帖子信息导入出错: " + re)


def do2(cz):
    #    第二步：获取第一步插入表 pre_forum_thread 的数据ID，作为主题ID,即 tid 
    conn = cz.getDBH()
    cur = conn.cursor()
    sqli = "select count(1) from " + cz.DEST_DB + ".pre_forum_thread"
    cur.execute(sqli)
    a = cur.fetchall()[0][0]
    for i in range(a):
        sqli3 = "insert into " + cz.DEST_DB + ".pre_forum_post_tableid values();"
        cur.execute(sqli3)
    cur.close()
    conn.commit()
    logging.info("pre_forum_thread中帖子id更新完毕")

def do3(cz):
    sqli = "update " + cz.DEST_DB + ".pre_forum_thread t, " + cz.DEST_DB + ".pre_ucenter_members as m  \
        set t.authorid = m.uid  \
        where t.author = m.username"

    re = cz.justdoit(sqli)

    if isinstance(re, str):
        logging.error("发帖用户id更新出错: " + re)
        return False
    logging.info("发帖用户id更新完毕")


def do6(cz):
    #    第六步：更新版块 pre_forum_forum 相关主题数量信息 
    sqli1 = "CREATE view " + cz.DEST_DB + ".temp_threadscount as  \
            select count(1) as num, fid from " + cz.DEST_DB + ".pre_forum_thread group by fid;"

    sqli21 = cz.DEST_DB + ".pre_forum_forum, " + cz.DEST_DB + ".temp_threadscount"
    sqli22 = "set " + cz.DEST_DB + ".pre_forum_forum.threads = " + cz.DEST_DB + ".temp_threadscount.num"
    sqli23 = "where " + cz.DEST_DB + ".pre_forum_forum.fid = " + cz.DEST_DB + ".temp_threadscount.fid"

    sqli3 = "drop view " + cz.DEST_DB + ".temp_threadscount;"

    re1 = cz.justdoit(sqli1)
    re2 = cz.change(sqli21, sqli22, sqli23)
    re3 = cz.justdoit(sqli3)

    if isinstance(re1, str):
        logging.error(re1)
    if isinstance(re3, str):
        logging.error(re3)
    
    if (re2):
        logging.info("帖子数量计数器更新完毕")
    elif isinstance(re2, str):
        logging.error("帖子数量计数器更新出错: " + re2)


def do7(cz):
    #    第七步：更新用户 pre_common_member_count 帖子数量信息 
   # sqli = "replace into discuz.pre_common_member_count(uid, threads) select distinct authorid, count(tid) from discuz.pre_forum_thread group by authorid"
    
    ORIGON_TABLE = cz.DEST_DB + '.pre_forum_thread'
    DEST_TABLE = cz.DEST_DB + '.pre_common_member_count '
    WHERE = "group by authorid"

    orignFields =   "distinct authorid, count(tid)"
    targetFields  = "uid, threads"

    re = cz.transfer(ORIGON_TABLE, DEST_TABLE, orignFields, targetFields, WHERE)

    if (re):
        logging.info("用户发帖计数更新完毕")
    elif isinstance(re, str):
        logging.error("用户发帖计数更新出错: " + re)

