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

global RAW_DATA_FOLDER, RESULT_FOLDER, SYMBOL_LIST_FOLDER, SPREAD_COLUMNS, ROUND_NAME, call_chains_backup, put_chains_backup

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
general_helpers = GeneralHelpers()