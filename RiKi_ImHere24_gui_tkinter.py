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
#import PySimpleGUI as sg

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import numpy as np
import cv2

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux

# �C���^�[�t�F�[�X
qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'

# ���ʃ��[�`��
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
        #self.layout         = [
        #                    sg.InputText('Hallo World'),
        #                    sg.Button('OK', key='-OK-'),
        #                    ]

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

        # ���O
        self.proc_name = 'gui'
        self.proc_id   = '{0:10s}'.format(self.proc_name).replace(' ', '_')
        if (not os.path.isdir(qPath_log)):
            os.makedirs(qPath_log)
        if (qLog_fn == ''):
            nowTime  = datetime.datetime.now()
            qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
        qLog.init(mode='logger', filename=qLog_fn, )
        qLog.log('info', self.proc_id, 'init')

        # ���s���[�h
        self.runMode = runMode

        # �X�N���[��
        if (str(screen) != 'auto'):
            try:
                self.screen = int(screen)
            except Exception as e:
                print(e)

        # �p�l��
        if (panel != 'auto'):
            self.panel = panel

        # �^�C�g��
        if (title != ''):
            self.title  = title
        else:
            titlex      = os.path.basename(__file__)
            titlex      = titlex.replace('.py','')
            self.title  = titlex + '[' + runMode + ']'

        # �e�[�}
        if (theme is not None):
            self.theme = theme
        #sg.theme(self.theme)

        # �{�[�_�[
        if (self.no_border != True):
            self.element_padding= ((2,2),(2,2)) #((left/right),(top/bottom))
        else:
            self.element_padding= ((0,0),(0,0)) #((left/right),(top/bottom))
            #sg.set_options(element_padding=(0,0), margins=(0,0), border_width=0)

        # �őO��
        if (keep_on_top != 'no'):
            self.keep_on_top = True
        else:
            self.keep_on_top = False

        # ���ߕ\��
        if (str(alpha_channel) != ''):
            try:
                self.alpha_channel = float(alpha_channel)
            except Exception as e:
                print(e)

        # �A�C�R��
        if (icon is not None):
            self.icon = icon

        # �\���ʒu
        qGUI.checkUpdateScreenInfo(update=True, )
        self.left, self.top, self.width, self.height = qGUI.getScreenPanelPosSize(screen=self.screen, panel=self.panel, )

        # ���C�A�E�g
        self.setLayout()

        # �E�B���h�E�ݒ�
        self.close()
        try:
            if (qPLATFORM == 'darwin'):
                self.no_titlebar = False
            if (self.no_titlebar == True):
                self.window = tk.Tk()
                self.window.title(self.title)
                self.window.geometry(f"{self.width}x{self.height}+{self.left}+{self.top}")
                self.window.overrideredirect(True)  # �^�C�g���o�[���폜
                #self.window.attributes("-topmost", self.keep_on_top)  # ��ɍőO�ʂɕ\��
                self.window.resizable(self.resizable, self.resizable)
                if self.icon:
                    self.window.iconbitmap(self.icon)
            else:
                self.window = tk.Tk()
                self.window.title(self.title)
                self.window.geometry(f"{self.width}x{self.height}+{self.left}+{self.top}")
                #self.window.attributes("-topmost", self.keep_on_top)  # ��ɍőO�ʂɕ\��
                self.window.resizable(self.resizable, self.resizable)
                if self.icon:
                    self.window.iconbitmap(self.icon)

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
        # �X�V�E�\��
        try:
            if (self.window is not None):
                self.window.deiconify()
                if (refresh == True):
                    self.window.update()
                return True
        except Exception as e:
            print(e)
        return False

    def read(self, timeout=20, timeout_key='-timeout-', ):
        # �ǎ�
        try:
            if (self.window is not None):
                self.window.after(timeout, lambda: self.window.event_generate('<<Timeout>>'))
                self.window.update_idletasks()
                self.window.update()
                event = '<<Timeout>>' if self.window.event_info() == '<<Timeout>>' else None
                values = None  # tkinter�ł�values�͎g�p���Ȃ�
                return event, values
        except Exception as e:
            print(e)
        return False, False

    def close(self, ):
        # ����
        if (self.window is not None):
            try:
                self.read()
                self.window.withdraw()
                self.window.update()
            except Exception as e:
                print(e)
        return True

    def terminate(self, ):
        # �I��
        if (self.window is not None):
            try:
                self.read()
                self.window.destroy()
            except Exception as e:
                print(e)
        self.window = None
        return True

    def hex2(self, num): # 10�i�����16�i������ɕϊ�
        num2 = hex(num).replace('0x', '')
        if len(num2) == 1:
            num2 = '0' + num2
        return num2

    def rgb2hex(self, r, g, b): # r,g,b����16�i�J���[�R�[�h������ɕϊ�
        color_code = '#' + '{}{}{}'.format(self.hex2(r), self.hex2(g), self.hex2(b))
        return color_code

    # GUI �����t�F�[�h
    def autoFadeControl(self, reset=False, intervalSec=60, fadeSec=10, ):

        # ���ߗ��ݒ莞�ɏ���
        if (self.alpha_channel < 1):

            # ���Z�b�g
            if (reset == True):
                #self.window.attributes('-alpha', 1.0)
                self.last_afc_reset = time.time()

                # �}�E�X�ʒu
                (x, y) = qGUI.position()
                self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                # �E�B���h�E�ʒu�A�傫��
                #(l, t) = self.window.winfo_x(), self.window.winfo_y()
                #(w, h) = self.window.winfo_width(), self.window.winfo_height()
                #self.last_afc_window_l, self.last_afc_window_t = l, t
                #self.last_afc_window_w, self.last_afc_window_h = w, h

                return True

            # �}�E�X�ʒu�ω��H
            (x, y) = qGUI.position()
            if (x != self.last_afc_mouse_x) or (y != self.last_afc_mouse_y):
                self.last_afc_mouse_x, self.last_afc_mouse_y = x, y

                return True #danger!

                # �E�B���h�E�ʒu�A�傫���ω��H
                (l, t) = self.window.winfo_x(), self.window.winfo_y()
                (w, h) = self.window.winfo_width(), self.window.winfo_height()
                if (l != self.last_afc_window_l) or (t != self.last_afc_window_t) \
                or (w != self.last_afc_window_w) or (h != self.last_afc_window_h):
                    self.last_afc_window_l, self.last_afc_window_t = l, t
                    self.last_afc_window_w, self.last_afc_window_h = w, h
                    #self.window.attributes('-alpha', 1.0)
                    self.last_afc_reset = time.time()
                    return True

                # �}�E�X�I�[�o�[�Ń��Z�b�g
                if (x >= l) and (x <= (l+w)) and (y >= t) and (y <= (t+h)):
                    #self.window.attributes('-alpha', 1.0)
                    self.last_afc_reset = time.time()
                    return True

            # �t�F�[�h����
            sec = (time.time() - self.last_afc_reset)
            if (sec < (intervalSec + fadeSec)):
                v = 1 - float(self.alpha_channel)
                p = (sec - intervalSec) / fadeSec
                if (p <= 0):
                    #self.window.attributes('-alpha', 1.0)
                    pass
                else:
                    # �t�F�[�h�A�E�g
                    if (p > 1):
                        p = 1
                    alpha = 1 - v * p
                    #self.window.attributes('-alpha', alpha)

        return True



    def setLayout(self, ):

        # ���C�A�E�g
        #self.layout = [
        #        # ���e
        #        [sg.Image(filename='', key='_output_img_', expand_x=True, expand_y=True, enable_events=True, )],
        #]
        self.output_img_label = tk.Label(self.window)
        self.output_img_label.pack(expand=True, fill="both")

        return True



    # GUI ��ʃ��Z�b�g
    def reset(self, ):
        try:
            (w, h) = self.window.winfo_width(), self.window.winfo_height() #�\���̈�̃T�C�Y
        except:
            return False

        # �K��l(�C���[�W)
        self.default_img = np.zeros((240, 320, 3), np.uint8)
        cv2.rectangle(self.default_img,(0,0),(320,240),(255,0,0),-1)
        try:
            if (os.path.isfile(self.img_file)):
                self.default_img = cv2.imread(self.img_file)
        except:
            pass

        # ���ڃ��Z�b�g
        img = cv2.resize(self.default_img, (w, h))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV��BGR��RGB�ɕϊ�
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.output_img_label.config(image=self.photo)

        return True

    # GUI ��ʃ��T�C�Y
    def resize(self, reset=False, ):
        try:
            (w, h) = self.window.winfo_width(), self.window.winfo_height() #�\���̈�̃T�C�Y
        except:
            return False

        # ���Z�b�g
        if (reset == True):
            self.last_resize_w, self.last_resize_h = 0, 0

        # ��ʃ��T�C�Y�H
        if (w == self.last_resize_w) and (h == self.last_resize_h):
            return True

        self.last_resize_w, self.last_resize_h = w, h
        #self.window['_output_img_'].update(width=w,height=h)

        # ���ڃ��Z�b�g
        img = cv2.resize(self.default_img, (w, h))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV��BGR��RGB�ɕϊ�
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.output_img_label.config(image=self.photo)

        return True

    # GUI ��ʍX�V
    def refresh(self, ):
        #try:
        #    (w, h) = self.window.size #�\���̈�̃T�C�Y
        #except:
        #    return False
        return True

    # �摜�Z�b�g
    def setImage(self, image=None, refresh=True, ):
        try:
            (w, h) = self.window.winfo_width(), self.window.winfo_height() #�\���̈�̃T�C�Y
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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV��BGR��RGB�ɕϊ�
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.output_img_label.config(image=self.photo)
        if (refresh == True):
            self.window.update()

    # POPUP ��ʕ\��
    def popup_text(self, title='', text='', auto_close=False, size=(96,24), ):
        txt = text
        try:
            dic = json.loads(text)
            txt = json.dumps(dic, ensure_ascii=False, indent=4, )
        except:
            pass

        popup = tk.Toplevel(self.window)
        popup.title('[ ' + title + ' ] (Read only)')
        popup.geometry(f"{size[0]}x{size[1]}")
        #popup.attributes("-topmost", True)

        text_area = tk.Text(popup, font='Arial 16')
        text_area.pack(expand=True, fill="both")
        text_area.insert(tk.END, txt)
        text_area.config(state=tk.DISABLED)  # �ǂݎ���p�ɂ���

        if auto_close:
            popup.after(int(auto_close * 1000), popup.destroy)

        return True



