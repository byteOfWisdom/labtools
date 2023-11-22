from sys import argv
from sys import stdin
import tomllib
from labtools.plutils import some
from labtools.easyparse import parse
from labtools.cassy_parser import parse_cassy_file
import numpy as np


def numpyify(toml_data):
    data = toml_data
    for key in data.keys():
        if type(data[key]) == dict:
            data[key] = numpyify(data[key])
        elif type(data[key]) == list:
            data[key] = np.array(data[key])
    return data


def load_subfiles(toml_data):
    data = toml_data
    for key in data.keys():
        if type(data[key]) == dict:
            data[key] = load_subfiles(data[key])
        elif type(data[key]) == str and '.txt' in data[key]:
        	data[key] = parse_cassy_file(data[key])
        elif type(data[key]) == str:
            data[key] = parse(data[key])
    return data



def run_task_list(task_list, data_file = None):
    argv_ = []

    #use path provided in argv for the data
    for arg in argv:
        if arg[0] != '-':
            data_file = arg
        else:
            argv_.append(arg)


    data = None
    if some(data_file):
        with open(data_file) as file:
            file_content = file.read()
            data = tomllib.loads(file_content)
            data = load_subfiles(data)
            data = numpyify(data)


    preview = False
    if '-p' in argv: preview = True
    if len(argv_) == 0 or (len(argv_) == 1 and '-p' in argv_[0]):
        # run all tasks
        for key in task_list.keys():
            if some(data):
                task_list[key](preview, data)        
            else:
                task_list[key](preview)

    else:
        for task in argv_:
            if task.strip('-') in task_list.keys():
                if some(data):
                    task_list[task.strip('-')](preview, data)
                else:
                    task_list[task.strip('-')](preview)

    return preview