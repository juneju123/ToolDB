#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      8:40 PM
@Author:    Juju
@File:      ScreenLauncher
@Project:   OptionToolDb
"""
import logging

import pandas as pd
from tqdm import tqdm

from src.helpers import file_helpers
from src.option_objects.vertical_spread import VerticalSpread
from src.pre_and_post import global_vars

my_logger = logging.getLogger(__name__)


class SimpleScreener:
    def __init__(self, symbol_list, option_chains, conditions, min_days_to_expiration, max_days_to_expiration,
                 **kwargs):
        self.symbol_list = symbol_list
        self.option_chains = option_chains
        self.conditions = conditions
        self.min_days_to_expiration = min_days_to_expiration
        self.max_days_to_expiration = max_days_to_expiration
        self.min_volume = kwargs.get('min_volume', 20)
        self.min_open_interest = kwargs.get('min_open_interest', 20)
        self.max_bid_ask_spread = kwargs.get('max_bid_ask_spread', 0.15)
        self.iv_vs_hv = kwargs.get('iv_vs_hv', 1.1)
        self.max_delta = kwargs.get('max_delta', 0.4)

    def simple_screen(self):
        """
        :param min_volume:
        :param max_delta:
        :param iv_vs_hv:
        :param max_days_to_expiration:
        :param min_days_to_expiration:
        :param max_bid_ask_spread:
        :param min_open_interest:
        :param conditions:
        :type option_chains: option_chain.OptionChain
        """
        for symbol in tqdm(self.symbol_list):
            option_chains = self.option_chains[symbol]
            for date in option_chains.get_all_dates():
                date_chain: date_chain.DateChain = option_chains.get_date_chain(date)
                delete_strikes = []
                for single_option in date_chain.single_option_dict.values():
                    if single_option.daysToExpiration > self.max_days_to_expiration or single_option.daysToExpiration < self.min_days_to_expiration:
                        delete_strikes.append(single_option)
                        continue
                    for condition in self.conditions:
                        if condition == 'high_volume' and not high_volume(single_option, self.min_volume,
                                                                          self.min_open_interest):
                            delete_strikes.append(single_option)
                            break
                        elif condition == 'narrow_bid_ask' and not narrow_bid_ask(single_option,
                                                                                  self.max_bid_ask_spread):
                            delete_strikes.append(single_option)
                            break
                        elif condition == 'OTM' and not is_otm(single_option):
                            delete_strikes.append(single_option)
                            break
                        elif condition == 'high_iv' and not high_iv(single_option, self.iv_vs_hv):
                            delete_strikes.append(single_option)
                            break
                        elif condition == 'low_delta' and not low_delta(single_option, self.max_delta):
                            delete_strikes.append(single_option)
                            break
                        elif condition == 'low_theo' and not low_theo(single_option):
                            delete_strikes.append(single_option)
                            break
                for option in delete_strikes:
                    date_chain.del_option(option.get_strike())


class SpreadScreener:
    def __init__(self, symbol_list, option_chain, conditions, credit_debit, put_call, spread_name, max_loss,
                 min_profit, min_expectation, prob_of_max_profit, max_strikes_wide):
        self.symbol_list = symbol_list
        self.option_chain = option_chain
        self.credit_debit = credit_debit
        self.put_call = put_call
        self.spread_name = spread_name
        self.max_loss = max_loss
        self.min_profit = min_profit
        self.min_expectation = min_expectation
        self.prob_of_max_profit = prob_of_max_profit
        self.max_strikes_wide = max_strikes_wide
        self.conditions = conditions

    def vertical_screen_launcher(self):
        spread_result = pd.DataFrame(columns=global_vars.SPREAD_COLUMNS)
        for symbol in tqdm(self.symbol_list):
            # Screen Spread based on spread conditions
            spread = self.spread_screen(symbol)
            if not spread.empty:
                # Add filtered spreads to result list
                spread_result = spread_result.append(spread, ignore_index=True)
        # Generate output csv file
        output_file = file_helpers.FileHelpers.save_spread_to_csv(spread_result, self.spread_name + '_spread_result',
                                                      self.conditions)
        my_logger.info('Option screen completed. Start writing results to csv files...')
        return output_file

    def spread_screen(self, symbol):
        spread_df = pd.DataFrame(columns=global_vars.SPREAD_COLUMNS)
        spread_list = self.good_verticals_list(symbol)
        if len(spread_list) > 0:
            for spread in spread_list:
                spread_df = spread_df.append(spread.convert_to_df(), ignore_index=True)
        return spread_df

    def good_verticals_list(self, symbol):
        """

        :param put_call: PUT or CALL
        :param credit_debit: CREDIT or DEBIT
        :type option_chain: option_chain.OptionChain
        """

        good_verticals = []
        for date_chain in self.option_chain[symbol].date_chain_dict.values():
            for option in date_chain.single_option_dict.values():
                leg1 = option
                wide = 1
                while wide <= self.max_strikes_wide:
                    leg2 = date_chain.get_next_x_option(leg1.strikePrice, wide)
                    if leg2:
                        spread = VerticalSpread(leg1, leg2, self.credit_debit, self.put_call)
                        if spread.max_loss >= self.max_loss and spread.max_profit_prob > self.prob_of_max_profit \
                                and spread.get_max_profit() > self.min_profit and spread.expectation > self.min_expectation:
                            spread.to_string()
                            good_verticals.append(spread)
                    wide += 1
        return good_verticals


def high_volume(single_option, min_volume, min_open_interest):
    """

    :param min_open_interest:
    :param min_volume:
    :type single_option: single_option_obj
    """
    return single_option.totalVolume >= min_volume and single_option.openInterest >= min_open_interest


def narrow_bid_ask(single_option, max_bid_ask_spread):
    """

    :param max_bid_ask_spread:
    :type single_option: single_option_obj
    """
    return single_option.bidAskSpread < single_option.last * max_bid_ask_spread


def is_itm(single_option):
    """

    :type single_option: single_option_obj
    """
    return single_option.inTheMoney == '1'


def is_otm(single_option):
    return single_option.inTheMoney == '0'


def high_iv(single_option, iv_vs_hv):
    """

    :param iv_vs_hv:
    :type single_option: single_option_obj
    """
    return single_option.volatility > single_option.underlying_hv * iv_vs_hv


def low_delta(single_option, max_delta):
    """

    :param max_delta:
    :type single_option: single_option_obj
    """
    return abs(single_option.delta) <= max_delta


def low_theo(single_option):
    """

    :type single_option: single_option_obj
    """
    return single_option.theoreticalOptionValue < single_option.bid
