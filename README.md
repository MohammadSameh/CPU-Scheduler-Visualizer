# OS CPU Scheduler Visualizer

This project is a **CPU Scheduling Visualizer** built with **Python** and **PyQt5**. It supports multiple CPU scheduling algorithms such as **FCFS**, **SJF (Preemptive and Non-Preemptive)**, **Priority (Preemptive and Non-Preemptive)**, and **Round Robin**.

The application provides a **real-time simulation** of scheduling algorithms, allowing users to visualize the **Gantt chart** of process execution and view performance metrics like **Average Waiting Time** and **Average Turnaround Time**.

---

## **Project Features**

1. **Multiple Scheduling Algorithms**:
   - **FCFS** (First-Come First-Served)
   - **SJF** (Shortest Job First) – Preemptive and Non-Preemptive
   - **Priority Scheduling** – Preemptive and Non-Preemptive
   - **Round Robin**

2. **Live Scheduling Visualization**:
   - Gantt chart showing the order and execution times of processes.
   - Dynamic **live updates** of **remaining burst time** during scheduling.
   - **Real-time updates** on waiting time and turnaround time.

3. **Interactive GUI**:
   - Built using **PyQt5**, allowing users to input processes and visualize results in a user-friendly way.
   - Add new processes **dynamically** while the scheduler is running.

---

## **How to Run the Project**

### **Running the Executable**

1. Download the executable from the **\dist** folder (for Windows):
   - Go to the `\dist` directory after the build.
   - The executable file will be named something like `CPUScheduler.exe`.

2. **Run the executable**:
   - Double-click `CPUScheduler.exe` to launch the application.
   - The application window will open, showing a **main menu** with buttons for each scheduler type.

---

## **Using the Application**

### **Step-by-Step Guide**

#### 1. **Selecting the Scheduler Type**

- Upon opening the application, you'll see a window with **buttons** for each CPU scheduling algorithm:
  - **FCFS (First-Come First-Served)**
  - **SJF (Preemptive and Non-Preemptive)**
  - **Priority Scheduling (Preemptive and Non-Preemptive)**
  - **Round Robin**
  
- **Click on the desired scheduler** to open the input form.

#### 2. **Entering Process Information**

- **Number of processes**: Enter the number of processes you want to simulate.
- **Arrival times**: Enter the arrival times for each process (space-separated values).
- **Burst times**: Enter the burst times for each process.
- **Priority numbers** (if applicable): Enter the priority for each process (lower number means higher priority).
- **Quantum** (for Round Robin only): Enter the quantum time for process rotation.

Example for **Round Robin**:
- Number of processes: 3
- Arrival times: `0 2 4`
- Burst times: `5 6 4`
- Quantum: `2`

#### 3. **Start the Scheduling Process**

- After entering the necessary information, click the **Generate** button to run the scheduler.
- The program will **start scheduling** the processes and display the results:
  - **Gantt chart** showing the order and time taken by each process.
  - **Average waiting time** and **average turnaround time** at the bottom of the window.
  - **Remaining burst time table** updating dynamically as time progresses.

#### 4. **Live Scheduling (Optional)**

- To enable **live scheduling**, check the **"Live Scheduling"** checkbox before clicking **Generate**.
- When **live scheduling is enabled**, the following will occur:
  - The scheduler will **run in real-time**, updating the Gantt chart and remaining burst times every second.
  - The **waiting time** and **turnaround time** will update live as processes are executed.

#### 5. **Adding New Processes Dynamically**

- While the scheduler is running, you can **add new processes**:
  - Simply click on the **"Add Process"** button, and input the arrival time, burst time, and priority number.
  - The new process will be added to the queue and handled by the scheduler.
  
---

## **Expected Output**

- After the scheduler finishes running, you’ll see:
  - A **Gantt chart** displaying the processes and their execution times.
  - **Average Waiting Time** and **Average Turnaround Time**.
  - A **remaining burst time table** that shows the current burst time left for each process.

### **Example Output for Round Robin**

- **Gantt Chart**: The Gantt chart should show processes in the order they are executed with their burst times. For instance:
  ```
  [P1:0-2] [P2:2-4] [P3:4-6] [P1:6-8] [P2:8-10] [P3:10-12]
  ```

- **Average Waiting Time**: `3.5 seconds`
- **Average Turnaround Time**: `6.25 seconds`

---

## **Building the Executable**

To create the executable (`.exe`) file for distribution:
1. Install **PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. From the root directory of your project, run the following command to create the executable:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

3. After the build process completes, you’ll find the executable in the **`dist`** folder.

---

## **Troubleshooting**

- **Missing Dependencies**: Ensure that all dependencies (like `PyQt5`, `matplotlib`) are installed in your environment. You can install them with:
  ```bash
  pip install PyQt5 matplotlib
  ```

- **Executable Not Working**: If the executable doesn’t run, try building it again with the `--windowed` flag to avoid opening a command prompt window alongside the GUI.

---

## **Team Members**

This project was developed by the following team members:

- **Mohamed Sameh Mohamed** – 2100678
- **Jan Farag Hanna** – 2001814
- **Ahmed Tarek Sayed** – 2002327
- **Ahmed Abdelsamad Ahmed** – 2101945
- **Hussam elsayed mohamed** - 2101852
- **Abdelrahman Ashour Hassan** - 2101736

---
