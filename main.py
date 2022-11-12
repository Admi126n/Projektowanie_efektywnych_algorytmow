import csv
import itertools
import datetime


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
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((cost_dict.get((prev, m))[0] + graph[m][k], m))
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


test_graph = read_test_data(r"Test_data/tsp_4.txt")
start = datetime.datetime.now()
print(held_karp(test_graph))
end = datetime.datetime.now()

print((end - start).microseconds)
