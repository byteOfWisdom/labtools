#!python3.11

from labtools.defaults import *

def main():
    print('expecting 1.1 +- 0.1, getting: ', ev(1.1, 0.1)) # should print 1.1 +- 0.1
    print('expecting 101 +- 3, getting: ', ev(100.5, 3)) # should print 101 +- 3
    print('expecting (0 +- 1)*10^-2, getting: ', ev(1e-3, 1e-2)) # should print (0.1 +- 1)*10^-2
    print(ev(1e6, 1))
    print(ev(0.0015, 0.015))
    print(ev(82.5, 7.778425692259328))
    a = ev(42, 2)
    print(np.sqrt(a))
    print(np.log(a))


#    b = ev(range(100), 5)
#    print(b)


if __name__ == '__main__':
    main()