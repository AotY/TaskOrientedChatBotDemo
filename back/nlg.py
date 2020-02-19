#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2020 LeonTao
#
# Distributed under terms of the MIT license.

"""
Simple NLG
基于规则或模板
"""

class NLG:
    def __init__(self):
        self.msg_list = list()
        pass

    def generate(self, action):
        '''
        Args:
            action: tuple (Dn, {Ai, Vi})
        Returns:
            msg: str
        '''

        Dn, (Ai, Vi) = action

        # if Dn
        msg = ''
        if Dn == 'GREET':
            msg = '您好。请问有什么可以帮您？'
        elif Dn == 'RESULT':
            if Ai == 'TEMPORARY_LIMIT_INQUIRY':
                msg = '您目前的临时额度为2万伍仟元整。'
            elif Ai == 'FIXED_LIMIT_INQUIRY':
                msg = '您目前的固定额度为1万伍仟元整。'
            elif Ai == 'BILL_INQUIRY':
                msg = '您本月的账单为1527元。'
            elif Ai == 'BILL_DAY_INQUIRY':
                msg = '您的账单日为每月的23号。'
            elif Ai == 'REPAYMENT_DAY_INQUIRY':
                msg = '您的还款日为每月的9号。'
            elif Ai == 'ANNUAL_FEE_INQUIRY':
                msg = '您的信用卡是没有年费的。'
            elif Ai == 'APPLY_FOR_TEMPORARY_LIMIT':
                msg = '申请临时额度成功，您目前的临时额度为3万元整。'
            elif Ai == 'APPLY_FOR_FIXED_LIMIT':
                msg = '申请临时额度成功，您目前的固定额度为5万元整。'
        elif Dn == 'ASK':
            if Ai == 'APPLY_FOR_TEMPORARY_LIMIT':
                msg = '由于您的消费状况良好，我行可以将您目前的临时额度调为3万元整，请问您确认要调整吗？'
            elif Ai == 'APPLY_FOR_FIXED_LIMIT':
                msg = '由于您的消费状况良好，我行可以将您目前的固定额度调为5万元整，请问您确认要调整吗？'
        elif Dn == 'BYE':
            msg = '再见。'
        else:
            msg = '请问有什么可以帮您？'

        self.msg_list.append(msg)
        return msg
