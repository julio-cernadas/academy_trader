#!/usr/bin/env/ python3
from sqlite3 import connect
from contextlib import contextmanager

class Base:
    '''Used for Connections to Database for SQL commands!'''
    def connect(self, sql_cmd):
        with connect('master.db', check_same_thread=False) as conn:
            cur = conn.cursor()
            cur.execute(sql_cmd)
            conn.commit()
            cur.close()

    def connect_fetch(self, sql_cmd):
        with connect('master.db', check_same_thread=False) as conn:
            cur = conn.cursor()
            cur.execute(sql_cmd)
            return cur.fetchall()[0][0]

    def connect_list(self, sql_cmd):
        with connect('master.db', check_same_thread=False) as conn:
            cur = conn.cursor()
            cur.execute(sql_cmd)
            return cur.fetchall()[0]
    
    def connect_multi(self, sql_cmd):
        with connect('master.db', check_same_thread=False) as conn:
            cur = conn.cursor()
            cur.execute(sql_cmd)
            return cur.fetchall()

