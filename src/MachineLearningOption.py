import os

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.utils import shuffle
from tqdm import tqdm

from src.process.clean_data import start_clean
from src.process.learn_methods import Learnings

os.chdir('../')
data_path = 'Data/'
symbol = 'SPY'
year = 2020

old_data = False
# month = 11
train_month = [5, 6, 7, 8]
predict_month = [9]
predict_option_type = 'P'
action = 'SELL'
if not old_data:
    for month in tqdm(train_month + predict_month):
        data_c, data_p = start_clean(data_path, symbol, year, month, action)
        data_c.to_csv(data_path + symbol + '_' + str(year) + str(month) + '_C_' + "clean.csv", index=False)
        data_p.to_csv(data_path + symbol + '_' + str(year) + str(month) + '_P_' + "clean.csv", index=False)

first_loop = True
for month in train_month:
    if first_loop:
        train = pd.read_csv(
            data_path + symbol + '_' + str(year) + str(month) + "_" + predict_option_type + "_" + "clean.csv").sample(
            frac=1)
        first_loop = False
    else:
        train = train.append(pd.read_csv(
            data_path + symbol + '_' + str(year) + str(month) + "_" + predict_option_type + "_" + "clean.csv").sample(
            frac=1))
    train = train.reset_index(drop=True)
    train = shuffle(train)

first_loop = True
for month in predict_month:
    if first_loop:
        test = pd.read_csv(
            data_path + symbol + '_' + str(year) + str(month) + "_" + predict_option_type + "_" + "clean.csv").sample(
            frac=1)
    else:
        test = test.append(pd.read_csv(
            data_path + symbol + '_' + str(year) + str(month) + "_" + predict_option_type + "_" + "clean.csv").sample(
            frac=1))
    test = test.reset_index(drop=True)

X_train = train.iloc[:, :-1]
X_test = test.iloc[:, :-1]
y_train = train.iloc[:, -1]
y_test = test.iloc[:, -1]
feature_select = True
learning = Learnings(X_train, X_test, y_train, y_test, feature_select)
dt_predict, dt_report = learning.decision_tree()
test['dt_predict'] = pd.Series(dt_predict, name='predict')
# test.to_csv(data_path + symbol + '_' + str(year) + str(month) + '_C_' + "predict.csv", index=False)
print(dt_report)
print("Accurancy: " + str(np.sum(learning.y_test == learning.dt_predict) / len(y_test)))


rf_predict, rf_report = learning.random_forest()
test['rf_predict'] = pd.Series(rf_predict, name='predict')
print(rf_report)
print("Accurancy: " + str(np.sum(learning.y_test == learning.rf_predict) / len(y_test)))

kn_predict, kn_report = learning.k_neighbor()
test['kn_predict'] = pd.Series(kn_predict, name='predict')
print(kn_report)
print("Accurancy: " + str(np.sum(learning.y_test == learning.kn_predict) / len(y_test)))


test.to_csv(data_path + symbol + '_' + str(year) + str(predict_month[0]) + '_' + str(
    predict_month[-1]) + '_' + predict_option_type + '_' + "predict.csv", index=False)

learning.plot_result(dt_predict)

pass
