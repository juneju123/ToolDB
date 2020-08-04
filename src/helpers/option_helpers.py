#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      8:59 PM
@Author:    Juju
@File:      Study
@Project:   OptionToolDb
"""
import math
from datetime import datetime

import numpy as np
from numpy import sqrt, mean, log, diff
from scipy.stats import norm

from src.pre_and_post import global_vars

# def historical_volatility(symbol):
#     try:
#         price_history = request_price_history(symbol=symbol, periodType='month', period=1,
#                                               frequencyType='daily', frequency=1)
#     except RequestError:
#         raise
#     r = diff(log(price_history['close']))
#     r_mean = mean(r)
#     diff_square = [(r[i] - r_mean) ** 2 for i in range(0, len(r))]
#     std = sqrt(sum(diff_square) * (1.0 / (len(r) - 1)))
#     return round(std * sqrt(252), 2)

class OptionHelpers:
    def __init__(self):
        pass

    @staticmethod
    def cal_prob_itm(strike, underlying_price, volatility, days_to_expiration, put_call):
        if days_to_expiration == 0:
            days_to_expiration = 0.01
        try:
            temp = norm.cdf(math.log(strike / underlying_price) / (volatility / 100 * np.sqrt(days_to_expiration / 365)))
        except ValueError:
            pass
        prob_itm = temp if put_call == "PUT" else 1 - temp
        return float(prob_itm)

    @staticmethod
    def search_near_strike_volatility(underlying_symbol, price, date, put_call):
        """

        :param underlying_symbol:
        :param date:
        :param put_call: 'PUT' or 'CALL'
        :param price: Given price
        """

        if put_call == 'PUT':
            option_chains = global_vars.put_chains_backup[underlying_symbol]
        else:
            option_chains = global_vars.call_chains_backup[underlying_symbol]
        single_date_chain = option_chains.get_date_chain(date)
        strike = single_date_chain.get_closest_strike(price)
        return single_date_chain.get_single_option(strike).volatility

    @staticmethod
    def clean_option_dict(option, underlying_price, underlying_symbol):
        for key in ['tradeTimeInLong', 'quoteTimeInLong', 'expirationDate', 'lastTradingDay']:
            option[key] = str(datetime.fromtimestamp(option[key] / 1e3).date())
        for key in ['optionDeliverablesList', 'deliverableNote', 'tradeDate', 'isIndexOption', 'settlementType']:
            del option[key]
        option['underlying_price'] = underlying_price
        option['underlying_symbol'] = underlying_symbol
        option['bidAskSpread'] = option['ask'] - option['bid']
        option['probITM'] = OptionHelpers.cal_prob_itm(option['strikePrice'], option['underlying_price'], option['volatility'],
                                                       option['daysToExpiration'], option['putCall'])

        return option