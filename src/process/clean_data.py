import calendar

import pandas as pd
from src.process.tda_api import TdApi
from datetime import datetime
import re
import datetime
import csv


def clean_raw_csv(data_path, symbol, year, month):
    input_path = data_path + symbol + '_' + str(year) + str(month) + ".csv"
    output_path = data_path + symbol + '_' + str(year) + str(month) + "_temp" + ".csv"

    with open(input_path, "r") as fp_in, open(output_path, "w") as fp_out:
        reader = csv.reader(fp_in)
        writer = csv.writer(fp_out)
        head_flag = False
        for row in reader:
            if len(row) == 0:
                continue
            elif not head_flag and "Option Code" in row[0]:
                head_flag = True
                writer.writerow(row)
            elif bool(re.search(symbol+'\d+', row[0])):
                writer.writerow(row)
            else:
                continue
    raw = pd.read_csv(output_path)
    df = raw.drop(raw.columns[-2:], axis=1)
    df = df.drop(columns=['LX', 'BX', 'AX', 'BX.1', 'AX.1', 'LX.1', 'Theo Price', 'Theo Price.1'])
    df_c = df.iloc[:, 0:22]
    df_p = df.iloc[:, 20:]
    df_c.to_csv(output_path[:-4] + "_C_" + output_path[-4:])
    df_p.to_csv(output_path[:-4] + "_P_" + output_path[-4:])
    return df_c, df_p


def remove_unwanted(data):
    data = data.astype(str)
    data = data.loc[:, ~data.columns.str.replace("(\.\d+)$", "").duplicated()]
    data.columns = data.columns.str.replace("(\.\d+)$", "")
    data = data[data.columns.drop(list(data.filter(regex='Option Code.*')))]
    data = data[data.columns.drop(list(data.filter(regex='Unnamed:.*')))]
    columns = data.columns
    data = data.apply(lambda x: x.str.replace(',', ''))
    data = data.apply(lambda x: x.str.replace('%', ''))
    for column in columns:
        data = data.drop(data[data[column] == '--'].index)
        data = data.drop(data[data[column] == '++'].index)
        data.loc[data[column] == '<empty>', column] = '0'
        data.loc[data[column] == '<empty>', column] = '0'
        if column != 'Exp':
            data[column] = pd.to_numeric(data[column])
    data = data[data['Volume'] > 0]
    data = data[data['Intrinsic'] == 0]
    data = data.reset_index(drop=True)
    return data


def add_expire_days(df, year, month):
    df["expire_days"] = ""
    index = 0
    for exp in df['Exp']:
        expiration = exp2date(exp)
        today = datetime.datetime(year, month, 1)
        exp_days = (expiration - today).days
        df.loc[index, "expire_days"] = int(exp_days)
        index = index + 1
    return df


def exp2str(exp):
    day_pattern = re.compile('\d+')
    month_pattern = re.compile('[A-Za-z]+')
    day = str(day_pattern.search(exp).group())
    if len(day) == 1:
        day = '0' + day
    month = str(month_name2int(month_pattern.search(exp).group()))
    if len(month) == 1:
        month = '0' + month
    year = "20" + str(exp[-2:])
    return year + "-" + month + "-" + day


def exp2date(exp):
    return datetime.datetime.strptime(exp2str(exp), '%Y-%m-%d')


def month_name2int(month_name):
    month_name = month_name[0] + month_name[-2:].lower()
    dic = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    return dic[month_name]


def add_target(data, symbol, option_type):
    api = TdApi()
    history_price = api.request_price_history(symbol=symbol, periodType='year', period=2, frequencyType='daily', frequency=1)
    index = 0
    data['expire_price'] = ""
    data["target"] = ""
    for exp in data["Exp"]:
        if option_type == 'C':
            if history_price.loc[exp2str(exp), "high"] >= data.loc[index, "Strike"] + data.loc[index, "LAST"]:
                data.loc[index, "target"] = 1
            else:
                data.loc[index, "target"] = 0
            data.loc[index, "expire_price"] = history_price.loc[exp2str(exp), "high"]
        elif option_type == 'P':
            if history_price.loc[exp2str(exp), "low"] <= data.loc[index, "Strike"] - data.loc[index, "LAST"]:
                data.loc[index, "target"] = 1
            else:
                data.loc[index, "target"] = 0
            data.loc[index, "expire_price"] = history_price.loc[exp2str(exp), "low"]
        index = index + 1
    return data.drop('Exp', axis='columns')


def start_clean(data_path, symbol, year, month):
    df_c, df_p = clean_raw_csv(data_path, symbol, year, month)
    clean_df = []
    option_type = ['C', 'P']
    n = 0
    for df in [df_c, df_p]:
        df = remove_unwanted(df)
        df = add_expire_days(df, year, month)
        clean_df.append(add_target(df, symbol, option_type[n]))
        n = n + 1
    return clean_df
