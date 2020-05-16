#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      7:59 PM
@Author:    Juju
@File:      DateChain
@Project:   OptionToolDb
"""


class DateChain:
    def __init__(self):
        # self.expiration = date
        self.single_option_dict = {}

    def append_single_option(self, strike, single_option):
        self.single_option_dict[strike] = single_option

    def del_option(self, strike):
        del self.single_option_dict[strike]

    def get_next_x_option(self, strike, x):
        next_index = list(self.single_option_dict.keys()).index(strike) + x
        if next_index < list(self.single_option_dict).__len__():
            next_strike = list(self.single_option_dict)[next_index]
            return self.single_option_dict[next_strike]
        else:
            return None

    def get_single_option(self, strike):
        return self.single_option_dict[strike]

    def get_closest_strike(self, given_price):
        all_strikes = list(self.single_option_dict.keys())
        absolute_difference_function = lambda list_value: abs(list_value - given_price)
        closest_value = min(all_strikes, key=absolute_difference_function)
        return closest_value
