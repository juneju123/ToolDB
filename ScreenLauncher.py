#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      8:40 PM
@Author:    Juju
@File:      ScreenLauncher
@Project:   OptionToolDb
"""
import logging

from tqdm import tqdm

import FileHelpers
import SimpleScreen
import SpreadScreen
import pandas as pd
import GlobarVars

my_logger = logging.getLogger(__name__)


def vertical_screen_launcher(symbol_list, option_chain, conditions, credit_debit,
                             put_call, spread_name, max_loss, min_profit, min_expectation, prob_of_max_profit,
                             max_strikes_wide):
    spread_result = pd.DataFrame(columns=GlobarVars.SPREAD_COLUMNS)

    for symbol in tqdm(symbol_list):
        # Screen Spread based on spread conditions
        spread = SpreadScreen.spread_screen(option_chain[symbol], credit_debit, put_call, max_loss, min_profit,
                                            min_expectation, prob_of_max_profit, max_strikes_wide)
        if not spread.empty:
            # Add filtered spreads to result list
            spread_result = spread_result.append(spread, ignore_index=True)
    # Generate output csv file
    output_file = FileHelpers.save_spread_to_csv(spread_result, spread_name + '_spread_result', conditions)
    my_logger.info('Option screen completed. Start writing results to csv files...')
    return output_file


def simple_screen_launcher(symbol_list, option_chain, conditions, min_days_to_expiration, max_days_to_expiration,
                           **kwargs):
    min_volume = kwargs.get('min_volume', 20)
    min_open_interest = kwargs.get('min_open_interest', 20)
    max_bid_ask_spread = kwargs.get('max_bid_ask_spread', 0.15)
    iv_vs_hv = kwargs.get('iv_vs_hv', 1.1)
    max_delta = kwargs.get('max_delta', 0.4)
    for symbol in tqdm(symbol_list):
        # Do a simple screen to filter out unwanted single options based on option conditions
        SimpleScreen.simple_screen(option_chain[symbol], conditions, min_days_to_expiration, max_days_to_expiration,
                                   min_volume, min_open_interest, max_bid_ask_spread, iv_vs_hv, max_delta)
