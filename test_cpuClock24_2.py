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
import glob
import queue

# PySimpleGUI の代わりに tkinter を利用（GUI は RiKi_cpuClock24_gui.py 内で実装）
# dummy import
if (os.name == 'nt'):
    import comtypes.client
    import comtypes.stream

# パス設定
qPath_base = os.path.dirname(sys.argv[0]) + '/'
if (qPath_base == '/'):
    qPath_base = os.getcwd() + '/'
else:
    os.chdir(qPath_base)

# インターフェース
qCtrl_control_clock = 'temp/control_cpuClock.txt'
qCtrl_control_self  = qCtrl_control_clock

qPath_temp   = 'temp/'
qPath_log    = 'temp/_log/'
qPath_work   = 'temp/_work/'
qPath_icons  = '_icons/'

# 共通ルーチン
import _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import _v6__qGUI
qGUI   = _v6__qGUI.qGUI_class()
import _v6__qLog
qLog   = _v6__qLog.qLog_class()

#import _v6__qFFmpeg
#qFFmpeg= _v6__qFFmpeg.qFFmpeg_class()

# 処理ルーチン
import RiKi_cpuClock24_conf
conf      = RiKi_cpuClock24_conf._conf()
import test_cpuClock24_2_gui
gui       = test_cpuClock24_2_gui._gui()
import RiKi_cpuClock24_proc
proc      = RiKi_cpuClock24_proc._proc()

# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)

#runMode  = 'debug'
#runMode  = 'analog'
#runMode  = 'digital'
runMode  = 'personal'

p_screen = 'auto'
p_panel  = 'auto'
p_design = 'auto'

