
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


class RoundRobinWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Round Robin")
        self.arrival_times = []
        self.burst_times = []
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.labels = [
            "Number of processes:",
            "Arrival times:",
            "Burst times:",
            "Quantum:",
        ]
        self.inputs = [QLineEdit(self) for _ in self.labels]

        for label, input in zip(self.labels, self.inputs):
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(label))
            h_layout.addWidget(input)
            self.layout.addLayout(h_layout)

        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.add_RR)
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
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Process", "Arrival Time", "Burst Time"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )  # Make the table auto adjusted
        self.v_addlayout = QVBoxLayout()
        self.v_addlayout.addWidget(self.table)

        self.addlabels = ["Arrival time:", "Burst time:"]
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
        # Add the process to the table

        self.table.insertRow(row)
        self.table.setItem(
            row, 0, QTableWidgetItem("Process " + str(len(self.burst_times)))
        )
        self.table.setItem(row, 1, QTableWidgetItem(str(arrival_time)))
        self.table.setItem(row, 2, QTableWidgetItem(str(burst_time)))
        # Add the process to the algorithm
        self.arrival_times.append(arrival_time)
        self.burst_times.append(burst_time)

        # Clear the form inputs
        self.addinputs[0].clear()
        self.addinputs[1].clear()

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

    def DecrementLastColumn(self, value, quantum):
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)  # 0 is the index of the first column
            if item is not None and item.text() == value:
                item = self.table.item(i, 2)  # 2 is the index of the last column
                val = int(item.text())
                if val > quantum:
                    item.setText(str(val - quantum))
                else:
                    self.table.removeRow(i)

    def RR(self, n, quantum, live, fig, timer):
        wt = [0] * n
        tat = [0] * n
        rem_bt = [0] * n

        for i in range(n):
            rem_bt[i] = self.burst_times[i]
        t = 0  # Current time
        check = False
        complete = 0
        fig.clear()
        # Plotting
        self.startTimers()
        ax = fig.add_subplot(111)
        while complete != n:
            old_n = n
            n = len(self.burst_times)

            # Update rt to reflect any new processes
            rem_bt += self.burst_times[old_n:n]
            wt += [0] * (n - old_n)
            tat += [0] * (n - old_n)

            for j in range(n):

                if rem_bt[j] > 0 and self.arrival_times[j] <= t:

                    check = True
                    if rem_bt[j] > quantum:
                        if live:
                            fig.canvas.draw()
                            fig.canvas.flush_events()
                            # Create a local event loop
                            loop = QEventLoop()

                            # Start the timer with a delay of bt[i] milliseconds
                            timer.singleShot(quantum * 1000, loop.quit)
                            # Start the event loop
                            loop.exec_()
                        self.DecrementLastColumn("Process " + str(j), quantum)
                        ax.barh(y=1, left=t, width=quantum, height=0.5, alpha=0.5)
                        ax.text(
                            t + (0.5 * quantum),
                            1,
                            s="P" + str(j),
                            ha="left",
                            va="center",
                        )

                        t += quantum
                        rem_bt[j] -= quantum

                    else:
                        if live:
                            fig.canvas.draw()
                            fig.canvas.flush_events()
                            # Create a local event loop
                            loop = QEventLoop()

                            # Start the timer with a delay of bt[i] milliseconds
                            timer.singleShot(quantum * 1000, loop.quit)
                            # Start the event loop
                            loop.exec_()
                        self.DecrementLastColumn("Process " + str(j), quantum)
                        ax.barh(y=1, left=t, width=rem_bt[j], height=0.5, alpha=0.5)
                        ax.text(
                            t + (0.5 * rem_bt[j]),
                            1,
                            s="P" + str(j),
                            ha="left",
                            va="center",
                        )

                        t = t + rem_bt[j]
                        wt[j] = t - self.burst_times[j] - self.arrival_times[j]
                        rem_bt[j] = 0
                        complete += 1
            if check == False:
                t += 1
                continue
            check = False

        for i in range(n):
            tat[i] = self.burst_times[i] + wt[i]

        total_wt = 0
        total_tat = 0
        for i in range(n):
            total_wt = total_wt + wt[i]
            total_tat = total_tat + tat[i]

        AWT = total_wt / n
        ATT = total_tat / n
        # plt.show()
        self.update_timer.stop()
        return AWT, ATT

    def add_RR(self):
        self.resetElapsedTime()
        live = self.live_scheduling_checkbox.isChecked()
        try:
            num_processes = int(self.inputs[0].text())
            quantum = int(self.inputs[3].text())
            if num_processes <= 0:
                raise ValueError("Number of processes must be a positive integer.")
        except ValueError as e:
            self.show_error_message("Invalid Input", str(e))
            return

        try:
            self.arrival_times = list(map(int, self.inputs[1].text().split()))
            self.burst_times = list(map(int, self.inputs[2].text().split()))
        except ValueError:
            self.show_error_message(
                "Invalid Input",
                "Arrival times and burst times must be valid numbers.",
            )
            return

        if (
            len(self.arrival_times) != num_processes
            or len(self.burst_times) != num_processes
        ):
            self.show_error_message(
                "Invalid Input",
                "Please enter arrival and burst times for all processes.",
            )
            return
        self.table.setRowCount(num_processes)
        for i in range(num_processes):
            self.table.setItem(i, 0, QTableWidgetItem("Process " + str(i)))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.arrival_times[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.burst_times[i])))
        avg_waiting_time, avg_turnaround_time = self.RR(
            num_processes, quantum, live, self.figure, self.timer
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
    rr_window = RoundRobinWindow()
    rr_window.show()
    sys.exit(app.exec_())