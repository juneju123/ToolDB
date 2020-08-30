import os
import sys
from PyQt5 import QtWidgets

from src.mainwindow import MainWindow
from src.pre_and_post import global_vars
from src import start


class OptionToolGui(MainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setup_ui(main_window)
        self.init_ui()

    def init_ui(self):
        self.pushButton_Start.released.connect(self.start_clicked)
        self.radioButton_manual_symbol.toggled.connect(self.lineEdit_symbols.setEnabled)
        self.radioButton_symbol_file.toggled.connect(self.lineEdit_symbols_file.setEnabled)

    def start_clicked(self):
        global_vars.IS_GUI = True
        global_vars.MAX_LOSS = -round(self.doubleSpinBox_max_loss.value(), 2)
        global_vars.IS_LIVE = self.radioButton_live.isChecked()
        global_vars.MIN_PROFIT = round(self.doubleSpinBox_min_profit.value(), 2)
        global_vars.MAX_DAYS_TO_EXPIRATION = round(self.spinBox_max_days_expire.value())
        global_vars.MIN_DAYS_TO_EXPIRATION = round(self.spinBox_min_days_expire.value())
        global_vars.MAX_STRIKES_WIDE = round(self.spinBox_max_strike_width.value())
        global_vars.MIN_EXPECTATION = round(self.doubleSpinBox_min_expect.value(), 2)
        global_vars.PROB_OF_MAX_PROFIT = round(self.doubleSpinBox_prob_max_profit.value(), 2)
        if self.radioButton_bullish.isChecked():
            global_vars.SPREAD_STRATEGY = 'bullish'
        elif self.radioButton_bearish.isChecked():
            global_vars.SPREAD_STRATEGY = 'bearish'
        elif self.radioButton_both.isChecked():
            global_vars.SPREAD_STRATEGY = 'all'
        for i in range(self.gridLayout_Conditions.count()):
            if self.gridLayout_Conditions.itemAt(i).widget().isChecked():
                global_vars.CONDITIONS.append(self.gridLayout_Conditions.itemAt(i).widget().objectName())

        for i in range(self.verticalLayout_choice.count()):
            if self.verticalLayout_choice.itemAt(i).widget().isChecked():
                global_vars.CHOICE = i
                break

        if global_vars.CHOICE == 0:
            global_vars.SYMBOL_LIST = global_vars.general_helpers.read_symbol_list('symbol_list/Optionable.xlsx')
        elif global_vars.CHOICE == 1:
            global_vars.SYMBOL_LIST = global_vars.general_helpers.read_symbol_list('symbol_list/High_IV.xlsx')
        elif global_vars.CHOICE == 2:
            global_vars.SYMBOL_LIST = global_vars.general_helpers.read_symbol_list(self.lineEdit_symbols_file.text())
        elif global_vars.CHOICE == 3:
            global_vars.SYMBOL_LIST = self.lineEdit_symbols.text().split(',')
        start.start()


if __name__ == "__main__":
    os.chdir("..")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    form = OptionToolGui(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
