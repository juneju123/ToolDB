#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      4:39 PM
@Author:    Juju
@File:      ProcessHelpers
@Project:   OptionToolDb
"""
from datetime import datetime
import Study

def clean_option_dict(option, underlying_price, underlying_symbol):
    for key in ['tradeTimeInLong', 'quoteTimeInLong', 'expirationDate', 'lastTradingDay']:
        option[key] = str(datetime.fromtimestamp(option[key] / 1e3).date())
    for key in ['optionDeliverablesList', 'deliverableNote', 'tradeDate', 'isIndexOption', 'settlementType']:
        del option[key]
    option['underlying_price'] = underlying_price
    option['underlying_symbol'] = underlying_symbol
    option['bidAskSpread'] = option['ask'] - option['bid']
    option['probITM'] = Study.cal_prob_itm(option['strikePrice'], option['underlying_price'], option['volatility'],
                                           option['daysToExpiration'], option['putCall'])

    return option

