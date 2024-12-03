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

import urllib
from sqlalchemy import create_engine
import pandas as pd

class _database:

    # 設定
    def __init__(self, ):

        # データベース定義
        self.azip_db_server     = 'tcp:azipdevsql.database.windows.net,1433'
        self.azip_db_database   = 'AZiP社内システム'
        self.azip_db_username   = 'sanko'
        self.azip_db_password   = 'System3022'

        self.勤怠_db_server     = 'tcp:azipdevsql.database.windows.net,1433'
        self.勤怠_db_database   = '三光勤怠管理DB'
        self.勤怠_db_username   = 'sanko'
        self.勤怠_db_password   = 'System3022'

        self.portal_db_server   = 'tcp:azipdevsql.database.windows.net,1433'
        self.portal_db_database = 'A-ZiPポータルDB'
        self.portal_db_username = 'sanko'
        self.portal_db_password = 'System3022'

    # 初期化
    def init(self, db_server='', db_database='', db_username='', db_password='', ):
        self.db_server   = db_server
        self.db_database = db_database
        self.db_username = db_username
        self.db_password = db_password
        return True

    # DB オープン
    def open(self, ):
        connection_flag = False
        err_msg = ''
        for v in reversed(range(13,19)):
            try:
                odbc_connect = urllib.parse.quote_plus(
                      'DRIVER={ODBC Driver ' + str(v) + ' for SQL Server};'
                    + 'SERVER=' +self.db_server+ ';DATABASE=' +self.db_database+ ';' \
                    + 'UID=' +self.db_username+ ';PWD=' +self.db_password+ ';' \
                    + 'ApplicationIntent=ReadOnly;' )
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

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "get_daily_report_hours_and_summary_from_project_code_to_text"
        self.func_ver  = "v0.20230803"
        self.func_auth = ""
        self.function  = {
            "name": self.func_name,
            "description": "案件コードから日報時間と案件状況サマリーをテキストで返す",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_code": {
                            "type": "string",
                            "description": "案件コード (例) '95000153' "
                    },
                },
                "required": ["project_code"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        project_code = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            project_code = str(args_dic.get('project_code'))


        _DB = _database()

        res_text  = ''
        分析_text = ''
        res_msg   = ''

        # --------
        # 案件情報
        # --------
        案件コード     = ''
        案件名         = ''
        案件工事コード = ''
        案件工事名     = ''
        営業状況コード = ''
        営業状況名     = ''
        受注日付       = ''
        案件金額合計 = 0
        原価金額合計 = 0
        案件時間合計 = 0
        原価時間合計 = 0

        _DB.init(_DB.azip_db_server, _DB.azip_db_database, _DB.azip_db_username, _DB.azip_db_password, )
        res = _DB.open()
        if (res == False):
            msg = 'DB Open Error !'
            dic = {}
            dic['result'] = 'データ取得に失敗しました'
            dic['error'] = msg
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

        sql  = " SELECT 案件管理伝票番号,案件管理名,工事コード,工事名, "
        sql += "        受注日,営業フェイズコード,営業フェイズ名,見積金額,見積原価 "
        sql += " FROM   T案件管理H "
        sql += " WHERE 案件管理伝票番号 = '" + project_code + "' "
        sql += " OR    工事コード = '" + project_code + "' "
        res, anken_df = _DB.sql2pandas(sql=sql, )
        if (res != True):
            _DB.close()
            msg = 'DB SQL Error !'
            dic = {}
            dic['result'] = 'データ取得に失敗しました'
            dic['error'] = msg
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

        _DB.close()

        if (len(anken_df) > 0):

            案件コード = anken_df.loc[0, '案件管理伝票番号']
            if (pd.isnull(案件コード)):
                案件コード = ''
            else:
                案件コード = str(案件コード)
            案件名 = anken_df.loc[0, '案件管理名']
            if (pd.isnull(案件名)):
                案件名 = 'null'
            else:
                案件名 = str(案件名)

            案件工事コード = anken_df.loc[0, '工事コード']
            if (pd.isnull(案件工事コード)):
                案件工事コード = ''
            else:
                案件工事コード = str(案件工事コード)
            案件工事名 = anken_df.loc[0, '工事名']
            if (pd.isnull(案件工事名)):
                案件工事名 = 'null'
            else:
                案件工事名 = str(案件工事名)

            受注日付 = anken_df.loc[0, '受注日']
            if (pd.isnull(受注日付)):
                受注日付 = ''
            else:
                受注日付 = 受注日付.strftime('%Y/%m/%d')

            営業状況コード = anken_df.loc[0, '営業フェイズコード']
            if (pd.isnull(営業状況コード)):
                営業状況コード = ''
            else:
                営業状況コード = str(営業状況コード)
            営業状況名 = anken_df.loc[0, '営業フェイズ名']
            if (pd.isnull(営業状況名)):
                営業状況名 = ''
            else:
                営業状況名 = str(営業状況名)
            #if (受注日付 != ''):
            #    営業状況名 += ' (受注:' + 受注日付 + ')'

            案件金額合計 = anken_df.loc[0, '見積金額']
            if (pd.isnull(案件金額合計)):
                案件金額合計 = 0
            else:
                案件金額合計 = int(案件金額合計)
            原価金額合計 = anken_df.loc[0, '見積原価']
            if (pd.isnull(原価金額合計)):
                原価金額合計 = 0
            else:
                原価金額合計 = int(原価金額合計)

            案件時間合計 = float( '{:.2f}'.format(案件金額合計 / 6250) )
            原価時間合計 = float( '{:.2f}'.format(原価金額合計 / 6250) )

        res_text += '\n' + '【案件情報】' + '\n'
        res_text += '　案件 = ' + 案件コード + '_' + 案件名 + '\n'
        res_text += '　案件工事 = ' + 案件工事コード + '_' + 案件工事名 + '\n'
        res_text += '　営業状況 = ' + 営業状況コード + '_' + 営業状況名 + '\n'
        if (受注日付 != ''):
            res_text += '　受注日付 = ' + 受注日付 + '\n'
        if (案件金額合計 != 0):
            res_text += '　案件金額 = ' + '{:.1f}'.format(案件金額合計/10000) + ' (万円)' + '\n'
            res_text += '　案件時間 = ' + '{:.2f}'.format(案件時間合計) + ' (時間)' + '\n'
        if (原価金額合計 != 0):
            res_text += '　原価金額 = ' + '{:.1f}'.format(原価金額合計/10000) + ' (万円)' + '\n'
            res_text += '　原価時間 = ' + '{:.2f}'.format(原価時間合計) + ' (時間)' + '\n'


        res_msg += '　案件情報：' + 案件コード + '：' + 案件名
        if (受注日付 != ''):
            res_msg += '　（受注 ' + 受注日付 + ' ）'
        else:
            res_msg += '　（' + 営業状況名 + '）'
        res_msg += '\n'

        if (案件金額合計 != 0) \
        or (原価金額合計 != 0):
            res_msg += '　案件金額：'
            if (案件金額合計 != 0):
                res_msg += '　見積金額＝' + '{:.1f}'.format(案件金額合計/10000) + '万円'
            if (原価金額合計 != 0):
                res_msg += '　原価予定金額＝' + '{:.1f}'.format(原価金額合計/10000) + '万円'
            res_msg += '\n'

        if (案件金額合計 != 0) \
        or (原価金額合計 != 0):
            res_msg += '　案件工数：'
            if (案件金額合計 != 0):
                res_msg += '　損益工数＝' + '{:.2f}'.format(案件時間合計) + 'h'
            if (原価金額合計 != 0):
                res_msg += '　原価予定工数＝' + '{:.2f}'.format(原価時間合計) + 'h'
            res_msg += '\n'

        # --------
        # 分析
        # --------

        # データ不明
        if (案件コード == ''):
            分析_text += '　案件情報が見つかりません' + '\n'

        else:
            # 異常データ確認
            if (営業状況コード == '500') and (受注日付 == ''):
                分析_text += '　営業状況が' + 営業状況名 + 'ですが、受注日が登録されていません' + '\n'
            if (受注日付 != '') and (営業状況コード != '500'):
                分析_text += '　受注日が登録されていますが、営業状況に' + 営業状況名 + 'が設定されています' + '\n'

            # 受注済みの場合
            if (営業状況コード == '500') or (受注日付 != ''):
                if (案件金額合計 == 0):
                    分析_text += '　受注案件ですが、見積金額が登録されていません' + '\n'
                if (原価金額合計 == 0):
                    分析_text += '　受注案件ですが、見積原価が登録されていません' + '\n'

        # --------
        # 日報工事
        # --------

        日報工事コード = ''
        日報工事名     = ''

        _DB.init(_DB.portal_db_server, _DB.portal_db_database, _DB.portal_db_username, _DB.portal_db_password, )
        res = _DB.open()
        if (res == False):
            msg = 'DB Open Error !'
            dic = {}
            dic['result'] = 'データ取得に失敗しました'
            dic['error'] = msg
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

        sql  = " SELECT 工事コード,工事名 FROM M工事 "
        sql += " WHERE 工事コード = '" + project_code + "' "
        if (案件工事コード !='' ):
            sql += " OR 工事コード = '" + 案件工事コード + "' "
        res, koji_df = _DB.sql2pandas(sql=sql, )
        if (res != True):
            _DB.close()
            msg = 'DB SQL Error !'
            dic = {}
            dic['result'] = 'データ取得に失敗しました'
            dic['error'] = msg
            json_dump = json.dumps(dic, ensure_ascii=False, )
            return json_dump

        _DB.close()

        if (len(koji_df) > 0):
            日報工事コード = koji_df.loc[0, '工事コード']
            if (pd.isnull(日報工事コード)):
                日報工事コード = ''
            else:
                日報工事コード = str(日報工事コード)
            日報工事名 = koji_df.loc[0, '工事名']
            if (pd.isnull(日報工事名)):
                日報工事名 = 'null'
            else:
                日報工事名 = str(日報工事名)

        res_text += '\n' + '【日報情報】' + '\n'
        res_text += '　日報工事 = ' + 日報工事コード + '_' + 日報工事名 + '\n'

        res_msg += '　工事情報：' + 日報工事コード + '：' + 日報工事名 + '\n'

        # --------
        # 分析
        # --------

        # データ不明
        if (日報工事コード == ''):
            分析_text += '　日報(工事コードが見つかりません' + '\n'

        else:

            # --------
            # 日報時間
            # --------

            日報時間合計 = 0
            日報最終日付 = ''

            if (案件工事コード !='' ) or (日報工事コード !='' ):

                _DB.init(_DB.portal_db_server, _DB.portal_db_database, _DB.portal_db_username, _DB.portal_db_password, )
                res = _DB.open()
                if (res == False):
                    msg = 'DB Open Error !'
                    dic = {}
                    dic['result'] = 'データ取得に失敗しました'
                    dic['error'] = msg
                    json_dump = json.dumps(dic, ensure_ascii=False, )
                    return json_dump

                sql  = " SELECT SUM(B.作業時間),MAX(H.作業日付) FROM T作業日報B B "
                sql += " LEFT JOIN T作業日報H H "
                sql += " ON H.日報伝票番号 = B.日報伝票番号 "
                # 工事コード
                if (案件工事コード !='' ):
                    if (日報工事コード !='' ):
                        sql += " WHERE 工事コード in ( " + 案件工事コード + ", " + 日報工事コード + " ) "
                    else:
                        sql += " WHERE 工事コード in ( " + 案件工事コード + " ) "
                else:
                    if (日報工事コード !='' ):
                        sql += " WHERE 工事コード in ( " + 日報工事コード + " ) "

                res, sum_df = _DB.sql2pandas(sql=sql, )
                if (res != True):
                    _DB.close()
                    msg = 'DB SQL Error !'
                    dic = {}
                    dic['result'] = 'データ取得に失敗しました'
                    dic['error'] = msg
                    json_dump = json.dumps(dic, ensure_ascii=False, )
                    return json_dump

                _DB.close()

                if (len(sum_df) > 0):
                    日報時間合計 = sum_df.iloc[0, 0]
                    if (pd.isnull(日報時間合計)):
                        日報時間合計 = 0
                    else:
                        日報時間合計 = float(日報時間合計)
                    日報最終日付 = sum_df.iloc[0, 1]
                    if (pd.isnull(日報最終日付)):
                        日報最終日付 = ''
                    else:
                        日報最終日付 = 日報最終日付.strftime('%Y/%m/%d')

                res_text += '　日報時間合計 = ' + str(日報時間合計) + ' (時間) ' + '\n'
                res_text += '　日報最終日付 = ' + str(日報最終日付) + '\n'

                res_msg += '　工数消化：'
                res_msg += '　日報全体＝' + '{:.2f}'.format(日報時間合計) + 'h'
                if (案件金額合計 != 0):
                    res_msg += '　損益消化率＝' + '{:.1f}'.format((日報時間合計/案件時間合計)*100) + '%'
                    if (日報時間合計 > 案件時間合計):
                        res_msg += '★'
                if (原価金額合計 != 0):
                    res_msg += '　原価予定消化率＝' + '{:.1f}'.format((日報時間合計/原価時間合計)*100) + '%'
                    if (日報時間合計 > 原価時間合計):
                        res_msg += '☆'
                res_msg += '\n'

            # --------
            # 分析
            # --------
            if (日報時間合計 == 0):
                分析_text += '　まだ日報は登録されていません' + '\n'

            else:

                # 工数分析
                if   (案件時間合計 > 0) and (日報時間合計 > 案件時間合計):
                    分析_text += '　★重要★　日報時間合計が、案件時間を超過しています。赤字懸念案件です' + '\n'
                elif (原価時間合計 > 0) and (日報時間合計 > 原価時間合計):
                    分析_text += '　☆注意☆　日報時間合計が、原価予定時間を超過しています。効率よく推進お願いします' + '\n'

                # --------
                # 個人時間
                # --------

                個人負荷集中発生 = 0

                _DB.init(_DB.portal_db_server, _DB.portal_db_database, _DB.portal_db_username, _DB.portal_db_password, )
                res = _DB.open()
                if (res == False):
                    msg = 'DB Open Error !'
                    dic = {}
                    dic['result'] = 'データ取得に失敗しました'
                    dic['error'] = msg
                    json_dump = json.dumps(dic, ensure_ascii=False, )
                    return json_dump

                sql  = " SELECT H.社員コード, H.社員名, SUM(B.作業時間), MAX(H.作業日付) FROM T作業日報B B "
                sql += " LEFT JOIN T作業日報H H "
                sql += " ON H.日報伝票番号 = B.日報伝票番号 "
                # 工事コード
                if (案件工事コード !='' ):
                    if (日報工事コード !='' ):
                        sql += " WHERE 工事コード in ( " + 案件工事コード + ", " + 日報工事コード + " ) "
                    else:
                        sql += " WHERE 工事コード in ( " + 案件工事コード + " ) "
                else:
                    if (日報工事コード !='' ):
                        sql += " WHERE 工事コード in ( " + 日報工事コード + " ) "
                sql += " GROUP BY H.社員コード, H.社員名 "

                res, staff_df = _DB.sql2pandas(sql=sql, )
                if (res != True):
                    _DB.close()
                    msg = 'DB SQL Error !'
                    dic = {}
                    dic['result'] = 'データ取得に失敗しました'
                    dic['error'] = msg
                    json_dump = json.dumps(dic, ensure_ascii=False, )
                    return json_dump

                _DB.close()

                if (len(staff_df) > 0):

                    res_text += '\n' + '【日報時間】' + '\n'

                    for s in range(len(staff_df)):
                        社員コード = staff_df.iloc[s, 0]
                        if (pd.isnull(社員コード)):
                            社員コード = '0'
                        else:
                            社員コード = str(社員コード)
                        社員名 = staff_df.iloc[s, 1]
                        if (pd.isnull(社員名)):
                            社員名 = ''
                        else:
                            社員名 = str(社員名)
                        日報時間 = staff_df.iloc[s, 2]
                        if (pd.isnull(日報時間)):
                            日報時間 = 0
                        else:
                            日報時間 = float( '{:.2f}'.format(日報時間) )
                        最終報告 = staff_df.iloc[s, 3]
                        if (pd.isnull(最終報告)):
                            最終報告 = ''
                        else:
                            最終報告 = 最終報告.strftime('%Y/%m/%d')

                        負荷集中 = ''
                        if (日報時間 > (日報時間合計 * 0.5)):
                            負荷集中 = ', ★負荷がものすごく集中しています(50%超)'
                            if (個人負荷集中発生 < 2):
                                個人負荷集中発生 = 2
                        elif (日報時間 > (日報時間合計 * 0.3)):
                            負荷集中 = ', ☆負荷が集中しています(30%超)'
                            if (個人負荷集中発生 < 1):
                                個人負荷集中発生 = 1

                        res_text += '　' + 社員コード + '_' + 社員名 + ' = ' + '{:.2f}'.format(日報時間) + ' (時間), 最終報告 = ' + 最終報告 + 負荷集中 + '\n'

                        res_msg += '　　' + 社員名 + '：' + '{:.2f}'.format(日報時間) + 'h' + 負荷集中 + '\n'

                # --------
                # 分析
                # --------
                if (個人負荷集中発生 == 2):
                    分析_text += '　★重要★　一部個人に負荷がものすごく集中しています' + '\n'
                if (個人負荷集中発生 == 1):
                    分析_text += '　☆注意☆　一部個人に負荷が集中しています' + '\n'

        # JSON化
        #res = pandas_df.to_json(force_ascii=False)

        # --------
        # 分析
        # --------
        if (分析_text != ''):
            res_text += '\n' + '【簡易分析】' + '\n'
            res_text += 分析_text
            res_msg  += 分析_text

        #print(res_text)
        #print()
        print(res_msg)

        dic = {}
        dic['result'] = 'データ取得できました'
        #dic['text']   = res_text
        dic['text']   = res_msg
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump

if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "project_code" : "95000153" }'))
