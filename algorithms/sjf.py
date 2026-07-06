import copy


def sjf(processes):
    procs = copy.deepcopy(processes)
    n = len(procs)
    completed = 0
    time = 0
    segments = []
    done = [False] * n

    while completed < n:
        idx = -1
        shortest = float('inf')

        for i, p in enumerate(procs):
            if not done[i] and p.arrival <= time and p.burst < shortest:
                shortest = p.burst
                idx = i

        if idx == -1:
            time += 1
            continue

        p = procs[idx]
        p.start_time = time
        p.response_time = p.start_time - p.arrival
        time += p.burst
        p.completion_time = time
        p.turnaround_time = p.completion_time - p.arrival
        p.waiting_time = p.turnaround_time - p.burst

        segments.append((p.pid, p.start_time, p.completion_time))
        done[idx] = True
        completed += 1

    return segments, procs