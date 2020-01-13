#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Project: PROJECTNAME(PROJECTURL) 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-13 18:14:51 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-14 15:19:33 
# 本代码从html2bbcode库修改而来,因为不知怎么调用此库, 所以直接改了源码
# 需要安装此库直接pip install html2bbcode即可.

from configparser import RawConfigParser
from html.parser import HTMLParser
from collections import defaultdict
from os.path import join, dirname

class Attributes(dict):
    def __getitem__(self, name):
        try:
            return super(Attributes, self).__getitem__(name)
        except KeyError:
            return ''

class ConfigParser(RawConfigParser, object):
    def get(self, section, option):
        value = super(ConfigParser, self).get(section, option)
        return value.replace('\\n', '\n')

class HTML2BBCode(HTMLParser):

    def __init__(self, map=None):
        HTMLParser.__init__(self)
        self.map = RawConfigParser()
        self.map.read(join(dirname(__file__),'data/defaults.conf'))
        if map:
            self.map.read(map)

    def handle_starttag(self, tag, attrs):
        if self.map.has_section(tag):
            self.data.append(self.map.get(tag, 'start') % Attributes(attrs or {}))

    def handle_endtag(self, tag):
        if self.map.has_section(tag):
            self.data.append(self.map.get(tag, 'end'))

    def handle_data(self, data):
        self.data.append(data)

    def feed(self, data):
        self.data = []
        HTMLParser.feed(self, data)
        return u''.join(self.data)

def trans(instr):
    a = HTML2BBCode()
    #print(a.config)
    b = str(a.feed(instr))
    return b




def run():
    from lib.chanzhi_class import chanzhi
    cz = chanzhi()
    sqli = "select pid, message from " + cz.DEST_DB + ".pre_forum_post;"
    #sqli = "select id, content from " + cz.ORIGON_DB + ".eps_thread;"
    sqli2 = '''
    update %s.pre_forum_post set message="%s" where pid=%s;
    '''
    conn =cz.getDBH()
    cur = conn.cursor()
    cur.execute(sqli)
    for pid, message in cur.fetchall():
	#开始转码
        resp = trans(message)
        #print(resp)
        #return
        resp = resp.replace("'", "\\'")
        resp = resp.replace('\\', '\\\\')
        resp = resp.replace('"', '\\"')
        #三步replace, 因为sql语句中的'与"特殊含义, 所以需要提前转义.
      #  print((sqli2 % (cz.DEST_DB, resp, pid)))
        cur.execute(sqli2 % (cz.DEST_DB, resp, pid))
        conn.commit()
    cur.close()
    conn.close()

run()
