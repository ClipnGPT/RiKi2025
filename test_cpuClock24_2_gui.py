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
import platform
import numpy as np
import cv2
import tkinter as tk
from tkinter import messagebox

qPLATFORM = platform.system().lower()  # windows, darwin, linux

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
        self.screen = '0'
        self.panel = '3--'
        self.img_file = '_icons/RiKi_cpuClock24.png'
        titlex = os.path.basename(__file__)
        self.title = titlex.replace('.py','')
        self.theme = 'Dark'
        self.alpha_channel = 1.0
        self.icon = None
        self.font = ('Arial', 8)
        self.keep_on_top = True
        self.no_titlebar = False
        self.disable_close = False
        self.resizable = True
        self.no_border = True
        self.root = None
        self.image_label = None
        self.left = 0
        self.top = 0
        self.width = 320
        self.height = 240
        self.event_queue = queue.Queue()
        self.tk_image = None
        self.default_img = None
        self.last_resize_w = 0
        self.last_resize_h = 0
        self.last_afc_reset = time.time()
        self.last_afc_mouse_x = 0
        self.last_afc_mouse_y = 0
        self.last_afc_window_l = 0
        self.last_afc_window_t = 0
        self.last_afc_window_w = 0
        self.last_afc_window_h = 0

    def init(self, qLog_fn='', runMode='debug',
             screen='auto', panel='auto',
             title='', theme=None,
             keep_on_top='yes', alpha_channel='1', icon=None):
        if self.root is not None:
            self.terminate()
        self.root = tk.Tk()
        if title != '':
            self.title = title
        else:
            titlex = os.path.basename(__file__).replace('.py','')
            self.title = titlex + '[' + runMode + ']'
        self.root.title(self.title)
        if icon is not None and os.path.isfile(icon):
            try:
                self.root.iconbitmap(icon)
            except Exception as e:
                print(e)
        # デフォルトでは 320x240、位置は (100,100) とする
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 240
        geometry_str = f"{self.width}x{self.height}+{self.left}+{self.top}"
        self.root.geometry(geometry_str)
        self.root.wm_attributes("-topmost", True if keep_on_top != 'no' else False)
        try:
            self.alpha_channel = float(alpha_channel)
        except Exception as e:
            print(e)
        self.root.attributes("-alpha", self.alpha_channel)
        self.root.resizable(self.resizable, self.resizable)
        if self.no_titlebar:
            self.root.overrideredirect(True)
        self.image_label = tk.Label(self.root)
        self.image_label.pack(fill="both", expand=True)
        self.image_label.bind("<Button-1>", self.handle_img_click)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.default_img = np.zeros((self.height, self.width, 3), np.uint8)
        cv2.rectangle(self.default_img, (0, 0), (self.width, self.height), (255, 0, 0), -1)
        self.reset()
        return True

    def handle_img_click(self, event):
        self.event_queue.put("_output_img_")

    def on_close(self):
        self.event_queue.put("WIN_CLOSED")
        self.terminate()

    def bind(self):
        # 必要に応じて追加のキー操作等もバインド可能
        return True

    def open(self, refresh=True):
        if self.root is not None:
            self.root.deiconify()
            if refresh:
                self.refresh()
            return True
        return False

    def read(self, timeout=20, timeout_key='-idoling-'):
        start_time = time.time()
        while (time.time() - start_time) * 1000 < timeout:
            try:
                event = self.event_queue.get_nowait()
                return event, {}
            except queue.Empty:
                pass
            self.root.update()
            time.sleep(0.005)
        return timeout_key, {}

    def close(self):
        if self.root is not None:
            self.root.withdraw()
            self.root.update()
        return True

    def terminate(self):
        if self.root is not None:
            self.root.destroy()
            self.root = None
        return True

    def hex2(self, num):
        num2 = hex(num).replace('0x', '')
        if len(num2) == 1:
            num2 = '0' + num2
        return num2

    def rgb2hex(self, r, g, b):
        color_code = '#' + '{}{}{}'.format(self.hex2(r), self.hex2(g), self.hex2(b))
        return color_code

    def autoFadeControl(self, reset=False, intervalSec=60, fadeSec=10):
        if self.alpha_channel < 1:
            if reset:
                self.root.attributes("-alpha", 1.0)
                self.last_afc_reset = time.time()
                self.last_afc_mouse_x = self.root.winfo_pointerx()
                self.last_afc_mouse_y = self.root.winfo_pointery()
                self.last_afc_window_l = self.root.winfo_x()
                self.last_afc_window_t = self.root.winfo_y()
                self.last_afc_window_w = self.root.winfo_width()
                self.last_afc_window_h = self.root.winfo_height()
                return True
            current_mouse_x = self.root.winfo_pointerx()
            current_mouse_y = self.root.winfo_pointery()
            if (current_mouse_x != self.last_afc_mouse_x) or (current_mouse_y != self.last_afc_mouse_y):
                self.last_afc_mouse_x, self.last_afc_mouse_y = current_mouse_x, current_mouse_y
                current_window_l = self.root.winfo_x()
                current_window_t = self.root.winfo_y()
                current_window_w = self.root.winfo_width()
                current_window_h = self.root.winfo_height()
                if (current_window_l != self.last_afc_window_l or current_window_t != self.last_afc_window_t or 
                    current_window_w != self.last_afc_window_w or current_window_h != self.last_afc_window_h):
                    self.last_afc_window_l, self.last_afc_window_t = current_window_l, current_window_t
                    self.last_afc_window_w, self.last_afc_window_h = current_window_w, current_window_h
                    self.root.attributes("-alpha", 1.0)
                    self.last_afc_reset = time.time()
                    return True
                if (current_mouse_x >= self.root.winfo_rootx() and 
                    current_mouse_x <= self.root.winfo_rootx() + self.root.winfo_width() and
                    current_mouse_y >= self.root.winfo_rooty() and 
                    current_mouse_y <= self.root.winfo_rooty() + self.root.winfo_height()):
                    self.root.attributes("-alpha", 1.0)
                    self.last_afc_reset = time.time()
                    return True
            sec = time.time() - self.last_afc_reset
            if sec >= intervalSec:
                p = (sec - intervalSec) / fadeSec
                if p > 1:
                    p = 1
                new_alpha = 1 - (1 - self.alpha_channel) * p
                if new_alpha < self.alpha_channel:
                    new_alpha = self.alpha_channel
                self.root.attributes("-alpha", new_alpha)
        return True

    def setLayout(self):
        # Tkinter では init() 内で image_label によりレイアウト済み
        return True

    def reset(self):
        try:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
        except:
            return False
        self.default_img = np.zeros((h, w, 3), np.uint8)
        cv2.rectangle(self.default_img, (0,0), (w, h), (255, 0, 0), -1)
        if os.path.isfile(self.img_file):
            try:
                self.default_img = cv2.imread(self.img_file)
            except:
                pass
        self.setImage(self.default_img, refresh=False)
        return True

    def resize(self, reset=False):
        try:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
        except:
            return False
        if reset:
            self.last_resize_w, self.last_resize_h = 0, 0
        if w == self.last_resize_w and h == self.last_resize_h:
            return True
        self.last_resize_w, self.last_resize_h = w, h
        if self.default_img is not None:
            img = cv2.resize(self.default_img, (w, h))
            self.setImage(img, refresh=True)
        return True

    def refresh(self):
        self.root.update_idletasks()
        return True

    def setImage(self, image=None, refresh=True):
        try:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
        except:
            return False
        if image is None:
            img = np.zeros((h, w, 3), np.uint8)
        else:
            img = cv2.resize(image, (w, h))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        from PIL import Image, ImageTk
        im = Image.fromarray(img_rgb)
        self.tk_image = ImageTk.PhotoImage(im)
        self.image_label.config(image=self.tk_image)
        if refresh:
            self.refresh()
        return True

    def popup_text(self, title='', text='', auto_close=False, size=(96,24)):
        try:
            dic = json.loads(text)
            txt = json.dumps(dic, ensure_ascii=False, indent=4)
        except:
            txt = text
        if not auto_close:
            messagebox.showinfo(title='[ ' + title + ' ] (Read only)', message=txt)
        else:
            popup = tk.Toplevel(self.root)
            popup.title('[ ' + title + ' ] (Read only)')
            label = tk.Label(popup, text=txt, font=('Arial', 16))
            label.pack()
            popup.after(int(float(auto_close)*1000), popup.destroy)
        return True

