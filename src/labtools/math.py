from labtools.misc import some, slice_pairs
from labtools.libs import numpy as np
from kafe2.fit import Fit, xy_fit # type: ignore
from scipy.optimize import curve_fit # type: ignore
from labtools import perror

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


def fit_func(func, x, y, use_kafe=False):
    if not type(x[0]) == perror.ErrVal:
        x = perror.ev(x, None)

    if not type(y[0]) == perror.ErrVal:
        y = perror.ev(y, None)
    
    if use_kafe:
        res = xy_fit(
            model_function=func,
            x_data = perror.value(x),
            y_data = perror.value(y),
            x_error = perror.error(x),
            y_error = perror.error(x),
            p0 = perror.value(fit_func(func, x, y, False))[1],
            profile = True,
        )

        params = [*res['parameter_values'].values()]
        errors = [*res['parameter_errors'].values()]

        fitted_func = lambda x: func(x, *params)
        fit_results = perror.ev(params, errors)
        return fitted_func, fit_results
    else:
        params, pcov = curve_fit(func, perror.value(x), perror.value(y))
        fitted_func = lambda x: func(x, *params)

        perr = np.sqrt(np.diag(pcov))

        fit_results = perror.ev(params, perr)

        return fitted_func, fit_results