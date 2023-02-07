#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from connects import DB
from datetime import datetime
from bs4 import BeautifulSoup
import pymysql
import json
import dateparser

db = DB()

class Parsing():
    pass

class Queries():

    def getRepostAccount(self):
        return db.q_new('social_services', 'select', """SELECT login, password, id, sessionid
                                                FROM soc_accounts 
                                                WHERE type = 'RepostsFB1'
                                                LIMIT 1""")

    def UpdateUseDate(self, id_):
        db.q_new("python_rest", 'update', """UPDATE soc_accounts
                                         SET use_date=NOW()
                                         WHERE id={0}""".format(id_))

    def getRepostProxy(self):
        return db.q_new('python_rest', 'select', """SELECT CONCAT(proxy,":",port)
                                                FROM proxies WHERE type = 'static' 
                                                AND script LIKE '%reposts_fb%' 
                                                LIMIT 1""")[0][0]

    def getTasks(self):
        return db.q('imasv2', 'select', """SELECT id,url,user_id,project_id FROM add_post 
                                           WHERE type=2 AND repost=1
                                           ORDER BY  priority DESC LIMIT 1""")

    def get_GoToken2(self):
        return db.q_new('python_rest', 'select', """SELECT sessionid
                                                    FROM soc_accounts
                                                    WHERE type='GoLogin'
                                                    ORDER BY use_date DESC LIMIT 1""")

    def get_PofileIdPort(self):
        return db.q_new('python_rest', 'select', """SELECT sessionid,port,name
                                                    FROM soc_accounts
                                                    WHERE type = 'RepostsFB1' LIMIT 1""")

    def updating(self, query):
        db.q("imasv2", 'update', query)