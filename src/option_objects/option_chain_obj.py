#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      7:08 PM
@Author:    Juju
@File:      OptionChain
@Project:   OptionToolDb
"""
from src.option_objects.date_chain_obj import DateChain


class OptionChain:
    def __init__(self, underlying_symbol: str):
        """

        :param underlying_symbol: underlying symbol
        """
        self.underlying_symbol = underlying_symbol
        self.date_chain_dict = {}

    def append_date_chain(self, date: str, date_chain: DateChain):
        """

        :param date: date, string
        :param date_chain: DateChain obj
        :return: single date chain
        """
        self.date_chain_dict[date] = date_chain

    def has_date_chain(self, date: str) -> bool:
        """

        :param date: date, string
        :return: True or False
        """
        return date in self.date_chain_dict.keys()

    def get_date_chain(self, date):
        """

        :param date: date, string
        :return:
        """
        return self.date_chain_dict[date]

    def get_all_dates(self):
        return list(self.date_chain_dict.keys())
