from dataclasses import dataclass

from labtools.libs import numpy as np
from labtools.misc import list_like

from math import inf, nan

def sq(a):
    return a ** 2


#for quickly generating multiple ErrVal with the same error
def const_err(e):
    return lambda v: make_errval(v, e)


def value(a):
    return unzip(a)[0]


def error(a):
    return unzip(a)[1]


#just a helper function
def make_errval(v, e):
    return ErrVal(v, e)


def vnum(a, b):
    return ezip(a, b)


# combines a list of values with a list of errors into a list of ErrVal
def ezip(values, errors):
    return np.array([ErrVal(values[i], errors[i]) for i in range(len(values))])



def ev(v, e):
    if list_like(v) and list_like(e):
        return np.array(ezip(v, e))
    elif list_like(v):
        return np.array(list(map(const_err(e), v)))
    else:
        return ErrVal(v, e)


def unzip(values):
    if isinstance(values[0], ErrVal):
        values_ = np.array([v.value for v in values])
        errors = np.array([v.error for v in values])
        return values_, errors
    else:
        return values, None



num_type = [float, int, np.float64]


def within_deviation(a, b):
    return abs(a.value - b.value) < (a.error + b.error)


def magnitude(x):
    if x == 0.0:
        return 0
    try:
        if x > 1:
            return int(np.log10(x))
        else:
            return int(np.log10(x)) - 0
    except:
        return 0 # if the value is zero, the magnitude of that is 10^0



@dataclass
class ErrVal:
    value : float
    error : float

    def __init__(self, v, e):
        self.value = v
        self.error = abs(e)


    def __eq__(self, other):
        #if type(other) == float:
        #    if other == inf or other == nan:
        #        return self.value == other

        if type(other) in num_type:
            return self.value == other
            #return False #special case where we compare a value with an error to a float or int

        return self.value == other.value and self.error == other.error


    def __gt__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        return self.value > other.value


    def __lt__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        return self.value < other.value


    def __add__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        v = self.value + other.value
        
        # add errors using gaussion error propagation
        e = np.sqrt(sq(self.error) + sq(other.error))

        return ErrVal(v, e)


    def __sub__(self, other):
        return self + (-1 * other)


    def __rsub__(self, other):
        return other + (-1 * self)


    def __radd__(self, other):
        return self + other 
        

    def __rmul__(self, other):
        return self * other


    def __rtruediv__(self, other):
        temp = ErrVal(1, 0)
        return other * (temp / self)


    def __mul__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        v = self.value * other.value
        e = np.sqrt(sq(other.value * self.error) + sq(self.value * other.error))

        return ErrVal(v, e)


    def __truediv__(self, other):
        if type(other) in num_type:
            other = ErrVal(other, 0)

        v = self.value / other.value
        e = np.sqrt(sq(self.error / other.value) + sq(other.error * self.value / sq(other.value)))

        return ErrVal(v, e)


    def __pow__(self, exp):
        if type(exp) in num_type:
            exp = ErrVal(exp, 0)

        v = self.value ** exp.value
        e = np.sqrt(sq(exp.value * (self.value ** (exp.value - 1)) * self.error) + sq((self.value ** exp.value) * np.log(self.value) * exp.error))

        return ErrVal(v, e)


    def __rpow__(self, other):
        other = ErrVal(other, 0)
        return other ** self


    def __abs__(self):
        return ErrVal(abs(self.value), self.error)


    def __float__(self):
        if self.value == inf or self.error == inf:
            return 'inf'

        err_magn = int(np.log10(abs(self.error)))
        val_magn = int(np.log10(abs(self.value)))

        if err_magn <= val_magn:
            significant = - err_magn
        else:
            significant = 0

        return float(round(self.value, significant))


    def __int__(self):
        return int(self.value)


    def sqrt(self):
        return self ** 0.5


    def log(self):
        value = np.log(self.value)
        # d/dx ln(x) = 1/x
        error = self.error / self.value
        return ErrVal(value, error)


    def old__str__(self):
        if self.value == inf or self.error == inf or self.value == -inf or self.error == -inf:
            return 'inf'



        if self.value == 0.0:
            return '{} +- {}'.format(self.value, round(self.error, 3))


        val_magn = int(np.log10(abs(self.value)))

        if self.error == 0.0:
            return '{}*10^{}'.format(
                round(self.value * (10 ** (- val_magn + 1)), 4),
                val_magn - 1
                )

        err_magn = int(np.log10(abs(self.error)))


        if self.error == 0.0:
            return str(round(self.value * (10 ** exponent), significant - exponent)) + "* 10^" + str(- exponent)

        exponent = - min(err_magn, val_magn)
        significant = abs(err_magn - exponent)


        return '({} +- {})*10^{}'.format(
            round(self.value * (10 ** exponent), - err_magn - exponent + 1),
            round(self.error * (10 ** exponent), - err_magn - exponent + 1),
            int(- exponent)
        )


        if exponent == 0 or self.value == 0.0:
            return '{} +- {}'.format(
                round(self.value * (10 ** exponent), significant - exponent),
                str(round(self.error * (10 ** exponent), significant - exponent))
            )



        fmt = "( "
        fmt += str(round(self.value * (10 ** exponent), significant - exponent))
        fmt += " +- "
        fmt += str(round(self.error * (10 ** exponent), significant - exponent))
        fmt += " ) * 10^" + str(- exponent)

        return fmt


    def __str__(self):
        error_magn = magnitude(self.error)
        value_magn = magnitude(self.value)

        significant_value = np.round(self.value, - error_magn + 1)
        significant_error = np.round(self.error, - error_magn + 1)
        oom = 10 ** (- error_magn)

        if error_magn == 0 or value_magn == 0:
            return '{} +- {}'.format(significant_value, significant_error)

        return '({} +- {})*10^{}'.format(round(self.value * oom, 1), round(self.error * oom, 1), error_magn)