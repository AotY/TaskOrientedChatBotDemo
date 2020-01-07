#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2020 LeonTao
#
# Distributed under terms of the MIT license.

"""
实现简单的DPL（Dialogue Policy Learning）
在限制条件下采用Action

输入：Sn (Gn, Un, Hn)
    Gn: 用户目标
    Un: SLU/NLU结果
    Hn: (U0, A0, U1, A1, ..., Un-1, An-1)

输出: An (Dn, {Ai, Vi})
    Dn: 对话类型
    {Ai, Vi}: 第n轮对话的attribute和value

Dn:
    [GREET] -> RESULT -> [BYE]
    [GREET] -> ASK (CONFIRM) -> RESULT -> [BYE]
"""

class DPL:
    def __init__(self):
        self.D_list = list() # 历史对话类型列表
        self.A_list = list() # 历史{An, Vn}列表

    def get_action(state):
        '''
        Args:
            state: tuple (Gn, Un, Hn)
        Returns:
            action: tuple (Dn, {Ai, Vi})
    Dn: 对话类型
        '''
        Gn, Un, Hn = state
        intent, slots = nlu_result

        # Dn 对话类型
        if Gn == 'GREET':
            Dn = 'GREET'
        elif Gn == 'ASK':
            Dn = 'RESULT'
        elif Gn == 'APPLY':
            Dn = 'ASK'
        elif Gn == 'CONFIRM':
            Dn = 'RESULT'
        elif Gn == 'BYE':
            Dn = 'BYE'

        # Ai Action
        real_intent = None
        if Dn in ['RESULT', 'ASK']:
            if intent not in ['TEMPORARY_LIMIT_INQUIRY', 'FIXED_LIMIT_INQUIRY', 'BILL_INQUIRY', \
                            'BILL_DAY_INQUIRY', 'REPAYMENT_DAY_INQUIRY', 'ANNUAL_FEE_INQUIRY', \
                            'APPLY_FOR_TEMPORARY_LIMIT', 'APPLY_FOR_FIXED_LIMIT']:
                # 从Hn中获取最近一个真正的意图
                for hi in Hn[::-1]:
                    if isinstance(hi, str):
                        if hi in ['TEMPORARY_LIMIT_INQUIRY', 'FIXED_LIMIT_INQUIRY', 'BILL_INQUIRY', \
                                    'BILL_DAY_INQUIRY', 'REPAYMENT_DAY_INQUIRY', 'ANNUAL_FEE_INQUIRY', \
                                'APPLY_FOR_TEMPORARY_LIMIT', 'APPLY_FOR_FIXED_LIMIT']:
                            real_intent = hi
                            break
        else:
            real_intent = intent

        # 如果没有业务相关意图
        # if real_intent is None

        if real_intent == 'TEMPORARY_LIMIT_INQUIRY':
            Ai = real_intent
        elif real_intent == 'FIXED_LIMIT_INQUIRY':
            Ai = real_intent
        elif real_intent == 'BILL_INQUIRY':
            Ai = real_intent
        elif real_intent == 'BILL_DAY_INQUIRY':
            Ai = real_intent
        elif real_intent == 'REPAYMENT_DAY_INQUIRY':
            Ai = real_intent
        elif real_intent == 'ANNUAL_FEE_INQUIRY':
            Ai = real_intent
        elif real_intent == 'APPLY_FOR_TEMPORARY_LIMIT':
            Ai = real_intent
        elif real_intent == 'APPLY_FOR_FIXED_LIMIT':
            Ai = real_intent
        else:
            Ai = intent

        # Vi
        Vi = slots

        # Vn 属性值
        action = (Dn, (Ai, Vi))

        # append Un
        Hn.append(Un)

        self.D_list.append(Dn)
        self.A_list.append((Ai, Vi))

        return action, Hn

