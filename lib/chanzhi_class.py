#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
# @Author:	wjsaya(http://www.wjsaya.top) 
# @Date:	2018-07-10 11:54:22 
# @Last Modified by:	wjsaya(http://www.wjsaya.top) 
# @Last Modified time:	2018-07-10 11:54:22 
 
import pymysql

from conf import config


class chanzhi:
    def __init__(self):
        self.setConfig()
        self.connectDB()
    
    def setConfig(self):
        self.__db_host = config.dh_host
        self.__db_user = config.db_user
        self.__db_password = config.db_password
        self.ORIGON_DB = config.ORIGON_DB
        self.DEST_DB = config.DEST_DB


    def connectDB(self):
        try:
            self.__conn = pymysql.connect(host=self.__db_host, user=self.__db_user, password=self.__db_password)
        except Exception as e:
            print("failed to connect to db")
            print(e)

    def getDBH(self):
        return self.__conn

    def transfer(self, FROM, TO, orignFields, targetFields, where = ''):
        sqli = "replace into %s (%s) select %s from %s %s;"
        print(sqli % (TO, targetFields, orignFields, FROM, where))
        cur = self.__conn.cursor()
        try:
            cur.execute(sqli % (TO, targetFields, orignFields, FROM, where))
            cur.close()
            return True
        except Exception as e:
            cur.close()
            return (e.__str__())

    def change(self, table, operate, where=''):
        sqli = "update %s %s %s;"
    #    print(sqli % (table, operate, where))
        cur = self.__conn.cursor()
        try:
            cur.execute(sqli % (table, operate, where))
            self.__conn.commit()
            cur.close()
            return True
        except Exception as e:
            cur.close()
            return (e.__str__())

    def justdoit(self, sqli):
        cur = self.__conn.cursor()
        try:
            cur.execute(sqli)
            cur.close()
            return True
        except Exception as e:
            cur.close()
            return e.__str__()
        
    def get(self, sqli):
        cur = self.__conn.cursor()
        try:
            cur.execute(sqli)
            re = cur.fetchall()
            cur.close()
            return [True, re[0][0]]
        except Exception as e:
            cur.close()
            return [False, e.__str__()]
