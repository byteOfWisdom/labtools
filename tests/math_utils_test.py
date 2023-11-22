#!python3

import labtools as tools


def main():
	assert tools.math.gcd(42, 7) == 7
	print(tools.math.gcd(42, 8, 0.0))
	#assert tools.math.bf_gcd(7.2, 0.7, 0.1) == 0.7
	print(tools.math.gcd(43, 1.5, 0.01))


if __name__ == '__main__':
	main()