import csv
import datetime
import os
import sys
import warnings


class Ant:
    def __init__(self, n, curr):
        self.cost = 0
        self.path = [curr]
        self.start_ver = curr
        self.curr_ver = curr
        self.next_ver = 0
        self.tabu_list = self.initialize_tabu(n, curr)

    @staticmethod
    def initialize_tabu(n, curr):
        tabu_list = [0 * n for _ in range(n)]
        tabu_list[curr] = 1
        return tabu_list

    def update_cost(self, cost):
        self.cost += cost

    def update_path(self):
        self.path.append(self.next_ver)

    def update_tabu_list(self, ver):
        self.tabu_list[ver] = 1

    def set_current_vertex(self, current_ver):
        self.curr_ver = current_ver

    def set_next_vertex(self, next_ver):
        self.next_ver = next_ver


class AntColonyOptimisation:
    pheromone_value_per_iteration = 100

    def __init__(self, graph, alpha, beta, ro, initial_tau):
        self.graph_size = len(graph)
        self.graph_costs = graph
        self.alpha = alpha
        self.beta = beta
        self.ro = ro
        self.initial_tau = initial_tau
        self.ants = self.initialise_ants()
        self.pheromone_list = self.initialize_pheromone_list()

    def initialise_ants(self):
        ants = []
        for i in range(self.graph_size):
            ants.append(Ant(self.graph_size, i))
        return ants

    def initialize_pheromone_list(self):
        pheromone_list = [[self.initial_tau] * self.graph_size for _ in range(self.graph_size)]
        return pheromone_list

    def cas(self, path_cost):
        return self.pheromone_value_per_iteration / path_cost

    def das(self):
        return self.pheromone_value_per_iteration

    def qas(self, edge_cost):
        return self.pheromone_value_per_iteration / edge_cost

    def update_pheromones(self, cost, path):
        for i in range(len(path) - 1):
            self.pheromone_list[path[i]][path[i + 1]] += self.qas(cost)

    def evaporating(self):
        for i in range(len(self.pheromone_list)):
            for j in range(len(self.pheromone_list[i])):
                self.pheromone_list[i][j] = self.ro * self.pheromone_list[i][j]

                if self.pheromone_list[i][j] < self.initial_tau:
                    self.pheromone_list[i][j] = self.initial_tau

    def calculate_probability(self, curr_vertex: int, next_vertex: int) -> float:
        prob = pow(self.pheromone_list[curr_vertex][next_vertex], self.alpha) * \
               pow(1 / self.graph_costs[curr_vertex][next_vertex], self.beta)
        return prob

    def choose_next_vertex(self, tabu_list, curr_ver):
        best_vertex = 0
        max_pheromone_value = 0

        for vertex in range(self.graph_size):
            if not tabu_list[vertex]:
                pheromone_value = self.calculate_probability(curr_ver, vertex)
                if pheromone_value >= max_pheromone_value:
                    best_vertex = vertex
                    max_pheromone_value = pheromone_value

        return best_vertex

    def ACO(self, generations):
        best_cost = sys.maxsize
        optimal_path = []

        for k in range(generations):
            for ant in self.ants:
                for _ in range(self.graph_size - 1):
                    ant.set_next_vertex(self.choose_next_vertex(ant.tabu_list, ant.curr_ver))

                    ant.update_cost(self.graph_costs[ant.curr_ver][ant.next_ver])
                    ant.update_path()
                    ant.update_tabu_list(ant.next_ver)
                    ant.set_current_vertex(ant.next_ver)

            for i, ant in enumerate(self.ants):
                ant.update_cost(self.graph_costs[ant.curr_ver][ant.start_ver])
                ant.set_next_vertex(ant.start_ver)
                ant.update_path()

                if best_cost > ant.cost:
                    best_cost = ant.cost
                    optimal_path = ant.path

                self.update_pheromones(ant.cost, ant.path)

            self.evaporating()
            self.ants = self.initialise_ants()

        return best_cost, optimal_path


class Main:
    def __init__(self, ini_path):
        graphs_to_check, output = self.read_ini(ini_path)
        self.clear_output(output)

        for graph in graphs_to_check:
            mean_time = 0
            mean_cost = 0
            mean_percent = 0

            graph_name = graph[0]
            optimal_cost = int(graph[1])
            repetitions = int(graph[2])
            alpha = float(graph[3])
            beta = float(graph[4])
            ro = float(graph[5])
            generations = int(graph[6])

            graph_file = self.read_test_data(os.path.join("Test_data", graph_name))

            initial_tau = self.calculate_initial_tau(graph_file, len(graph_file))

            output_message = graph_name
            print(f"Graph {graph_name} in progress...")

            for _ in range(repetitions):
                aco = AntColonyOptimisation(graph_file, alpha, beta, ro, initial_tau)

                start_time = datetime.datetime.now()
                calculated_cost, optimal_path = aco.ACO(generations)
                end_time = datetime.datetime.now()

                execution_time = (end_time - start_time).microseconds
                error = round((calculated_cost / optimal_cost) * 100 - 100, 2)

                if error < 0:
                    warnings.warn(f"Calculated cost better than optimal cost! ({calculated_cost} < {optimal_cost})")

                output_message += f"\n{execution_time} {calculated_cost} ({error} %) " \
                                  f"{self.path_to_string(optimal_path)}"

                mean_cost += calculated_cost
                mean_percent += error
                mean_time += execution_time

            output_message += "\n"
            self.write_output(output, output_message)

            output_message = f"{graph_name}: " \
                             f"mean cost: {round(mean_cost / repetitions, 2)}; " \
                             f"mean error: {round(mean_percent / repetitions, 2)}%; " \
                             f"mean execution time: {round((mean_time / repetitions) / 1_000_000, 2)} s\n"
            self.write_output(output, output_message)

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_greedy_initial(graph):
        """
        Gets initial solution by greedy choosing vertexes
        :return:
        """
        cost = 0
        vertex = 0
        k = 0
        to_visit = [*range(1, len(graph))]
        for _ in range(len(graph) - 1):
            vertex = to_visit[0]
            for el in to_visit:
                if graph[k][vertex] > graph[k][el]:
                    vertex = el
            cost += graph[k][vertex]
            to_visit.remove(vertex)
            k = vertex
        cost += graph[vertex][0]
        return cost

    def calculate_initial_tau(self, graph, vertices_count):
        estimated_cost = self.get_greedy_initial(graph)
        return vertices_count / estimated_cost


if __name__ == "__main__":
    Main(".ini")
