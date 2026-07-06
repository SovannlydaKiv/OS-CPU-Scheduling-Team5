import copy
from process import Process
from input_parser import load_processes, input_from_console
from gantt import print_gantt
from metrics import print_metrics, get_averages

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.srt import srt_scheduling
from algorithms.rr import round_robin
from algorithms.mlfq import run_mlfq


SAMPLE_PROCESSES = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 8),
    Process("P4", 3, 6),
]


def get_input_processes():
    print("\nProcess Input")
    print("1. Use sample scenario (P1-P4)")
    print("2. Load from CSV file")
    print("3. Load from JSON file")
    print("4. Enter manually via console")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        return copy.deepcopy(SAMPLE_PROCESSES)
    elif choice == "2":
        path = input("Enter CSV file path: ").strip()
        return load_processes(path)
    elif choice == "3":
        path = input("Enter JSON file path: ").strip()
        return load_processes(path)
    elif choice == "4":
        return input_from_console()
    else:
        print("Invalid choice, using sample scenario.")
        return copy.deepcopy(SAMPLE_PROCESSES)


def run_fcfs(processes):
    return fcfs(processes)


def run_sjf(processes):
    return sjf(processes)


def run_srt(processes):
    return srt_scheduling(processes)


def run_rr(processes):
    quantum_input = input("Enter time quantum (default 2): ").strip()
    quantum = int(quantum_input) if quantum_input else 2
    procs, gantt = round_robin(processes, quantum=quantum)
    return gantt, procs


def run_mlfq_wrapper(processes):
    q1_input = input("Queue 1 quantum (default 2): ").strip()
    q2_input = input("Queue 2 quantum (default 4): ").strip()
    aging_input = input("Aging threshold (default 10): ").strip()

    q1 = int(q1_input) if q1_input else 2
    q2 = int(q2_input) if q2_input else 4
    aging = int(aging_input) if aging_input else 10

    fresh_processes = copy.deepcopy(processes)
    gantt, procs = run_mlfq(fresh_processes, q1_quantum=q1, q2_quantum=q2, aging_threshold=aging)
    return gantt, procs


ALGORITHMS = {
    "1": ("FCFS", run_fcfs),
    "2": ("SJF (Non-preemptive)", run_sjf),
    "3": ("SRT (Preemptive)", run_srt),
    "4": ("Round Robin", run_rr),
    "5": ("MLFQ", run_mlfq_wrapper),
}


def run_single_algorithm(processes):
    print("\nSelect Algorithm")
    for key, (name, _) in ALGORITHMS.items():
        print(f"{key}. {name}")
    choice = input("Choice: ").strip()

    if choice not in ALGORITHMS:
        print("Invalid choice.")
        return

    name, func = ALGORITHMS[choice]
    segments, procs = func(copy.deepcopy(processes))

    print(f"\n--- {name} ---")
    print_gantt(segments)
    print()
    print_metrics(procs)


def run_comparison(processes):
    print("\nRunning all algorithms with default settings for comparison...\n")
    results = {}

    for key, (name, func) in ALGORITHMS.items():
        if name in ("Round Robin", "MLFQ"):
            fresh = copy.deepcopy(processes)
            if name == "Round Robin":
                procs, gantt = round_robin(fresh, quantum=2)
            else:
                gantt, procs = run_mlfq(fresh, q1_quantum=2, q2_quantum=4, aging_threshold=10)
        else:
            gantt, procs = func(copy.deepcopy(processes))

        results[name] = get_averages(procs)

    print(f"{'Algorithm':<20}{'Avg Waiting':<15}{'Avg Turnaround':<18}{'Avg Response':<15}")
    for name, avg in results.items():
        print(f"{name:<20}{avg['avg_waiting']:<15.2f}{avg['avg_turnaround']:<18.2f}{avg['avg_response']:<15.2f}")


def main():
    print("CPU Scheduling Algorithm Simulator")
    processes = get_input_processes()

    while True:
        print("\nMain Menu")
        print("1. Run a single algorithm")
        print("2. Compare all algorithms (default settings)")
        print("3. Load new processes")
        print("4. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            run_single_algorithm(processes)
        elif choice == "2":
            run_comparison(processes)
        elif choice == "3":
            processes = get_input_processes()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()