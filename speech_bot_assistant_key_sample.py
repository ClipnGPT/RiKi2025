#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

def getkey(api, key):

    # assistant チャットボット
    if (api == 'assistant'):
        print('speech_bot_assistant_key.py')
        print('set your key!')
        if (key == 'assistant_api_type'):
            return 'use assistant api type'
        if (key == 'assistant_default_gpt'):
            return 'use assistant default gpt'
        if (key == 'assistant_default_class'):
            return 'use chat default class'
        if (key == 'assistant_auto_continue'):
            return 'use chat auto continue'
        if (key == 'assistant_max_step'):
            return 'chat max step'
        if (key == 'assistant_max_session'):
            return 'use max session'
        if (key == 'assistant_max_wait_sec'):
            return 'chat max wait(sec)'

        if (key == 'openai_organization'):
            return 'your openai organization'
        if (key == 'openai_key_id'):
            return 'your openai key'

        if (key == 'azure_endpoint'):
            return 'your azure endpoint'
        if (key == 'azure_version'):
            return 'your azure version'
        if (key == 'azure_key_id'):
            return 'your azure key'

        if (key == 'assistant_a_nick_name'):
            return 'your assistant (a) nick name'
        if (key == 'assistant_a_model'):
            return 'your assistant (a) model'
        if (key == 'assistant_a_token'):
            return 'your assistant (a) token'
        if (key == 'assistant_a_use_tools'):
            return 'your assistant (a) use tools'

        if (key == 'assistant_b_nick_name'):
            return 'your assistant (b) nick name'
        if (key == 'assistant_b_model'):
            return 'your assistant (b) model'
        if (key == 'assistant_b_token'):
            return 'your assistant (b) token'
        if (key == 'assistant_b_use_tools'):
            return 'your assistant (b) use tools'

        if (key == 'assistant_v_nick_name'):
            return 'your assistant (v) nick name'
        if (key == 'assistant_v_model'):
            return 'your assistant (v) model'
        if (key == 'assistant_v_token'):
            return 'your assistant (v) token'
        if (key == 'assistant_v_use_tools'):
            return 'your assistant (v) use tools'

        if (key == 'assistant_x_nick_name'):
            return 'your assistant (x) nick name'
        if (key == 'assistant_x_model'):
            return 'your assistant (x) model'
        if (key == 'assistant_x_token'):
            return 'your assistant (x) token'
        if (key == 'assistant_x_use_tools'):
            return 'your assistant (x) use tools'

    return False


