#!python3

import plutils
import easyparse


def main():
	data = easyparse.parse('test.data')
	plot = plutils.Plot('random x data', 'some y values')


	elem = {
		'x': data['x'],
		'y': data['y'],
		'yerr': 0.5,
		'label': 'a fancy label thing',
		'color': 'green'
	}

	dataset = plot.add_element(**elem)

	function = plot.add_element(lambda x: x ** 2)
	plot.mark_intersect(dataset, 12.5)
	plot.mark_intersect(function, 12.5, 'function intersect')
	plot.preview()

if __name__ == '__main__':
	main()