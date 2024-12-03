#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

# RiKi_Monjyu__addin.py

import sys
import os
import time
import datetime
import codecs
import shutil
import glob
import importlib

# インターフェースのパス設定
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチンのインポート
import _v6__qLog
qLog = _v6__qLog.qLog_class()
import _v6__qRiKi_key
qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()

# アドイン管理クラス
class _addin_class:

    # 初期化
    def __init__(self):
        self.runMode = 'debug'
        self.addins_path = '_extensions/monjyu/'
        self.secure_level = 'medium'
        self.organization_auth = ''
        self.addin_modules = {}

        # 各アドイン機能の初期化
        self.addin_directive = None
        self.addin_pdf = None
        self.addin_url = None
        self.addin_ocr = None
        self.addin_autoSandbox = None

    # 初期化メソッド
    def init(self, runMode='debug', qLog_fn='',
             addins_path='_extensions/monjyu/',
             secure_level='medium', 
             organization_auth=''):
        self.runMode = runMode
        
        # ログ設定
        self.proc_name = 'addin'
        self.proc_id = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if not os.path.isdir(qPath_log):
            os.makedirs(qPath_log)
        if qLog_fn == '':
            nowTime = datetime.datetime.now()
            qLog_fn = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn)
        qLog.log('info', self.proc_id, 'init')

        # パラメータ設定
        self.addins_path = addins_path
        self.secure_level = secure_level
        self.organization_auth = organization_auth
        self.addin_modules = {}

    # アドインのロード
    def addins_load(self):
        res_load_all = True
        res_load_msg = ''
        self.addins_unload()
        path = self.addins_path
        path_files = glob.glob(path + '*.py')
        path_files.sort()
        
        if len(path_files) > 0:
            for f in path_files:
                base_name = os.path.basename(f)
                if base_name[:4] != '_v6_' and base_name[:4] != '_v7_':
                    try:
                        # モジュールのロード
                        file_name = os.path.splitext(base_name)[0]
                        print('Addins    Loading ... "' + file_name + '" ...')
                        loader = importlib.machinery.SourceFileLoader(file_name, f)
                        ext_script = file_name
                        ext_module = loader.load_module()
                        ext_onoff = 'off'
                        ext_class = ext_module._class()
                        print('Addins    Loading ... "' + ext_script + '" (' + ext_class.func_name + ') _class.func_proc')
                        
                        # クラスの情報取得
                        ext_version = ext_class.version
                        ext_func_name = ext_class.func_name
                        ext_func_ver = ext_class.func_ver
                        ext_func_auth = ext_class.func_auth
                        ext_function = ext_class.function
                        ext_func_reset = ext_class.func_reset
                        ext_func_proc = ext_class.func_proc
                        # コード認証
                        auth = False
                        if self.secure_level in ['low', 'medium']:
                            if ext_func_auth == '':
                                auth = '1' # 注意
                                if self.secure_level != 'low':
                                    res_load_msg += '"' + ext_script + '"が認証されていません。(Warning!)' + '\n'
                            else:
                                auth = qRiKi_key.decryptText(text=ext_func_auth)
                                if auth != ext_func_name + '-' + ext_func_ver and (self.organization_auth != '' and auth != self.organization_auth):
                                    if self.secure_level == 'low':
                                        auth = '1' # 注意
                                        res_load_msg += '"' + ext_script + '"は改ざんされたコードです。(Warning!)' + '\n'
                                    else:
                                        res_load_msg += '"' + ext_script + '"は改ざんされたコードです。Loadingはキャンセルされます。' + '\n'
                                        res_load_all = False
                                else:
                                    auth = '2' # 認証
                                    ext_onoff = 'on'
                        else:
                            if ext_func_auth == '':
                                res_load_msg += '"' + ext_script + '"が認証されていません。Loadingはキャンセルされます。' + '\n'
                                res_load_all = False
                            else:
                                auth = qRiKi_key.decryptText(text=ext_func_auth)
                                if auth != ext_func_name + '-' + ext_func_ver and (self.organization_auth != '' and auth != self.organization_auth):
                                    res_load_msg += '"' + ext_script + '"は改ざんされたコードです。Loadingはキャンセルされます。' + '\n'
                                    res_load_all = False
                                else:
                                    auth = '2' # 認証
                                    ext_onoff = 'on'
                        # モジュールの登録
                        if auth != False:
                            module_dic = {
                                'script': ext_script,
                                'module': ext_module,
                                'onoff': ext_onoff,
                                'class': ext_class,
                                'func_name': ext_func_name,
                                'func_ver': ext_func_ver,
                                'func_auth': ext_func_auth,
                                'function': ext_function,
                                'func_reset': ext_func_reset,
                                'func_proc': ext_func_proc
                            }
                            self.addin_modules[ext_script] = module_dic
                            # 特定アドインのプロシージャを設定
                            if ext_script == 'addin_directive':
                                self.addin_directive = ext_func_proc
                            elif ext_script == 'addin_pdf':
                                self.addin_pdf = ext_func_proc
                            elif ext_script == 'addin_url':
                                self.addin_url = ext_func_proc
                            elif ext_script == 'addin_ocr':
                                self.addin_ocr = ext_func_proc
                            elif ext_script == 'addin_autoSandbox':
                                self.addin_autoSandbox = ext_func_proc
                    except Exception as e:
                        print(e)
        return res_load_all, res_load_msg

    # アドインのリセット
    def addins_reset(self):
        res_reset_all = True
        res_reset_msg = ''
        
        # アドインのリセット処理
        for module_dic in self.addin_modules.values():
            ext_script = module_dic['script']
            ext_func_name = module_dic['func_name']
            ext_func_reset = module_dic['func_reset']
            print('Addins    Reset   ... "' + ext_script + '" (' + ext_func_name + ') _class.func_reset')
            try:
                res = ext_func_reset()
            except:
                res = False
            if not res:
                module_dic['onoff'] = 'off'
                res_reset_all = False
                res_reset_msg += ext_func_name + 'のリセット中にエラーがありました。' + '\n'
        return res_reset_all, res_reset_msg

    # アドインのアンロード
    def addins_unload(self):
        res_unload_all = True
        res_unload_msg = ''
        # アドインのアンロード処理
        for module_dic in self.addin_modules.values():
            ext_script = module_dic['script']
            ext_func_name = module_dic['func_name']
            ext_module = module_dic['module']
            ext_class = module_dic['class']
            print('Addins    Unload  ... "' + ext_script + '" (' + ext_func_name + ') _class.func_proc')
            try:
                # クラスとモジュールの削除
                del ext_class
                del ext_module
            except:
                res_unload_all = False
                res_unload_msg += ext_func_name + 'の開放中にエラーがありました。' + '\n'
        self.addin_modules = {}
        return res_unload_all, res_unload_msg



# メイン処理
if __name__ == '__main__':
    addin = _addin_class()

    # addin 初期化
    runMode = 'debug'
    addin.init(qLog_fn='', runMode=runMode,
               addins_path='_extensions/monjyu/', secure_level='low',
               organization_auth='')

    # アドインのロード
    res, msg = addin.addins_load()
    if not res or msg:
        print(msg)
        print()

    # アドインのリセット
    res, msg = addin.addins_reset()
    if not res or msg:
        print(msg)
        print()

    # アドインのアンロード
    res, msg = addin.addins_unload()
    if not res or msg:
        print(msg)
        print()

    time.sleep(10)


