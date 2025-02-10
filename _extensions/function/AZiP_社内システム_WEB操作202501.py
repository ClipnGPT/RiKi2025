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
import codecs

# インターフェース
qIO_func2py       = 'temp/browser操作Agent_func2py.txt'



def io_text_write(filename='', text='', ):
    try:
        w = codecs.open(filename, 'w', 'utf-8')
        w.write(text)
        w.close()
        w = None
        return True
    except:
        pass
    return False



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "operation_internal_web_systems"
        self.func_ver  = "v0.20250101"
        self.func_auth = "UF/8l+PtMmcFgIQ+88JXQFPzB2J7DgWaR98Ak66/lK9oq4l4e3abF3mmYaz8lz00"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
この機能は、社内システム(WEB) 出退勤,日報,掲示板 の操作専用の機能です。
ログイン,出勤,退勤の操作が実行できます。
この機能から、自律的にブラウザ操作が可能なAIエージェント Web-Agent(ウェブエージェント: webBrowser_operation_agent ) に操作指示して実行します。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "system_name": {
                            "type": "string",
                            "description": "社内システムの名前 出退勤,日報または掲示板 (例) 日報"
                    },
                    "operation": {
                            "type": "string",
                            "description": "操作内容 ログイン,出勤,退勤 (例) ログイン"
                    },
                },
                "required": ["system_name", "operation"]
            }
        }

        res = self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        system_name = None
        operation = None
        if (json_kwargs != None):
            args_dic = json.loads(json_kwargs)
            system_name = args_dic.get('system_name')
            operation = args_dic.get('operation')

        # 操作内容生成
        req_text = ''
        if (system_name == '日報') and (operation == 'ログイン'):
            req_text += f"社内システム({ system_name })の{ operation }操作を実行してください。\n"
            req_text += f"URLは、'https://azip-portal.azurewebsites.net/'にアクセスしてください。\n"
            req_text += f"ログインIDは'95'です。パスワードは'95secret'です。\n"
            req_text += f"メニュー画面が出たら操作は停止してください。\n"

        if (system_name == '掲示板') and (operation == 'ログイン'):
            req_text += f"社内システム({ system_name })の{ operation }操作を実行してください。\n"
            req_text += f"URLは、'https://azip-whiteboard.azurewebsites.net/WhiteBoard/'にアクセスしてください。\n"
            req_text += f"ログインIDは'95'です。パスワードは'95secret'です。\n"
            req_text += f"ホワイトボード画面が出たら操作は停止してください。\n"

        if (system_name == '出退勤') and (operation == 'ログイン'):
            req_text += f"社内システム({ system_name })の{ operation }操作を実行してください。\n"
            req_text += f"URLは、'https://azipdevweb.azurewebsites.net/azipsyanaisystem/index.aspx'にアクセスしてください。\n"
            req_text += f"ログインIDは'95'です。パスワードは'95secret'です。\n"
            req_text += f"メニュー画面が出たら操作は停止してください。\n"

        # 操作
        res_okng = 'ng'
        res_msg  = f"社内システム({ system_name })の{ operation }操作の依頼が失敗しました。" 
        if (req_text != ''):
            req_dic  = { "request_text" : req_text }
            req_dump = json.dumps(req_dic, ensure_ascii=False, )
            res = io_text_write(filename=qIO_func2py, text=req_dump, )
            if (res == True):
                res_okng = 'ok'
                res_msg  = f"AIエージェント Web-Agent(ウェブエージェント) に、社内システム({ system_name })の{ operation }操作を依頼しました。\n" 
                res_msg += 'しばらくお待ちください。\n'

        # JSON化
        dic = {}
        dic['result'] = res_okng
        if (res_msg is not None):
            dic['message'] = res_msg
        json_dump = json.dumps(dic, ensure_ascii=False, )
        return json_dump



if __name__ == '__main__':

    ext = _class()
    print(ext.func_proc('{ "system_name" : "日報", "operation" : "ログイン" }'))


