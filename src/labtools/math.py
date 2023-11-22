from labtools.misc import some, slice_pairs
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


motivation = 10000 # higher number more precision but also more runtime

def gcd(a, b, deviation=0.0):
    if deviation == 0:
        return euclid_gcd(a, b)
    #print(min(a, b), deviation)
    #possible = np.linspace(min(a, b), deviation, int(motivation * (1 / deviation)))
    possible = np.linspace(min(a, b), deviation, int(motivation ** 2))
    leftover_a = (a % possible) / (a // possible)
    leftover_b = (b % possible) / (b // possible)

    # contains the bigger remainder from deviding a and b by the respective value
    remainder = np.array([max(*n) for n in np.transpose(np.array([leftover_a, leftover_b]))])
    remainder = np.array([crop(n, min(a, b)) for n in remainder])

    #print(remainder)

    return possible[remainder <= deviation][0]


import math

'''
def gcd(a, b, deviation=0.0) :
    if (a < b) :
        return gcd(b, a)
     
    # base case
    if (abs(b) < deviation) :
        return a
    else :
        return (gcd(b, a - math.floor(a / b) * b))
'''

def gcd(a, b, deviation=0.0):
    print('called gcd with {}, {}'.format(a, b))

    magn = min(int(np.log10(abs(a))), int(np.log10(abs(b))))
    if magn < 0:
        a = a * (10 ** -magn)
        b = b * (10 ** -magn)
        deviation = deviation * (10 ** -magn)


    while not abs(b) <= deviation:
        temp = a % b
        a = b
        b = temp

    print('result is {}'.format(a * (10 ** magn) ))
    return a * (10 ** magn) 


def approx_greatest_common_divisor(nums, deviation=None):
    if not some(deviation):
        # TODO change this to return a list of possible results and deviations
        return approx_greatest_common_divisor(nums, 0.1)

    # as greatest common divisor ist associative i.e. gcd(a, b, c) = gcd(a, gcd(b, c)) ...
    # 

    # make sure the lenght of nums is divisble by two
    if len(nums) % 2:
        nums.append(nums[-1])

    while len(nums) > 1:
        nums = [gcd(*ns, deviation) for ns in slice_pairs(nums)]

    return nums[0]


agcd = approx_greatest_common_divisor #because i might find the long name annoying
