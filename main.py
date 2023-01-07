import csv
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


def main():
    pass


if __name__ == "__main__":
    ini_file_path = ".ini"
    main()
