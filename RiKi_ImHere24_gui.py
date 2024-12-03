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

import json

import queue

#import PySimpleGUI_key
#PySimpleGUI_License=PySimpleGUI_key.PySimpleGUI_License
import PySimpleGUI as sg

import numpy as np
import cv2

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



class _gui:

    def __init__(self, ):
        self.screen         = '0'
        self.panel          = '8--'

        self.img_file        = '_icons/RiKi_ImHere24.png'

        titlex              = os.path.basename(__file__)
        self.title          = titlex.replace('.py','')
        self.layout         = [
                            sg.InputText('Hallo World'),
                            sg.Button('OK', key='-OK-'),
                            ]

        self.theme          = 'Dark' # 'Default1', 'Dark',
        self.alpha_channel  = 1.0
        self.icon           = None
        self.font           = 'Arial 8'

        self.keep_on_top    = True
        self.no_titlebar    = True
        self.disable_close  = False
        self.resizable      = True
        self.no_border      = True

        self.window         = None
        self.left           = 0
        self.top            = 0
        self.width          = 320
        self.height         = 240



    def init(self, qLog_fn='', runMode='debug',
             screen='auto', panel='auto',
             title='', theme=None,
             keep_on_top='yes', alpha_channel='1', icon=None, ):

        #if (runMode == 'camera'):
        #    self.no_titlebar = False

        # ログ
        self.proc_name = 'gui'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        # 実行モード
        self.runMode = runMode

        # スクリーン
        if (str(screen) != 'auto'):
            try:
                self.screen = int(screen)
            except Exception as e:
                print(e)

        # パネル
        if (panel != 'auto'):
            self.panel = panel

        # タイトル
        if (title != ''):
            self.title  = title
        else:
            titlex      = os.path.basename(__file__)
            titlex      = titlex.replace('.py','')
            self.title  = titlex + '[' + runMode + ']'

        # テーマ
        if (theme is not None):
            self.theme = theme
        sg.theme(self.theme)

        # ボーダー
        if (self.no_border != True):
            self.element_padding= ((2,2),(2,2)) #((left/right),(top/bottom))
        else:
            self.element_padding= ((0,0),(0,0)) #((left/right),(top/bottom))
            sg.set_options(element_padding=(0,0), margins=(0,0), border_width=0)

        # 最前面
        if (keep_on_top != 'no'):
            self.keep_on_top = True
        else:
            self.keep_on_top = False

        # 透過表示
        if (str(alpha_channel) != ''):
            try:
                self.alpha_channel = float(alpha_channel)
            except Exception as e:
                print(e)

        # アイコン
        if (icon is not None):
            self.icon = icon

        # 表示位置
        qGUI.checkUpdateScreenInfo(update=True, )
        self.left, self.top, self.width, self.height = qGUI.getScreenPanelPosSize(screen=self.screen, panel=self.panel, )

        # レイアウト
        self.setLayout()

        # ウィンドウ設定
        self.close()
        try:
            if (qPLATFORM == 'darwin'):
                self.no_titlebar = False
            if (self.no_titlebar == True):
                self.window = sg.Window(self.title, self.layout,
                            keep_on_top=self.keep_on_top,
                            font=self.font,
                            element_padding=self.element_padding,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=True,
                            disable_close=self.disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(15, 1),
                            return_keyboard_events=False, #Danger!
                            alpha_channel=self.alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width, self.height),
                            resizable=self.resizable,
                            icon=self.icon, )
            else:
                self.window = sg.Window(self.title, self.layout,
                            keep_on_top=self.keep_on_top,
                            font=self.font,
                            element_padding=self.element_padding,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=False,
                            disable_close=self.disable_close,
                            default_element_size=(12, 1),
                            default_button_element_size=(15, 1),
                            return_keyboard_events=False, #Danger!
                            alpha_channel=self.alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width, self.height),
                            resizable=self.resizable,
                            icon=self.icon, )

        except Exception as e:
            print(e)
            self.window = None

        if (self.window is not None):
            return True
        else:
            return False

    def bind(self, ):
        #self.window['_input_text_'].bind('<Double-Button-1>', ' double')
        return True

    def open(self, refresh=True, ):
        # 更新・表示
        try:
            if (self.window is not None):
                self.window.un_hide()
                if (refresh == True):
                    self.window.refresh()
                return True
        except Exception as e:
            print(e)
        return False

    def read(self, timeout=20, timeout_key='-timeout-', ):
        # 読取
        try:
            if (self.window is not None):
                event, values = self.window.read(timeout=timeout, timeout_key=timeout_key, )
                return event, values
        except Exception as e:
            print(e)
        return False, False

    def close(self, ):
        # 消去
        if (self.window is not None):
            try:
                self.read()
                self.window.hide()
                self.window.refresh()
            except Exception as e:
                print(e)
        return True

    def terminate(self, ):
        # 終了
        if (self.window is not None):
            try:
                self.read()
                self.window.close()
                del self.window
            except Exception as e:
                print(e)
        self.window = None
        return True

    def hex2(self, num): # 10進数を二桁16進文字列に変換
        num2 = hex(num).replace('0x', '')
        if len(num2) == 1:
            num2 = '0' + num2
        return num2

    def rgb2hex(self, r, g, b): # r,g,b数を16進カラーコード文字列に変換
        color_code = '#' + '{}{}{}'.format(self.hex2(r), self.hex2(g), self.hex2(b))
        return color_code

    # GUI 自動フェード
    def autoFadeControl(self, reset=False, intervalSec=60, fadeSec=10, ):

        # 透過率設定時に処理
        if (self.alpha_channel < 1):

            # リセット
            if (reset == True):
                self.window.alpha_channel = 1
                self.last_afc_reset = time.time()

                # マウス位置
                (x, y) = qGUI.position()
                self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                # ウィンドウ位置、大きさ
                (l, t) = self.window.current_location()
                (w, h) = self.window.size
                self.last_afc_window_l, self.last_afc_window_t = l, t
                self.last_afc_window_w, self.last_afc_window_h = w, h

                return True

            # マウス位置変化？
            (x, y) = qGUI.position()
            if (x != self.last_afc_mouse_x) or (y != self.last_afc_mouse_y):
                self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                # ウィンドウ位置、大きさ変化？
                (l, t) = self.window.current_location()
                (w, h) = self.window.size
                if (l != self.last_afc_window_l) or (t != self.last_afc_window_t) \
                or (w != self.last_afc_window_w) or (h != self.last_afc_window_h):
                    self.last_afc_window_l, self.last_afc_window_t = l, t
                    self.last_afc_window_w, self.last_afc_window_h = w, h
                    self.window.alpha_channel = 1
                    self.last_afc_reset = time.time()
                    return True

                # マウスオーバーでリセット
                if (x >= l) and (x <= (l+w)) and (y >= t) and (y <= (t+h)):
                    self.window.alpha_channel = 1
                    self.last_afc_reset = time.time()
                    return True

            # フェード処理
            sec = (time.time() - self.last_afc_reset)
            if (sec < (intervalSec + fadeSec)):
                v = 1 - float(self.alpha_channel)
                p = (sec - intervalSec) / fadeSec
                if (p <= 0):
                    self.window.alpha_channel = 1
                else:
                    # フェードアウト
                    if (p > 1):
                        p = 1
                    alpha = 1 - v * p
                    self.window.alpha_channel = alpha

        return True



    def setLayout(self, ):

        # レイアウト
        self.layout = [
                # 内容
                [sg.Image(filename='', key='_output_img_', expand_x=True, expand_y=True, enable_events=True, )],
        ]

        return True



    # GUI 画面リセット
    def reset(self, ):
        try:
            (w, h) = self.window.size #表示領域のサイズ
        except:
            return False

        # 規定値(イメージ)
        self.default_img = np.zeros((240, 320, 3), np.uint8)
        cv2.rectangle(self.default_img,(0,0),(320,240),(255,0,0),-1)
        try:
            if (os.path.isfile(self.img_file)):
                self.default_img = cv2.imread(self.img_file)
        except:
            pass

        # 項目リセット
        img = cv2.resize(self.default_img, (w, h))
        png_bytes = cv2.imencode('.png', img)[1].tobytes()
        self.window['_output_img_'].update(data=png_bytes)

        return True

    # GUI 画面リサイズ
    def resize(self, reset=False, ):
        try:
            (w, h) = self.window.size #表示領域のサイズ
        except:
            return False

        # リセット
        if (reset == True):
            self.last_resize_w, self.last_resize_h = 0, 0

        # 画面リサイズ？
        if (w == self.last_resize_w) and (h == self.last_resize_h):
            return True

        self.last_resize_w, self.last_resize_h = w, h
        #self.window['_output_img_'].update(width=w,height=h)

        # 項目リセット
        img = cv2.resize(self.default_img, (w, h))
        png_bytes = cv2.imencode('.png', img)[1].tobytes()
        self.window['_output_img_'].update(data=png_bytes)

        return True

    # GUI 画面更新
    def refresh(self, ):
        #try:
        #    (w, h) = self.window.size #表示領域のサイズ
        #except:
        #    return False
        return True

    # 画像セット
    def setImage(self, image=None, refresh=True, ):
        try:
            (w, h) = self.window.size #表示領域のサイズ
        except:
            return False

        if (image is None):
            self.image = None
        else:
            self.image = image.copy()
        if (self.image is not None):
            img = cv2.resize(self.image, (w, h))
        else:
            img = np.zeros((h, w, 3), np.uint8)
        png_bytes = cv2.imencode('.png', img)[1].tobytes()
        self.window['_output_img_'].update(data=png_bytes)
        if (refresh == True):
            self.window.refresh()

    # POPUP 画面表示
    def popup_text(self, title='', text='', auto_close=False, size=(96,24), ):
        txt = text
        try:
            dic = json.loads(text)
            txt = json.dumps(dic, ensure_ascii=False, indent=4, )
        except:
            pass
        if (auto_close == False):
            res= sg.popup_scrolled(txt, title='[ ' + title + ' ] (Read only)', keep_on_top=True,
                                non_blocking=True, font='Arial 16', size=size, )
        else:            
            res= sg.popup_scrolled(txt, title='[ ' + title + ' ] (Read only)', keep_on_top=True,
                                non_blocking=True, font='Arial 16', size=size, yes_no=None, 
                                auto_close=True, auto_close_duration=float(auto_close), )
        return True



