#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      7:08 PM
@Author:    Juju
@File:      OptionChain
@Project:   OptionToolDb
"""


class OptionChain:
    def __init__(self, underlying_symbol):
        self.underlying_symbol = underlying_symbol
        self.date_chain_dict = {}

    def append_date_chain(self, date, date_chain):
        self.date_chain_dict[date] = date_chain

    def has_date_chain(self, date):
        return date in self.date_chain_dict.keys()

    def get_date_chain(self, date):
        return self.date_chain_dict[date]

    def get_all_dates(self):
        return list(self.date_chain_dict.keys())