runMode = 'debug'

if __name__ == '__main__':

    gui = _gui()

    # �����ݒ�
    if (True):

        # �^�C�g���Aicon
        titlex = os.path.basename(__file__)
        titlex = titlex.replace('.py','')
        title  = titlex + '[' + runMode + ']'
        #icon  = None
        icon   = './_icons/' + titlex + '.ico'

        # GUI ������
        gui.init(qLog_fn='', runMode='debug',
                 screen='auto', panel='auto',
                 title=title, theme=None,
                 keep_on_top='yes', alpha_channel='0.5', icon=icon, )
        gui.bind()

        # GUI ��p�L���[
        gui_queue = queue.Queue()

    # GUI �\�����[�v
    reset_flag   = True
    refresh_flag = True
    break_flag   = False
    values       = None
    while (break_flag == False):

        # GUI ���Z�b�g
        if (reset_flag == True):
            reset_flag   = False
            refresh_flag = True

            # GUI ��ʃ��Z�b�g
            gui.reset()

            # GUI �����t�F�[�h���Z�b�g
            gui.autoFadeControl(reset=True, )

            # GUI ��ʃ��T�C�Y���Z�b�g
            gui.resize(reset=True, )

        # GUI ���ڍX�V
        while (gui_queue.qsize() >= 1):
            [res_name, res_value] = gui_queue.get()
            gui_queue.task_done()
            #gui.window[res_name].update(res_value) # tkinter�ł͎g�p���Ȃ�

        # GUI �����t�F�[�h
        gui.autoFadeControl(reset=False, )

        # GUI ��ʃ��T�C�Y
        gui.resize(reset=False, )

        # GUI ��ʍX�V
        if (refresh_flag == True):
            refresh_flag = False
            gui.refresh()

        # GUI �C�x���g�m�F                 ���@timeout�l��time.sleep��p
        event, values = gui.read(timeout=150, timeout_key='-idoling-')

        # GUI �I���C�x���g����
        #if event == sg.WIN_CLOSED: # tkinter�ł͎g�p���Ȃ�
        #    gui.window = None
        #    break_flag = True
        #    break
        if event in (None, '-exit-'): # <<Timeout>> ���폜
            break_flag = True
            break

        try:
            # ------------------------------
            # �A�C�h�����O���̏���
            # ------------------------------
            if (event == '-idoling-' or event == '<<Timeout>>'): # tkinter�ł�Timeout
                pass

            # ------------------------------
            # �{�^���C�x���g����
            # ------------------------------
            # ���Z�b�g
            elif (event == '-reset-'):
                print(event, )
                reset_flag = True

            else:
                print(event, values, )
        except Exception as e:
            print(e)
            time.sleep(5.00)

    # �I������
    if (True):

        # GUI ��ʏ���
        try:
            gui.close()
            gui.terminate()
        except:
            pass

        # �I��
        sys.exit(0)
