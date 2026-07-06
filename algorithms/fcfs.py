import copy


def fcfs(processes):
    procs = sorted(copy.deepcopy(processes), key=lambda p: p.arrival)
    time = 0
    segments = []

    for p in procs:
        if time < p.arrival:
            time = p.arrival

        p.start_time = time
        p.response_time = p.start_time - p.arrival
        time += p.burst
        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival
        p.waiting_time = p.turnaround_time - p.burst

        segments.append((p.pid, p.start_time, p.completion_time))

    return segments, procs