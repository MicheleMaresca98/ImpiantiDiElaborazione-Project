import matplotlib.pyplot as plt


def draw_plots(cpu_times, IO_times):
    assert len(cpu_times) == len(IO_times)
    x = [i for i in range(len(cpu_times))]
    ymax = max(max(cpu_times), max(IO_times))
    xlabel = "Number of users"
    plt.subplot(1,2,1)
    plt.plot(x, cpu_times)
    plt.xlabel(xlabel)
    plt.ylabel("Mean CPU subsystem's response time")
    plt.ylim(0, ymax)

    plt.subplot(1,2,2)
    plt.plot(x, IO_times)
    plt.xlabel(xlabel)
    plt.ylabel("Mean I/O subsystem's response time")
    plt.ylim(0, ymax)

    plt.show()


def mean_value_analysis(visit_rates, service_rates, num_users, N=None, T=None, lamb=None, disable_assertions=True):
    # N, T and lamb as optional input to provide memoization in case of repeated calls with increasing num_users
    # disable assertions (sanity checks) for increased performance; it tooks 75% more time with all the assertions
    num_queues = len(visit_rates)
    if not disable_assertions:
        assert len(visit_rates) == len(service_rates)
        assert num_queues > 0
        assert num_users >= 0
        assert (N is None and T is None and lamb is None) or (N is not None and T is not None and lamb is not None)
    if N is not None:
        if not disable_assertions:
            assert (len(N) == len(T) and len(T) == len(lamb) and len(N) == num_queues)
            assert all([( len(N[i]) == len(T[i]) and len(T[i]) == len(lamb[i]) ) for i in range(num_queues)])
            assert all([( len(N[i]) == len(N[i+1]) ) for i in range(num_queues-1)])
    else:
        N = [[0] for _ in range(num_queues)]
        T = [[0] for _ in range(num_queues)]
        lamb = [[0] for _ in range(num_queues)]
    memo_len = len(N[0])
    for k in range(memo_len, num_users+1):
        for i in range(num_queues):
            T_i_k = (1 + N[i][k-1]) / service_rates[i]
            T[i].append(T_i_k)
        current_T = [T[i][k] for i in range(num_queues)]
        denominator = sum([visit_rate * visit_time for (visit_rate, visit_time) in zip(visit_rates, current_T)])
        for i in range(num_queues):
            N_i_k = (k * visit_rates[i] * T[i][k]) / denominator
            N[i].append(N_i_k)
            lambda_i_k = N[i][k] / T[i][k]
            lamb[i].append(lambda_i_k)
    return N, T, lamb


if __name__ == "__main__":
    visit_rates = [3, 1]
    # service_times = [1/5, 1/2]
    service_rates = [5, 2]
    max_users = 100
    cpu_times, IO_times = [0], [0]
    N, T, lamb = mean_value_analysis(visit_rates, service_rates, 0)
    for k in range(1, max_users+1):
        N, T, lamb = mean_value_analysis(visit_rates, service_rates, k, N, T, lamb)
        cpu_times.append(T[0][-1])
        IO_times.append(T[1][-1])
    print(f"T0[3]: {T[0][3]}, T1[3]: {T[1][3]}")
    print(f"N0[3]: {N[0][3]}, N1[3]: {N[1][3]}")
    print(f"lamb0[3]: {lamb[0][3]}, lamb1[3]: {lamb[1][3]}")
    print()
    print(f"T0[max_users]: {T[0][max_users]}, T1[max_users]: {T[1][max_users]}")
    print(f"N0[max_users]: {N[0][max_users]}, N1[max_users]: {N[1][max_users]}")
    print(f"lamb0[max_users]: {lamb[0][max_users]}, lamb1[max_users]: {lamb[1][max_users]}")
    draw_plots(cpu_times, IO_times)
