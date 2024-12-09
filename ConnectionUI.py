from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QAbstractItemView



class ConnectionUi(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(531, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.connectButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(50, 270, 101, 41))
        self.connectButton.setObjectName("connectButton")
        self.connectButton.setEnabled(False)

        self.FlushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.FlushButton.setGeometry(QtCore.QRect(220, 270, 101, 41))
        self.FlushButton.setObjectName("FlushButton")

        self.textBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(360, 260, 131, 61))
        self.textBrowser.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.textBrowser.setAcceptDrops(False)
        self.textBrowser.setAutoFillBackground(True)
        self.textBrowser.setObjectName("textBrowser")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(50, 20, 441, 211))
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.setHorizontalHeaderLabels(['设备名称', '连接状态'])
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        # 只可以选中一整行
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # 只可以选一个
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # 隐藏序号
        self.tableWidget.verticalHeader().setHidden(True)
        # 最后一列自动吸附
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 自适应列宽
        # self.tableWidget.resizeColumnsToContents()
        # 禁止编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 531, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "设备连接"))
        self.connectButton.setText(_translate("MainWindow", "连接"))
        self.FlushButton.setText(_translate("MainWindow", "刷新"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:11.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">连接状态：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><font color=\"red\">无设备连接</font></p></body></html>"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "设备名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "连接状态"))









