def run_mlfq(processes, q1_quantum=2, q2_quantum=4, aging_threshold=10):
    """
    Multilevel Feedback Queue (MLFQ) Scheduling Algorithm.
    Returns:
        merged_gantt (list of tuples): Execution segments formatted as (pid, start_time, end_time).
        processes (list): Updated process objects with completed metrics.
    """
    # Sort processes by arrival time initially
    unarrived = sorted(processes, key=lambda p: p.arrival)
    
    # 3 Queues based on project requirements:
    # Queue 0: RR (Quantum = 2)
    # Queue 1: RR (Quantum = 4)
    # Queue 2: FCFS (Infinite Quantum)
    queues = [[], [], []]
    
    time = 0
    completed = 0
    n = len(processes)
    gantt = []
    
    # Initialize MLFQ-specific trackers safely within the function
    for p in processes:
        p.queue_level = 0
        p.wait_time_current_queue = 0
        p.remaining = p.burst
        p.start_time = None
        p.completion_time = None

    current_process = None
    current_quantum_used = 0
    segment_start = None

    while completed < n:
        # 1. Arrival of new processes (Always join Queue 0 first)
        while unarrived and unarrived[0].arrival == time:
            p = unarrived.pop(0)
            queues[0].append(p)

        # 2. Preemption, Demotion, and Completion Logic
        if current_process:
            # Check if any higher priority queue has processes waiting
            higher_priority_waiting = any(len(queues[i]) > 0 for i in range(current_process.queue_level))
            
            # Determine quantum limit based on the current queue level
            if current_process.queue_level == 0:
                quantum_limit = q1_quantum
            elif current_process.queue_level == 1:
                quantum_limit = q2_quantum
            else:
                quantum_limit = float('inf') # Queue 2 is FCFS
            
            # Condition A: Process Finished
            if current_process.remaining == 0:
                current_process.completion_time = time
                current_process.turnaround_time = time - current_process.arrival
                current_process.waiting_time = current_process.turnaround_time - current_process.burst
                completed += 1
                
                if segment_start is not None and time > segment_start:
                    gantt.append((current_process.pid, segment_start, time))
                current_process = None
                
            # Condition B: Quantum Expired (Demotion)
            elif current_quantum_used == quantum_limit:
                if segment_start is not None and time > segment_start:
                    gantt.append((current_process.pid, segment_start, time))
                
                # Demote if not already at the lowest queue
                if current_process.queue_level < 2:
                    current_process.queue_level += 1
                    
                current_process.wait_time_current_queue = 0
                queues[current_process.queue_level].append(current_process)
                current_process = None
                
            # Condition C: Preempted by a higher priority process arriving
            elif higher_priority_waiting:
                if segment_start is not None and time > segment_start:
                    gantt.append((current_process.pid, segment_start, time))
                
                current_process.wait_time_current_queue = 0
                queues[current_process.queue_level].append(current_process)
                current_process = None

        # 3. Context Switch / Select Next Process
        if not current_process:
            for level in range(3):
                if queues[level]:
                    current_process = queues[level].pop(0)
                    current_quantum_used = 0
                    segment_start = time
                    
                    # Log start time for Response Time calculation
                    if current_process.start_time is None:
                        current_process.start_time = time
                        current_process.response_time = time - current_process.arrival
                    break

        # 4. Aging to Prevent Starvation (Only applies to waiting processes in Q1 and Q2)
        for level in range(1, 3):
            i = 0
            while i < len(queues[level]):
                p = queues[level][i]
                p.wait_time_current_queue += 1
                
                if p.wait_time_current_queue >= aging_threshold:
                    queues[level].pop(i)
                    p.queue_level -= 1  # Promote to a higher queue
                    p.wait_time_current_queue = 0
                    queues[p.queue_level].append(p)
                else:
                    i += 1

        # 5. Execute Current Process
        if current_process:
            current_process.remaining -= 1
            current_quantum_used += 1

        # Advance the CPU clock
        time += 1

    # Merge consecutive Gantt segments of the same process for a cleaner visual chart
    merged_gantt = []
    for pid, start, end in gantt:
        if merged_gantt and merged_gantt[-1][0] == pid and merged_gantt[-1][2] == start:
            merged_gantt[-1] = (pid, merged_gantt[-1][1], end)
        else:
            merged_gantt.append((pid, start, end))

    return merged_gantt, processes