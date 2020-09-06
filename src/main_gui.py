import logging
import os
import sys
from PyQt5 import QtWidgets, QtCore

from src.ui.dialog_result import ui_result_window
from src.ui.main_window import Ui_MainWindow
from src.pre_and_post import global_vars
from src import start
from src.ui.result_window import Ui_result_window

helpers = global_vars.general_helpers
helpers.log_config()
my_logger = logging.getLogger(__name__)


class OptionToolGui(Ui_MainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(main_window)
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        # Connect Start button
        self.pushButton_Start.released.connect(self.start_clicked)
        # Connect radio Button with lineEdit
        self.radioButton_manual_symbol.toggled.connect(self.lineEdit_symbols.setEnabled)
        self.radioButton_symbol_file.toggled.connect(self.lineEdit_symbols_file.setEnabled)
        # output log to textEdit
        self.plainTextEdit_output = QPlainTextEditLogger(self.main_window)
        self.plainTextEdit_output.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        my_logger.addHandler(self.plainTextEdit_output)
        my_logger.setLevel(logging.DEBUG)


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
        start.start(my_logger)



class QPlainTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.widget.setEnabled(False)
        self.widget.setGeometry(QtCore.QRect(390, 270, 381, 261))
        self.widget.setObjectName("plainTextEdit_output")
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)


class result_window(Ui_result_window):
    def __init__(self, result_window_base):
        super(result_window, self).__init__()
        self.setupUi(result_window_base)
        self.init_ui()
        self.result_window_base = result_window_base

    def init_ui(self):
        pass

    def result_clicked(self):
        self.result_window_base.show()
        pass

if __name__ == "__main__":
    os.chdir("..")
    app = QtWidgets.QApplication(sys.argv)
    mainWindow_base = QtWidgets.QMainWindow()
    main_window = OptionToolGui(mainWindow_base)
    result_dialog_base = QtWidgets.QDialog()
    result_dialog = result_window(result_dialog_base)

    main_window.pushButton_Result.clicked.connect(result_dialog.result_clicked)

    mainWindow_base.show()
    sys.exit(app.exec_())