runMode = 'debug'

if __name__ == '__main__':

    gui = _gui()

    # 初期設定
    if (True):

        # タイトル、icon
        titlex = os.path.basename(__file__)
        titlex = titlex.replace('.py','')
        title  = titlex + '[' + runMode + ']'
        #icon  = None
        icon   = './_icons/' + titlex + '.ico'

        # GUI 初期化
        gui.init(qLog_fn='', runMode='debug',
                 screen='auto', panel='auto',
                 title=title, theme=None,
                 keep_on_top='yes', alpha_channel='0.5', icon=icon, )
        gui.bind()

        # GUI 専用キュー
        gui_queue = queue.Queue()

    # GUI 表示ループ
    reset_flag   = True
    refresh_flag = True
    break_flag   = False
    values       = None
    while (break_flag == False):

        # GUI リセット
        if (reset_flag == True):
            reset_flag   = False
            refresh_flag = True

            # GUI 画面リセット
            gui.reset()

            # GUI 自動フェードリセット
            gui.autoFadeControl(reset=True, )

            # GUI 画面リサイズリセット
            gui.resize(reset=True, )

        # GUI 項目更新
        while (gui_queue.qsize() >= 1):
            [res_name, res_value] = gui_queue.get()
            gui_queue.task_done()
            gui.window[res_name].update(res_value)

        # GUI 自動フェード
        gui.autoFadeControl(reset=False, )

        # GUI 画面リサイズ
        gui.resize(reset=False, )

        # GUI 画面更新
        if (refresh_flag == True):
            refresh_flag = False
            gui.refresh()

        # GUI イベント確認                 ↓　timeout値でtime.sleep代用
        event, values = gui.read(timeout=150, timeout_key='-idoling-')

        # GUI 終了イベント処理
        if event == sg.WIN_CLOSED:
            gui.window = None
            break_flag = True
            break
        if event in (None, '-exit-'):
            break_flag = True
            break

        try:
            # ------------------------------
            # アイドリング時の処理
            # ------------------------------
            if (event == '-idoling-'):
                pass

            # ------------------------------
            # ボタンイベント処理
            # ------------------------------
            # リセット
            elif (event == '-reset-'):
                print(event, )
                reset_flag = True

            else:
                print(event, values, )
        except Exception as e:
            print(e)
            time.sleep(5.00)

    # 終了処理
    if (True):

        # GUI 画面消去
        try:
            gui.close()
            gui.terminate()
        except:
            pass

        # 終了
        sys.exit(0)


