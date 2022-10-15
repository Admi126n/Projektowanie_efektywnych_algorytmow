import csv
import time
import os
# import sys
# import itertools


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


def write_output(file_name, new_element):
    with open(file_name, mode='a') as file:
        file.write(new_element)


def tsp_brute_force():
    pass


def main(ini_path):
    graphs_to_check = read_ini(ini_path)
    output_file_path = graphs_to_check.pop()[0]

    # remove output file if already exist
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    for graph in graphs_to_check:
        output = ""
        for i in range(len(graph)):
            output += graph[i] + " "

        graph_path = graph[0]
        iterations = int(graph[1])

        for i in range(iterations):
            start_time = time.time()
            end_time = time.time()
            output += "\n" + str(end_time - start_time)
            pass

        output += "\n"
        write_output(r"Output\output.csv", output)


ini = ".ini"

main(ini)
