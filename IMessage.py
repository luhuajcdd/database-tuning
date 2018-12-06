# -*- coding:utf-8  -*-
class IMessage:
    def insert(self,conn, sql, json_content, content, from_pid, to_pid, session_id, msg_id, owner_id, did):
        raise Exception('必须实现该方法')

