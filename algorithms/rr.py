import copy
from collections import deque
from metrics import compute_metrics

def round_robin(processes, quantum=2):
    procs = copy.deepcopy(processes)
    
    for p in procs:
        p.remaining = p.burst
        p.start_time = None
        p.completion_time = None
        p.waiting_time = 0
        p.turnaround_time = 0
        p.response_time = None

    sorted_procs = sorted(enumerate(procs), key=lambda x: (x[1].arrival, x[0]))
    
    queue = deque()
    gantt = []
    
    current_time = 0
    next_proc_idx = 0
    
    def enqueue_new_arrivals(limit_time):
        nonlocal next_proc_idx
        while next_proc_idx < len(sorted_procs) and sorted_procs[next_proc_idx][1].arrival <= limit_time:
            queue.append(sorted_procs[next_proc_idx][1])
            next_proc_idx += 1

    enqueue_new_arrivals(current_time)

    while next_proc_idx < len(sorted_procs) or len(queue) > 0:
        if len(queue) == 0:
            next_arrival = sorted_procs[next_proc_idx][1].arrival
            if current_time < next_arrival:
                gantt.append(("Idle", current_time, next_arrival))
            current_time = next_arrival
            enqueue_new_arrivals(current_time)
            
        curr_p = queue.popleft()
        
        if curr_p.start_time is None:
            curr_p.start_time = current_time
            
        run_duration = min(quantum, curr_p.remaining)
        next_time = current_time + run_duration
        
        gantt.append((curr_p.pid, current_time, next_time))
        
        curr_p.remaining -= run_duration
        
        enqueue_new_arrivals(next_time)
        
        if curr_p.remaining > 0:
            queue.append(curr_p)
        else:
            curr_p.completion_time = next_time
            
        current_time = next_time
        
    compute_metrics(procs)
    
    return procs, gantt
