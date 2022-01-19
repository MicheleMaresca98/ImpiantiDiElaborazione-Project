# Author: Marco Carlo Feliciano
import sys
import os


def _join(ts, event):
    line = f"{str(ts)} {event}"
    return line
    

def _split(line):
    line = line.split()
    ts = int(line[0])
    event = " ".join(line[1:])
    return ts, event


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} log_file coalescence_window")
        print('log_file => log nel formato "TIMESTAMP NODE ERR-CATEGORY MESSAGE"')
        print('coalescence_window => coalescence window selezionata con la "knee" rule')
        exit(1)
    interarrivals, lengths, startingPoints, tuples = [], [], [], []
    log_file, cwin = sys.argv[1], int(sys.argv[2])
    tsPrev, tsSucc, tupleCount = 0, 0, 0
    with open(log_file, 'r') as f:
        line = f.readline().strip()
        tsPrev, event = _split(line)
        tuples.append([])
        tuples[tupleCount].append((tsPrev, event))
        line = f.readline().strip()
        while line:
            tsSucc, event = _split(line)
            diff = tsSucc - tsPrev
            if diff < cwin:
                tuples[tupleCount].append((tsSucc, event))
            else:
                interarrivals.append(diff)
                start = tuples[tupleCount][0][0]
                end = tuples[tupleCount][-1][0]
                duration = end - start
                lengths.append(duration)
                startingPoints.append(start)
                # creating new tuple
                tuples.append([])
                tupleCount += 1
                tuples[tupleCount].append((tsSucc, event))
            tsPrev = tsSucc
            line = f.readline().strip()
        # last tuple
        start = tuples[tupleCount][0][0]
        end = tuples[tupleCount][-1][0]
        duration = end - start
        lengths.append(duration)
        startingPoints.append(start)
    folder = f"tupling_{log_file.split('.')[0]}-{str(cwin)}-py"
    os.mkdir(folder)
    with open(os.path.join(folder, "interarrivals.txt"), 'w') as f:
        for t in interarrivals:
            f.write(str(t) + os.linesep)
    with open(os.path.join(folder, "lengths.txt"), 'w') as f:
        for t in lengths:
            f.write(str(t) + os.linesep)
    with open(os.path.join(folder, "startingPoints.txt"), 'w') as f:
        for i in range(len(startingPoints)):
            t = f"{startingPoints[i]} {lengths[i]}"
            f.write(t + os.linesep)
    for i in range(len(tuples)):
        t = tuples[i]
        with open(os.path.join(folder, f"tuple_{i+1}"), 'w') as f:
            for log in t:
                line = _join(*log)
                f.write(line + os.linesep)

        
