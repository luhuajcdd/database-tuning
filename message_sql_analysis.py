# -*- coding:utf-8  -*-
import time


def execute(conn,sql,*values):
    start = time.time() * 1000
    cursor = conn.cursor()
    cursor.execute(sql, values)
    values = cursor.fetchall()
    end = time.time() * 1000
    cursor.close()

    #print values

    return end - start