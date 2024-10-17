# Branch Predictor Simulator

## Overview
The Branch Predictor Simulator is a Python-based simulation tool to evaluate the performance of different branch prediction algorithms. This README will guide you through the steps needed to run the simulator, generate branch traces, and understand the workings of each branch predictor implemented. This simulator helps to gain insights into branch prediction mechanisms used in modern computer architecture, suitable for educational purposes.

## Features
- Implements six branch predictors:
  1. **Static Predictors** (Always Taken, Always Not Taken)
  2. **One-Bit Branch Predictor**
  3. **Two-Bit Branch Predictor**
  4. **Bimodal Branch Predictor**
  5. **GShare Branch Predictor**
  6. **Hybrid Branch Predictor** (GShare + Bimodal)
- Generates branch traces with a configurable number of branches.
- Provides detailed logs and visualization of prediction accuracy.

## Running the Simulator
The process of running the simulator involves the following steps:

### 1. Generating the Branch Trace
The `branch_trace_generator.py` script generates synthetic branch traces that are used by the simulator to evaluate each branch predictor. To generate a branch trace, you can use the command below:

```sh
python branch_trace_generator.py --branches <number_of_branches> --seed <random_seed>
```

- `--branches` (optional): Specifies the number of branches to generate. Default is 10,000.
- `--seed` (compulsory): Specifies the random seed as your PSU ID for reproducibility.

The generated trace is stored in a file called `branch_trace.csv` and contains two columns:
- **BranchAddress**: The address of the branch instruction.
- **Outcome**: The actual outcome (taken or not taken).

### 2. Running the Branch Predictor Simulator
Once the trace file has been generated, you can run the main simulator using the `main_simulator.py` script.

```sh
python main_simulator.py --visualize --x <interval_length> --fast
```

- `--visualize` (optional): Enables real-time plotting of prediction accuracy for each predictor.
- `--x` (optional): Specifies the number of branches for calculating interval-based accuracy (default is 10).
- `--fast` (optional): Skips the 2-second pause between intervals, making the simulation run faster.

The simulator reads the `branch_trace.csv` file and runs each of the implemented branch predictors, providing cumulative accuracy statistics during and after the simulation.

## Logs and Output Data
### Real-Time Statistics
The simulator logs real-time statistics in a file named `realtime_stats.txt`. This file contains cumulative accuracy information for each branch predictor during the simulation, formatted as follows:

```
Predictor, Branches Processed, Cumulative Accuracy (%)
```

### Predictor-Specific Logs
Each predictor generates a detailed log of predictions during the simulation. These logs are stored in the `logs` directory, with one file per predictor, e.g., `logs/One_Bit_log.txt`. Each file contains information in the format:

```
Branch: <branch_number>, Correct: <0_or_1>
```

### Branch History Table (BHT) Logs
The simulator also saves the state of the Branch History Table (BHT) for applicable predictors in the `bht_logs` directory. Each predictor's BHT log provides insight into the internal state of the predictor after the simulation.

## Visualization and Analysis
The simulator includes an option to visualize the prediction accuracy over time. If the `--visualize` flag is used, the simulator will produce an interactive plot that displays the prediction accuracy of each predictor as the number of branches processed increases. Additionally, you can inspect the generated log files to plot the data using external tools like Python, MATLAB, or spreadsheet software for more detailed analysis.

## Branch Predictors Explained
### 1. Static Predictors
- **Static Taken / Not Taken**: These predictors always predict the branch will be taken (or not taken). No learning occurs.

### 2. One-Bit Branch Predictor
- Maintains a **Branch History Table (BHT)** that stores a single bit for each branch address. This bit represents whether the branch was previously taken or not. The predictor simply repeats the last outcome.

### 3. Two-Bit Branch Predictor
- Utilizes a **two-bit saturating counter** for each branch address. The counter ranges from `00` (strongly not taken) to `11` (strongly taken). Prediction is considered taken if the counter value is `10` or higher. The counter is incremented or decremented based on the actual outcome.

### 4. Bimodal Branch Predictor
- Uses a fixed-size **BHT** indexed by the lower bits of the branch address. Each entry in the BHT has a two-bit counter similar to the Two-Bit Predictor. The prediction accuracy is improved by reducing aliasing in the prediction table.

### 5. GShare Branch Predictor
- Employs **global branch history** to determine prediction outcomes. It XORs the global history register with the branch address to generate an index into the BHT. This approach helps to correlate predictions across different branches.

### 6. Hybrid Branch Predictor
- Combines the **GShare** and **Bimodal** predictors. A **choice table** determines which predictor (GShare or Bimodal) should be trusted for each branch. The choice table is updated to improve the accuracy of prediction based on which predictor was correct for each branch.

## Directory Structure
The simulator organizes its files and logs as follows:
```
.
├── branch_predictors.py          # Branch predictor implementations
├── branch_trace_generator.py     # Generates branch trace files
├── main_simulator.py             # Main branch predictor simulator
├── branch_trace.csv              # Generated branch trace file
├── logs/                         # Logs for each branch predictor
│   ├── One_Bit_log.txt           # Detailed logs for the One-Bit predictor
│   └── ...
├── bht_logs/                     # Logs for BHT states
│   ├── GShare_bht.txt            # GShare BHT state
│   └── ...
└── realtime_stats.txt            # Real-time statistics log
```

## Requirements
- Python 3.x
- `matplotlib` for visualization
- `tabulate` for tabular progress display

To install the dependencies, run:
```sh
pip install matplotlib tabulate
```

Feel free to explore the logs, visualize the results, and modify the predictor implementations for experimental learning.


