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

import datetime
import pandas as pd
import io

import     AZiP_社内システム_SQL実行202405
proc_sql = AZiP_社内システム_SQL実行202405._class()



# インターフェース

qPath_output = 'temp/output/'



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_staff_attendance_info"
        self.func_ver  = "v0.20240526"
        self.func_auth = "4acXaGs5zo6yhTBn2OmvGkblm8xQFSKEOWRBQMMz31cRXYwiXfxP9wE531pUbGBR"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
勤怠システムを検索し、社員の出退勤情報を取得する。
神戸や姫路への全出勤者の状況を検索する場合は、名前をallで呼び出す。
個人の出勤状況を検索する場合は、名前を指定して呼び出す。
名前の指定の場合、以下の名前は、一度ひらがなに戻して正しい漢字で、検索してください。

ひでお：秀夫
みなべ：三鍋
のぶまさ：信正
はまだ：濱田
おおた：大田
ひだ：飛田
どい：土居
こうへい：昂平
みちゆき：道行
こぎそ：小木曽
やすぎ：安木
いまさか：今坂

結果はjsonやEXCELで出力する。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "staff_name": {
                            "type": "string",
                            "description": "社員の名前 all,近藤などの名前 (例) all"
                    },
                },
                "required": ["staff_name"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        staff_name = None
        if (json_kwargs != None):
            args_dic  = json.loads(json_kwargs)
            staff_name = args_dic.get('staff_name')

        # 日付
        now_dt     = datetime.datetime.now()
        now_YYMMDD = now_dt.strftime('%Y/%m/%d')
        now_TIME   = now_dt.strftime('%H:%M:%S')

        # 検索処理
        sql  = " SELECT \n"
        sql += "        '" + now_YYMMDD + "' AS 勤怠日付, \n"
        sql += "        M.社員コード, \n"
        sql += "        REPLACE( REPLACE(M.社員名, '　', ''), ' ', '') AS 社員名, \n"
        sql += "        M.携帯電話番号, \n"
        sql += "        T.出勤場所名, T.出勤時刻, W.行先_予定, T.退勤時刻 \n"
        sql += " FROM      M社員 M \n"
        sql += " LEFT JOIN T勤怠 T \n"
        sql += " ON        T.社員コード = M.社員コード \n"
        sql += " AND       T.勤怠日付 = '" + now_YYMMDD + "' \n"
        sql += " LEFT JOIN Mホワイトボード W \n"
        sql += " ON        W.社員コード = M.社員コード \n"
        sql += " WHERE     M.社員コード not in (0) \n"
        sql += " AND       M.退職日 is Null \n"
        if (staff_name is not None) and (staff_name != '') and (staff_name != 'all'):
            sql += " AND REPLACE( REPLACE(M.社員名, '　', ''), ' ', '') like '%" + staff_name + "%' \n"
        sql += " ORDER BY  M.社員コード "

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


        out_json = None
        if (res_okng == 'ok'):

            # json変換
            inp_dic = json.loads(res_json)
            out_dic = {
                "勤怠日付": {},
                "社員コード": {},
                "社員名": {},
                "携帯電話番号": {},
                "出勤場所名": {},
                "出勤時刻": {},
                "行先_予定": {},
                "退勤時刻": {},
                "出退勤状況": {}
            }

            # ループして値を表示
            for key, value in inp_dic.items():
                for sub_key, sub_value in value.items():
                    if key == "勤怠日付":
                        val = str(sub_value)
                        out_dic["勤怠日付"][sub_key] = val
                    elif key == "社員コード":
                        val = str(sub_value)
                        out_dic["社員コード"][sub_key] = val
                    elif key == "社員名":
                        val = str(sub_value)
                        out_dic["社員名"][sub_key] = val
                    elif key == "携帯電話番号":
                        val = str(sub_value).strip()
                        out_dic["携帯電話番号"][sub_key] = val
                    elif key == "出勤場所名":
                        val = str(sub_value)
                        out_dic["出勤場所名"][sub_key] = val
                    elif key == "出勤時刻":
                        if (sub_value is None):
                            val = None
                            out_dic["出勤時刻"][sub_key] = val
                            out_dic["出退勤状況"][sub_key] = '＿'
                        else:
                            val = datetime.datetime.fromtimestamp(sub_value / 1000, tz=datetime.timezone.utc).strftime('%H:%M:%S')
                            out_dic["出勤時刻"][sub_key] = val
                            out_dic["出退勤状況"][sub_key] = '出勤中'
                    elif key == "行先_予定":
                        val = str(sub_value)
                        out_dic["行先_予定"][sub_key] = val
                    elif key =="退勤時刻":
                        if (sub_value is None):
                            val = None
                            out_dic["退勤時刻"][sub_key] = val
                        else:
                            val = datetime.datetime.fromtimestamp(sub_value / 1000, tz=datetime.timezone.utc).strftime('%H:%M:%S')
                            out_dic["退勤時刻"][sub_key] = val
                            out_dic["出退勤状況"][sub_key] = '退勤済'
                            
                            # 退勤打刻ミス？
                            if (out_dic["出勤時刻"][sub_key] is not None):
                                # 出勤時刻と退勤時刻の差を計算
                                check_in_time = datetime.datetime.fromtimestamp(inp_dic["出勤時刻"][sub_key] / 1000, tz=datetime.timezone.utc)
                                check_out_time = datetime.datetime.fromtimestamp(inp_dic["退勤時刻"][sub_key] / 1000, tz=datetime.timezone.utc)
                                time_difference = check_out_time - check_in_time
                                if (abs(time_difference.total_seconds()) <= 5 * 60):
                                    val = None
                                    out_dic["退勤時刻"][sub_key] = val
                                    out_dic["出退勤状況"][sub_key] = '出勤中'

                    if (staff_name is not None) and (staff_name != '') and (staff_name != 'all'):
                        print(f"{ key }: { val }")
                        if key =="退勤時刻":
                            print(f"出退勤状況: { out_dic["出退勤状況"][sub_key] }")

            # json変換
            out_json = json.dumps(out_dic, ensure_ascii=False, )

            # EXCEL出力
            try:
                nowTime  = datetime.datetime.now()
                excel_path = qPath_output + nowTime.strftime('%Y%m%d.%H%M%S') + '.出退勤情報.xlsx'
                pandas_df = pd.read_json(io.StringIO(out_json))
                pandas_df.to_excel(excel_path, sheet_name='Sheet1', index=False)
            except:
                excel_path = None

        # JSON化
        dic = {}
        dic['result'] = res_okng
        if (res_msg is not None):
            dic['message'] = res_msg
        if (out_json is not None):
            dic['json']    = out_json
        if (excel_path is not None):
            dic['excel_path'] = excel_path
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "staff_name" : "近藤" }'))
    #print(ext.func_proc('{}'))


