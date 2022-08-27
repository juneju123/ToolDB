#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      10:44 AM
@Author:    Juju
@File:      setting_global_variables
@Project:   TOS_API
"""
from datetime import datetime

from src.helpers.general_helpers import GeneralHelpers

global RAW_DATA_FOLDER, RESULT_FOLDER, SYMBOL_LIST_FOLDER, SPREAD_COLUMNS, ROUND_NAME, call_chains_backup, put_chains_backup, OPTION_COLUMNS, OPTION_ATT_NAMES, DB_COL_NAMES

ROUND_NAME = datetime.today().strftime('%Y%m%d_%H%M')

SYMBOL_LIST_FOLDER = 'symbol_list/' + ROUND_NAME + '/'
RAW_DATA_FOLDER = 'raw_data/' + ROUND_NAME + '/'
RESULT_FOLDER = 'result/' + ROUND_NAME + '/'
SPREAD_COLUMNS = ['underlying symbol', 'underlying price', 'description',
                  'max profit', 'max loss', 'max profit prob', 'max loss prob',
                  'spread premium', 'spread theo premium', 'expectation', 'leg1 symbol', 'leg2 symbol', 'leg1 theo',
                  'leg2 theo', 'leg1 delta', 'leg2 delta', 'leg1 volume', 'leg2 volume', 'leg1 inTheMoney',
                  'leg2 inTheMoney']
OPTION_COLUMNS = ['underlying symbol', 'underlying price', 'symbol',
                  'strike', 'daysToExpiration', 'bid', 'ask', 'implied volatility',
                  'theoretical price', 'delta', 'total volume', 'putCall']
# Align names with new TD API response
OPTION_ATT_NAMES = ['underlying_symbol', 'underlying_price', 'putCall', 'symbol', 'description', 'exchangeName', 'bid',
                 'ask', 'last', 'mark', 'bidSize', 'askSize', 'bidAskSize', 'lastSize', 'highPrice', 'lowPrice',
                 'openPrice', 'closePrice', 'totalVolume', 'tradeDate', 'tradeTimeInLong', 'quoteTimeInLong', 'netChange',
                 'volatility', 'delta', 'gamma', 'theta', 'vega', 'rho', 'openInterest', 'timeValue',
                 'theoreticalOptionValue', 'theoreticalVolatility', 'optionDeliverablesList', 'strikePrice', 'expirationDate',
                 'daysToExpiration', 'expirationType', 'lastTradingDay', 'multiplier', 'settlementType', 'deliverableNote', 'isIndexOption', 'percentChange', 'markChange',
                 'markPercentChange', 'intrinsicValue', 'pennyPilot', 'inTheMoney', 'mini', 'nonStandard', 'bidAskSpread', 'probITM']
# Align names with new TD API response
DB_COL_NAMES = """underlying_symbol CHAR(10), underlying_price FLOAT, putCall CHAR(5), 
            symbol CHAR(20), description VARCHAR(50), exchangeName CHAR(10), bid FLOAT, ask FLOAT, last FLOAT, mark FLOAT, 
            bidSize INT, askSize INT, bidAskSize CHAR(20), lastSize INT, highPrice FLOAT, lowPrice FLOAT, openPrice FLOAT, 
            closePrice FLOAT, totalVolume INT, tradeDate CHAR(10), tradeTimeInLong DATE, quoteTimeInLong DATE, netChange FLOAT, 
            volatility FLOAT, delta FLOAT, gamma FLOAT, theta FLOAT, vega FLOAT, rho FLOAT, openInterest INT, 
            timeValue FLOAT, theoreticalOptionValue FLOAT, theoreticalVolatility FLOAT, optionDeliverablesList CHAR(10), strikePrice FLOAT, 
            expirationDate DATE, daysToExpiration INT, expirationType CHAR(5), lastTradingDay DATE, multiplier FLOAT, settlementType CHAR(10), 
            deliverableNote CHAR(10), isIndexOption CHAR(10), percentChange FLOAT, markChange FLOAT, 
            markPercentChange FLOAT, intrinsicValue FLOAT, pennyPilot CHAR(5), inTheMoney CHAR(5), mini CHAR(5), nonStandard CHAR(5), bidAskSpread FLOAT, 
            probITM FLOAT"""
general_helpers = GeneralHelpers()

IS_GUI = False

IS_LIVE = True
MAX_LOSS = -3.5
MIN_PROFIT = 0.5
MIN_EXPECTATION = 0.05
PROB_OF_MAX_PROFIT = 0.7
MAX_STRIKES_WIDE = 3
MIN_DAYS_TO_EXPIRATION = 30
MAX_DAYS_TO_EXPIRATION = 50
SPREAD_STRATEGY = 'all'
CONDITIONS = []
CHOICE = 1
SYMBOL_LIST = []

RESULT_LIST = []