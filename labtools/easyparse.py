import numpy as np


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


def write_printable(data, file):
    content = ''
    numbers = []
    for key in data:
        content += key + ", "
        numbers.append(list(data[key]))

    content = content[:-2] + "\n"
    for i in range(len(numbers[0])):
        for col in numbers:
            content += str(round(col[i], 2)) + ", "
        content = content[:-2] + "\n"

    with open(file, 'w') as handle:
        handle.write(content)