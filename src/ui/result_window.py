# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/result_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_result_window(object):
    def setupUi(self, result_window):
        result_window.setObjectName("result_window")
        result_window.resize(1167, 602)
        self.close = QtWidgets.QPushButton(result_window)
        self.close.setGeometry(QtCore.QRect(250, 80, 161, 51))
        self.close.setObjectName("close")
        self.open = QtWidgets.QPushButton(result_window)
        self.open.setGeometry(QtCore.QRect(250, 20, 161, 51))
        self.open.setObjectName("open")
        self.radio_button_bullish = QtWidgets.QRadioButton(result_window)
        self.radio_button_bullish.setGeometry(QtCore.QRect(70, 40, 100, 20))
        self.radio_button_bullish.setChecked(True)
        self.radio_button_bullish.setObjectName("radio_button_bullish")
        self.radio_button_bearish = QtWidgets.QRadioButton(result_window)
        self.radio_button_bearish.setGeometry(QtCore.QRect(70, 90, 100, 20))
        self.radio_button_bearish.setObjectName("radio_button_bearish")
        self.result_table = QtWidgets.QTableView(result_window)
        self.result_table.setGeometry(QtCore.QRect(5, 190, 1161, 411))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.result_table.sizePolicy().hasHeightForWidth())
        self.result_table.setSizePolicy(sizePolicy)
        self.result_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.result_table.setSortingEnabled(True)
        self.result_table.setObjectName("result_table")
        self.result_table.horizontalHeader().setCascadingSectionResizes(True)
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.verticalHeader().setCascadingSectionResizes(True)

        self.retranslateUi(result_window)
        QtCore.QMetaObject.connectSlotsByName(result_window)

    def retranslateUi(self, result_window):
        _translate = QtCore.QCoreApplication.translate
        result_window.setWindowTitle(_translate("result_window", "Form"))
        self.close.setText(_translate("result_window", "Close"))
        self.open.setText(_translate("result_window", "Open"))
        self.radio_button_bullish.setText(_translate("result_window", "Bullish"))
        self.radio_button_bearish.setText(_translate("result_window", "Bearish"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    result_window = QtWidgets.QWidget()
    ui = Ui_result_window()
    ui.setupUi(result_window)
    result_window.show()
    sys.exit(app.exec_())