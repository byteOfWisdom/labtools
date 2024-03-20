# this is used to make all charts and tables printable as one pdf file
# it works by outputting latex code, which can then be compiled using pdflatex

from labtools.libs import numpy as np
from labtools.settings import get_setting
from labtools.perror import ErrVal

header = r"""
\documentclass{article}
\usepackage[left=1cm,top=1cm,right=1cm,bottom=1.5cm,bindingoffset=0.5cm]{geometry}
\usepackage{longtable}
\usepackage{graphicx}
\begin{document}
\graphicspath{{./}}
"""

footer = r"""
\end{document}
"""

tables = []
charts = []


def printable(number, sig_digits=100) -> str:
    str_num = ''
    if type(number) == ErrVal:
        str_num = str(number)
        str_num = str_num.replace('+-', r'\pm')
        str_num = str_num.replace('^', r'^{') 
        if '{' in str_num: str_num += r'}'
    else:
        if type(number) == str:
            str_num = number
        else:
            str_num = str(round(number, sig_digits))

    if get_setting('localization') == 'de_De':
        str_num = str_num.replace('.', ',')

    return '$' + str_num + '$'




def queue_table(table : dict, name : str, sig_digits=100):
    global tables
    tables.append((table, name))


def queue_chart(file : str):
    global charts
    charts.append(file)


def tex_table(table : dict, name : str) -> str:
    hline = r'\hline'
    newline = r'\\' + '\n'
    row = ' & '

    # backwards compatibility
    name = name.replace('results/', '').replace('.csv', '')
    name = name.replace('/', '').replace('.', '').replace('_', ' ')

    table_header = r'\section{' + name + '} ' + '\n' + r'\centering' + '\n' + r' \begin{longtable} {|' + 'c|' * len(table.keys()) + r'}' + '\n'
    table_footer = r'\end{longtable}' + '\n'

    table_content = r''

    for header in table.keys():
        table_content += '$' + header + '$' + row

    table_content = table_content[:-len(row)] + newline + hline * 2 + '\n'

    data = [table[key] for key in table.keys()]
    data = np.transpose(data)

    for line in data:
        tex_line = r''
        for point in line:
            tex_line += printable(point) + row
        tex_line = tex_line[:-len(row)] + newline + hline + '\n'

        table_content += tex_line


    return table_header + table_content + table_footer



def tex_chart(file : str) -> str:
    file = file.replace('results/', '').replace('.png', '')
    name = file
    name = name.replace('/', '').replace('.', '').replace('_', ' ')

    chart_header = ''#r'\section{' + name + '} ' + '\n'

    chart_string = r'\includegraphics[height=0.45\textheight]{' + file + r'} \\'
    return chart_header + chart_string



def make_tex_file(file : str):
    content = header

    for table in tables:
        content += tex_table(*table)

    content += r'\newpage'

    for chart in charts:
        content += tex_chart(chart)


    content += footer

    with open(file, 'w') as handle:
        handle.write(content)