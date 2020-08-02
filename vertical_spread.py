#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      8:58 PM
@Author:    Juju
@File:      VerticalSpread
@Project:   OptionToolDb
"""

import pandas as pd
import study


class VerticalSpread:
    def __init__(self, leg1, leg2, credit_debit, put_call):
        """

        :type put_call: str
        PUT Vertical or CALL Vertical
        :type credit_debit: str
        CREDIT spread or DEBIT spread
        :type leg2: single_option_obj
        :type leg1: single_option_obj
        """
        self.leg1 = leg1
        self.leg2 = leg2
        self.credit_debit = credit_debit
        self.put_call = put_call
        self.premium = self.get_premium()
        self.theo_premium = self.get_theo_premium()
        self.max_loss = self.get_max_loss()
        self.max_profit = self.get_max_profit()
        self.max_profit_prob = self.get_max_profit_prob()
        self.max_loss_prob = self.get_max_loss_prob()
        self.expectation = self.get_expectation()
        self.__str = self.to_string()

    def get_premium(self):
        if self.credit_debit == "CREDIT":
            credit = self.leg2.get_mid_price() - self.leg1.get_mid_price() if self.put_call == 'PUT' else self.leg1.get_mid_price() - self.leg2.get_mid_price()
            return credit
        elif self.credit_debit == "DEBIT":
            debit = self.leg2.get_mid_price() - self.leg1.get_mid_price() if self.put_call == 'PUT' else self.leg1.get_mid_price() - self.leg2.get_mid_price()
            return debit

    def get_theo_premium(self):
        return self.leg2.theoreticalOptionValue - self.leg1.theoreticalOptionValue if self.put_call == 'PUT' \
            else self.leg1.theoreticalOptionValue - self.leg2.theoreticalOptionValue
        # if self.credit_debit == "CREDIT":
        #     credit = self.leg2.theoreticalOptionValue - self.leg1.theoreticalOptionValue if self.put_call == 'PUT' \
        #         else self.leg1.theoreticalOptionValue - self.leg2.theoreticalOptionValue
        #     return credit
        # elif self.credit_debit == "DEBIT":
        #     debit = self.leg2.theoreticalOptionValue - self.leg1.theoreticalOptionValue if self.put_call == 'PUT' \
        #         else self.leg1.theoreticalOptionValue - self.leg2.theoreticalOptionValue
        #     return debit

    def get_max_loss(self):
        if self.credit_debit == "DEBIT":
            return -self.get_premium() if self.get_premium() != 0 else 0.01
        elif self.credit_debit == "CREDIT":
            return self.get_premium() - self.get_strike_wide() if self.get_premium() != self.get_strike_wide() else 0.01

    def get_max_profit(self):
        if self.credit_debit == "DEBIT":
            return self.get_strike_wide() - self.get_premium()
        elif self.credit_debit == "CREDIT":
            return self.get_premium()

    def get_max_profit_price(self):
        if self.put_call == "PUT" and self.credit_debit == "CREDIT":
            return self.leg2.strikePrice
        elif self.put_call == "CALL" and self.credit_debit == "CREDIT":
            return self.leg1.strikePrice
        elif self.put_call == "PUT" and self.credit_debit == "DEBIT":
            return self.leg1.strikePrice
        elif self.put_call == "CALL" and self.credit_debit == "DEBIT":
            return self.leg2.strikePrice

    def get_max_loss_price(self):
        if self.put_call == "PUT" and self.credit_debit == "CREDIT":
            return self.leg1.strikePrice
        elif self.put_call == "CALL" and self.credit_debit == "CREDIT":
            return self.leg2.strikePrice
        elif self.put_call == "PUT" and self.credit_debit == "DEBIT":
            return self.leg2.strikePrice
        elif self.put_call == "CALL" and self.credit_debit == "DEBIT":
            return self.leg1.strikePrice

    def get_max_profit_prob(self):
        if self.put_call == "PUT" and self.credit_debit == "CREDIT":
            return 1 - self.leg2.probITM
        elif self.put_call == "CALL" and self.credit_debit == "CREDIT":
            return 1 - self.leg1.probITM
        elif self.put_call == "PUT" and self.credit_debit == "DEBIT":
            return self.leg1.probITM
        elif self.put_call == "CALL" and self.credit_debit == "DEBIT":
            return self.leg2.probITM

    def get_max_loss_prob(self):
        if self.put_call == "PUT" and self.credit_debit == "CREDIT":
            return self.leg1.probITM
        elif self.put_call == "CALL" and self.credit_debit == "CREDIT":
            return self.leg2.probITM
        elif self.put_call == "PUT" and self.credit_debit == "DEBIT":
            return 1 - self.leg2.probITM
        elif self.put_call == "CALL" and self.credit_debit == "DEBIT":
            return 1 - self.leg1.probITM

    def get_leg1_delta(self):
        return self.leg1.delta

    def get_leg2_delta(self):
        return self.leg2.delta

    def get_strike_wide(self):
        return abs(self.leg1.strikePrice - self.leg2.strikePrice)

    def get_expectation(self):
        # return self.get_max_profit() * self.get_max_profit_prob() - \
        #        self.get_max_loss() * self.get_max_loss_prob()
        return self.real_expectation()

    def get_break_even(self):
        if self.put_call == "PUT":
            return self.leg2.get_strike() - self.get_premium()
        elif self.put_call == "CALL":
            return self.leg1.get_strike() + self.get_premium()

    def get_profit_prob(self):
        return study.cal_prob_itm(self.get_break_even(), self.leg1.underlying_price,
                                  study.search_near_strike_volatility(self.leg1.underlying_symbol,
                                                                      self.get_break_even(), self.leg1.expirationDate,
                                                                      self.leg1.putCall),
                                  self.leg1.daysToExpiration, self.leg1.putCall)

    def get_date_string(self):
        option_symbol = self.leg1.symbol
        return '20' + option_symbol.split('_')[1][4:6] + '-' + option_symbol.split('_')[1][0:2] + '-' \
               + option_symbol.split('_')[1][2:4] + ':' + str(self.leg1.daysToExpiration)

    def get_payoff(self, price):
        payoff = 0
        if self.credit_debit == "CREDIT" and self.put_call == "PUT":
            if price >= self.leg2.get_strike():
                payoff = self.get_max_profit()
            elif price <= self.leg1.get_strike():
                payoff = self.get_max_loss()
            else:
                payoff = self.get_premium() - (self.leg2.get_strike() - price)
        elif self.credit_debit == "CREDIT" and self.put_call == "CALL":
            if price >= self.leg2.get_strike():
                payoff = self.get_max_loss()
            elif price <= self.leg1.get_strike():
                payoff = self.get_max_profit()
            else:
                payoff = self.get_premium() - (price - self.leg1.get_strike())
        elif self.credit_debit == "DEBIT" and self.put_call == "PUT":
            if price >= self.leg2.get_strike():
                payoff = self.get_max_loss()
            elif price <= self.leg1.get_strike():
                payoff = self.get_max_profit()
            else:
                payoff = self.leg2.get_strike() - price - self.premium
        elif self.credit_debit == "DEBIT" and self.put_call == "CALL":
            if price >= self.leg2.get_strike():
                payoff = self.max_profit()
            elif price <= self.leg1.get_strike():
                payoff = self.max_loss()
            else:
                payoff = price - self.leg1.get_strike() - self.premium
        return payoff

    def to_string(self):
        if self.credit_debit == "CREDIT" and self.put_call == "PUT":
            return "Buy " + self.leg1.symbol + "; Sell " + self.leg2.symbol
        elif self.credit_debit == "CREDIT" and self.put_call == "CALL":
            return "Buy " + self.leg2.symbol + "; Sell " + self.leg1.symbol
        elif self.credit_debit == "DEBIT" and self.put_call == "PUT":
            return "Buy " + self.leg2.symbol + "; Sell " + self.leg1.symbol
        elif self.credit_debit == "DEBIT" and self.put_call == "CALL":
            return "Buy " + self.leg1.symbol + "; Sell " + self.leg2.symbol

    def convert_to_df(self):
        vertical_spread = {'description': self.to_string()}
        vertical_spread['underlying symbol'] = self.leg1.underlying_symbol
        vertical_spread['underlying price'] = self.leg1.underlying_price
        vertical_spread['spread premium'] = self.get_premium()
        vertical_spread['spread theo premium'] = self.get_theo_premium()
        vertical_spread['expectation'] = self.get_expectation() / abs(self.get_max_loss())
        vertical_spread['max profit'] = self.get_max_profit()
        vertical_spread['max loss'] = self.get_max_loss()
        vertical_spread['max profit prob'] = self.get_max_profit_prob()
        vertical_spread['max loss prob'] = self.get_max_loss_prob()
        vertical_spread['leg1 symbol'] = self.leg1.symbol
        vertical_spread['leg2 symbol'] = self.leg2.symbol
        vertical_spread['leg1 theo'] = self.leg1.theoreticalOptionValue
        vertical_spread['leg2 theo'] = self.leg2.theoreticalOptionValue
        vertical_spread['leg1 delta'] = self.leg1.delta
        vertical_spread['leg2 delta'] = self.leg2.delta
        vertical_spread['leg1 volume'] = self.leg1.totalVolume
        vertical_spread['leg2 volume'] = self.leg2.totalVolume
        vertical_spread['leg1 inTheMoney'] = self.leg1.inTheMoney
        vertical_spread['leg2 inTheMoney'] = self.leg2.inTheMoney

        return pd.DataFrame(vertical_spread, index=[0])

    def real_expectation(self):

        put_call = self.leg1.putCall
        break_even = self.get_break_even()
        mid_profit_price = (break_even + self.get_max_profit_price()) / 2
        mid_profit_volatility = study.search_near_strike_volatility(self.leg1.underlying_symbol, mid_profit_price,
                                                                    self.leg1.expirationDate, put_call)
        mid_profit_prob = study.cal_prob_itm(mid_profit_price,
                                             self.leg1.underlying_price,
                                             mid_profit_volatility,
                                             self.leg1.daysToExpiration, put_call)
        break_even_prob = self.get_profit_prob()
        mid_profit_expect = abs(mid_profit_prob - break_even_prob) * self.get_max_profit() / 2

        mid_loss_price = (break_even + self.get_max_loss_price()) / 2
        mid_loss_volatility = study.search_near_strike_volatility(self.leg1.underlying_symbol, mid_loss_price,
                                                                  self.leg1.expirationDate, put_call)
        mid_loss_prob = study.cal_prob_itm(mid_loss_price,
                                           self.leg1.underlying_price,
                                           mid_loss_volatility,
                                           self.leg1.daysToExpiration, put_call)
        mid_loss_expect = abs(mid_loss_prob - break_even_prob) * self.get_max_loss() / 2

        return mid_loss_expect + mid_profit_expect + self.max_profit * self.max_profit_prob + \
               self.max_loss * self.max_loss_prob
