import csv
import datetime
import math
import os
import random


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
    Reads given .ini file and returns it as a tuple of list and string
    :param ini_path: path to .ini file
    :type ini_path: string
    :return: .ini file as a list and string with output file path
    :rtype: tuple[list | string]
    """
    with open(ini_path) as file:
        things = csv.reader(file, delimiter=' ')
        next(things)
        things = list(things)
    output_path = things.pop()[0]
    return things, output_path


def clear_output(output_path):
    """
    Creates output directory if not present and removes output file
    if already present
    :param output_path: path to output file
    :rtype output_path: string
    :return: None
    """
    if not os.path.exists(output_path.split("\\")[0]):
        os.mkdir(output_path.split("\\")[0])
    elif os.path.exists(output_path):
        os.remove(output_path)


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


def path_to_string(path):
    """
    Takes list and returns it as a string in expected format
    :param path: list with vertexes of path
    :type path: list
    :return: string with square brackets and vertexes
    :rtype: string
    """
    output = "["
    for el in path:
        output += f"{el} "
    output = output[0:-1]
    output += "]"
    return output


def get_random_initial(graph):
    """
    Gets initial solution by random choosing vertexes
    :return:
    """
    cost = 0
    path = [0]
    vertex = 0
    k = 0
    to_visit = [*range(1, len(graph))]
    for _ in range(len(graph) - 1):
        vertex = random.choice(to_visit)
        cost += graph[k][vertex]
        path.append(vertex)
        to_visit.remove(vertex)
        k = vertex
    cost += graph[vertex][0]
    path.append(0)
    return cost, path


def get_greedy_initial(graph):
    """
    Gets initial solution by greedy choosing vertexes
    :return:
    """
    cost = 0
    path = [0]
    vertex = 0
    k = 0
    to_visit = [*range(1, len(graph))]
    for _ in range(len(graph) - 1):
        vertex = to_visit[0]
        for el in to_visit:
            if graph[k][vertex] > graph[k][el]:
                vertex = el
        cost += graph[k][vertex]
        path.append(vertex)
        to_visit.remove(vertex)
        k = vertex
    cost += graph[vertex][0]
    path.append(0)
    return cost, path


def calculate_distance(solution, graph):
    dist = 0
    for i in range(len(solution)):
        if i != len(solution) - 1:
            # dist += graph[solution[i], solution[i + 1]]
            dist += graph[solution[i]][solution[i + 1]]
        else:
            # dist += graph[solution[i], solution[0]]
            dist += graph[solution[i]][solution[0]]
    return dist


def switch_neighbour(solution):
    neighbour = solution[:]
    x, y = random.sample(range(len(neighbour)), 2)
    neighbour[x], neighbour[y] = neighbour[y], neighbour[x]
    return neighbour


def simulated_annealing(temp, cooling_rate, iterations, graph):
    random_solution_distance, solution = get_random_initial(graph)
    best_solution = solution[:]
    for i in range(iterations):
        new_solution = switch_neighbour(solution)

        best_distance = calculate_distance(best_solution, graph)

        delta = calculate_distance(new_solution, graph) - random_solution_distance

        # If solution is worse or probability is very high
        if delta < 0 or random.random() < math.exp(-delta / temp):
            solution = new_solution[:]
        if random_solution_distance < best_distance:
            best_solution = solution[:]
        temp *= (1 - cooling_rate)
    return calculate_distance(best_solution, graph), best_solution


def main(ini):
    graphs_to_check, output = read_ini(ini)
    clear_output(output)

    for graph in graphs_to_check:
        graph_name = graph[0]
        repetitions = int(graph[1])
        optimal_cost = int(graph[2])
        t_0 = int(graph[-3])
        cooling_rate = float(graph[-2])
        eras = int(graph[-1])

        # graph_file = np.array(read_test_data(os.path.join("Test_data", graph_name)))
        graph_file = read_test_data(os.path.join("Test_data", graph_name))

        output_message = graph_name
        print(f"Graph {graph_name} in progress...")

        for _ in range(repetitions):
            start_time = datetime.datetime.now()
            calculated_cost, optimal_path = simulated_annealing(t_0, cooling_rate, eras, graph_file)
            end_time = datetime.datetime.now()

            execution_time = (end_time - start_time).microseconds
            cost_ratio = round((calculated_cost / optimal_cost) * 100, 2)

            assert cost_ratio >= 100, "Calculated cost better than optimal cost!"

            output_message += f"\n{execution_time} {calculated_cost} ({cost_ratio} %) {optimal_path}"

        output_message += "\n"
        write_output(output, output_message)


if __name__ == "__main__":
    ini_file_path = ".ini"
    main(ini_file_path)
