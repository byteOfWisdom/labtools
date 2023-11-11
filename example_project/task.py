import labtools as tools

def example(preview, data_file=None):
	data = data_file['example']

	plot = tools.Plot('x axis', 'y axis')
	plot.add_element(data['x'], data['y'], 0, data['dy'], 'some data')
	plot.add_element(lambda x: x ** 2, 'a function')

	plot.finish(preview, 'sample_plot.png')
