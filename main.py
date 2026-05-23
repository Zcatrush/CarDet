from control import TrafficApp
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TrafficApp()
    win.show()
    sys.exit(app.exec_())