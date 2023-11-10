from sys import argv

def run_task_list(task_list):
    preview = False
    if '-p' in argv: preview = True
    if len(argv) == 1 or (len(argv) == 2 and '-p' in argv[1]):
        # run all tasks
        for key in task_list.keys():
            task_list[key](preview)

    else:
        for task in argv[1:]:
            if task.strip('-') in task_list.keys():
                task_list[task.strip('-')](preview)

    return preview