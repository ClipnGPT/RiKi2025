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
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import numpy as np
import cv2

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux

# インターフェース
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_icons  = '_icons/'

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
        self.panel          = '5-'
        self.img_file       = '_icons/__black.png'
        titlex              = os.path.basename(__file__)
        self.title          = titlex.replace('.py','')
        self.theme          = 'Dark' 
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

        # イベント、フェード制御用
        self.last_event = None
        self.last_values = {}
        self.last_afc_reset = time.time()
        self.last_afc_mouse_x = 0
        self.last_afc_mouse_y = 0
        self.last_resize_w = 0
        self.last_resize_h = 0
        self.default_img = None
        self.image = None


    def init(self, qLog_fn='', runMode='debug',
             screen='auto', panel='auto',
             title='', theme=None,
             keep_on_top='yes', alpha_channel='1', icon=None, ):

        if (str(screen) != 'auto'):
            self.screen = screen
        if (panel != 'auto'):
            self.panel = panel

        if (title != ''):
            self.title  = title
        else:
            titlex      = os.path.basename(__file__)
            titlex      = titlex.replace('.py','')
            self.title  = titlex + '[' + runMode + ']'

        if (theme is not None):
            self.theme = theme

        self.window = tk.Tk()
        self.root = self.window
        self.root.title(self.title)
        
        # デフォルトの位置・サイズ設定
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 240
        self.root.geometry(f"{self.width}x{self.height}+{self.left}+{self.top}")

        self.keep_on_top = (keep_on_top != 'no')
        self.root.attributes("-topmost", self.keep_on_top)

        try:
            self.alpha_channel = float(alpha_channel)
        except Exception as e:
            print(e)
            self.alpha_channel = 1.0
        self.root.attributes("-alpha", self.alpha_channel)

        if self.no_titlebar:
            self.root.overrideredirect(True)

        self.root.resizable(self.resizable, self.resizable)

        if icon is not None and os.path.exists(icon):
            if qPLATFORM == 'windows':
                self.root.iconbitmap(icon)
            else:
                img_icon = Image.open(icon)
                self.icon = ImageTk.PhotoImage(img_icon)
                self.root.iconphoto(False, self.icon)

        self.setLayout()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.bind("<Key>", self._on_key_event)

        self.last_afc_reset = time.time()
        self.last_afc_mouse_x = self.root.winfo_pointerx()
        self.last_afc_mouse_y = self.root.winfo_pointery()
        self.last_window_x = self.root.winfo_x()
        self.last_window_y = self.root.winfo_y()
        self.last_window_w = self.root.winfo_width()
        self.last_window_h = self.root.winfo_height()

        return True

    def _on_key_event(self, event):
        self.last_event = event.keysym
        self.last_values = {}

    def on_close(self):
        self.last_event = "WIN_CLOSED"
        self.root.destroy()

    def bind(self, ):
        return True

    def open(self, refresh=True, ):
        self.root.deiconify()
        if refresh:
            self.root.update()
        return True

    def read(self, timeout=20, timeout_key='-timeout-', ):
        start_time = time.time()
        event = None
        while (time.time() - start_time) < (timeout/1000.0):
            self.root.update()
            if self.last_event is not None:
                event = self.last_event
                self.last_event = None
                break
            time.sleep(0.01)
        if event is None:
            event = timeout_key
        return event, self.last_values

    def close(self, ):
        self.root.withdraw()
        self.root.update()
        return True

    def terminate(self, ):
        if self.window is not None:
            self.root.destroy()
            self.window = None
        return True

    def hex2(self, num):
        num2 = hex(num).replace('0x', '')
        if len(num2) == 1:
            num2 = '0' + num2
        return num2

    def rgb2hex(self, r, g, b):
        color_code = '#' + '{}{}{}'.format(self.hex2(r), self.hex2(g), self.hex2(b))
        return color_code

    def autoFadeControl(self, reset=False, intervalSec=60, fadeSec=10, ):
        if self.alpha_channel < 1.0:
            pass
        current_alpha = self.root.attributes("-alpha")
        if reset:
            self.root.attributes("-alpha", 1.0)
            self.last_afc_reset = time.time()
            self.last_afc_mouse_x = self.root.winfo_pointerx()
            self.last_afc_mouse_y = self.root.winfo_pointery()
            self.last_window_x = self.root.winfo_x()
            self.last_window_y = self.root.winfo_y()
            self.last_window_w = self.root.winfo_width()
            self.last_window_h = self.root.winfo_height()
            return True

        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        if (x != self.last_afc_mouse_x) or (y != self.last_afc_mouse_y):
            self.last_afc_mouse_x, self.last_afc_mouse_y = x, y
            self.root.attributes("-alpha", 1.0)
            self.last_afc_reset = time.time()
            return True

        l = self.root.winfo_x()
        t = self.root.winfo_y()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        if (x >= l) and (x <= (l+w)) and (y >= t) and (y <= (t+h)):
            self.root.attributes("-alpha", 1.0)
            self.last_afc_reset = time.time()
            return True

        sec = (time.time() - self.last_afc_reset)
        if sec < intervalSec:
            return True
        p = (sec - intervalSec) / fadeSec
        if p > 1:
            p = 1
        new_alpha = 1 - (1 - self.alpha_channel) * p
        self.root.attributes("-alpha", new_alpha)
        return True

    def setLayout(self, ):
        self.label = tk.Label(self.root, bg="black")
        self.label.pack(fill=tk.BOTH, expand=True)
        return True

    def reset(self, ):
        try:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
        except:
            return False

        self.default_img = np.zeros((240, 320, 3), np.uint8)
        cv2.rectangle(self.default_img,(0,0),(320,240),(255,0,0),-1)
        try:
            if (os.path.isfile(self.img_file)):
                self.default_img = cv2.imread(self.img_file)
        except:
            pass

        img_resized = cv2.resize(self.default_img, (w, h))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        from PIL import Image
        pil_img = Image.fromarray(img_rgb)
        photo = ImageTk.PhotoImage(pil_img)
        self.label.image = photo
        self.label.config(image=photo)
        return True

    def resize(self, reset=False, ):
        try:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
        except:
            return False

        if (reset == True):
            self.last_resize_w, self.last_resize_h = 0, 0

        if (w == self.last_resize_w) and (h == self.last_resize_h):
            return True

        self.last_resize_w, self.last_resize_h = w, h
        if self.default_img is not None:
            img_resized = cv2.resize(self.default_img, (w, h))
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            photo = ImageTk.PhotoImage(pil_img)
            self.label.image = photo
            self.label.config(image=photo)
        return True

    def refresh(self, ):
        self.root.update_idletasks()
        return True

    def setImage(self, image=None, refresh=True, ):
        try:
            w = self.root.winfo_width()
            h = self.root.winfo_height()
        except:
            return False

        if (image is None):
            self.image = None
        else:
            self.image = image.copy()
        if (self.image is not None):
            img_resized = cv2.resize(self.image, (w, h))
        else:
            img_resized = np.zeros((h, w, 3), np.uint8)
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        from PIL import Image
        pil_img = Image.fromarray(img_rgb)
        photo = ImageTk.PhotoImage(pil_img)
        self.label.image = photo
        self.label.config(image=photo)
        if (refresh == True):
            self.root.update()
        return True

    def popup_text(self, title='', text='', auto_close=False, size=(96,24), ):
        try:
            dic = json.loads(text)
            txt = json.dumps(dic, ensure_ascii=False, indent=4, )
        except:
            txt = text
        if (auto_close == False):
            messagebox.showinfo(title='[ ' + title + ' ] (Read only)', message=txt)
        else:            
            popup = tk.Toplevel(self.root)
            popup.title('[ ' + title + ' ] (Read only)')
            msg = tk.Message(popup, text=txt, width=size[0]*10)
            msg.pack()
            popup.after(int(float(auto_close)*1000), popup.destroy)
        return True

    def setAlphaChannel(self, alpha_channel=1, ):
        try:
            self.root.attributes("-alpha", alpha_channel)
        except:
            pass

    def fadeOut(self, screen=0, panel='0', mask='black', outSec=2, ):
        if (mask != 'white'):
            img_path = os.path.join(qPath_icons, '__black.png')
        else:
            img_path = os.path.join(qPath_icons, '__white.png')
        if os.path.isfile(img_path):
            img   = cv2.imread(img_path)
        else:
            img = np.zeros((self.height, self.width, 3), np.uint8)
        self.reset()
        self.setImage(image=img, )
        self.resize(reset=True, )
        self.open()
        self.setAlphaChannel(0)
        start_time = time.time()
        steps = 50
        while ((time.time() - start_time) < outSec):
            elapsed = time.time() - start_time
            new_alpha = elapsed / outSec
            if new_alpha > 1:
                new_alpha = 1
            self.setAlphaChannel(new_alpha)
            self.root.update()
            time.sleep(outSec/steps)
        self.setAlphaChannel(1)
        return True

    def fadeIn(self, inSec=1, ):
        self.setAlphaChannel(1)
        start_time = time.time()
        steps = 50
        while ((time.time() - start_time) < inSec):
            elapsed = time.time() - start_time
            new_alpha = 1 - (elapsed / inSec)
            if new_alpha < 0:
                new_alpha = 0
            self.setAlphaChannel(new_alpha)
            self.root.update()
            time.sleep(inSec/steps)
        self.setAlphaChannel(0)
        self.close()
        self.terminate()
        return True



runMode = 'debug'

if __name__ == '__main__':

    gui = _gui()

    titlex = os.path.basename(__file__)
    titlex = titlex.replace('.py','')
    title  = titlex + '[' + runMode + ']'
    icon   = os.path.join('_icons', titlex + '.ico')

    gui.init(qLog_fn='', runMode='debug',
             screen='auto', panel='auto',
             title=title, theme=None,
             keep_on_top='yes', alpha_channel='0.5', icon=icon, )
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
            gui.autoFadeControl(reset=True, )
            gui.resize(reset=True, )

        while (gui_queue.qsize() >= 1):
            [res_name, res_value] = gui_queue.get()
            gui_queue.task_done()

        gui.autoFadeControl(reset=False, )
        gui.resize(reset=False, )

        if (refresh_flag == True):
            refresh_flag = False
            gui.refresh()

        event, values = gui.read(timeout=150, timeout_key='-idoling-')

        if (event == "WIN_CLOSED"):
            gui.window = None
            break_flag = True
            break
        if (event in (None, '-exit-')):
            break_flag = True
            break

        try:
            if (event == '-idoling-'):
                pass
            elif (event == '-reset-'):
                print(event, )
                reset_flag = True
            else:
                print(event, values, )
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


