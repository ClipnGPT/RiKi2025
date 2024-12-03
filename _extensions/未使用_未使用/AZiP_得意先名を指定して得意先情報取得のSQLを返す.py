#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import json

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_customer_info_sql"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "指定した得意先の住所、電話番号、FAX番号等の情報取得するためのデータベースとSQLを返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                            "type": "string",
                            "description": "得意先の名前 (例) トダ"
                    },
                },
                "required": ["customer_name"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        customer_name = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            customer_name = args_dic.get('customer_name')

        # 検索処理
        sql  = " SELECT 得意先コード, \n"
        sql += "        得意先名, 郵便番号, 住所1, 住所2, 電話番号, FAX番号 \n"
        sql += " FROM M得意先 \n"
        sql += " WHERE 取引終了日 is Null \n"
        if (customer_name != None):
            sql += " AND  得意先名 like '%" + customer_name + "%' \n"

        # JSON化
        dic = {}
        dic['database'] = '管理'
        dic['SQL']      = sql
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "customer_name" : "トダ" }'))
