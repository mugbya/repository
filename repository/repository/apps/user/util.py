#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

def generator_token():
    '''
    生成固定唯一的随机序列
    :return:
    '''

    code = str(uuid.uuid1())

    return code[0:8]+code[-12:-1]
