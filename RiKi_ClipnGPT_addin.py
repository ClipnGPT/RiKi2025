#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

import sys
import os
import time
import datetime
import codecs
import shutil

import glob
import importlib



# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチン
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()

import _v6__qRiKi_key
qRiKi_key = _v6__qRiKi_key.qRiKi_key_class()



class _addin:

    def __init__(self, ):
        self.runMode            = 'debug'

        self.addins_path        = '_extensions/clipngpt/'
        self.secure_level       = 'medium' 
        self.organization_auth  = ''
        self.addin_modules      = {}

        self.addin_directive    = None
        self.addin_pdf          = None
        self.addin_url          = None
        self.addin_ocr          = None
        self.addin_autoSandbox  = None

    def init(self, qLog_fn='', runMode='debug',
                addins_path='_extensions/clipngpt/',
                secure_level='medium', 
                organization_auth='',
            ):
        self.runMode            = runMode
        
        # ログ
        self.proc_name = 'addin'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        # パラメータ
        self.addins_path        = addins_path
        self.secure_level       = secure_level
        self.organization_auth  = organization_auth
        self.addin_modules      = {}

    def addins_load(self, ):
        res_load_all = True
        res_load_msg = ''
        self.addins_unload()
        #print('Load Addins... ')

        path = self.addins_path
        path_files = glob.glob(path + '*.py')
        path_files.sort()
        if (len(path_files) > 0):
            for f in path_files:
                base_name = os.path.basename(f)
                if (base_name[:4] != '_v6_') and (base_name[:4] != '_v7_'):

                    try:
                        file_name   = os.path.splitext(base_name)[0]
                        print('Addins    Loading ... "' + file_name + '" ...')
                        loader = importlib.machinery.SourceFileLoader(file_name, f)
                        ext_script = file_name
                        ext_module = loader.load_module()
                        ext_onoff  = 'off'
                        ext_class  = ext_module._class()
                        print('Addins    Loading ... "' + ext_script + '" (' + ext_class.func_name + ') _class.func_proc')
                        ext_version     = ext_class.version
                        ext_func_name   = ext_class.func_name
                        ext_func_ver    = ext_class.func_ver
                        ext_func_auth   = ext_class.func_auth
                        ext_function    = ext_class.function
                        ext_func_reset  = ext_class.func_reset
                        ext_func_proc   = ext_class.func_proc
                        #print(ext_version, ext_func_auth, )

                        # コード認証
                        auth = False
                        if   (self.secure_level == 'low') or (self.secure_level == 'medium'):
                            if (ext_func_auth == ''):
                                auth = '1' #注意
                                if (self.secure_level != 'low'):
                                    res_load_msg += '"' + ext_script + '"が認証されていません。(Warning!)' + '\n'
                            else:
                                auth = qRiKi_key.decryptText(text=ext_func_auth)
                                if  (auth != ext_func_name + '-' + ext_func_ver) \
                                and ((self.organization_auth != '') and (auth != self.organization_auth)):
                                    #print(ext_func_auth, auth)
                                    if (self.secure_level == 'low'):
                                        auth = '1' #注意
                                        res_load_msg += '"' + ext_script + '"は改ざんされたコードです。(Warning!)' + '\n'
                                    else:
                                        res_load_msg += '"' + ext_script + '"は改ざんされたコードです。Loadingはキャンセルされます。' + '\n'
                                        res_load_all = False
                                else:
                                    auth = '2' #認証
                                    ext_onoff  = 'on'
                        else:
                            if (ext_func_auth == ''):
                                res_load_msg += '"' + ext_script + '"が認証されていません。Loadingはキャンセルされます。' + '\n'
                                res_load_all = False
                            else:
                                auth = qRiKi_key.decryptText(text=ext_func_auth)
                                if  (auth != ext_func_name + '-' + ext_func_ver) \
                                and ((self.organization_auth != '') and (auth != self.organization_auth)):
                                    #print(ext_func_auth, auth)
                                    res_load_msg += '"' + ext_script + '"は改ざんされたコードです。Loadingはキャンセルされます。' + '\n'
                                    res_load_all = False
                                else:
                                    auth = '2' #認証
                                    ext_onoff  = 'on'

                        if (auth != False):
                            module_dic = {}
                            module_dic['script']     = ext_script
                            module_dic['module']     = ext_module
                            module_dic['onoff']      = ext_onoff
                            module_dic['class']      = ext_class
                            module_dic['func_name']  = ext_func_name
                            module_dic['func_ver']   = ext_func_ver
                            module_dic['func_auth']  = ext_func_auth
                            module_dic['function']   = ext_function
                            module_dic['func_reset'] = ext_func_reset
                            module_dic['func_proc']  = ext_func_proc
                            self.addin_modules[ext_script] = module_dic

                            if   (ext_script == 'addin_directive'):
                                self.addin_directive    = ext_func_proc
                            elif (ext_script == 'addin_pdf'):
                                self.addin_pdf          = ext_func_proc
                            elif (ext_script == 'addin_url'):
                                self.addin_url          = ext_func_proc
                            elif (ext_script == 'addin_ocr'):
                                self.addin_ocr          = ext_func_proc
                            elif (ext_script == 'addin_autoSandbox'):
                                self.addin_autoSandbox  = ext_func_proc

                    except Exception as e:
                        print(e)

        return res_load_all, res_load_msg

    def addins_reset(self, ):
        res_reset_all = True
        res_reset_msg = ''
        #print('Reset Addins... ')
        for module_dic in self.addin_modules.values():
            ext_script     = module_dic['script']
            ext_func_name  = module_dic['func_name']
            ext_func_reset = module_dic['func_reset']
            print('Addins    Reset   ... "' + ext_script + '" (' + ext_func_name + ') _class.func_reset')
            try:
                res = False
                res = ext_func_reset()
            except:
                pass
            if (res == False):
                module_dic['onoff'] = 'off'
                res_reset_all = False
                res_reset_msg += ext_func_name + 'のリセット中にエラーがありました。' + '\n'

        return res_reset_all, res_reset_msg

    def addins_unload(self, ):
        res_unload_all = True
        res_unload_msg = ''
        #print('Unload Addins... ')

        for module_dic in self.addin_modules.values():
            ext_script    = module_dic['script']
            ext_func_name = module_dic['func_name']
            ext_module    = module_dic['module']
            ext_class     = module_dic['class']
            ext_func_proc = module_dic['func_proc']
            print('Addins    Unload  ... "' + ext_script + '" (' + ext_func_name + ') _class.func_proc')

            try:
                #del ext_func_proc
                del ext_class
                del ext_module
            except:
                res_unload_all = False
                res_unload_msg += ext_func_name + 'の開放中にエラーがありました。' + '\n'

        self.addin_modules = {}

        return res_unload_all, res_unload_msg



if __name__ == '__main__':

        #addins = RiKi_ClipnGPT_addin._addin()
        addin = _addin()

        # addin 初期化
        runMode   = 'debug'
        addin.init(qLog_fn='', runMode=runMode,
                   addins_path='_extensions/clipngpt/', secure_level='low',
                   organization_auth='',
                  )

        res, msg = addin.addins_load()
        if (res != True) or (msg != ''):
            print(msg)
            print()

        res, msg = addin.addins_reset()
        if (res != True) or (msg != ''):
            print(msg)
            print()

        if False:
            for module_dic in addin.addin_modules.values():
                ext_script    = module_dic['script']
                ext_func_name = module_dic['func_name']
                ext_onoff     = module_dic['onoff']
                print(ext_func_name, ext_onoff, )

        res, msg = addin.addins_unload()
        if (res != True) or (msg != ''):
            print(msg)
            print()



        time.sleep(10)

