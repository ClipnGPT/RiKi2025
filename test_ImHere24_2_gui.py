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
import numpy as np
import cv2
import platform
qPLATFORM = platform.system().lower() #windows, darwin, linux

# tkinter版へ変換
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# 共通ルーチン
import _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import _v6__qLog
qLog   = _v6__qLog.qLog_class()

class _gui:

    def __init__(self):
        self.screen         = 0
        self.panel          = '8--'
        self.img_file       = '_icons/RiKi_ImHere24.png'
        titlex              = os.path.basename(__file__)
        self.title          = titlex.replace('.py','')
        self.layout         = None
        self.theme          = 'Dark'
        self.alpha_channel  = 1.0
        self.icon           = None
        self.font           = ('Arial', 8)
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
        self.event          = None
        self.values         = {}
        self.last_resize_w  = 0
        self.last_resize_h  = 0

    def init(self, qLog_fn='', runMode='debug',
             screen='auto', panel='auto',
             title='', theme=None,
             keep_on_top='yes', alpha_channel='1', icon=None):

        if screen != 'auto':
            try:
                self.screen = int(screen)
            except Exception as e:
                print(e)
        if panel != 'auto':
            self.panel = panel
        if title != '':
            self.title  = title
        else:
            titlex      = os.path.basename(__file__)
            titlex      = titlex.replace('.py','')
            self.title  = titlex + '[' + runMode + ']'
        if theme is not None:
            self.theme = theme
        self.keep_on_top = (keep_on_top != 'no')
        try:
            self.alpha_channel = float(alpha_channel)
        except Exception as e:
            print(e)
        if icon is not None:
            self.icon = icon

        # 仮の表示位置・サイズ（本来はqGUI.getScreenPanelPosSize()で決定）
        self.left, self.top = 100, 100
        self.width, self.height = 320, 240

        # Tkウィンドウ生成
        self.window = tk.Tk()
        self.window.title(self.title)
        if self.keep_on_top:
            self.window.attributes("-topmost", True)
        self.window.geometry(f"{self.width}x{self.height}+{self.left}+{self.top}")
        self.window.resizable(self.resizable, self.resizable)
        self.window.attributes("-alpha", self.alpha_channel)
        if self.icon is not None:
            try:
                self.window.iconbitmap(self.icon)
            except Exception as e:
                print(e)
        if self.no_titlebar:
            self.window.overrideredirect(True)

        # レイアウト設定（キャンバス）
        self.setLayout()

        # イベントバインド
        self.bind()
        self.closed = False
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.last_afc_reset = time.time()
        self.last_afc_mouse_x, self.last_afc_mouse_y = 0, 0
        self.last_afc_window_l, self.last_afc_window_t = self.left, self.top
        self.last_afc_window_w, self.last_afc_window_h = self.width, self.height

        return True

    def on_close(self):
        self.event = "WIN_CLOSED"
        self.closed = True

    def bind(self):
        self.window.bind("<Key>", self.on_key)
        self.window.bind("<Button>", self.on_mouse)
        return True

    def on_key(self, event):
        self.event = event.keysym
        self.values['key'] = event.keysym

    def on_mouse(self, event):
        self.event = "mouse_click"
        self.values['x'] = event.x
        self.values['y'] = event.y

    def open(self, refresh=True):
        if self.window is not None:
            self.window.deiconify()
            if refresh:
                self.window.update()
            return True
        return False

    def read(self, timeout=150, timeout_key='-timeout-'):
        start = time.time()
        self.event = None
        self.values = {}
        while (time.time() - start) < (timeout/1000.0):
            self.window.update()
            if self.event is not None:
                e = self.event
                v = self.values.copy()
                self.event = None
                self.values = {}
                return e, v
            time.sleep(0.01)
        return timeout_key, {}

    def close(self):
        if self.window is not None:
            try:
                self.window.withdraw()
                self.window.update()
            except Exception as e:
                print(e)
        return True

    def terminate(self):
        if self.window is not None:
            try:
                self.window.destroy()
            except Exception as e:
                print(e)
            self.window = None
        return True

    def autoFadeControl(self, reset=False, intervalSec=60, fadeSec=10):
        if self.alpha_channel < 1:
            if reset:
                self.window.attributes("-alpha", 1)
                self.last_afc_reset = time.time()
                return True
            sec = time.time() - self.last_afc_reset
            if sec < (intervalSec + fadeSec):
                v = 1 - self.alpha_channel
                p = (sec - intervalSec) / fadeSec
                if p <= 0:
                    self.window.attributes("-alpha", 1)
                else:
                    if p > 1:
                        p = 1
                    alpha = 1 - v * p
                    self.window.attributes("-alpha", alpha)
        return True

    def setLayout(self):
        if self.window is None:
            return False
        self.canvas = tk.Canvas(self.window, bg="black")
        self.canvas.pack(fill="both", expand=True)
        self.photo = None
        return True

    def reset(self):
        try:
            w = self.window.winfo_width()
            h = self.window.winfo_height()
        except:
            return False
        self.default_img = np.zeros((240,320,3), np.uint8)
        cv2.rectangle(self.default_img,(0,0),(320,240),(255,0,0),-1)
        try:
            if os.path.isfile(self.img_file):
                self.default_img = cv2.imread(self.img_file)
        except:
            pass
        img = cv2.resize(self.default_img, (w, h))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        from PIL import Image
        pil_img = Image.fromarray(img_rgb)
        self.photo = ImageTk.PhotoImage(image=pil_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        return True

    def resize(self, reset=False):
        try:
            w = self.window.winfo_width()
            h = self.window.winfo_height()
        except:
            return False
        if reset:
            self.last_resize_w, self.last_resize_h = 0, 0
        if w == self.last_resize_w and h == self.last_resize_h:
            return True
        self.last_resize_w, self.last_resize_h = w, h
        if hasattr(self, 'default_img'):
            img = cv2.resize(self.default_img, (w, h))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            from PIL import Image
            pil_img = Image.fromarray(img_rgb)
            self.photo = ImageTk.PhotoImage(image=pil_img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        return True

    def refresh(self):
        if self.window is not None:
            self.window.update_idletasks()
            self.window.update()
        return True

    def setImage(self, image=None, refresh=True):
        try:
            w = self.window.winfo_width()
            h = self.window.winfo_height()
        except:
            return False
        if image is not None:
            self.image = image.copy()
            img = cv2.resize(self.image, (w, h))
        else:
            img = np.zeros((h, w, 3), np.uint8)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        from PIL import Image
        pil_img = Image.fromarray(img_rgb)
        self.photo = ImageTk.PhotoImage(image=pil_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        if refresh:
            self.window.update()
        return True

    def popup_text(self, title='', text='', auto_close=False, size=(96,24)):
        if not auto_close:
            messagebox.showinfo(title, text)
        else:
            top = tk.Toplevel(self.window)
            top.title(title)
            msg = tk.Message(top, text=text, width=300)
            msg.pack()
            top.after(int(auto_close*1000), top.destroy)
        return True

runMode = 'debug'

if __name__ == '__main__':

    gui = _gui()

    # 初期設定
    if (True):

        titlex = os.path.basename(__file__).replace('.py','')
        title  = titlex + '[' + runMode + ']'
        icon   = './_icons/' + titlex + '.ico'

        gui.init(qLog_fn='', runMode='debug',
                 screen='auto', panel='auto',
                 title=title, theme=None,
                 keep_on_top='yes', alpha_channel='0.5', icon=icon)
        gui.bind()

        gui_queue = queue.Queue()

    reset_flag   = True
    refresh_flag = True
    break_flag   = False
    values       = None
    while (break_flag == False):

        if (reset_flag == True):
            reset_flag   = False
            refresh_flag = True

            gui.reset()
            gui.autoFadeControl(reset=True)
            gui.resize(reset=True)

        while (not gui_queue.empty()):
            res = gui_queue.get()
            gui_queue.task_done()

        gui.autoFadeControl(reset=False)
        gui.resize(reset=False)
        if (refresh_flag == True):
            refresh_flag = False
            gui.refresh()

        event, values = gui.read(timeout=150, timeout_key='-idoling-')

        if event == "WIN_CLOSED":
            gui.window = None
            break_flag = True
            break
        if event in (None, '-exit-'):
            break_flag = True
            break

        try:
            if (event == '-idoling-'):
                pass
            elif (event == '-reset-'):
                print(event)
                reset_flag = True
            else:
                print(event, values)
        except Exception as e:
            print(e)
            time.sleep(5.00)

    if (True):

        try:
            gui.close()
            gui.terminate()
        except:
            pass

        sys.exit(0)


