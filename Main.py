#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:11 PM
@Author:    Juju
@File:      Main
@Project:   OptionToolDb
"""
import copy
import traceback
from datetime import datetime

import FileHelpers
import GlobarVars
import OptionToolLauncher
import TDA_API_Request
import pymysql
import OptionDb
from tqdm import tqdm
import InitialData
import SingleOption
import OptionChain
import DateChain
import SimpleScreen
import SpreadScreen
import pandas as pd
import logging
import LogConfig
import UserInput
from SendNotification import send_notification

if __name__ == '__main__':
    LogConfig.log_config()
    my_logger = logging.getLogger(__name__)

    # Initial Variables
    result_files_list = []
    exclude_symbols = FileHelpers.read_symbol_list('symbol_list/Exclude_Symbols.xlsx')
    symbol_list = FileHelpers.read_symbol_list('symbol_list/Optionable.xlsx')
    # symbol_list = ['SPY']
    for symbol in exclude_symbols:
        if symbol in symbol_list:
            symbol_list.remove(symbol)
    # Option Conditions
    OC1 = 'high_volume'  # volume & open interest > 10
    OC2 = 'narrow_bid_ask'  # bid ask spread < 0.2 * last price
    OC3 = 'OTM'  # OTM
    OC4 = 'high_iv'  # iv > hv * 1.1
    OC5 = 'low_delta'  # delta < 0.4
    OC6 = 'low_theo'  # bid > theo

    start_time = GlobarVars.ROUND_NAME
    is_live = False
    try:
        symbol_list, option_conditions, is_live, max_loss, min_profit, min_expectation, prob_of_max_profit, \
        max_strikes_wide, min_days_to_expiration, max_days_to_expiration, spread_strategy = UserInput.user_input()
        result_files_list = OptionToolLauncher.option_tool_launcher(symbol_list, option_conditions, is_live, max_loss,
                                                                    min_profit, min_expectation, prob_of_max_profit,
                                                                    max_strikes_wide, min_days_to_expiration,
                                                                    max_days_to_expiration, spread_strategy)
        email_msg = "Test starts at: " + str(start_time) + "\nTest ends at: " + str(datetime.today().strftime(
            '%Y%m%d_%H%M')) + "\nResult folder: " + GlobarVars.RESULT_FOLDER + '\n' + "Raw data folder: " + \
                    GlobarVars.RAW_DATA_FOLDER + '\n' + 'Conditions: ' + str(option_conditions)
        email_subject = GlobarVars.ROUND_NAME + "; is_live_data: " + str(is_live) + '; Option Screen Finished'

    except Exception as e:
        print(traceback.format_exc())
        my_logger.debug(traceback.format_exc())
        # Send exception information
        email_msg = "Exception happened on test: " + start_time
        email_subject = "Exception happened on test: " + start_time
        send_notification(email_subject, traceback.format_exc(), [])

    # Send email notification with results
    send_notification(email_subject, email_msg, result_files_list)
