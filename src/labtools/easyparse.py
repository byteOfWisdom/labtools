import numpy as np
from labtools.settings import get_setting
from labtools.pdf_maker import queue_table, make_tex_file

def parse(file, seperator=' '):
    table = []
    consts = []
    with open(file) as raw:
        content = raw.readlines()
        for line in content:
            if '=' in line:
                consts.append(line)
            elif not line.isspace():
                table.append(line)

    res = {}

    for const in consts:
        parts = const.split('=')
        res[parts[0].strip()] = float(parts[1])

    if len(table) == 0: return res

    cols = table[0].split(seperator)
    cols = remove_false_headers(cols)


    for i in range(len(cols)):
        data = np.array([float(line.split(seperator)[i]) for line in table[1:]])
        res[cols[i].strip()] = data

    for const in consts:
        parts = const.split('=')
        res[parts[0].strip()] = float(parts[1])

    return res


def remove_false_headers(arr):
    res = []
    for elem in arr:
        # kick out false elements due to windows newlines
        if elem.isspace(): continue

        res.append(elem)

    return res


def write_printable(data, file, sig_digits=100):
    queue_table(data, file, sig_digits)


def merge_all():
    make_tex_file('results/prints.tex')