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

from src.core import data_request
from src.helpers import option_db_helper, general_helpers
from src.pre_and_post import global_vars
from src.process import screen_launcher


class OptionTool:
    def __init__(self):
        self.symbol_list = []
        self.exclude_symbols = general_helpers.GeneralHelpers.read_symbol_list('symbol_list/Exclude_Symbols.xlsx')
        self.start_time = global_vars.ROUND_NAME
        self.is_live = False
        self.conditions = []
        self.max_loss = -3.5
        self.min_profit = 0.5
        self.min_expectation = 0.05
        self.prob_of_max_profit = 0.7
        self.max_strikes_wide = 2
        self.min_days_to_expiration = 30
        self.max_days_to_expiration = 50
        self.spread_strategy = 'all'
        self.all_call_chains = {}
        self.all_put_chains = {}
        # Connect to Database
        self.option_db = option_db_helper.OptionDbHelpers('option_tool_db')

    def pre_execution(self):
        choice = 0
        while choice not in ['1', '2', '3', '4']:
            choice = input('''
                Please make a choice:
                1. Screen all optional stocks/ETF in the market
                2. Screen all high volatility stocks/ETF in the market
                3. Screen specific symbol list file
                4. Screen small number of symbols
                ''')

        if choice == '1':
            self.symbol_list = general_helpers.GeneralHelpers.read_symbol_list('symbol_list/Optionable.xlsx')
        elif choice == '2':
            self.symbol_list = general_helpers.GeneralHelpers.read_symbol_list('symbol_list/High_IV.xlsx')
        elif choice == '3':
            self.symbol_list = input(
                "Please provide your symbol list file name. File should be saved in symbol_list directory.")
        elif choice == '4':
            self.symbol_list = input("Please input symbol list(separate by comma, example: AAPL,SPY):").split(',')

        option_conditions = input('''Please select conditions, separate by comma(example: C1, C3, C6)[OC1,OC2,OC3]:
            OC1 = 'high_volume'     # volume & open interest > 10
            OC2 = 'narrow_bid_ask'  # bid ask spread < 0.2 * last price
            OC3 = 'OTM'         # OTM
            OC4 = 'high_iv'     # iv > hv * 1.1
            OC5 = 'low_delta'   # delta < 0.4
            OC6 = 'low_theo'    # bid > theo

                ''') or "OC1,OC2,OC3"
        self.conditions = option_conditions.split(',')
        while len(set(self.conditions) - set(['OC1', 'OC2', 'OC3', 'C4', 'OC5', 'OC6'])) != 0:
            print('The entered conditions are not correct: ' + str(option_conditions))
            option_conditions = input('''Please select conditions, separate by comma(example: C1, C3, C6):
                    OC1 = 'high_volume'     # volume & open interest > 10
                    OC2 = 'narrow_bid_ask'  # bid ask spread < 0.2 * last price
                    OC3 = 'OTM'         # OTM
                    OC4 = 'high_iv'     # iv > hv * 1.1
                    OC5 = 'low_delta'   # delta < 0.4
                    OC6 = 'low_theo'    # bid > theo

                        ''')
            self.conditions = option_conditions.split(',')
        option_conditions_dec = []
        for condition in self.conditions:
            if condition == 'OC1':
                option_conditions_dec.append('high_volume')
            elif condition == 'OC2':
                option_conditions_dec.append('narrow_bid_ask')
            elif condition == 'OC3':
                option_conditions_dec.append('OTM')
            elif condition == 'OC4':
                option_conditions_dec.append('high_iv')
            elif condition == 'OC5':
                option_conditions_dec.append('low_delta')
            elif condition == 'OC6':
                option_conditions_dec.append('low_theo')

        self.conditions = option_conditions_dec
        self.is_live = input('Do you want to use live data or not?[No]') == 'Yes'
        self.max_loss = process_input(input('Spread max_loss[-3.5]:')) or -3.5
        self.min_profit = process_input(input('Spread min_profit[0.5]:')) or 0.5
        self.min_expectation = process_input(input('Spread min_expectation[0.05]:')) or 0.05
        self.prob_of_max_profit = process_input(input('Spread prob_of_max_profit[0.7]:')) or 0.7
        self.max_strikes_wide = process_input(input('Spread max_strikes_wide[2]:')) or 2
        self.min_days_to_expiration = process_input(input('Minimum days to expiration[30]: ')) or 30
        self.max_days_to_expiration = process_input(input('Maximum days to expiration[50]: '))or 50
        self.spread_strategy = process_input(input('Please choose your spread strategy(bullish, bearish, all)[all]: ')) or 'all'

    def execution(self):
        my_logger = logging.getLogger(__name__)

        # Initial parameters
        results_files_list = []

        # Request Live or Delayed data
        requester = data_request.DataRequest(self.symbol_list, self.option_db, self.is_live)
        [self.all_call_chains, self.all_put_chains] = requester.request_all_data()

        # Copy raw data as a backup
        global_vars.call_chains_backup = copy.deepcopy(self.all_call_chains)
        global_vars.put_chains_backup = copy.deepcopy(self.all_put_chains)

        # Disconnect Database
        self.option_db.conn_close()
        my_logger.info('Database connection closed...')

        my_logger.info('Start screen options...')

        if self.spread_strategy == 'bullish':
            put_simple_screener = screen_launcher.SimpleScreener(self.symbol_list, self.all_put_chains, self.conditions,
                                                                 self.min_days_to_expiration,
                                                                 self.max_days_to_expiration)
            put_simple_screener.simple_screen()
            bullish_spread_screener = screen_launcher.SpreadScreener(self.symbol_list, self.all_put_chains,
                                                                     self.conditions, 'CREDIT',
                                                                     'PUT',
                                                                     'bullish_put', self.max_loss,
                                                                     self.min_profit, self.min_expectation,
                                                                     self.prob_of_max_profit,
                                                                     self.max_strikes_wide)
            bullish_put = bullish_spread_screener.spread_screen()
            results_files_list = [bullish_put]
        elif self.spread_strategy == 'bearish':
            call_simple_screener = screen_launcher.SimpleScreener(self.symbol_list, self.all_call_chains,
                                                                  self.conditions,
                                                                  self.min_days_to_expiration,
                                                                  self.max_days_to_expiration)
            call_simple_screener.simple_screen()
            bearish_spread_screener = screen_launcher.SpreadScreener(self.symbol_list, self.all_call_chains,
                                                                     self.conditions, 'CREDIT',
                                                                     'CALL',
                                                                     'bearish_call', self.max_loss,
                                                                     self.min_profit, self.min_expectation,
                                                                     self.prob_of_max_profit,
                                                                     self.max_strikes_wide)
            bearish_call = bearish_spread_screener.vertical_screen_launcher()

            results_files_list = [bearish_call]
        elif self.spread_strategy == 'all':
            put_simple_screener = screen_launcher.SimpleScreener(self.symbol_list, self.all_put_chains, self.conditions,
                                                                 self.min_days_to_expiration,
                                                                 self.max_days_to_expiration)
            put_simple_screener.simple_screen()
            bullish_spread_screener = screen_launcher.SpreadScreener(self.symbol_list, self.all_put_chains,
                                                                     self.conditions, 'CREDIT',
                                                                     'PUT',
                                                                     'bullish_put', self.max_loss,
                                                                     self.min_profit, self.min_expectation,
                                                                     self.prob_of_max_profit,
                                                                     self.max_strikes_wide)
            bullish_put = bullish_spread_screener.vertical_screen_launcher()

            call_simple_screener = screen_launcher.SimpleScreener(self.symbol_list, self.all_call_chains,
                                                                  self.conditions,
                                                                  self.min_days_to_expiration,
                                                                  self.max_days_to_expiration)
            call_simple_screener.simple_screen()
            bearish_spread_screener = screen_launcher.SpreadScreener(self.symbol_list, self.all_call_chains,
                                                                     self.conditions, 'CREDIT',
                                                                     'CALL',
                                                                     'bearish_call', self.max_loss,
                                                                     self.min_profit, self.min_expectation,
                                                                     self.prob_of_max_profit,
                                                                     self.max_strikes_wide)
            bearish_call = bearish_spread_screener.vertical_screen_launcher()

            results_files_list = [bullish_put, bearish_call]

        return results_files_list


def process_input(message):
    try:
        return float(message)
    except ValueError:
        return 0.0
