import subprocess
import sys
import math


def average(values):
    listSum = sum(values)
    listLen = len(values)
    return listSum/(listLen-1)


def dev_std(values, mean):
    sqr_values = [val**2 for val in values]
    return math.sqrt(abs( ( sum(sqr_values) / (len(values) - 1) ) - mean**2))


def experiment(r, n):
    lines = subprocess.check_output(['./launch_nbody.sh', '-r', str(r), '-n', str(n)]).decode().split('\n')
    values = [float(line.split(' ')[1]) for line in lines if len(line) > 0]
    return values


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} n_bodies n_reps")
        exit(1)
    n_bodies = int(sys.argv[1])
    n_reps = int(sys.argv[2])
    values = experiment(n_reps, n_bodies)
    avg = average(values)
    dev = dev_std(values, avg)
    print(f"Sample mean: {avg}, sample standard deviation: {dev}")




