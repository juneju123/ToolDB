#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time:      9:13 PM
@Author:    Juju
@File:      UserInput
@Project:   OptionToolDb
"""
import file_helpers


def user_input():
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
        symbol_list = file_helpers.read_symbol_list('symbol_list/Optionable.xlsx')
    elif choice == '2':
        symbol_list = file_helpers.read_symbol_list('symbol_list/High_IV.xlsx')
    elif choice == '3':
        symbol_list = input("Please provide your symbol list file name. File should be saved in symbol_list directory.")
    elif choice == '4':
        symbol_list = input("Please input symbol list(separate by comma, example: AAPL,SPY):").split(',')

    option_conditions = input('''Please select conditions, separate by comma(example: C1, C3, C6)[OC1,OC2,OC3]:
        OC1 = 'high_volume'     # volume & open interest > 10
        OC2 = 'narrow_bid_ask'  # bid ask spread < 0.2 * last price
        OC3 = 'OTM'         # OTM
        OC4 = 'high_iv'     # iv > hv * 1.1
        OC5 = 'low_delta'   # delta < 0.4
        OC6 = 'low_theo'    # bid > theo
            
            ''') or "OC1,OC2,OC3"
    option_conditions = option_conditions.split(',')
    while len(set(option_conditions) - set(['OC1', 'OC2', 'OC3', 'C4', 'OC5', 'OC6'])) != 0:
        print('The entered conditions are not correct: ' + str(option_conditions))
        option_conditions = input('''Please select conditions, separate by comma(example: C1, C3, C6):
                OC1 = 'high_volume'     # volume & open interest > 10
                OC2 = 'narrow_bid_ask'  # bid ask spread < 0.2 * last price
                OC3 = 'OTM'         # OTM
                OC4 = 'high_iv'     # iv > hv * 1.1
                OC5 = 'low_delta'   # delta < 0.4
                OC6 = 'low_theo'    # bid > theo

                    ''')
        option_conditions = option_conditions.split(',')
    option_conditions_dec = []
    for condition in option_conditions:
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

    is_live = input('Do you want to use live data or not?[No]') == 'Yes'

    max_loss = input('Spread max_loss[-3.5]:') or -3.5
    min_profit = input('Spread min_profit[0.5]:') or 0.5
    min_expectation = input('Spread min_expectation[0.05]:') or 0.05
    prob_of_max_profit = input('Spread prob_of_max_profit[0.7]:') or 0.7
    max_strikes_wide = input('Spread max_strikes_wide[2]:') or 2
    min_days_to_expiration = input('Minimum days to expiration[30]: ') or 30
    max_days_to_expiration = input('Maximum days to expiration[50]: ') or 50

    spread_strategy = input('Please choose your spread strategy(bullish, bearish, all)[all]: ') or 'all'
    return symbol_list, option_conditions_dec, is_live, float(max_loss), float(min_profit), \
           float(min_expectation), float(prob_of_max_profit), int(max_strikes_wide), \
           int(min_days_to_expiration), int(max_days_to_expiration), spread_strategy


if __name__ == '__main__':
    user_input()
