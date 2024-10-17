# Main Branch Predictor Simulator (Enhanced with Tabular Visualization and Detailed Logging)
import csv
import time
import sys
import os
import argparse
from branch_predictors import StaticPredictor, OneBitBranchPredictor, TwoBitBranchPredictor, BimodalBranchPredictor, GShareBranchPredictor, HybridBranchPredictor
from branch_trace_generator import BranchTraceGenerator
import matplotlib.pyplot as plt
from tabulate import tabulate
import time

class BranchPredictorSimulator:
    def __init__(self, trace_file="branch_trace.csv", visualize=False, x=10, fast=False):
        self.trace_file = trace_file
        self.visualize = visualize
        self.x = x  # Number of instructions for accuracy calculation
        self.fast = fast  # Skip pauses if fast mode is enabled
        self.predictors = {
            "Static Taken": StaticPredictor(always_taken=True),
            "Static Not Taken": StaticPredictor(always_taken=False),
            "One Bit": OneBitBranchPredictor(),
            "Two Bit": TwoBitBranchPredictor(),
            "Bimodal": BimodalBranchPredictor(),
            "GShare": GShareBranchPredictor(),
            "Hybrid": HybridBranchPredictor()
        }
        self.stats = {name: [] for name in self.predictors}
        self.realtime_log_file = "realtime_stats.txt"
        if not os.path.exists("logs"):
            os.makedirs("logs")
        with open(self.realtime_log_file, 'w') as f:
            f.write("Predictor, Branches Processed, Cumulative Accuracy (%)\n")

    def run_simulation(self):
        with open(self.trace_file, 'r') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader):
                address = int(row['BranchAddress'])
                outcome = int(row['Outcome'])
                for name, predictor in self.predictors.items():
                    prediction = predictor.predict(address)
                    correct = 1 if prediction == outcome else 0
                    predictor.update(address, outcome)
                    self.stats[name].append(correct)
                    self.log_statistics(name, row_num + 1, correct)
                if (row_num + 1) % self.x == 0:
                    self.display_progress(row_num + 1, address)
                    if not self.fast:
                        time.sleep(2)  # Pause for 2 seconds after every x instructions
                if self.visualize:
                    self.visualize_statistics()
        self.save_bht()
        self.display_final_accuracy()

    def log_statistics(self, predictor_name, branch_num, correct):
        log_file = f"logs/{predictor_name}_log.txt"
        with open(log_file, 'a') as f:
            f.write(f"Branch: {branch_num}, Correct: {correct}\n")

    def visualize_statistics(self):
        plt.figure(figsize=(10, 6))
        for name, results in self.stats.items():
            accuracy = [sum(results[:i+1]) / (i+1) * 100 for i in range(len(results))]
            plt.plot(accuracy, label=name)
        plt.xlabel('Number of Branches')
        plt.ylabel('Prediction Accuracy (%)')
        plt.title('Branch Predictor Accuracy Over Time')
        plt.legend()
        plt.pause(0.05)
        plt.clf()

    def display_progress(self, branches_processed, current_address):
        table_data = []
        for name, results in self.stats.items():
            cumulative_accuracy = (sum(results) / len(results)) * 100 if results else 0.0
            table_data.append([name, branches_processed, cumulative_accuracy])
        headers = ["Predictor", "Branches Processed", "Cumulative Accuracy (%)"]
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Processing Branch Address: {current_address}")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        with open(self.realtime_log_file, 'a') as f:
            for row in table_data:
                f.write(f"{row[0]}, {row[1]}, {row[2]}\n")

    def save_bht(self):
        if not os.path.exists("bht_logs"):
            os.makedirs("bht_logs")
        for name, predictor in self.predictors.items():
            if hasattr(predictor, 'bht'):
                bht_file = f"bht_logs/{name}_bht.txt"
                with open(bht_file, 'w') as f:
                    if isinstance(predictor.bht, dict):
                        for address, value in predictor.bht.items():
                            f.write(f"Address: {address}, Value: {value}\n")
                    elif isinstance(predictor.bht, list):
                        for index, value in enumerate(predictor.bht):
                            f.write(f"Index: {index}, Value: {value}\n")

    def display_final_accuracy(self):
        table_data = []
        for name, results in self.stats.items():
            total_branches = len(results)
            accuracy = (sum(results) / total_branches) * 100 if total_branches > 0 else 0.0
            table_data.append([name, total_branches, accuracy])
        headers = ["Predictor", "Total Branches Processed", "Overall Accuracy (%)"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Branch Predictor Simulator")
    parser.add_argument("--visualize", action="store_true", help="Enable interactive plotting of accuracy")
    parser.add_argument("--x", type=int, default=10, help="Number of instructions for per-interval accuracy calculation")
    parser.add_argument("--fast", action="store_true", help="Skip pauses and run the simulation quickly")
    args = parser.parse_args()

    BranchTraceGenerator.generate_trace()  # Generate a branch trace file
    simulator = BranchPredictorSimulator(visualize=args.visualize, x=args.x, fast=args.fast)

    if args.visualize:
        plt.ion()  # Turn on interactive plotting
    simulator.run_simulation()
    if args.visualize:
        plt.ioff()  # Turn off interactive plotting
        plt.show()  # Show final plot

