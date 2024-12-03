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

import     AZiP_社内システム_SQL実行202405
proc_sql = AZiP_社内システム_SQL実行202405._class()

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_customer_info"
        self.func_ver  = "v0.20240526"
        self.func_auth = "B7TjduUv8DIN5hiXe9C2l0TqX0zgQa8OW7kW79xpsu0="
        self.function  = {
            "name": self.func_name,
            "description": \
"""
社内システムの得意先情報を検索し、得意先名、住所、電話番号、FAX番号等の情報を取得する。
結果はjson形式で返す。同時に同内容をEXCELへ出力する。
""",
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
        if (customer_name is not None) and (customer_name != ''):
            sql += " AND  得意先名 like '%" + customer_name + "%' \n"

        # SQL実行
        dic = {}
        dic['database'] = '管理'
        dic['SQL']      = sql
        json_dump  = json.dumps(dic, ensure_ascii=False, )
        res_json   = proc_sql.func_proc(json_dump)
        args_dic   = json.loads(res_json)
        res_okng   = args_dic.get('result')
        res_msg    = args_dic.get('message')
        res_json   = args_dic.get('json')
        excel_path = args_dic.get('excel_path')

        # JSON化
        dic = {}
        dic['result'] = res_okng
        if (res_msg is not None):
            dic['message'] = res_msg
        if (res_json is not None):
            dic['json']    = res_json
        if (excel_path is not None):
            dic['excel_path'] = excel_path
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "customer_name" : "トダ" }'))


