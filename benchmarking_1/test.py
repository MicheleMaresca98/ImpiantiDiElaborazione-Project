import subprocess
import csv
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
    medie = []
    deviazioni = []
    num_bod = [100, 500, 1000, 5000, 10000]
    # sample sizes
    num_rip = [100 for _ in range(len(num_bod))]
    # getting sample standard deviations
    for i in range(len(num_bod)):
        r, n = num_rip[i], num_bod[i]
        values = experiment(r, n)
        avg = average(values)
        medie.append(avg)
        deviazioni.append(dev_std(values, avg))
    E = lambda x: x / 100
    z = 1.96
    # big std_dev -> large CI
    # computing required number of repetitions for each size of the experiment
    for i in range(len(num_bod)):
        print(f"N bodies: {num_bod[i]}, sample mean: {medie[i]}, sample dev std: {deviazioni[i]}, max error: {E(medie[i])}")
    target_rip = [int((z * deviazioni[i] / E(medie[i])) ** 2) for i in range(len(medie))]
    print(f"Number of repetitions to do for each number of bodies: {target_rip}")
    medie = []
    deviazioni = []
    # repeating the experiments
    for i in range(len(num_bod)):
        r, n = target_rip[i], num_bod[i]
        values = experiment(r, n)
        avg = average(values)
        medie.append(avg)
        deviazioni.append(dev_std(values, avg))
    with open('risultati.csv', 'w', newline='') as average_file:
        writer = csv.writer(average_file)
        writer.writerow(["Number of Bodies", "Average", "Dev Std"])
        for i in range(0,len(num_bod)):
            writer.writerow([num_bod[i], medie[i], deviazioni[i]])



