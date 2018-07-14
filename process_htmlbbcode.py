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

    def __init__(self, config=None):
        HTMLParser.__init__(self)
        self.config = ConfigParser(allow_no_value=True)
        self.config.read(join(dirname(__file__), 'data/defaults.conf'))
        if config:
            self.config.read(config)

    def handle_starttag(self, tag, attrs):
        if self.config.has_section(tag):
            self.attrs[tag].append(dict(attrs))
            self.data.append(
                self.config.get(tag, 'start') % Attributes(attrs or {}))
            if self.config.has_option(tag, 'expand'):
                self.expand_starttags(tag)

    def handle_endtag(self, tag):
        if self.config.has_section(tag):
            self.data.append(self.config.get(tag, 'end'))
            if self.config.has_option(tag, 'expand'):
                self.expand_endtags(tag)
            self.attrs[tag].pop()

    def handle_data(self, data):
        self.data.append(data)

    def feed(self, data):
        self.data = []
        self.attrs = defaultdict(list)
        HTMLParser.feed(self, data)
        return ''.join(self.data)

    def expand_starttags(self, tag):
        for expand in self.get_expands(tag):
            if expand in self.attrs[tag][-1]:
                self.data.append(
                    self.config.get(expand, 'start') % self.attrs[tag][-1])

    def expand_endtags(self, tag):
        for expand in reversed(self.get_expands(tag)):
            if expand in self.attrs[tag][-1]:
                self.data.append(
                    self.config.get(expand, 'end') % self.attrs[tag][-1])

    def get_expands(self, tag):
        expands = self.config.get(tag, 'expand').split(',')
        return [x.strip() for x in expands]

    def handle_entityref(self, name):
        self.data.append('&{};'.format(name))

    def handle_charref(self, name):
        self.data.append('&#{};'.format(name))


def trans(instr):
    a = HTML2BBCode()
    print(a.config)
    b = str(a.feed(instr))
    return b




def run():
    from lib.chanzhi_class import chanzhi
    cz = chanzhi()
    sqli = "select pid, message from " + cz.DEST_DB + ".pre_forum_post;"
    sqli2 = '''
    update %s.pre_forum_post set message="%s" where pid=%s;
    '''
    conn =cz.getDBH()
    cur = conn.cursor()
    cur.execute(sqli)
    for pid, message in cur.fetchall():
        resp = trans(message)
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