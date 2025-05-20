
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QWidget,
)

import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import QTimer, QEventLoop, QTime


class PriorityNonPreemptiveWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Priority Non Preemptive")
        self.arrival_times = []
        self.burst_times = []
        self.priorities = []
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.labels = [
            "Number of processes:",
            "Arrival times:",
            "Burst times:",
            "Priority numbers:",
        ]
        self.inputs = [QLineEdit(self) for _ in self.labels]

        for label, input in zip(self.labels, self.inputs):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(label))
            h_layout.addWidget(input)
            self.layout.addLayout(h_layout)

        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.calculate_priority_non)
        self.layout.addWidget(self.generate_button)
        # Create a QHBoxLayout
        self.horizontal_layout = QHBoxLayout()

        # Create a QLabel to show the elapsed time
        self.elapsed_time_label = QLabel("Elapsed time: 0 seconds", self)

        # Create a QCheckBox for live scheduling
        self.live_scheduling_checkbox = QCheckBox("Live scheduling", self)

        self.horizontal_layout.addWidget(self.live_scheduling_checkbox)
        self.horizontal_layout.addWidget(self.elapsed_time_label)
        # Add the horizontal layout to the main layout
        self.layout.addLayout(self.horizontal_layout)

        self.avg_labels = ["Average waiting time:", "Average turn around time:"]
        self.avg_outputs = [QLineEdit(self) for _ in self.avg_labels]
        for output in self.avg_outputs:
            output.setReadOnly(True)

        for label, output in zip(self.avg_labels, self.avg_outputs):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(label))
            h_layout.addWidget(output)
            self.layout.addLayout(h_layout)

        # Create a figure and a canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Create a QTableWidget for displaying the burst times
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Process", "Arrival Time", "Burst Time", "Priority"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )  # Make the table auto adjusted
        self.v_addlayout = QVBoxLayout()
        self.v_addlayout.addWidget(self.table)

        self.addlabels = ["Arrival time:", "Burst time:", "Priority number:"]
        self.addinputs = [QLineEdit(self) for _ in self.addlabels]

        for label, input in zip(self.addlabels, self.addinputs):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(label))
            h_layout.addWidget(input)
            self.v_addlayout.addLayout(h_layout)

        self.add_process_button = QPushButton("Add Process", self)
        self.v_addlayout.addWidget(self.add_process_button)
        self.add_process_button.clicked.connect(self.add_process)
        v_addlayout_widget = QWidget()
        v_addlayout_widget.setLayout(self.v_addlayout)

        # Add the new widget to self.table_canvas_layout

        # Create a QHBoxLayout for the table and the canvas
        self.table_canvas_layout = QHBoxLayout()
        self.table_canvas_layout.addWidget(v_addlayout_widget)
        self.table_canvas_layout.addWidget(self.canvas)
        self.layout.addLayout(
            self.table_canvas_layout
        )  # Add the QHBoxLayout to the main layout

        # Add a navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)
        # Create a QTimer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.updateElapsedTime)
        self.timer = QTimer()
        self.total_elapsed_time = 0

    def add_process(self):
        # Get the process details from the form inputs
        row = self.table.rowCount()
        arrival_time = int(self.addinputs[0].text())
        burst_time = int(self.addinputs[1].text())
        priority = int(self.addinputs[2].text())
        # Add the process to the table

        self.table.insertRow(row)
        self.table.setItem(
            row, 0, QTableWidgetItem("Process " + str(len(self.burst_times)))
        )
        self.table.setItem(row, 1, QTableWidgetItem(str(arrival_time)))
        self.table.setItem(row, 2, QTableWidgetItem(str(burst_time)))
        self.table.setItem(row, 3, QTableWidgetItem(str(priority)))
        # Add the process to the algorithm
        self.arrival_times.append(arrival_time)
        self.burst_times.append(burst_time)
        self.priorities.append(priority)

        # Clear the form inputs
        self.addinputs[0].clear()
        self.addinputs[1].clear()
        self.addinputs[2].clear()

    def startTimers(self):
        # Start the update timer with a 1 second interval
        self.update_timer.start(1000)

        # Start the FCFS timer
        self.timer.start()

    def updateElapsedTime(self):
        # Add seconds to the total elapsed time
        self.total_elapsed_time += 1
        # Update the elapsed time label
        self.elapsed_time_label.setText(
            f"Elapsed time: {self.total_elapsed_time} seconds"
        )

    def resetElapsedTime(self):
        # Update the elapsed time label
        self.total_elapsed_time = 0
        self.elapsed_time_label.setText("Elapsed time: 0 seconds")

    def removeRowByValue(self, value):
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).text() == value:
                self.table.removeRow(i)
                break

    def Prioritynon(self, n, live, fig, timer):
        wt = [0] * n
        tat = [0] * n

        complete = 0
        t = 0
        prior = 99999999
        first = 0
        check = False
        fig.clear()
        # Plotting
        self.startTimers()
        ax = fig.add_subplot(111)
        while complete != n:
            old_n = n
            n = len(self.burst_times)

            # Update rt to reflect any new processes
            wt += [0] * (n - old_n)
            tat += [0] * (n - old_n)
            for j in range(n):
                if (self.arrival_times[j] <= t) and (self.priorities[j] <= prior):

                    if self.priorities[j] == prior:
                        if self.arrival_times[j] > self.arrival_times[first]:
                            continue

                    prior = self.priorities[j]
                    first = j
                    check = True
            if check == False:
                t += 1
                continue

            self.priorities[first] = 999999999

            prior = 99999999
            if live:
                fig.canvas.draw()
                fig.canvas.flush_events()
                # Create a local event loop
                loop = QEventLoop()

                # Start the timer with a delay of bt[i] milliseconds
                timer.singleShot(self.burst_times[first] * 1000, loop.quit)
                # Start the event loop
                loop.exec_()
            self.removeRowByValue("Process " + str(first))
            ax.barh(y=1, left=t, width=self.burst_times[first], height=0.5, alpha=0.5)
            ax.text(
                t + (0.5 * self.burst_times[first]),
                1,
                s="P" + str(first),
                ha="left",
                va="center",
            )

            complete += 1
            check = False
            t += self.burst_times[first]

            wt[first] = t - self.burst_times[first] - self.arrival_times[first]

            if wt[first] < 0:
                wt[first] = 0

        for i in range(n):
            tat[i] = self.burst_times[i] + wt[i]
        total_wt = 0
        total_tat = 0
        for i in range(n):
            total_wt = total_wt + wt[i]
            total_tat = total_tat + tat[i]

        awt = total_wt / n
        att = total_tat / n
        # plt.show()
        self.update_timer.stop()
        return att, awt

    def calculate_priority_non(self):
        self.resetElapsedTime()
        live = self.live_scheduling_checkbox.isChecked()
        try:
            num_processes = int(self.inputs[0].text())
            if num_processes <= 0:
                raise ValueError("Number of processes must be a positive integer.")
        except ValueError as e:
            self.show_error_message("Invalid Input", str(e))
            return

        try:
            self.arrival_times = list(map(int, self.inputs[1].text().split()))
            self.burst_times = list(map(int, self.inputs[2].text().split()))
            self.priorities = list(map(int, self.inputs[3].text().split()))
        except ValueError:
            self.show_error_message(
                "Invalid Input",
                "Arrival times, burst times, and priorities must be valid numbers.",
            )
            return

        if (
            len(self.arrival_times) != num_processes
            or len(self.burst_times) != num_processes
            or len(self.priorities) != num_processes
        ):
            self.show_error_message(
                "Invalid Input",
                "Please enter arrival, burst times, and priorities for all processes.",
            )
            return
        self.table.setRowCount(num_processes)
        for i in range(num_processes):
            self.table.setItem(i, 0, QTableWidgetItem("Process " + str(i)))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.arrival_times[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.burst_times[i])))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.priorities[i])))
        avg_waiting_time, avg_turnaround_time = self.Prioritynon(
            num_processes, live, self.figure, self.timer
        )
        self.canvas.draw()
        self.avg_outputs[0].setText(str(avg_waiting_time))
        self.avg_outputs[1].setText(str(avg_turnaround_time))

    def show_error_message(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    priority_non_window = PriorityNonPreemptiveWindow()
    priority_non_window.show()
    sys.exit(app.exec_())
