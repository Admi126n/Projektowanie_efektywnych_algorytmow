import csv
import sys
import itertools


def read_test_data(file_path):
    with open(file_path) as file:
        things = csv.reader(file, delimiter=' ')
        next(things)
        things = list(things)
    # change data from string to int
    for i in range(len(things)):
        for j in range(len(things[i])):
            things[i][j] = int(things[i][j])
    return things


def read_ini(ini_path):
    with open(ini_path) as file:
        things = csv.reader(file, delimiter=' ')
        next(things)
        things = list(things)
    return things


def write_output():
    pass


def tsp_brute_force():
    pass


def main(ini_path):
    graphs_to_check = read_ini(ini_path)
    output_file_path = graphs_to_check.pop()
    for graph in graphs_to_check:
        graph_path = graph[0]
        iterations = int(graph[1])
        for i in range(iterations):
            print(i)
    # print(graphs_to_check)
    # print(output_file_path)


ini = ".ini"

# main(ini)
print(read_test_data(r"Test_data\tsp_6_1.txt"))
