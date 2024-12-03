#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2024 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/ClipnGPT
# Thank you for keeping the rules.
# ------------------------------------------------

import sys
import os
import time
import datetime
import codecs
import glob
import shutil

import json
import requests



# 定数の定義
CORE_PORT = '8000'
CONNECTION_TIMEOUT = 15
REQUEST_TIMEOUT = 30



class _monjyu_class:
    def __init__(self, runMode='assistant' ):
        self.runMode   = runMode

        # ポート設定等
        self.local_endpoint = f'http://localhost:{ CORE_PORT }'
        self.webui_port = str(int(CORE_PORT) + 8)
        self.webui_endpoint = self.local_endpoint.replace(CORE_PORT, self.webui_port)

    def request(self, req_mode='chat', user_id='admin', sysText='', reqText='', inpText='', ):
        res_port = ''

        # ファイル添付
        file_names = []
        try:
            response = requests.get(
                self.webui_endpoint + '/get_input_list',
                timeout=(CONNECTION_TIMEOUT, REQUEST_TIMEOUT)
            )
            if response.status_code == 200:
                results = response.json()
                for f in results['files']:
                    fx = f.split(' ')
                    if (fx[3] == 'checked'):
                        file_names.append(fx[0])
            else:
                print('error', f"Error response ({self.webui_port}/get_input_list) : {response.status_code}")
        except Exception as e:
            print('error', f"Error communicating ({self.webui_port}/get_input_list) : {e}")

        # AI要求送信
        try:
            #res_port = ''
            res_port = CORE_PORT
            response = requests.post(
                self.local_endpoint + '/post_req',
                json={'user_id': user_id, 'from_port': CORE_PORT, 'to_port': res_port,
                    'req_mode': req_mode,
                    'system_text': sysText, 'request_text': reqText, 'input_text': inpText,
                    'file_names': file_names, 'result_savepath': '', 'result_schema': '', },
                timeout=(CONNECTION_TIMEOUT, REQUEST_TIMEOUT)
            )
            if response.status_code == 200:
                if (res_port == ''):
                    res_port = str(response.json()['port'])
            else:
                print('error', f"Error response ({ CORE_PORT }/post_req) : {response.status_code}")
        except Exception as e:
            print('error', f"Error communicating ({ CORE_PORT }/post_req) : {e}")

        # AI結果受信
        res_text = ''
        if res_port != '':
            try:

                # AIメンバー応答待機
                timeout = time.time() + 120
                while time.time() < timeout:

                    response = requests.get(
                        self.local_endpoint + '/get_sessions_port?user_id=' + user_id + '&from_port=' + CORE_PORT,
                        timeout=(CONNECTION_TIMEOUT, REQUEST_TIMEOUT)
                    )
                    if response.status_code == 200:
                        results = response.json()
                        key_val = f"{ user_id }:{ CORE_PORT }:{ res_port }"
                        if key_val in results:
                            if results[key_val]["out_time"] is not None:
                                res_text = str(results[key_val]["out_text"])
                                break
                        else:
                            time.sleep(1.00)
                    else:
                        print('error', f"Error response ({ CORE_PORT }/get_sessions_port) : {response.status_code} - {response.text}")

            except Exception as e:
                print('error', f"Error communicating ({ CORE_PORT }/get_sessions_port) : {e}")

        return res_text



class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "execute_monjyu_request"
        self.func_ver  = "v0.20241029"
        self.func_auth = "n9UbwFiHQDP7UfVFM01VFS6M/2A7j1VoYhPAse082fa4FwZbpYP3S+LcetDyaAi2"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
この機能は、RealTimeAPIセッションからのみ実行する。
この機能で、画像認識機能などマルチモーダルなAI機能が呼び出せます。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "runMode": {
                        "type": "string",
                        "description": "実行モード 例) assistant"
                    },
                    "userId": {
                        "type": "string",
                        "description": "ユーザーID 例) admin"
                    },
                    "reqText": {
                        "type": "string",
                        "description": "要求文字列 例) 添付画像を解説して？"
                    },
                },
                "required": ["runMode", "userId", "reqText"]
            }
        }

        # 初期設定
        self.runMode = 'assistant'
        self.monjyu  = _monjyu_class()
        
    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        runMode = None
        userId  = None
        reqText = None
        if (json_kwargs is not None):
            args_dic = json.loads(json_kwargs)
            runMode  = args_dic.get('runMode')
            userId   = args_dic.get('userId')
            reqText  = args_dic.get('reqText')

        if (runMode is None) or (runMode == ''):
            runMode      = self.runMode
        else:
            self.runMode = runMode

        # 処理
        req_mode = 'clip'
        sysText  = 'あなたは美しい日本語を話す賢いアシスタントです。'
        reqText  = reqText
        inpText  = ''
        resText  = self.monjyu.request(req_mode=req_mode, user_id=userId, sysText=sysText, reqText=reqText, inpText=inpText,)

        # 戻り
        dic = {}
        if (resText != ''):
            dic['result'] = "ok"
            dic['result_text'] = resText
        else:
            dic['result'] = "ng"
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump

if __name__ == '__main__':

    ext = _class()
    json_dic = {}
    json_dic['runMode'] = "assistant"
    json_dic['userId']  = "admin"
    json_dic['reqText'] = "おはようございます"
    json_kwargs = json.dumps(json_dic, ensure_ascii=False, )
    print(ext.func_proc(json_kwargs))

    time.sleep(60)


