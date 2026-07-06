def print_metrics(procs):
    print(f"{'PID':<6}{'Arrival':<10}{'Burst':<8}{'Waiting':<10}{'Turnaround':<12}{'Response':<10}")

    total_wait = 0
    total_tat = 0
    total_rt = 0

    for p in procs:
        print(f"{p.pid:<6}{p.arrival:<10}{p.burst:<8}{p.waiting_time:<10}{p.turnaround_time:<12}{p.response_time:<10}")
        total_wait += p.waiting_time
        total_tat += p.turnaround_time
        total_rt += p.response_time

    n = len(procs)
    print()
    print(f"Average Waiting Time: {total_wait / n:.2f}")
    print(f"Average Turnaround Time: {total_tat / n:.2f}")
    print(f"Average Response Time: {total_rt / n:.2f}")


def get_averages(procs):
    n = len(procs)
    total_wait = sum(p.waiting_time for p in procs)
    total_tat = sum(p.turnaround_time for p in procs)
    total_rt = sum(p.response_time for p in procs)

    return {
        "avg_waiting": total_wait / n,
        "avg_turnaround": total_tat / n,
        "avg_response": total_rt / n,
    }