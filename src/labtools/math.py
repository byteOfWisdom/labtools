from labtools.misc import some
from labtools.libs import numpy as np



def approx_eq(a, b, dev):
    return abs(b - a) <= dev



# this works both better and faster
# when no deviation is allowed. 
# works well for ints, kinda sus for floats
def euclid_gcd(a, b):
    if a == 0: return abs(b)
    if b == 0: return abs(a)

    while b != 0:
        temp = a % b
        a = b
        b = temp

    return abs(a)


def crop(a, b):
    return min(abs(a), abs(b - a))


def gcd(a, b, deviation=0.0):
    if deviation == 0:
        return euclid_gcd(a, b)
    possible = np.linspace(min(a, b), deviation, int(100 * (1 / deviation)))
    leftover_a = (a % possible) / (a // possible)
    leftover_b = (b % possible) / (b // possible)

    # contains the bigger remainder from deviding a and b by the respective value
    remainder = np.array([max(*n) for n in np.transpose(np.array([leftover_a, leftover_b]))])
    remainder = np.array([crop(n, min(a, b)) for n in remainder])

    #print(remainder)

    return possible[remainder <= deviation][0]



def approx_greatest_common_divisor(nums, deviation=None):
    if not some(deviation):
        # TODO change this to return a list of possible results and deviations
        return approx_greatest_common_divisor(nums, 0.1)

    # as greatest common divisor ist associative i.e. gcd(a, b, c) = gcd(a, gcd(b, c)) ...
    # 

agcd = approx_greatest_common_divisor #because i might find the long name annoying
