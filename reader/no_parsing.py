import os


def get_no_parsing():
    ret = []
    module_dir = os.path.dirname(__file__)
    filename = os.path.join(module_dir, 'no_parsing.txt')
    file = open(filename, "r", encoding="utf8")
    for line in file.readlines():
        ret += [line.strip("\n")]
    return ret
