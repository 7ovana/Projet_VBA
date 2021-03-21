import numpy as np


def brownian_trajectory_onedimensional(N, m):
    """
     A function that generates 1-dimensional brownian motion.

    :param  N:      Number of trajectories to generate
    :param  m:      Number of jumps
    :return space:  A time vector for the moments of the jumps
    :return W:      The Brownian Motion positions/values
    """
    dt = 1 / m
    Z = np.random.normal(0, 1, size=(N, m))
    W = np.zeros((N, m + 1))
    space = np.linspace(0, 1, m + 1)
    for i in range(m):
        W[:, i + 1] = W[:, i] + (np.sqrt(dt) * Z[:, i])

    return space, W


def brownian_trajectory_multidimensional(N, m, d, correlation_matrix):
    dt = 1 / m
    space = np.linspace(0, 1, m + 1)
    results = list()
    Choleski = np.linalg.cholesky(correlation_matrix)
    for j in range(N):
        Z = np.random.normal(0, 1, size=(N, m))
        W = np.zeros((d, m + 1))

        for i in range(m):
            W[:, i + 1] = W[:, i] + (np.sqrt(dt) * Z[:, i])

        Wcorr = np.zeros((d, m + 1))
        for i in range(1, m + 1):
            Wcorr[:, i] = np.matmul(W[:, i], Choleski)

        results.append(Wcorr)
    return space, results
