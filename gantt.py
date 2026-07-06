def print_gantt(segments):
    if not segments:
        print("No segments to display")
        return

    top = "|"
    labels = "|"
    bottom = " "

    for pid, start, end in segments:
        width = max((end - start) * 3, len(str(pid)) + 2)
        top += "-" * width + "|"
        labels += pid.center(width) + "|"

    print(top)
    print(labels)
    print(top)

    line = f"{segments[0][1]}"
    pos = len(line)
    for pid, start, end in segments:
        width = max((end - start) * 3, len(str(pid)) + 2)
        marker = str(end)
        pad = width + 1 - len(marker)
        line += " " * pad + marker
    print(line)


def print_gantt_simple(segments):
    for pid, start, end in segments:
        print(f"{pid}: [{start} -> {end}]")