from labtools.misc import some, slice_pairs
from labtools.libs import numpy as np


def gcd(a, b, deviation=0.0):
    #print('called gcd with {}, {}'.format(a, b))

    magn = min(int(np.log10(abs(a))), int(np.log10(abs(b))))
    if magn < 0:
        a = a * (10 ** -magn)
        b = b * (10 ** -magn)
        deviation = deviation * (10 ** -magn)


    while not abs(b) <= deviation:
        temp = a % b
        a = b
        b = temp

    #print('result is {}'.format(a * (10 ** magn) ))
    return a * (10 ** magn) 


def approx_greatest_common_divisor(nums, deviation=None):
    if not some(deviation):
        # TODO change this to return a list of possible results and deviations
        return approx_greatest_common_divisor(nums, 0.1)

    # as greatest common divisor ist associative i.e. gcd(a, b, c) = gcd(a, gcd(b, c)) ...
    # 

    # make sure the lenght of nums is divisble by two
    if len(nums) % 2:
        np.append(nums, nums[-1])

    while len(nums) > 1:
        nums = [gcd(*ns, deviation) for ns in slice_pairs(nums)]

    return nums[0]


agcd = approx_greatest_common_divisor #because i might find the long name annoying
