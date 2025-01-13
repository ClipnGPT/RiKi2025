#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import json
import datetime

import     AZiP_社内システム_SQL実行202405
proc_sql = AZiP_社内システム_SQL実行202405._class()

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_planned_day_off_staff"
        self.func_ver  = "v0.20250101"
        self.func_auth = "RWB17g1bkXyUbuC97KsouhaLnYVN0v7EdLP/K4gMSJNVq1u0vyJIZvsURT5Dpm5d"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
社内システムの勤退情報を検索し、今日または明日の休暇予定者(お休み予定)の情報を取得する。
結果はjson形式で返す。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_date": {
                            "type": "string",
                            "description": "勤退情報を検索する日付文字(今日または明日) (例) 明日"
                    },
                },
                "required": ["search_date"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        search_date = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            search_date = args_dic.get('search_date')

        # 検索処理
        def execute_sql (search_date='今日', hankyu_kubun="0"):
            # 検索日
            now_dt = datetime.datetime.now()
            if (search_date != '明日'):
                search_ymd = now_dt.strftime('%Y/%m/%d')
            else:
                now_dt1 = now_dt + datetime.timedelta(days=1)
                search_ymd = now_dt1.strftime('%Y/%m/%d')

            # SQL作成
            sql  = " SELECT M.社員名 FROM T有給休暇申請 T "
            sql += " LEFT JOIN M社員 M "
            sql += " ON M.社員コード = T.社員コード "
            sql += " WHERE T.有給休暇取得日 = '" + search_ymd + "' "
            sql += " AND T.半休区分コード = " + hankyu_kubun
            #sql += "union "
            #sql += " SELECT M.社員名 FROM T振替休暇届H T "
            #sql += " LEFT JOIN M社員 M "
            #sql += " ON M.社員コード = T.社員コード "
            #sql += " WHERE T.休暇取得日 = '" + search_ymd + "' "
            sql += "union "
            sql += " SELECT M.社員名 FROM T特別休暇届H H "
            sql += " LEFT JOIN T特別休暇届B B "
            sql += " ON B.特別休暇届伝票番号 = H.特別休暇届伝票番号 "
            sql += " LEFT JOIN M社員 M "
            sql += " ON M.社員コード = H.社員コード "
            sql += " WHERE B.休暇日 = '" + search_ymd + "' "
            sql += "union "
            sql += " SELECT M.社員名 FROM T欠勤届 T "
            sql += " LEFT JOIN M社員 M "
            sql += " ON M.社員コード = T.社員コード "
            sql += " WHERE T.欠勤日 = '" + search_ymd + "' "

            # SQL実行
            dic = {}
            dic['database'] = '管理'
            dic['SQL']      = sql
            json_dump = json.dumps(dic, ensure_ascii=False, )
            res_json  = proc_sql.func_proc(json_dump)
            args_dic  = json.loads(res_json)
            res_okng  = args_dic.get('result')
            res_msg   = args_dic.get('message')
            res_json  = args_dic.get('json')
            #excel_path = args_dic.get('excel_path')

            # 名前抽出
            staff_names = []
            try:
                res_dic = json.loads(res_json)
                staff_names = list( res_dic['社員名'].values() )
                staff_names = [item.replace('　', '') for item in staff_names]
                staff_names = [item.replace(' ', '')  for item in staff_names]
            except:
                pass

            return res_okng, search_ymd, staff_names

        # 当日休暇を検索
        res_okng0, search_ymd0, staff_names0 = execute_sql(search_date=search_date, hankyu_kubun="0")

        # 午前休を検索
        res_okng1, search_ymd1, staff_names1 = execute_sql(search_date=search_date, hankyu_kubun="1")

        # 午後休を検索
        res_okng2, search_ymd2, staff_names2 = execute_sql(search_date=search_date, hankyu_kubun="2")

        # JSON化
        dic = {}
        dic['result'] = res_okng0
        dic['日付'] = search_ymd0
        dic['休暇予定'] = staff_names0
        dic['午前休予定'] = staff_names1
        dic['午後休予定'] = staff_names2
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "search_date" : "今日" }'))

    print(ext.func_proc('{ "search_date" : "明日" }'))