if __name__ == '__main__':
    main_name = 'clock'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    # ライセンス設定
    limit_date     = '2026/12/31'
    dt = datetime.datetime.now()
    dateinfo_today = dt.strftime('%Y/%m/%d')
    dt = datetime.datetime.strptime(limit_date, '%Y/%m/%d') + datetime.timedelta(days=-365)
    dateinfo_start = dt.strftime('%Y/%m/%d')
    main_start = time.time()

    # ディレクトリ作成(基本用)
    qFunc.makeDirs(qPath_temp,   remove=False)
    qFunc.makeDirs(qPath_log,    remove=False)
    qFunc.makeDirs(qPath_work,   remove=False)

    # ログ
    nowTime  = datetime.datetime.now()
    basename = os.path.basename(__file__)
    basename = basename.replace('.py', '')
    qLog_fn  = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + basename + '.log'
    qLog.init(mode='logger', filename=qLog_fn)
    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, basename + ' runMode, ... ')

    # パラメータ
    if True:
        if (len(sys.argv) >= 2):
            runMode  = str(sys.argv[1]).lower()
        if (len(sys.argv) >= 3):
            p_screen = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            p_panel  = str(sys.argv[3])
        if (len(sys.argv) >= 5):
            p_design = str(sys.argv[4])

        qLog.log('info', main_id, 'runMode = ' + str(runMode))
        qLog.log('info', main_id, 'screen  = ' + str(p_screen))
        qLog.log('info', main_id, 'panel   = ' + str(p_panel))
        qLog.log('info', main_id, 'design  = ' + str(p_design))

    # 初期設定
    if True:
        # ライセンス制限
        if dateinfo_today >= dateinfo_start:
            qLog.log('warning', main_id, '利用ライセンスは、 ' + limit_date + ' まで有効です。')
        if dateinfo_today > limit_date:
            time.sleep(60)
            sys.exit(0)

        # conf 初期化
        conf.init(qLog_fn=qLog_fn, runMode=runMode, 
                gui_screen=p_screen, gui_panel=p_panel,
                clock_design=p_design)
        
        # コントロールリセット
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if txts != False:
            if (txt == '_end_') or (txt == '_stop_'):
                qFunc.remove(qCtrl_control_self)

        # 実行優先設定
        nice = conf.run_priority
        if nice == 'auto':
            nice = 'below'
        qFunc.setNice(nice)

        # タイトル、icon
        titlex = os.path.basename(__file__)
        titlex = titlex.replace('.py','')
        if dateinfo_today >= dateinfo_start:
            title  = titlex + ' [ ' + runMode + ' ] (License=' + limit_date + ')'
        else:
            title  = titlex + ' [ ' + runMode + ' ]'
        icon   = './_icons/' + titlex + '.ico'

        # GUI 専用キュー
        gui_queue = queue.Queue()

        # proc 初期化
        proc.init(qLog_fn=qLog_fn, runMode=runMode, conf=conf)

    # 起動
    if True:
        qLog.log('info', main_id, 'start')

        # 画面構成初期化
        change_screen = qGUI.checkUpdateScreenInfo(update=True)
        while change_screen == True:
            time.sleep(5.00)
            change_screen = qGUI.checkUpdateScreenInfo(update=True)
        dev_lastCheck = time.time()
        dev_setting   = True

        # 時刻変化確認用
        bk_s = 60
        bk_m = 60
        bk_h = 24

        # 目玉表示
        if runMode != 'personal':
            eyes = False
        else:
            eyes = True

    # GUI 表示ループ
    reset_flag   = True
    refresh_flag = True
    break_flag   = False
    values       = None
    while break_flag == False:
        # コントロール終了確認
        txts, txt = qFunc.txtsRead(qCtrl_control_self)
        if txts != False:
            if txt == '_end_':
                break_flag = True
                break

        # 実行制限
        if limit_date != '':
            nowTime = datetime.datetime.now()
            nowDate = nowTime.strftime('%Y/%m/%d')
            if nowDate > limit_date:
                qLog.log('critical', main_id, 'Check license [over limit date] ! (' + str(limit_date) + ')')
                break_flag = True
                break

        # 画面構成変更？
        if dev_setting == True or ((time.time() - dev_lastCheck) > float(conf.dev_intervalSec)):
            dev_change    = False
            change_screen = qGUI.checkUpdateScreenInfo(update=True)
            while change_screen == True:
                dev_change = True
                time.sleep(5.00)
                change_screen = qGUI.checkUpdateScreenInfo(update=True)
            dev_lastCheck = time.time()
            if dev_setting == True or dev_change == True:
                dev_setting = False
                qLog.log('warning', main_id, 'Screen (re) Setting... ')
                gui.close()
                gui.terminate()

        # GUI 初期化
        if gui.root is None:
            # GUI 表示位置
            screen = conf.gui_screen
            if screen == 'auto':
                screen = qGUI.getCornerScreen(rightLeft='right', topBottom='top', checkPrimary=False)
            panel = conf.gui_panel

            # GUI 初期化
            gui.init(qLog_fn=qLog_fn, runMode=runMode,
                    screen=screen, panel=panel,
                    title=title, theme=conf.gui_theme,
                    keep_on_top=conf.gui_keep_on_top, alpha_channel=conf.gui_alpha,
                    icon=icon)
            gui.bind()
            reset_flag = True

        # GUI リセット
        if reset_flag == True:
            reset_flag   = False
            refresh_flag = True

            # GUI 画面リセット
            gui.reset()

            # GUI 自動フェードリセット
            gui.autoFadeControl(reset=True)

            # GUI 画面リサイズリセット
            gui.resize(reset=True)

        # GUI 自動フェード
        gui.autoFadeControl(reset=False)

        # GUI 画面リサイズ
        gui.resize(reset=False)

        # GUI 画面更新
        if refresh_flag == True:
            refresh_flag = False
            gui.refresh()

        # GUI イベント確認
        event, values = gui.read(timeout=250, timeout_key='-idoling-')

        # GUI 終了イベント処理
        if event == "WIN_CLOSED":
            gui.root = None
            break_flag = True
            break
        if event in (None, '-exit-'):
            break_flag = True
            break

        try:
            # ------------------------------
            # アイドリング時の処理
            # ------------------------------
            if event == '-idoling-':
                # サイズ変更対応
                sg_left = gui.root.winfo_x()
                sg_top = gui.root.winfo_y()
                sg_width = gui.root.winfo_width()
                sg_height = gui.root.winfo_height()
                sg_left2 = sg_left
                sg_top2  = sg_top
                if not gui.no_titlebar:
                    sg_left2 = sg_left + 10
                    sg_top2  = sg_top  + 32

                # 時計
                dt_now    = datetime.datetime.now()
                dt_YYMMDD = dt_now.strftime('%Y%m%d')
                dt_YOUBI  = dt_now.strftime('%a')
                dt_HHMM   = dt_now.strftime('%H%M')
                s = dt_now.second
                m = dt_now.minute
                h = dt_now.hour

                # 時報処理
                if h != bk_h:
                    bk_h = h
                    proc.timeSign_info(h, m)

                # デザイン変更
                if m != bk_m:
                    bk_m = m
                    if conf.clock_design == 'auto':
                        design = h*60+m
                    else:
                        try:
                            design = int(conf.clock_design)
                        except:
                            design = 0

                # アナログ時計
                if runMode != 'digital' and runMode != 'personal':
                    if s != bk_s:
                        bk_s = s
                        try:
                            img = proc.getImage_analog(dt_now, design, eyes, sg_left2, sg_top2, sg_width, sg_height)
                            gui.setImage(image=img, refresh=True)
                        except Exception as e:
                            print(e)

                # デジタル時計 digital, personal
                if runMode == 'digital' or runMode == 'personal':
                    try:
                        img = proc.getImage_digital(dt_now, design, eyes, sg_left2, sg_top2, sg_width, sg_height)
                        gui.setImage(image=img, refresh=True)
                    except Exception as e:
                        print(e)

            # 画像クリック
            elif event == '_output_img_':
                eyes = not eyes

            # ------------------------------
            # ボタンイベント処理
            # ------------------------------
            # リセット
            elif event == '-reset-':
                print(event)
                reset_flag = True

            else:
                print(event, values)
        except Exception as e:
            print(e)
            time.sleep(5.00)

    # 終了処理
    if True:
        qLog.log('info', main_id, 'terminate')
        try:
            gui.close()
            gui.terminate()
        except:
            pass
        qLog.log('info', main_id, 'bye!')
        sys.exit(0)


