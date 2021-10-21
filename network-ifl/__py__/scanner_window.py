# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanner_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ScannerWindow(object):
    def setupUi(self, ScannerWindow):
        ScannerWindow.setObjectName("ScannerWindow")
        ScannerWindow.resize(380, 188)
        self.gridLayout = QtWidgets.QGridLayout(ScannerWindow)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtWidgets.QFrame(ScannerWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 3)
        self.label = QtWidgets.QLabel(ScannerWindow)
        self.label.setMaximumSize(QtCore.QSize(140, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ScannerWindow)
        self.label_2.setMaximumSize(QtCore.QSize(140, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(ScannerWindow)
        self.pushButton.setMaximumSize(QtCore.QSize(80, 24))
        self.pushButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(ScannerWindow)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(130, 24))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(ScannerWindow)
        self.lineEdit.setMinimumSize(QtCore.QSize(130, 24))
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 2)
        self.pushButton_2 = QtWidgets.QPushButton(ScannerWindow)
        self.pushButton_2.setMaximumSize(QtCore.QSize(80, 24))
        self.pushButton_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 2, 1, 1)

        self.retranslateUi(ScannerWindow)
        QtCore.QMetaObject.connectSlotsByName(ScannerWindow)

    def retranslateUi(self, ScannerWindow):
        _translate = QtCore.QCoreApplication.translate
        ScannerWindow.setWindowTitle(_translate("ScannerWindow", "Сканер сети"))
        self.label.setText(_translate("ScannerWindow", "Начальный адрес:"))
        self.label_2.setText(_translate("ScannerWindow", "Конечный адрес:"))
        self.pushButton.setText(_translate("ScannerWindow", "Старт"))
        self.lineEdit_2.setInputMask(_translate("ScannerWindow", "000.000.000.000;_"))
        self.lineEdit.setInputMask(_translate("ScannerWindow", "000.000.000.000;_"))
        self.pushButton_2.setText(_translate("ScannerWindow", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ScannerWindow = QtWidgets.QWidget()
    ui = Ui_ScannerWindow()
    ui.setupUi(ScannerWindow)
    ScannerWindow.show()
    sys.exit(app.exec_())
