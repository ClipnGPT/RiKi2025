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

import json

import socket
qHOSTNAME = socket.gethostname().lower()

import requests



# インターフェース

ext_assistant = {}
ext_assistant['kondou-latitude'] = {"name": "近藤PC",
                                    "id": "kondou-latitude",
                                    "rest_url": "http://kondou-latitude:61101/v0/assistant",
                                    "auth_key": "secret" }
ext_assistant['surface-pro7']    = {"name": "受付PC",
                                    "id": "surface-pro7",
                                    "rest_url": "http://surface-pro7:61101/v0/assistant",
                                    "auth_key": "secret" }
ext_assistant['test-10access64'] = {"name": "案内PC",
                                    "id": "test-10access64",
                                    "rest_url": "http://test-10access64:61101/v0/assistant",
                                    "auth_key": "secret" }



class com_class:
    def __init__(self, runMode='assistant', ):
        self.runMode = runMode
        self.conn_wait = 5
        self.proc_wait = 120

    def rest_interface(self, rest_url='http://localhost:61101/v0/assistant', auth_key='secret', request_text='おはよう', ):
        res_okng = 'ng'
        res_text = '!'

        # 送信
        headers = {
            'Authorization': f'Bearer { auth_key }',
            'Content-Type': 'application/json; charset=utf-8'
        }
        data = {
            'request_text': request_text
        }

        try:
            print('通信 ...')
            # POSTリクエストを送信、接続タイムアウト5秒、応答タイムアウト120秒
            response = requests.post(rest_url, json=data, headers=headers, timeout=(self.conn_wait, self.proc_wait))

            # ステータスコードをチェック
            if response.status_code == 200:
                # レスポンスのJSONをデコード
                response_data = response.json()
                res_okng = response_data.get('result', 'ng')
                res_text = response_data.get('result_text', '!')
            else:
                print(f"Request failed with status code { response.status_code }")
        except requests.exceptions.Timeout:
            print("Request timed out")
        except requests.exceptions.RequestException as e:
            print(e)

        if (res_text != '') and (res_text != '!'):
            print('通信 OK')

        return res_okng, res_text

