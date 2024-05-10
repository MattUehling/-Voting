import sys
from PyQt6.QtWidgets import QApplication
from gui_login import Ui_login_page
from gui import Ui_MainWindow
from logic_login import *
from logic import *


class MainApplication(QApplication):
    """This starts up the program"""
    def __init__(self, sys_argv) -> None:
        super().__init__(sys_argv)
        self.login_window = Ui_login_page()
        self.main_window = Ui_MainWindow()

        self.login_logic = Logic_Login()
        self.main_logic = None

        self.login_logic.loginSuccessful.connect(self.showMainWindow)
        self.login_logic.show()

    def showMainWindow(self) -> None:
        """Shows the main voting window"""
        self.login_logic.hide()
        self.main_logic = Logic(self.login_logic)
        self.main_logic.show()
        self.main_logic.additionSuccessful.connect(self.showLoginWindow)

    def showLoginWindow(self) -> None:
        """Shows the login window"""
        self.main_logic.hide()
        self.login_logic.show()


if __name__ == '__main__':
    app = MainApplication(sys.argv)
    sys.exit(app.exec())
