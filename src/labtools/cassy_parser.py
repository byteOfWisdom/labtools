from labtools.misc import try_float, some

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
	tag = ''
	line = []
	acc = []

	while True:
		line = lines[i]
		if not some(line): break

		if '=' in line and acc != []:
			data[tag] = transform_table(line)
		

		if '=' in line and '=' in lines[i + 1]:
			tag = line.split('=')[0].strip()
			line = line_to_list(line.split('=')[1])
			data[tag] = line
		elif '=' in line and not '=' in lines[i + 1]:
			acc = []
			tag = line.split('=')[0].strip()
			line = line_to_list(line.split('=')[1])
		else:
			acc.append(line_to_list(line))
		i += 1

	if acc != []:
		data[tag] = transform_table(line, acc)
	
	return data