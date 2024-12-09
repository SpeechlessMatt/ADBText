import os.path
from time import sleep
from PyQt6.QtCore import QThread, pyqtSignal, QCoreApplication, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMessageBox, QAbstractButton
from ConnectionUI import ConnectionUi
from MainWindows import Ui_MainWindow
from confirm import ConfirmUi
from loguru import logger
import adbs
import sys

logger.add("Adbtext.log", rotation="10 MB", level="TRACE")


# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if not os.path.exists("res") and os.path.exists("platform-tools"):
    # 修改当前工作目录，使得资源文件可以被正确访问
    cd = source_path('')
    os.chdir(cd)

logger.debug(os.getcwd())

class CheckIsInstall(QThread):
    status_code = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            ret = adbs.check_installed("com.android.adbkeyboard")
            self.msleep(3)
            if ret:
                self.status_code.emit(ret)
                break

class ConfirmWidget(QWidget):
    def __init__(self, check=CheckIsInstall()):
        super().__init__()
        self.ui = ConfirmUi()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        # 建议实例化的时候传入
        self.check_installed = check
        self.is_confirm = False

        self.create_connection()

    def create_connection(self):
        self.ui.pushButton.clicked.connect(self.cancel)
        self.ui.pushButton_2.clicked.connect(self.confirm)
        self.check_installed.status_code.connect(self.is_finish_install)

    def open_(self):
        self.show()

    def cancel(self):
        self.close()

    def confirm(self):
        _translate = QCoreApplication.translate
        self.ui.textBrowser.setText(_translate("Form", "* 正在安装 ADBKeyBoard.apk..."))
        QApplication.processEvents()
        try:
            adbs.adb_install("res/ADBKeyboard.apk")
            self.check_installed.run()
        except Exception as e:
            logger.warning(e)
            self.ui.textBrowser.append(_translate("Form", "安装失败，未知原因"))
            QApplication.processEvents()

    # 接收检测信号
    def is_finish_install(self, status_code):
        _translate = QCoreApplication.translate
        if status_code:
            logger.debug("已经安装 adbkeyboard.apk")
            self.ui.textBrowser.append(_translate("Form", "安装成功！！"))
            QApplication.processEvents()
            sleep(1)
            self.is_confirm = True
            self.close()
        else:
            logger.debug("未安装 或 未知原因")
            self.ui.textBrowser.append(_translate("Form", "安装失败，未知原因"))
            QApplication.processEvents()


class Main(QMainWindow):
    closing = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.device = "None"
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.check_installed = CheckIsInstall()
        self.confirm = ConfirmWidget(check=self.check_installed)
        self.create_connections()


    def open_(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", f"ADBText工具  --设备：{self.device}"))
        self.init_adb()
        self.show()

    # 设置连接器
    def create_connections(self):
        self.ui.pushButton_2.clicked.connect(self.clear_text)
        self.ui.pushButton.clicked.connect(self.upload_text)
        self.ui.actiondelete.triggered.connect(self.delete_apk)
        self.ui.actionexit.triggered.connect(self.exit_)
        self.check_installed.status_code.connect(self.is_finish_install)
        # 信号与槽
        self.closing.connect(self.on_closing)

    def closeEvent(self, event):
        self.closing.emit()
        event.accept()

    def on_closing(self):
        logger.debug("The window is closing!")
        if os.path.exists("./adbtext.conf"):
            with open("./adbtext.conf") as file:
                ime = file.read()
                logger.debug(ime)
                adbs.set_ime(ime)

    def init_adb(self):
        if not adbs.check_installed("com.android.adbkeyboard"):
            self.confirm.show()
            if not self.confirm.is_confirm:
                return 0
            # adbs.adb_install("ADBKeyboard.apk")
        # 菜单开
        self.ui.actiondelete.setEnabled(True)
        i = adbs.check_using_ime()
        if not i == "com.android.adbkeyboard/.AdbIME":
            with open("adbtext.conf", "w") as file:
                file.write(i)
        adbs.enable_ime("com.android.adbkeyboard/.AdbIME")
        adbs.set_ime("com.android.adbkeyboard/.AdbIME")

    # 接收检测信号
    def is_finish_install(self, status_code):
        if status_code:
            self.ui.actiondelete.setEnabled(True)
        else:
            self.ui.actiondelete.setEnabled(False)

    def clear_text(self):
        logger.trace("清除")
        self.ui.textEdit.clear()

    def upload_text(self):
        self.init_adb()
        text = self.ui.textEdit.toPlainText()
        adbs.send_text(text)

    def delete_apk(self):
        ret = adbs.uninstall("com.android.adbkeyboard")
        if ret:
            self.inited = 0
            QMessageBox.information(self, "已删除ADBKeyboard", "删除成功！")
        else:
            QMessageBox.information(self, "已删除ADBKeyboard", "ADBKeyBoard 已经被删除")

    def exit_(self):
        self.close()


class ConnectionWindow(QMainWindow):
    def __init__(self, main_window_: QMainWindow=None):
        super().__init__()
        # main window
        self.main_window = main_window_
        self.ui = ConnectionUi()
        self.ui.setupUi(self)
        self.create_connection()

    def create_connection(self):
        self.ui.FlushButton.clicked.connect(self.flush_list)
        self.ui.connectButton.clicked.connect(self.select_list)

    # select list
    def select_list(self):
        selected_obj = self.ui.tableWidget.selectedIndexes()
        row = 0
        if len(selected_obj) == 0:
            return 0
        for i in selected_obj:
            row = i.row()
        logger.info(f"选择多少行: {row}")
        device = self.ui.tableWidget.item(row, 0).text()
        logger.info(f"设备名称: {device}")
        if main_window is not None:
            main_window.device = device
            main_window.open_()
        self.close()

    def flush_list(self):
        _translate = QCoreApplication.translate
        if adbs.check_device():
            devices = adbs.get_devices()
            devices_name = []

            for i in devices:
                devices_name.append(i.split('\t')[0])
            logger.info(f"devices: {devices}")

            self.ui.tableWidget.setRowCount(len(devices))
            self.ui.connectButton.setEnabled(True)

            for i, device in enumerate(devices_name):
                row = int(i)
                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(device))
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem("连接成功"))

            # 已有设备
            self.ui.textBrowser.setHtml(_translate("MainWindow",
                                                   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "hr { height: 1px; border-width: 0; }\n"
                                                   "li.unchecked::marker { content: \"\\2610\"; }\n"
                                                   "li.checked::marker { content: \"\\2612\"; }\n"
                                                   "</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:11.25pt; font-weight:400; font-style:normal;\">\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">连接状态：</p>\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><font color=\"green\">已连接</font></p></body></html>"))
        else:
            self.ui.connectButton.setEnabled(False)
            self.ui.textBrowser.setHtml(_translate("MainWindow",
                                                   "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "hr { height: 1px; border-width: 0; }\n"
                                                   "li.unchecked::marker { content: \"\\2610\"; }\n"
                                                   "li.checked::marker { content: \"\\2612\"; }\n"
                                                   "</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:11.25pt; font-weight:400; font-style:normal;\">\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">连接状态：</p>\n"
                                                   "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><font color=\"red\">无设备连接</font></p></body></html>"))



if __name__ == '__main__':
    # 实例化，传参
    app = QApplication(sys.argv)
    main_window = Main()
    connection_window = ConnectionWindow(main_window)
    connection_window.show()
    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec())
