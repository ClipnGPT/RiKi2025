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

import os
import datetime
import urllib
from sqlalchemy import create_engine
import pyodbc

import pandas as pd



# インターフェース
qPath_output = 'temp/output/'



class _database:

    # 設定
    def __init__(self, ):

        # データベース定義
        self.azip_db_server     = 'tcp:azipdevsql.database.windows.net,1433'
        self.azip_db_database   = 'AZiP社内システム'
        self.azip_db_username   = 'sanko'
        self.azip_db_password   = 'System3022'

        #self.勤怠_db_server     = 'tcp:azipdevsql.database.windows.net,1433'
        #self.勤怠_db_database   = '三光勤怠管理DB'
        #self.勤怠_db_username   = 'sanko'
        #self.勤怠_db_password   = 'System3022'
        self.勤怠_db_server     = 'tcp:azipdevsql.database.windows.net,1433'
        self.勤怠_db_database   = 'AZiP社内システム'
        self.勤怠_db_username   = 'sanko'
        self.勤怠_db_password   = 'System3022'

        self.portal_db_server   = 'tcp:azipdevsql.database.windows.net,1433'
        self.portal_db_database = 'A-ZiPポータルDB'
        self.portal_db_username = 'sanko'
        self.portal_db_password = 'System3022'

        self.test_db_server     = 'tcp:azipdevsql.database.windows.net,1433'
        self.test_db_database   = 'データベース名'
        self.test_db_username   = 'sanko'
        self.test_db_password   = 'System3022'

    # 初期化
    def init(self, db_server='', db_database='', db_username='', db_password='', ):
        self.db_server   = db_server
        self.db_database = db_database
        self.db_username = db_username
        self.db_password = db_password
        return True

    # DB オープン
    def open(self, update=None, ):
        connection_flag = False
        err_msg = ''
        for v in reversed(range(13,19)):
            try:

                # 読取専用
                if (update != 'yes'):
                    odbc_connect = urllib.parse.quote_plus(
                        'DRIVER={ODBC Driver ' + str(v) + ' for SQL Server};'
                        + 'SERVER=' +self.db_server+ ';DATABASE=' +self.db_database+ ';' \
                        + 'UID=' +self.db_username+ ';PWD=' +self.db_password+ ';'
                        + 'ApplicationIntent=ReadOnly;' )
                    engine = create_engine('mssql+pyodbc:///?odbc_connect=' + odbc_connect)
                    self.pdconn = engine.connect()
                    connection_flag = True
                    break

                # 更新有り
                else:
                    odbc_connect = urllib.parse.quote_plus(
                        'DRIVER={ODBC Driver ' + str(v) + ' for SQL Server};'
                        + 'SERVER=' +self.db_server+ ';DATABASE=' +self.db_database+ ';' \
                        + 'UID=' +self.db_username+ ';PWD=' +self.db_password+ ';' )
                    engine = create_engine('mssql+pyodbc:///?odbc_connect=' + odbc_connect)
                    self.pdconn = engine.connect()
                    connection_flag = True
                    break

            except Exception as e:
                #print(e)
                err_msg += str(e) + '\n'
        if (err_msg != ''):
            print(err_msg)
        return connection_flag

    # DB クローズ
    def close(self, ):
        try:
            self.pdconn.close()
            return True
        except Exception as e:
            print(e)
        return False

    # DB 取得
    def sql2pandas(self, sql='', ):
        try:
            df = pd.read_sql(sql, self.pdconn )
            return True, df
        except Exception as e:
            print(e)
        return False, None

    # DB 更新
    def execute(self, sql='', ):
        try:
            conn = self.pdconn.connection
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            #count = cursor.rowcount
            return True
        except Exception as e:
            print(e)
        return False

    # EXCEL 出力
    def pd2excel(self, pandas_df=None, filename='temp/output/yymmdd.hhmmss.data.xlsx', ):
        excel_file = filename

        try:
            pandas_df.to_excel(excel_file, sheet_name='Sheet1', index=False)
            res_excel = True
        except:
            try:
                os.remove(excel_file)
            except:
                pass

        return res_excel

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_company_internal_data_to_json_and_excel"
        self.func_ver  = "v0.20240526"
        self.func_auth = "VIvDDgsouNBf688uRtQijsnvTDcrOR09NyRY4tmyPVykrU/Ta7p8mFlnmtIbqUVxlRxYIkWZNc/raatHF0Vb4Q=="
        self.function  = {
            "name": self.func_name,
            "description": \
"""
社内システムの指定したデータベース（管理、勤怠、日報、データベース名）でSQLを実行する。
結果はjsonやEXCELで出力する。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "database": {
                            "type": "string",
                            "description": "データベースの指定 管理,勤怠,日報またはデータベース名 (例) 管理 "
                    },
                    "SQL": {
                            "type": "string",
                            "description": "実行するSQL (例) SELECT TOP 100 * FROM M得意先 "
                    },
                },
                "required": ["SQL"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        try:
            os.makedirs(qPath_output)
        except:
            pass
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        database = None
        sql      = None
        update   = None #非公開パラメータ
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            database = args_dic.get('database')
            sql      = args_dic.get('SQL')
            update   = args_dic.get('update')

        # データベース選択
        _DB = _database()
        if   (database is None) or (database == '管理'):
            _DB.init(_DB.azip_db_server, _DB.azip_db_database, _DB.azip_db_username, _DB.azip_db_password, )
        elif (database == '勤怠'):
            _DB.init(_DB.勤怠_db_server, _DB.勤怠_db_database, _DB.勤怠_db_username, _DB.勤怠_db_password, )
        elif (database == '日報'):
            _DB.init(_DB.portal_db_server, _DB.portal_db_database, _DB.portal_db_username, _DB.portal_db_password, )
        else: #データベース名
            _DB.init(_DB.test_db_server, database, _DB.test_db_username, _DB.test_db_password, )

        # DBオープン
        res = _DB.open(update=update, )
        if (res == False):
            msg = 'DB Open Error !'
            dic = {}
            dic['result']  = 'ng'
            dic['message'] = msg
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

        # SQL更新
        if (update == 'yes'):
            dic = {}
            res = _DB.execute(sql=sql, )
            if (res == True):
                _DB.close()
                dic['result']  = 'ok'
            else:
                _DB.close()
                dic['result']  = 'ng'
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

        # SQL検索
        if (update != 'yes'):
            try:
                res, pandas_df = _DB.sql2pandas(sql=sql, )
            except Exception as e:
                print(e)
                _DB.close()
                dic = {}
                dic['result']  = 'ng'
                dic['message'] = e
                json_dump = json.dumps(dic, ensure_ascii=False, )
                return json_dump

        # DBクローズ
        _DB.close()

        if (res != True):
            msg = 'DB SQL Error !'
            dic = {}
            dic['result']  = 'ng'
            dic['message'] = msg
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

        if (len(pandas_df) == 0):
            msg = 'NO DATA !'
            dic = {}
            dic['result']  = 'ng'
            dic['message'] = msg
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump
 
        #if (len(pandas_df) > 1000):
        #    msg = 'MAX LIMIT 1000 !'
        #    dic = {}
        #    dic['result']  = 'ng'
        #    dic['message'] = msg
        #    json_dump = json.dumps(dic, ensure_ascii=False, )
        #    return json_dump
 
        # JSON化 (100件以下)
        out_json = None
        if (len(pandas_df) <= 100):
            out_json = pandas_df.to_json(force_ascii=False)

        # EXCEL出力
        nowTime  = datetime.datetime.now()
        excel_path = qPath_output + nowTime.strftime('%Y%m%d.%H%M%S') + '.data.xlsx'
        excel_res = _DB.pd2excel(pandas_df=pandas_df, filename=excel_path, )
        if (excel_res == False):
            excel_path = None

        dic = {}
        if (out_json is not None) or (excel_path is not None):
            dic['result'] = 'ok'
            if (out_json is not None):
                dic['json']   = out_json
            if (excel_path is not None):
                dic['excel_path'] = excel_path
        else:
            dic['result'] = 'ng'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "database" : "管理", "SQL" : "SELECT TOP 1 * FROM M得意先 " }'))
