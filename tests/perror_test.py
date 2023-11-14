#!python3

import labtools as tools 


def main():
	a = tools.perror.ErrVal(42, 2)
	print(tools.np.sqrt(a))
	print(tools.np.log(a))


	b = tools.perror.ev(range(100), 5)
	print(b)


if __name__ == '__main__':
	main()