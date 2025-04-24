
from PyQt5 import QtCore, QtGui, QtWidgets
from FCFS_info import FCFSWindow
from SJF_preem_info import SJFPreemptiveWindow
from SJF_non_info import SJFNonPreemptiveWindow
from RR_info import RoundRobinWindow
from priority_preem_info import PriorityPreemptiveWindow
from priority_non_info import PriorityNonPreemptiveWindow


class Ui_first(object):
    def __init__(self):
        self.windows = {}

    def open_window(self, window_name, WindowClass):
        self.windows[window_name] = WindowClass()
        self.windows[window_name].show()

    def setupUi(self, first):
        first.setObjectName("first")
        first.resize(300, 300)
        self.centralwidget = QtWidgets.QWidget(first)
        self.centralwidget.setObjectName("centralwidget")

        grid_layout = QtWidgets.QGridLayout(self.centralwidget)

        buttons = [
            ("FCFS", FCFSWindow),
            ("SJF Preemptive", SJFPreemptiveWindow),
            ("SJF NonPreemptive", SJFNonPreemptiveWindow),
            ("Round Robin", RoundRobinWindow),
            ("Priority Preemptive", PriorityPreemptiveWindow),
            ("Priority NonPreemptive", PriorityNonPreemptiveWindow),
        ]

        for i, (button_text, window_class) in enumerate(buttons):
            button = QtWidgets.QPushButton(button_text)
            button.clicked.connect(
                lambda _, name=button_text, cls=window_class: self.open_window(
                    name, cls
                )
            )
            grid_layout.addWidget(button, i, 0)

        first.setCentralWidget(self.centralwidget)

        self.retranslateUi(first)
        QtCore.QMetaObject.connectSlotsByName(first)

    def retranslateUi(self, first):
        _translate = QtCore.QCoreApplication.translate
        first.setWindowTitle(_translate("first", "CPU Scheduler"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    first = QtWidgets.QMainWindow()
    ui = Ui_first()
    ui.setupUi(first)
    first.show()
    sys.exit(app.exec_())