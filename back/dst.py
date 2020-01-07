#! /usr/bin/env python

# -*- coding: utf-8 -*-
# Copyright © 2020 LeonTao
#
# Distributed under terms of the MIT license.

"""
实现简单的DST
重点是追踪到用户的目标

输入：（Un, An-1, Sn-1)
    Un: SLU/NLU 结果 （In, Zn)
    An-1: 上一次DPL执行的动作
    Sn-1: 上一次DST状态

输出：Sn: (Gn, Un, Hn)
    Gn: 用户目标
    Un: SLU/NLU结果
    Hn: (U0, A0, U1, A1, ..., Un-1, An-1)

状态表示:
    [GREET] -> INQUIRY -> BYE
    [GREET] -> APPLY -> CONFIRM -> BYE
循环表示

状态追踪
   use if
"""

class DST:
    def __init__(self):
        self.U_list = list() # 历史意图列表
        self.G_list = list(['START']) # 历史用户目标列表

    def get_state(self, nlu_result, last_action, last_state, Hn):
        '''
        Args:
            nlu_result: tuple
            last_action: dict
            last_state: tuple Sn-1
        Returns:
            state: tuple (Gn, Un, Hn)
        'TEMPORARY_LIMIT_INQUIRY': '临时额度查询',
        'FIXED_LIMIT_INQUIRY': '固定额度查询',
        'BILL_INQUIRY': '账单查询',
        'BILL_DAY_INQUIRY': '账单日查询',
        'REPAYMENT_DAY_INQUIRY': '还款日查询',
        'ANNUAL_FEE_INQUIRY': '年费查询',
        'APPLY_FOR_TEMPORARY_LIMIT': '申请临时额度',
        'APPLY_FOR_FIXED_LIMIT': '申请固定额度'
        '''

        intent, slots = nlu_result

        # Gn
        if intent == 'TEMPORARY_LIMIT_INQUIRY':
            if self.G_list[-1] == 'START':
                Gn = 'RESULT'
            elif self.G_list[-1] == 'GREET':
                Gn = 'RESULT'
        elif intent == 'FIXED_LIMIT_INQUIRY':
            if self.G_list[-1] == 'START':
                Gn = 'RESULT'
            elif self.G_list[-1] == 'GREET':
                Gn = 'RESULT'
        elif intent == 'BILL_INQUIRY':
            if self.G_list[-1] == 'START':
                Gn = 'RESULT'
            elif self.G_list[-1] == 'GREET':
                Gn = 'RESULT'
        elif intent == 'REPAYMENT_DAY_INQUIRY':
            if self.G_list[-1] == 'START':
                Gn = 'RESULT'
            elif self.G_list[-1] == 'GREET':
                Gn = 'RESULT'
        elif intent == 'ANNUAL_FEE_INQUIRY':
            if self.G_list[-1] == 'START':
                Gn = 'RESULT'
            elif self.G_list[-1] == 'GREET':
                Gn = 'RESULT'
        elif intent == 'APPLY_FOR_TEMPORARY_LIMIT':
            if self.G_list[-1] == 'START':
                Gn = 'CONFIRM'
            elif self.G_list[-1] == 'GREET':
                Gn = 'CONFIRM'
        elif intent == 'CONFIRM':
            if self.G_list[-1] == 'CONFIRM':
                Gn = 'RESULT'
        elif intent == 'GREET':
            if self.G_list[-1] == 'START':
                Gn = 'GREET'
            elif self.G_list[-1] == 'GREET':
                Gn = 'GREET'
        elif intent == 'BYE':
            if self.G_list[-1] == 'RESULT':
                Gn = 'BYE'
            else:
                Gn = 'CONFIRM'

        self.G_list.append(Gn)

        # Un
        Un = nlu_result

        # Hn, TODO
        # self.H_list = list() # 对话历史列表
        # self.H_list.append(last_action)
        # Hn.append(last_action)

        state = (Gn, Un, Hn)

        return state
