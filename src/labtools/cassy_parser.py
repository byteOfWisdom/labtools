from labtools.misc import safe_float, some
from labtools.libs import numpy as np


def get_file(path):
    with open(path) as file:
        return file.readlines()
    return None



class Safe_list:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        if index >= 0 and index < len(self.data):
            return self.data[index]
        return None

    def __iter__(self):
        return iter(self.data)


def lazy_float(f):
    try: return float(f)
    except: return f.strip()



def line_to_list(line):
    return list(map(lazy_float, line.split()))


def transform_table(header, data):
    res = {}
    for name in header:
        res[name] = []  
    for n in range(len(data)):
        for i in range(len(header)):
            res[header[i]].append(data[n][i])
    return res



def parse_cassy_file(path):
    # why does cassy not use a reasonable file format
    # and also , seperation for floats....
    # i hate everything
    data = {}
    lines = Safe_list(get_file(path))
    i = 0

    while not 'DEF=' in lines[i]: i += 1

    headers = lines[i].removeprefix('DEF=').split('\t')

    indices = {}
    for h in headers:
        indices[h] = headers.index(h)

    data['headers'] = indices
    i += 1


    content = []
    while some(lines[i]):
        fields = lines[i].split()
        #print(fields)

        fields = map(lambda s: s.replace(',', '.'), fields)
        content.append( list( map( safe_float, fields)))

        i += 1

    #print(content)
    content = np.array(content)
    data['data'] = np.transpose(content)

    return data