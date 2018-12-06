# -*- coding:utf-8  -*-
import os
import time

import DatabaseUtils
import string_utils
from IMessage import IMessage
from MessageContent import get_txt_json


class UserMessage(IMessage):

    def insert(self, conn, sql, json_content, content, from_pid, to_pid, session_id, msg_id, owner_id, did):
        conn.text_factory = str
        cursor = conn.cursor()

        time_c_u = time.time() * 1000
        cursor.execute(sql, (json_content, content, len(content), "TXT", msg_id, msg_id,
                             from_pid, did, to_pid, did, session_id,
                             0, 0, 0,
                             0, 0,
                             did, owner_id,
                             time_c_u, time_c_u))
        cursor.close()
        debug = True
        if debug:
            print cursor.lastrowid

    def get_insert_sql(self):
        return "insert into t_user_chat_message(json_content,txt_content,size,content_type,msg_server_id,order_by," \
               "f_from,from_did,f_to,to_did,session_id," \
               "is_read,other_side_is_read,associate_id," \
               "send_status,send_to_server_id," \
               "client_id,own_id," \
               "created_time,updated_time)" \
               " values(?,?,?,?,?,?," \
               "?,?,?,?,?," \
               "?,?,?," \
               "?,?," \
               "?,?," \
               "?,?)"


def create(content, pid_1, pid_2, user_chat_msg_server_id, num):
    did = 15769

    user_message = UserMessage()
    import random
    conn = DatabaseUtils.create_connection('sangforpocket139494.db')
    time_start_insert = time.time()
    for i in range(0, num):

        from_pid = pid_1
        to_pid = pid_2
        if i % random.randint(2, 5) == 0:
            from_pid = pid_2
            to_pid = pid_1
        user_message.insert(conn, user_message.get_insert_sql(), get_txt_json(content), content, from_pid, to_pid, pid_2, user_chat_msg_server_id, pid_1, did)

        user_chat_msg_server_id = user_chat_msg_server_id + 1
    conn.commit()
    conn.close()
    time_end_insert = time.time()
    print "insert num = %d , time = %s" % (num, time_end_insert - time_start_insert)


def create_copy_clear(content, pid_1, pid_2, user_chat_msg_server_id, num, copy_file_name):
    create(content, pid_1, pid_2, user_chat_msg_server_id, num)
    vacuum()
    copy(copy_file_name)
    clear()


def create_copy(content, pid_1, pid_2, user_chat_msg_server_id, num, copy_file_name):
    create(content, pid_1, pid_2, user_chat_msg_server_id, num)
    vacuum()
    copy(copy_file_name)


def vacuum():
    conn = DatabaseUtils.create_connection('sangforpocket139494.db')
    cursor = conn.cursor()
    cursor.execute("vacuum")
    cursor.close()
    conn.commit()
    conn.close()


def copy(name):
    if string_utils.empty(name):
        return
    cp = 'cp sangforpocket139494.db ./database/%s.db' % name
    os.system(cp)


def clear():
    conn = DatabaseUtils.create_connection('sangforpocket139494.db')
    cursor = conn.cursor()
    cursor.execute("delete from t_user_chat_message")
    cursor.execute("delete from sqlite_sequence where name = 't_user_chat_message'")
    cursor.close()
    conn.commit()
    conn.close()


def one_user():
    content = "----->>>>> . 2018-12-05 测试消息，内容text-37350"
    user_chat_msg_server_id = 100001
    # login user
    pid_1 = 139497
    pid_2 = 139498

    list = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000]
    db_name = "1user-chat-%s"
    for index in range(len(list)):
        create_copy_clear(content, pid_1, pid_2, user_chat_msg_server_id, list[index], db_name % list[index])


def multi_user(num):
    content = "----->>>>> . 2018-12-05 测试消息，内容text-37350"
    user_chat_msg_server_id = 100001
    # login user
    pid_1 = 139497

    list = [139498, 139496, 139495, 139494, 139493, 139492, 139491, 139490, 139489, 139488, 139487, 139486, 139485, 139484, 139483, 139482, 139481, 139480]
    db_name = "%suser-chat-%s"

    for index in range(len(list)):
        user_count = index + 1
        if user_count == 1:
            database_name = ''
        else:
            database_name = db_name % (user_count, num)
        create_copy(content, pid_1, list[index], user_chat_msg_server_id, num, database_name)

    clear()


if __name__ == '__main__':
    one_user()
    #multi_user(1000)
