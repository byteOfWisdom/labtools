import numpy as np
from labtools.settings import get_setting

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


from csv2pdf import convert
from pypdf import PdfMerger

from labtools.perror import ErrVal

pdfs = []

def write_printable(data, file, sig_digits=100):
    content = ''
    numbers = []
    for key in data:
        content += key + ", "
        numbers.append(list(data[key]))

    content = content[:-2] + "\n"
    for i in range(len(numbers[0])):
        for col in numbers:
            if type(col[i]) == ErrVal:
                content += str(col[i]) + ", "
            else:
                content += str(round(col[i], sig_digits)) + ", "
        content = content[:-2] + "\n"

    delimiter = ','
    if get_setting('localization') == 'de_De':
        content = content.replace(',', ';')
        content = content.replace('.', ',')
        delimiter = ';'

    with open(file, 'w') as handle:
        handle.write(content)

    convert(file, file.replace('.csv', '.pdf'), align='J', delimiter=delimiter)
    pdfs.append(file.replace('.csv', '.pdf'))



def merge_all():
    merger = PdfMerger()

    for file in pdfs:
        merger.append(file)

    merger.write('results/all_tables.pdf')
    merger.close()