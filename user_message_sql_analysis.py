# -*- coding:utf-8  -*-
'''
    SELECT * FROM `t_user_chat_message` WHERE (((`session_id` = 139494 AND `is_delete` = 'NO' ) AND `own_id` = 139497 ) AND `client_id` = 15769 ) 
    ORDER BY `order_by` DESC,`id` DESC LIMIT 20 OFFSET 0
'''
import DatabaseUtils
import message_sql_analysis


def one_user_query_page():
    session_id = 139498
    owner_id = 139497
    did = 15769
    sql = "SELECT * FROM `t_user_chat_message` WHERE (((`session_id` = ? AND `is_delete` = 'NO' ) AND `own_id` = ? ) AND `client_id` = ? ) ORDER BY `order_by` DESC,`id` DESC LIMIT 20 OFFSET 0"

    list = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000]
    db_name = "./database/1user-chat-%s.db"
    for index in range(len(list)):
        database_name = db_name % (list[index])
        get_average(database_name, did, owner_id, session_id, sql, "1 user ",1, list[index])


def multi_user_query_page():
    owner_id = 139497
    did = 15769
    sql = "SELECT * FROM `t_user_chat_message` WHERE `session_id` = ? AND `is_delete` = 'NO' AND `own_id` = ?  AND `client_id` = ?  ORDER BY `order_by` DESC,`id` DESC LIMIT 20 OFFSET 0"

    list = [139498, 139496, 139495, 139494, 139493, 139492, 139491, 139490, 139489, 139488, 139487, 139486, 139485, 139484, 139483, 139482, 139481, 139480]
    db_name = "./database/%suser-chat-1000.db"

    for index in range(len(list)):
        get_average(db_name % (index + 1), did, owner_id, list[index], sql, "%s user " % (index + 1),(index + 1),1000)


debug = False
print_info = False
print_time = True
def get_average(db, did, owner_id, session_id, sql, desc,user_count,message_count):
    if debug:
        print "db = %s,did = %s, owner_id = %s, session_id = %s, desc = %s" % (db, did, owner_id, session_id, desc)
    list_time = []
    times = 10
    for i in range(0, times):
        conn = DatabaseUtils.create_connection(db)
        list_time.append(message_sql_analysis.execute(conn, sql, session_id, owner_id, did))
    if debug:
        print "times = %s" % list_time
    average = sum(list_time) / times
    if debug:
        print "%s : average = %s ; db = %s " % (desc, average, db)
    else:
        if print_info and print_time:
            print "%s-%s , %s" % (user_count, message_count, average)
        elif print_info:
            print "%s-%s" % (user_count, message_count)
        elif print_time:
            print "%s" % (average)


if __name__ == '__main__':
    one_user_query_page()
    #multi_user_query_page()
