import csv
import itertools
import datetime
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


def held_karp(graph):
    graph_len = len(graph)

    # słownik (maska bitowa,wierzchołek):(koszt dotarcia:poprzednik)
    cost_dict = {}

    # cost_dict[(maska_bitowa_dla_k, k)] = (koszt 0 -> k, previus (czyli 0))
    # sąsiedzi wierzchołka początkowego z kosztami dotarcia
    for k in range(1, graph_len):
        cost_dict.update({(1 << k, k): (graph[0][k], 0)})

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, graph_len):
        for subset in itertools.combinations(range(1, graph_len), subset_size):
            bits = 0

            # utworzenie maski bitowej dla aktualnej podsieci
            for node in subset:
                bits |= 1 << node

            # Find the lowest cost to get to this subset
            # uzyskanie maski bitowej poprzednika
            for k in subset:
                prev_mask = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((cost_dict.get((prev_mask, m))[0] + graph[m][k], m))
                cost_dict.update({(bits, k): min(res)})

    # maska bitowa odwiedzonych wszystkich w poza poczatkowym
    bits = (2**graph_len - 1) - 1

    res = []
    # utworzenie listy kosztów dotarcia do w poczatkowego dla wszyskich odwiedzonych wierzcholkow
    for k in range(1, graph_len):
        res.append((cost_dict.get((bits, k))[0] + graph[k][0], k))
    # wybór optymalnego
    opt, parent = min(res)

    # tablica ze sciezka konczaca sie wierzcholkiem poczatkowym
    path = [0]
    # backtracking po słowniku
    for _ in range(graph_len - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = cost_dict.get((bits, parent))
        bits = new_bits

    # dodanie wierzcholka poczatkowego
    path.append(0)

    return opt, list(reversed(path))


def main():
    graphs_to_check, output = read_ini(".ini")
    clear_output(output)

    for graph in graphs_to_check:
        print(f"Graph {graph[0]} in progress...")

        output_message = ""
        for i in range(len(graph)):
            output_message += graph[i] + " "

        iterations = int(graph[1])
        graph_file = read_test_data(os.path.join("Test_data", graph[0]))

        for _ in range(iterations):
            start_time = datetime.datetime.now()
            cost, optimal_path = held_karp(graph_file)
            end_time = datetime.datetime.now()
            optimal_path = path_to_string(optimal_path)
            output_message += f"\n{str((end_time - start_time).microseconds)} {cost} {optimal_path}"

        output_message += "\n"
        write_output(output, output_message)


if __name__ == "__main__":
    main()
    # test_graph = read_test_data(r"Test_data/tsp_4.txt")
    # start = datetime.datetime.now()
    # print(held_karp(test_graph))
    # end = datetime.datetime.now()
    # print((end - start).microseconds)
