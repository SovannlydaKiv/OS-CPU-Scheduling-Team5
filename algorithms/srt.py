"""
algorithms/srt.py

Shortest Remaining Time (SRT) Scheduling Algorithm
Preemptive version of Shortest Job First (SJF).

At every time unit, the scheduler checks if a newly arrived process
has less remaining burst time than the currently running process.
If so, the running process is preempted.
"""

import copy
from process import Process  # works if you run "python main.py" from the project root


def srt_scheduling(processes):
    """
    Simulates SRT scheduling.

    Args:
        processes (list[Process]): unscheduled list of Process objects

    Returns:
        gantt_chart (list[tuple]): list of (pid, start_time, end_time) segments
        scheduled_processes (list[Process]): same processes, with
            start_time, completion_time, waiting_time, turnaround_time,
            and response_time filled in
    """
    # Work on deep copies so the original list passed in isn't mutated
    procs = copy.deepcopy(processes)
    arrivals = sorted(procs, key=lambda p: p.arrival)
    n = len(arrivals)

    time = 0
    completed = 0
    arrival_index = 0
    ready_queue = []
    running = None

    gantt_chart = []
    current_segment_pid = "IDLE"
    current_segment_start = 0

    while completed < n:
        # 1. Bring in any processes that have arrived by this tick
        while arrival_index < n and arrivals[arrival_index].arrival <= time:
            ready_queue.append(arrivals[arrival_index])
            arrival_index += 1

        # 2. Pool of candidates = ready queue + whatever is currently running
        candidates = ready_queue + ([running] if running else [])

        # 3. Pick the process with the smallest remaining time
        #    (ties broken by arrival time, then pid, for determinism)
        next_process = min(candidates, key=lambda p: (p.remaining, p.arrival, p.pid)) if candidates else None

        # 4. Context switch / preemption check
        if next_process != running:
            # Close off the previous Gantt segment (skip zero-length ones)
            if time > current_segment_start:
                gantt_chart.append((current_segment_pid, current_segment_start, time))

            if next_process is not None and next_process in ready_queue:
                ready_queue.remove(next_process)

            # If the old process wasn't finished, it goes back into the ready queue
            if running is not None and running.remaining > 0 and running != next_process:
                ready_queue.append(running)

            running = next_process
            current_segment_pid = running.pid if running else "IDLE"
            current_segment_start = time

        # 5. Execute one tick (or idle)
        if running is None:
            time += 1
            continue

        if running.start_time is None:
            running.start_time = time
            running.response_time = running.start_time - running.arrival

        running.remaining -= 1
        time += 1

        # 6. Completion check
        if running.remaining == 0:
            running.completion_time = time
            running.turnaround_time = running.completion_time - running.arrival
            running.waiting_time = running.turnaround_time - running.burst
            completed += 1
            running = None

    # Close the final segment
    if time > current_segment_start:
        gantt_chart.append((current_segment_pid, current_segment_start, time))

    return gantt_chart, arrivals


# Quick standalone test using your project's sample scenario
if __name__ == "__main__":
    test_processes = [
        Process("P1", arrival=0, burst=5),
        Process("P2", arrival=1, burst=3),
        Process("P3", arrival=2, burst=8),
        Process("P4", arrival=3, burst=6),
    ]

    gantt, result = srt_scheduling(test_processes)

    print("Gantt Chart:")
    for pid, start, end in gantt:
        print(f"  [{start:>2} - {end:>2}] {pid}")

    print("\nMetrics:")
    print(f"{'PID':<5}{'Arrival':<10}{'Burst':<8}{'Start':<8}{'Completion':<12}{'Waiting':<10}{'Turnaround':<12}{'Response':<10}")
    for p in result:
        print(f"{p.pid:<5}{p.arrival:<10}{p.burst:<8}{p.start_time:<8}{p.completion_time:<12}{p.waiting_time:<10}{p.turnaround_time:<12}{p.response_time:<10}")

    avg_wt = sum(p.waiting_time for p in result) / len(result)
    avg_tat = sum(p.turnaround_time for p in result) / len(result)
    avg_rt = sum(p.response_time for p in result) / len(result)
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    print(f"Average Response Time: {avg_rt:.2f}")