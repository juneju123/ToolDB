#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      8:33 PM
@Author:    Juju
@File:      SimpleScreener
@Project:   OptionToolDb
"""
import OptionChain
import DateChain


def simple_screen(option_chains, conditions, min_days_to_expiration, max_days_to_expiration, **kwargs):
    """

    :param conditions:
    :type option_chains: OptionChain.OptionChain
    """
    min_volume = kwargs.get('min_volume', 20)
    min_open_interest = kwargs.get('min_open_interest', 20)
    max_bid_ask_spread = kwargs.get('max_bid_ask_spread', 0.15)
    iv_vs_hv = kwargs.get('iv_vs_hv', 1.1)
    max_delta = kwargs.get('max_delta', 0.4)
    for date in option_chains.get_all_dates():
        date_chain: DateChain.DateChain = option_chains.get_date_chain(date)
        delete_strikes = []
        for single_option in date_chain.single_option_dict.values():
            if single_option.daysToExpiration > max_days_to_expiration or single_option.daysToExpiration < min_days_to_expiration:
                delete_strikes.append(single_option)
                continue
            for condition in conditions:
                if condition == 'high_volume' and not high_volume_screen(single_option, min_volume, min_open_interest):
                    delete_strikes.append(single_option)
                    break
                elif condition == 'narrow_bid_ask' and not narrow_bid_ask(single_option, max_bid_ask_spread):
                    delete_strikes.append(single_option)
                    break
                elif condition == 'OTM' and not is_otm(single_option):
                    delete_strikes.append(single_option)
                    break
                elif condition == 'high_iv' and not high_iv(single_option, iv_vs_hv):
                    delete_strikes.append(single_option)
                    break
                elif condition == 'low_delta' and not low_delta(single_option, max_delta):
                    delete_strikes.append(single_option)
                    break
                elif condition == 'low_theo' and not low_theo(single_option):
                    delete_strikes.append(single_option)
                    break
        for option in delete_strikes:
            date_chain.del_option(option.get_strike())


def high_volume_screen(single_option, min_volume, min_open_interest):
    """

    :param min_open_interest:
    :param min_volume:
    :type single_option: SingleOption
    """
    return single_option.totalVolume >= min_volume and single_option.openInterest >= min_open_interest


def narrow_bid_ask(single_option, max_bid_ask_spread):
    """

    :param max_bid_ask_spread:
    :type single_option: SingleOption
    """
    return single_option.bidAskSpread < single_option.last * max_bid_ask_spread


def is_itm(single_option):
    """

    :type single_option: SingleOption
    """
    return single_option.inTheMoney == '1'


def is_otm(single_option):
    return single_option.inTheMoney == '0'


def high_iv(single_option, iv_vs_hv):
    """

    :param iv_vs_hv:
    :type single_option: SingleOption
    """
    return single_option.volatility > single_option.underlying_hv * iv_vs_hv


def low_delta(single_option, max_delta):
    """

    :param max_delta:
    :type single_option: SingleOption
    """
    return abs(single_option.delta) <= max_delta


def low_theo(single_option):
    """

    :type single_option: SingleOption
    """
    return single_option.theoreticalOptionValue < single_option.bid
