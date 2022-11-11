import csv
import itertools
import os
import sys
import random
import datetime
import numpy as np
from itertools import combinations


def read_test_data(file_path):
    """
    Reads test data file, converts it from string to int and returns it as a list
    :param file_path: path to test data
    :type file_path: string
    :return: test data as two-dimensional list
    :rtype: list
    """
    with open(file_path) as file:
        things = csv.reader(file, delimiter=' ')
        next(things)
        things = list(things)
    # change data from string to int
    for i in range(len(things)):
        for j in range(len(things[i])):
            things[i][j] = int(things[i][j])
    return things


def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2**n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = [0]
    for _ in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list(reversed(path))


def tutorial(mask, pos, level):
    global visited_all
    global test_graph
    global dp
    global path
    global ans

    if mask == visited_all:
        return test_graph[pos][0]

    if dp[mask][pos] != -1:
        return dp[mask][pos]

    for city in range(len(test_graph)):
        if mask & (1 << city) == 0:
            new_ans = test_graph[pos][city] + tutorial(mask | (1 << city), city, level + 1)
            ans = min(ans, new_ans)

    dp[mask][pos] = ans
    return ans


test_graph = read_test_data(r"Test_data/tsp_6_2.txt")

# ans = sys.maxsize
# path = []
# for _ in range(len(test_graph) + 1):
#     path.append(None)
# path[0] = 0
# path[-1] = 0
#
# level_global = 0
#
# # ustawienie maski na 1111 na wszystkich bitach
# visited_all = (1 << len(test_graph)) - 1
#
# dp = []
# for i in range(1 << len(test_graph)):
#     dp.append([])
#     for j in range(len(test_graph)):
#         dp[i].append(-1)
#
# start = datetime.datetime.now()
# print(tutorial(1, 0, level_global))
# end = datetime.datetime.now()
# print((end - start).microseconds, "ms")
# print(path)


# print(visited_all)

# for el in os.listdir("Test_data"):
#     print(el)
#     graph = read_test_data(os.path.join("Test_data", el))
#     start = datetime.datetime.now()
#     ans = held_karp(graph)
#     end = datetime.datetime.now()
#     print(str(ans), "%.10f" % (end - start).microseconds)

# graph = read_test_data(r"Test_data/tsp_12.txt")
# start = datetime.datetime.now()
# ans = held_karp(graph)
# end = datetime.datetime.now()
# print(str(ans), "%.10f" % (end - start).microseconds)

# x = read_test_data(r"Test_data/tsp_17_2.txt")
# for el in x:
#     print(len(el))
