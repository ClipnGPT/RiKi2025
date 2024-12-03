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
        self.func_name = "update_white_board_info"
        self.func_ver  = "v0.20240606"
        self.func_auth = "vVEPH5cwvkJyYqTyq7/G3P3S5eggdLnq/ZFBy+aQdYr74FF0Jc/K7794Me8LXohR"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
社内システムの掲示板機能であるホワイトボード内容を更新する。
更新する内容がゼロバイト文字列の場合、内容を消去できます。
更新できる社員IDは、以下にリストした社員だけです。
近藤さん,社員ID=95
藤本さん,社員ID=42
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "staff_id": {
                            "type": "string",
                            "description": "社員ID (例) 95"
                    },
                    "update_text": {
                            "type": "string",
                            "description": "更新する文字列 (例) 本日6/7の午後は、客先へ外出です。"
                    },
                },
                "required": ["staff_id", "update_text"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        staff_id    = None
        update_text = None
        if (json_kwargs != None):
            args_dic    = json.loads(json_kwargs)
            staff_id    = args_dic.get('staff_id')
            update_text = args_dic.get('update_text')

        # SQL作成
        sql  =  " UPDATE Mホワイトボード \n"
        if (update_text is not None) and (update_text != ''):
            update_text = update_text.replace("'", "''")
            sql += f" SET 行先_予定 = '{ update_text }' \n"
        else:
            sql += f" SET 行先_予定 = Null \n"
        sql += f" WHERE  社員コード = { staff_id } \n"
        sql +=  " AND    社員コード in (95, 42) \n"

        # SQL実行
        dic = {}
        dic['database'] = '管理'
        dic['SQL']      = sql
        dic['update']   = 'yes'
        json_dump  = json.dumps(dic, ensure_ascii=False, )
        res_json   = proc_sql.func_proc(json_dump)
        args_dic   = json.loads(res_json)
        res_okng   = args_dic.get('result')
        res_msg    = args_dic.get('message')

        # JSON化
        dic = {}
        dic['result'] = res_okng
        if (res_msg is not None):
            dic['message']    = res_msg
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "staff_id" : "95", "update_text" : "" }'))
    #print(ext.func_proc('{}'))


