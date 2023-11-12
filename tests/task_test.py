#!python3

import labtools

def test_a(preview, data=None):
	assert(data['a']['x'] == 42)


def test_b(preview, data=None):
	assert(type(data['b']['file']) == dict)


def main():
	tasks = {
		'a': test_a,
		'b': test_b,
	}

	labtools.task_list.run_task_list(tasks)



if __name__ == '__main__':
	main()