import tkinter as tk
from threading import Thread
import time

def long_running_operation():
    for _ in range(5):  # Simulate a long-running task
        time.sleep(1)  # Simulate time-consuming work
        root.after(0, runningProcess)  # Update GUI from the main thread

def startLoading():
    # Hide tree and labels
    tree.pack_forget()
    labelseller.pack_forget()
    labelcustomer.pack_forget()
    labeldd1.pack_forget()
    labeldd2.pack_forget()

def stopLoading():
    # Show tree and labels
    for lb in process_labels:
        lb.pack_forget()
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    labelseller.pack(side=tk.LEFT, expand=True, fill=tk.X)
    labelcustomer.pack(side=tk.LEFT, expand=True, fill=tk.X)
    labeldd1.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=5)
    labeldd2.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=5)

def run_task():
    startLoading()
    Thread(target=long_running_operation).start()
    root.after(5000, stopLoading)  # Adjust time according to your long-running task duration

def runningProcess():
    process_label = tk.Label(treeframe, text="Processing")
    process_label.pack()
    process_labels.append(process_label)

# Initialize main window
root = tk.Tk()
root.geometry("400x300")

treeframe = tk.Frame(root)
treeframe.pack(fill=tk.BOTH, expand=True)

process_labels = []

tree = tk.Label(treeframe, text="Tree")
labelseller = tk.Label(treeframe, text="Seller")
labelcustomer = tk.Label(treeframe, text="Customer")
labeldd1 = tk.Label(treeframe, text="Dropdown 1")
labeldd2 = tk.Label(treeframe, text="Dropdown 2")

tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
labelseller.pack(side=tk.LEFT, expand=True, fill=tk.X)
labelcustomer.pack(side=tk.LEFT, expand=True, fill=tk.X)
labeldd1.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=5)
labeldd2.pack(side=tk.LEFT, expand=True, fill=tk.X, pady=5)

# Button to start the loading process
start_button = tk.Button(root, text="Start Loading", command=run_task)
start_button.pack(pady=20)

root.mainloop()
