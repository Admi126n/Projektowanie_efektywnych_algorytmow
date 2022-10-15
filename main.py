import csv


def read_test_data(csv_patch):
    with open(csv_patch) as file:
        things = csv.reader(file, delimiter=' ')
        next(things)
        things = list(things)
    return things


def read_ini():
    pass


def write_output():
    pass


def tsp_brute_force():
    pass


print("Hello PEA!")
