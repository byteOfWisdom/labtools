import labtools as tools
import task

def main():
	tasks = {
		'a': task.example
	}

	preview = tools.task_list.run_task_list(tasks)

	if not preview:
		tools.notes.write_notes('notes.txt')
	else:
		tools.notes.print_notes()



if __name__ == '__main__':
	main()