class _class:

    def __init__(self, ):
        self.version   = "v0"
        self.func_name = "comunicate_external_assistant"
        self.func_ver  = "v0.20240518"
        self.func_auth = "hMzhKeF/wY5XJQgML380nfC36y6H9KFy/g3ISL/MLBXC2TybCL3c43DsnqJUBFGg"
        self.function  = {
            "name": self.func_name,
            "description": \
"""
外部のAIアシスタントと連携する。
外部のAIアシスタントは、あなたと同様の機能を実行できます。
例えば、以下のような連携を行います。
・受付PCから案内PCへ　「来客対応をお願いします」の音声合成を依頼する。
・近藤PCから受付PCへ　「しばらくお待ちください」の音声合成を依頼する。
利用できるAIアシスタントIDは kondou-latitude,surface-pro7,test-10access64 です。
kondou-latitude(近藤PC)は、近藤さんのアシスタント機能を実行しています。
surface-pro7(受付PC)は、会社入口に設置され、無人受付機能を実行しています。
test-10access64(案内PC)は、会社事務室に設置され、リアルタイム音声案内を実行しています。
""",
            "parameters": {
                "type": "object",
                "properties": {
                    "runMode": {
                        "type": "string",
                        "description": "実行モード 例) assistant"
                    },
                    "assistant_id": {
                        "type": "string",
                        "description": "AIアシスタントID kondou-latitude,surface-pro7,test-10access64 例) test-10access64"
                    },
                    "comunicate_text": {
                        "type": "string",
                        "description": "依頼内容 例) 「坪田」様が「打ち合わせ」の件で来社されています。"
                    },
                },
                "required": ["runMode", "assistant_id", "comunicate_text"]
            }
        }

        # 初期設定
        self.runMode  = 'assistant'
        self.com_proc = com_class(runMode=self.runMode, )
        self.func_reset()

    def func_reset(self, ):
        return True

    def func_proc(self, json_kwargs=None, ):
        #print(json_kwargs)

        # 引数
        runMode         = None
        assistant_id    = None
        comunicate_text = None
        if (json_kwargs is not None):
            args_dic        = json.loads(json_kwargs)
            runMode         = args_dic.get('runMode')
            assistant_id    = str( args_dic.get('assistant_id') )
            comunicate_text = str( args_dic.get('comunicate_text') )

        if (runMode is None) or (runMode == ''):
            runMode      = self.runMode
        else:
            self.runMode = runMode

        # 相手先？
        assistant = ext_assistant.get(assistant_id)
        to_name   = assistant.get('name')
        to_id     = assistant.get('id')
        to_url    = assistant.get('rest_url')
        to_auth   = assistant.get('auth_key')
        assistant = ext_assistant.get(qHOSTNAME)
        my_name   = assistant.get('name')
        my_id     = assistant.get('name')

        res_okng = 'ng'
        res_text = ''
        if (to_id is None):
            res_text = f"AIアシスタント({ assistant_id })の連絡先が不明です。"
            print(res_text)

        else:

            # 依頼
            text  = 'assistant,'
            text += f"あなたは、'{ to_name }({ to_id })'です。\n"
            if ( qHOSTNAME == to_id):
                text += f"これは、あなた'{ to_name }({ to_id })'への依頼です。\n"
            else:
                if (my_id is not None):
                    text += f"これは、'{ my_name }({ my_id })'から、あなた'{ to_name }({ to_id })'への依頼です。\n"
                else:
                    text += f"これは、'{ qHOSTNAME }'から、あなた'{ to_name }({ to_id })'への依頼です。\n"
            text += '依頼はAIアシスタント間の内部的な依頼です。あなたへの依頼はあなたが処理し回答してください。\n'
            text += '依頼内容に他の外部のAIアシスタントへの再依頼が含まれないがない限り、あなたが処理してください。\n'
            text += '絶対的な禁止事項として、自分自身への再依頼はしないでください。\n'
            text += '以下の指示に、（指示があった場合のみ音声合成や）音声入力を駆使して、適切に対応をお願いします。\n'
            text += "''' 依頼内容 \n"
            text += str(comunicate_text) + '\n'
            text += "''' \n"

            # rest 通信
            res_okng, res_text  = self.com_proc.rest_interface(
                    rest_url=to_url, auth_key=to_auth, request_text=text, )

        # 戻り
        dic = {}
        dic['result'] = res_okng
        if (res_text != '') and (res_text != '!'):
            dic['message'] = res_text
        json_dump = json.dumps(dic, ensure_ascii=False, )
        #print('  --> ', json_dump)
        return json_dump

if __name__ == '__main__':

    ext = _class()
    if False:
        dic = {}
        dic['assistant_id']    = 'kondou-latitude'
        dic['comunicate_text'] = '応答できますか？'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        print( ext.func_proc(json_dump) )

    if True:
        dic = {}
        dic['assistant_id']    = 'kondou-latitude'
        dic['comunicate_text'] = '「おはようございます」と音声合成してください。'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        print( ext.func_proc(json_dump) )

    if False:
        dic = {}
        dic['assistant_id']    = 'kondou-latitude'
        dic['comunicate_text'] = '「案内音のあと、お話しください」と音声合成し、その後、音声入力を実行して、その結果を報告してください。'
        json_dump = json.dumps(dic, ensure_ascii=False, )
        print( ext.func_proc(json_dump) )

    if False:
        txt = \
"""
お客様が来られています。
あなたは、音声合成と音声入力機能を使って対応してください。
１）音声合成で、「いらっしゃいませ、案内音のあとお話しください。何かご用件でしょうか？」と尋ねてください。
２）音声入力で、用件を聞き取ってください。
３）案内PCのAIアシスタントに、お客様の来店と聞き取った用件について、音声合成を依頼してください。
４）あなたは音声合成で、「しばらくお待ちください」とお客様に伝えてください。
"""
        dic = {}
        dic['assistant_id']    = 'kondou-latitude'
        dic['comunicate_text'] = txt
        json_dump = json.dumps(dic, ensure_ascii=False, )
        print( ext.func_proc(json_dump) )


