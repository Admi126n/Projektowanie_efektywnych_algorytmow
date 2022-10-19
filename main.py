import csv
import itertools
import sys
import time
import os


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


def read_ini(ini_path):
    """
    Reads given .ini file and returns it as a list
    :param ini_path: path to .ini file
    :type ini_path: string
    :return: .ini file as a list
    :rtype: list
    """
    with open(ini_path) as file:
        things = csv.reader(file, delimiter=' ')
        next(things)
        things = list(things)
    return things


def write_output(file_path, new_element):
    """
    Writes results to given file
    :param file_path: path to output file
    :type file_path: string
    :param new_element: output to write
    :type new_element: string
    :return: None
    """
    with open(file_path, mode='a') as file:
        file.write(new_element)


def clear_output(output_path):
    # TODO add docstring
    if not os.path.exists(output_path.split("\\")[0]):
        os.mkdir(output_path.split("\\")[0])
    elif os.path.exists(output_path):
        os.remove(output_path)


def path_to_string(path):
    """
    Takes list and returns it as a string in expected format
    :param path: list with vertexes of path
    :type path: list
    :return: string with square brackets and vertexes
    :rtype: string
    """
    output = "[0 "
    for el in path:
        output += f"{el} "
    output = output[0:-1]
    output += " 0]"
    return output


def tsp_brute_force(graph):
    """
    Reads two-dimensional list with graph, calculates minimal travel cost and optimal path
    :param graph: two-dimensional list with graph
    :type graph: list
    :return: tuple with minimal cost and optimal path
    :rtype: tuple[int | list]
    """
    optimal_path = []
    vertex = [*range(1, len(graph))]

    min_cost = sys.maxsize
    permutations = itertools.permutations(vertex)

    for permutation in permutations:
        curr_cost = 0
        k = 0
        for point in permutation:
            curr_cost += graph[k][point]
            k = point
        curr_cost += graph[k][0]
        min_cost = min(min_cost, curr_cost)
        if min_cost == curr_cost:
            optimal_path = permutation

    return min_cost, optimal_path


def main(ini_path):
    """
    Calls functions all needed functions to solve tsp problem
    :param ini_path: path to .ini file
    :type ini_path: string
    :return: None
    """
    graphs_to_check = read_ini(ini_path)  # load data from .ini
    output_file_path = graphs_to_check.pop()[0]  # pop last value from ini

    clear_output(output_file_path)

    for graph in graphs_to_check:
        print(f"Graph {graph[0]} in progress...")
        output = ""
        for i in range(len(graph)):
            output += graph[i] + " "

        graph_file_path = graph[0]
        iterations = int(graph[1])
        graph_file = read_test_data(os.path.join("Test_data", graph_file_path))
        cost = 0
        path = []

        start_time = time.time()
        for i in range(iterations):
            cost, path = tsp_brute_force(graph_file)
            path = path_to_string(path)
            print(f"\tGraph {graph[0]} iteration {i + 1}/{iterations} done")
        end_time = time.time()
        output += f"\n{str((end_time - start_time) / iterations)} {str(cost)} {str(path)}"

        output += "\n"
        write_output(r"Output\output.csv", output)


ini = ".ini"

main(ini)
