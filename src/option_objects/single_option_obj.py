#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      2:11 PM
@Author:    Juju
@File:      SingleOption
@Project:   OptionToolDb
"""
import numpy as np
from scipy.stats import norm
from src.pre_and_post import global_vars


class SingleOption:
    def __init__(self, option_info):
        """

        :type option_info: tuple
        """
        attrs = global_vars.OPTION_ATT_NAMES

        for attr in attrs:
            setattr(self, attr, option_info[attrs.index(attr)])

    def get_expiration_date(self):
        return self.expirationDate

    def get_strike(self):
        return self.strikePrice

    def get_mid_price(self):
        return (self.ask + self.bid) / 2

    def update_prob_itm(self):
        days_to_expiration = self.daysToExpiration
        if days_to_expiration == 0:
            days_to_expiration = 0.01
        strike = self.strikePrice
        option_type = self.putCall
        underlying_price = self.underlying_price
        temp = norm.cdf(np.log(strike / underlying_price) / (self.volatility / 100 * np.sqrt(days_to_expiration / 365)))
        prob_itm = temp if option_type == "PUT" else 1 - temp
        setattr(self, "probITM", round(prob_itm, 2))
