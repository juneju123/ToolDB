#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      8:30 PM
@Author:    Juju
@File:      SpreadScreener
@Project:   OptionToolDb
"""
from VerticalSpread import VerticalSpread
import pandas as pd
import GlobarVars
import OptionChain


def spread_screen(dates_chains, credit_debit, put_call, max_loss, min_profit,
                  min_expectation, prob_of_max_profit, max_strikes_wide):
    spread_df = pd.DataFrame(columns=GlobarVars.SPREAD_COLUMNS)
    spread_list = good_verticals_list(dates_chains, credit_debit, put_call, max_loss, min_profit,
                                      min_expectation, prob_of_max_profit, max_strikes_wide)
    if len(spread_list) > 0:
        for spread in spread_list:
            spread_df = spread_df.append(spread.convert_to_df(), ignore_index=True)
    return spread_df


def good_verticals_list(option_chain, credit_debit, put_call, max_loss, min_profit,
                        min_expectation, prob_of_max_profit, max_strikes_wide):
    """

    :param put_call: PUT or CALL
    :param credit_debit: CREDIT or DEBIT
    :type option_chain: OptionChain.OptionChain
    """
    # max_strikes_wide = kwargs.get('max_strikes_wide', 2)
    # min_profit = kwargs.get('min_profit', 0.5)
    # min_expectation = kwargs.get('min_expectation', 0)
    # prob_of_max_profit = kwargs.get('prob_of_max_profit', 0.7)
    # max_loss = kwargs.get('max_loss', -3.5)
    good_verticals = []
    for date_chain in option_chain.date_chain_dict.values():
        for option in date_chain.single_option_dict.values():
            leg1 = option
            wide = 1
            while wide <= max_strikes_wide:
                leg2 = date_chain.get_next_x_option(leg1.strikePrice, wide)
                if leg2:
                    spread = VerticalSpread(leg1, leg2, credit_debit, put_call)
                    if spread.max_loss >= max_loss and spread.max_profit_prob > prob_of_max_profit \
                            and spread.get_max_profit() > min_profit and spread.expectation > min_expectation:
                        spread.to_string()
                        good_verticals.append(spread)
                wide += 1
    return good_verticals
