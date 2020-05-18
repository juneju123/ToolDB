#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      8:42 PM
@Author:    Juju
@File:      OptionToolLauncher
@Project:   OptionToolDb
"""
import copy
import logging

import GlobarVars
import InitialData
import OptionDb
import ScreenLauncher


def option_tool_launcher(symbol_list, conditions, is_live, max_loss, min_profit, min_expectation, prob_of_max_profit,
                         max_strikes_wide, min_days_to_expiration, max_days_to_expiration, spread_strategy):
    my_logger = logging.getLogger(__name__)

    # Initial parameters
    results_files_list = []

    # Connect to Database
    option_db = OptionDb.OptionDb('option_tool_db')

    # Request Live or Delayed data
    [all_call_chains, all_put_chains] = InitialData.request_all_data(symbol_list, option_db, is_live)

    # Copy raw data as a backup
    GlobarVars.call_chains_backup = copy.deepcopy(all_call_chains)
    GlobarVars.put_chains_backup = copy.deepcopy(all_put_chains)

    # Disconnect Database
    option_db.conn_close()
    my_logger.info('Database connection closed...')

    my_logger.info('Start screen options...')

    if spread_strategy == 'bullish':
        ScreenLauncher.simple_screen_launcher(symbol_list, all_put_chains, conditions, min_days_to_expiration,
                                              max_days_to_expiration)
        bullish_put = ScreenLauncher.vertical_screen_launcher(symbol_list, all_put_chains, conditions, 'CREDIT', 'PUT',
                                                              'bullish_put', max_loss,
                                                              min_profit, min_expectation, prob_of_max_profit,
                                                              max_strikes_wide)
        results_files_list = [bullish_put]
    elif spread_strategy == 'bearish':
        ScreenLauncher.simple_screen_launcher(symbol_list, all_call_chains, conditions, min_days_to_expiration,
                                              max_days_to_expiration)
        bearish_call = ScreenLauncher.vertical_screen_launcher(symbol_list, all_call_chains, conditions, 'CREDIT',
                                                               'CALL',
                                                               'bearish_call', max_loss,
                                                               min_profit, min_expectation, prob_of_max_profit,
                                                               max_strikes_wide)
        results_files_list = [bearish_call]
    elif spread_strategy == 'all':
        ScreenLauncher.simple_screen_launcher(symbol_list, all_put_chains, conditions, min_days_to_expiration,
                                              max_days_to_expiration)
        ScreenLauncher.simple_screen_launcher(symbol_list, all_call_chains, conditions, min_days_to_expiration,
                                              max_days_to_expiration)
        bullish_put = ScreenLauncher.vertical_screen_launcher(symbol_list, all_put_chains, conditions, 'CREDIT', 'PUT',
                                                              'bullish_put', max_loss,
                                                              min_profit, min_expectation, prob_of_max_profit,
                                                              max_strikes_wide)
        bearish_call = ScreenLauncher.vertical_screen_launcher(symbol_list, all_call_chains, conditions, 'CREDIT',
                                                               'CALL',
                                                               'bearish_call',
                                                               max_loss,
                                                               min_profit, min_expectation, prob_of_max_profit,
                                                               max_strikes_wide)
        results_files_list = [bullish_put, bearish_call]

    return results_files_list