runMode = 'debug'

if __name__ == '__main__':
    gui = _gui()
    if True:
        titlex = os.path.basename(__file__).replace('.py','')
        title  = titlex + '[' + runMode + ']'
        icon   = './_icons/' + titlex + '.ico'
        gui.init(qLog_fn='', runMode='debug',
                 screen='auto', panel='auto',
                 title=title, theme=None,
                 keep_on_top='yes', alpha_channel='0.5', icon=icon)
        gui.bind()
        gui_queue = queue.Queue()

    reset_flag = True
    refresh_flag = True
    break_flag = False
    values = None
    while break_flag == False:
        if reset_flag == True:
            reset_flag = False
            refresh_flag = True
            gui.reset()
            gui.autoFadeControl(reset=True)
            gui.resize(reset=True)
        while not gui_queue.empty():
            res = gui_queue.get()
            gui.event_queue.put(res)
            gui_queue.task_done()
        gui.autoFadeControl(reset=False)
        gui.resize(reset=False)
        if refresh_flag == True:
            refresh_flag = False
            gui.refresh()
        event, values = gui.read(timeout=150, timeout_key='-idoling-')
        if event == "WIN_CLOSED":
            gui.root = None
            break_flag = True
            break
        if event in (None, '-exit-'):
            break_flag = True
            break
        try:
            if event == '-idoling-':
                pass
            elif event == '-reset-':
                print(event)
                reset_flag = True
            else:
                print(event, values)
        except Exception as e:
            print(e)
            time.sleep(5.00)
    if True:
        try:
            gui.close()
            gui.terminate()
        except:
            pass
        sys.exit(0)


