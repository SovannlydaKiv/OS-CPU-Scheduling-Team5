import csv
import json
from process import Process


def load_from_csv(path):
    procs = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["pid"]
            arrival = int(row["arrival"])
            burst = int(row["burst"])
            priority = int(row.get("priority", 0) or 0)
            procs.append(Process(pid, arrival, burst, priority))
    return procs


def load_from_json(path):
    with open(path) as f:
        data = json.load(f)

    procs = []
    for item in data:
        pid = item["pid"]
        arrival = int(item["arrival"])
        burst = int(item["burst"])
        priority = int(item.get("priority", 0))
        procs.append(Process(pid, arrival, burst, priority))
    return procs


def load_processes(path):
    if path.endswith(".csv"):
        return load_from_csv(path)
    elif path.endswith(".json"):
        return load_from_json(path)
    else:
        raise ValueError("Unsupported file type, use .csv or .json")


def input_from_console():
    procs = []
    n = int(input("Number of processes: "))
    for _ in range(n):
        pid = input("PID: ")
        arrival = int(input("Arrival time: "))
        burst = int(input("Burst time: "))
        priority = input("Priority (optional, press enter to skip): ")
        priority = int(priority) if priority.strip() != "" else 0
        procs.append(Process(pid, arrival, burst, priority))
    return procs