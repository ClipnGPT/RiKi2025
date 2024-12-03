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
        self.func_name = "get_daily_report_sample_sql"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "日付範囲が指定された日報情報を検索または集計するため、実行するデータベースとサンプルSQLを返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "request_type": {
                            "type": "string",
                            "description": "サンプルの種類。明細検索の場合は明細、作業時間集計の場合は集計 (例) 明細"
                    },
                    "start_date": {
                            "type": "string",
                            "description": "日付範囲の開始日付。日付は%Y/%m/%d形式 (例) 2023/07/10"
                    },
                    "end_date": {
                            "type": "string",
                            "description": "日付範囲の終了日付。日付は%Y/%m/%d形式 (例) 2023/07/14"
                    },
                    "staff_name": {
                            "type": "string",
                            "description": "社員名の指定 (例) 近藤"
                    },
                },
                "required": ["request_type", "start_date", "end_date"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        request_type = None
        start_date   = None
        end_date     = None
        staff_name   = None
        if (json_kwargs != None):
            args_dic   = json.loads(json_kwargs)
            request_type = args_dic.get('request_type')
            start_date   = args_dic.get('start_date')
            end_date     = args_dic.get('end_date')
            staff_name   = args_dic.get('staff_name')

        # 検索処理
        if (request_type != '集計'):
            sql  = " SELECT H.作業日付,H.社員コード,(ID.姓+ID.名) AS 社員名, \n"
            sql += "        B.工事コード,KJ.工事名,KJ.得意先コード,TK.得意先名, \n"
            sql += "        B.作業時間,B.作業内容,B.残作業 \n"
            sql += " FROM T作業日報H H \n"
            sql += " LEFT JOIN T作業日報B B \n"
            sql += " ON  B.日報伝票番号 = H.日報伝票番号 \n"
            sql += " LEFT JOIN M社員 ID \n"
            sql += " ON  ID.社員コード = H.社員コード \n"
            sql += " LEFT JOIN M工事 KJ \n"
            sql += " ON  KJ.工事コード = B.工事コード \n"
            sql += " LEFT JOIN M得意先 TK \n"
            sql += " ON  TK.得意先コード = KJ.得意先コード \n"
            sql += " WHERE H.作業日付 BETWEEN '" + start_date + "' AND '" + end_date + "' \n"
            sql += " AND   B.工事コード not in (1,10,50) \n"
            sql += " AND   B.作業時間 <> 0 \n "
            if (staff_name != None):
                sql += " AND  ( ID.姓 + ID.名 ) like '%" + staff_name + "%' \n"
            sql += " ORDER BY 作業日付,社員コード,工事コード \n"

        else:

            sql  = " SELECT B.工事コード,KJ.工事名, \n"
            sql += "        H.社員コード,(ID.姓+ID.名) AS 社員名, \n"
            sql += "        SUM(B.作業時間) \n"
            sql += " FROM T作業日報H H \n"
            sql += " LEFT JOIN T作業日報B B \n"
            sql += " ON  B.日報伝票番号 = H.日報伝票番号 \n"
            sql += " LEFT JOIN M社員 ID \n"
            sql += " ON  ID.社員コード = H.社員コード \n"
            sql += " LEFT JOIN M工事 KJ \n"
            sql += " ON  KJ.工事コード = B.工事コード \n"
            sql += " WHERE H.作業日付 BETWEEN '" + start_date + "' AND '" + end_date + "' \n"
            sql += " AND   B.工事コード not in (1,10,50) \n"
            sql += " AND   B.作業時間 <> 0 \n "
            if (staff_name != None):
                sql += " AND  ( ID.姓 + ID.名 ) like '%" + staff_name + "%' \n"
            sql += " GROUP BY B.工事コード,KJ.工事名,H.社員コード,(ID.姓+ID.名) \n"

        # JSON化
        dic = {}
        dic['database'] = '日報'
        dic['SQL']      = sql
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "request_type" : "明細", ' \
                     +  '"start_date" : "2023/07/13", ' \
                     +  '"end_date" : "2023/07/13", ' \
                     +  '"stuff_name" : "近藤" }' ))
