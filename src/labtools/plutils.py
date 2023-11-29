from enum import Enum

from labtools import perror

from labtools.libs import pyplot as plt # for the actualy plotting part
from labtools.libs import numpy as np

from labtools.misc import some, pairs, is_real

from scipy.stats import linregress


def get_error(maybe_data, maybe_error):
    if type(maybe_data[0]) == perror.ErrVal:
        data = list(map(v.value for v in maybe_data))
        error = list(map(v.error for v in maybe_data))


def crosses(a, b, c):
    up = a <= c and b >= c
    down = a >= c and b <= c
    return up or down


def interpolate_intersects(x, y, y_cutoff):
    intersects =[]
    for pair in pairs(y):
        if crosses(*pair, y_cutoff):
            id0 = list(y).index(pair[0])
            
            ydiff = y[id0 + 1] - y[id0]
            xdiff = x[id0 + 1] - x[id0]
            ycd = y_cutoff - y[id0]
            intersects.append(x[id0] + xdiff * (ycd / ydiff))

    return intersects


def ensure_np_array(a):
    """
    helper function for converting intervals and
    native arrays to numpy arrays
    """
    if type(a) == np.ndarray: return a
    if type(a) == tuple:
        return np.linspace(*a, 1000)
    return np.array(a)



class Dataset:
    def __init__(self, x, y, label=None, color=None):
        self.needs_xrange = False #this should be constant for this type
        self.x = x
        self.y = y
        self.label = label
        self.color = color


    def plot(self):
        plt.plot(self.x, self.y, 'x', label=self.label, color=self.color)


    def find_intersects(self, level):
        return interpolate_intersects(self.x, self.y, level)


    def lims(self):
        xlims = [min(filter(is_real, self.x)), max(filter(is_real, self.x))]
        ylims = [min(filter(is_real, self.y)), max(filter(is_real, self.y))]
        return (xlims, ylims)


    def linear_fit(self):
        res = linregress(self.x, self.y)
        return res.slope, res.intercept, res.stderr, res.intercept_stderr


class Errobar:
    def __init__(self, x, y, xerr=None, yerr=None, label=None, color=None):
        self.needs_xrange = False #this should be constant for this type
        self.x = x
        self.y = y
        self.xerr = xerr
        self.yerr = yerr
        self.label = label
        self.color = color


    def plot(self):
        plt.errorbar(
            self.x, 
            self.y, 
            xerr = self.xerr, 
            yerr = self.yerr, 
            label = self.label, 
            color = self.color, 
            linestyle = '', 
            fmt = '.')


    def find_intersects(self, level):
        return interpolate_intersects(self.x, self.y, level)


    def lims(self):
        xerr, yerr = 0, 0
        if some(self.xerr): xerr = self.xerr
        if some(self.yerr): yerr = self.yerr

        xlims = [min(filter(is_real, self.x - xerr)), max(filter(is_real, self.x + xerr))]
        ylims = [min(filter(is_real, self.y - yerr)), max(filter(is_real, self.y + yerr))]
        return (xlims, ylims)


    def linear_fit(self):
        res = linregress(self.x, self.y)
        return res.slope, res.intercept, res.stderr, res.intercept_stderr


class Function:
    def __init__(self, func, xinterval=None, label=None, color=None):
        self.func = func
        self.xinterval = xinterval
        self.needs_xrange = not some(self.xinterval)
        self.label = label
        self.color = color


    def plot(self):
        self.xinterval = ensure_np_array(self.xinterval)
        plt.plot(self.xinterval, self.func(self.xinterval), label=self.label, color=self.color)


    def x_values(self, xv):
        self.xinterval = xv
        self.needs_xrange = not some(xv)


    def find_intersects(self, level):
        if self.needs_xrange:
            return None
        return interpolate_intersects(self.xinterval, self.func(self.xinterval), level)


    def lims(self):
        # this may cause unintended behaviour. have an eye on this
        if some(self.xinterval):
            xlims = [min(filter(is_real, self.xinterval)), max(filter(is_real, self.xinterval))]
            ylims = [min(filter(is_real, self.func(self.xinterval))), max(filter(is_real(self.func(self.xinterval))))]
            return (xlims, ylims)
        return None

    def linear_fit(self):
        return None # fitting a function to a function is BS


def soft_iter(iterable):
    for element in iterable:
        yield element
    while 1: yield None


def make_plotable(args, kwds):
    # handle positional none string args
    arg_iter = soft_iter(filter(lambda e: type(e) != str, args))
    x = next(arg_iter)
    y = next(arg_iter)
    xerr = next(arg_iter)
    yerr = next(arg_iter)

    # handle positional string args
    arg_iter = soft_iter(filter(lambda e: type(e) == str, args))
    label = next(arg_iter)
    color = next(arg_iter)

    if 'x' in kwds.keys(): x = kwds['x']
    if 'y' in kwds.keys(): y = kwds['y']
    if 'label' in kwds.keys(): label = kwds['label']
    if 'color' in kwds.keys(): color = kwds['color']
    if 'xerr' in kwds.keys(): xerr = kwds['xerr']
    if 'yerr' in kwds.keys(): yerr = kwds['yerr']

    if callable(x):
        if some(y):
            return Function(x, y, label, color)
        # make function
        return Function(x, None, label, color)

    elif callable(y):
        # make function with set xrange
        return Function(y, x, label, color)

    elif some(xerr) or some(yerr):
        # make errorbar plot
        return Errobar(x, y, xerr, yerr, label, color)

    else:
        if type(x[0]) == perror.ErrVal or type(y[0]) == perror.ErrVal:
            x, xerr = perror.unzip(x)
            y, yerr = perror.unzip(y)
            return Errobar(x, y, xerr, yerr, label, color)
        return Dataset(x, y, label, color)


def reset_pyplot():
    plt.clf()
    plt.cla()
    plt.close()


pnum = 0
def plot_num():
    global pnum
    pnum += 1
    return pnum


class Plot():
    """
    wrapper for plotting common things faster and with less boilerplate
    """
    def __init__(self, *args, **kwds):
        """
        expects data to be array like with shape (2, n) 
        or (1, n) and ydata to be given as array like of (1, n)
        """

        self.num = plot_num()
    
        # all plotable elements
        self.elements = []

        # used to store calls that are not doable at time
        # of calling by the user.
        # for example mark_intersect of a function that does not yet have
        # an xinterval
        self.pending = []

        #limits for the overall diagram axes
        self.xlim = [0, 0] 
        self.ylim = [0, 0] 
        self.title = ''

        self.dpi = 250 # just a default value to make nice to look at charts
    
        self.x_marks = []
        self.y_marks = []


        if len(args) == 2 and type(args[0]) == str and type(args[1]) == str:
            self.xlabel = args[0]
            self.ylabel = args[1]
            return

        if some(args) and args != ():
            self.add_element(*args, **kwds)


    def add_element(self, *args, **kwds):
        """
        can take x as an interval over Real numbers (as a tuple) like: (a, b)
        or as an array like

        x may be none if y is a function. it will then be applied to any other active x intervals
        """
        ref = len(self.elements)
        self.elements.append(make_plotable(args, kwds))
        self.autorange()
        return ref


    def autorange(self):
        all_ranges = list(filter(some, [elem.lims() for elem in self.elements]))

        x_lower = min([bound[0][0] for bound in all_ranges])
        y_lower = min([bound[1][0] for bound in all_ranges])
        x_upper = max([bound[0][1] for bound in all_ranges])
        y_upper = max([bound[1][1] for bound in all_ranges])

        x_scale = x_upper - x_lower
        y_scale = y_upper - y_lower

        x_margin = x_scale * 2e-2
        y_margin = y_scale * 2e-2


        self.xlim = [x_lower - x_margin, x_upper + x_margin]
        self.ylim = [y_lower - y_margin, y_upper + y_margin]


    def mark_x(self, where, label=None, color=None):
        """
        expects where to either be a value within at least one of the added x ranges
        of a function with the pattern: f(a, b) -> bool
        """
        self.x_marks.append((where, label, color))
        #plt.vlines([where], *self.ylim, linestyle='--', label=label)


    def mark_y(self, where, label=None, color=None):
        """
        expects where to either be a value within at least one of the added x ranges
        of a function with the pattern: f(a, b) -> bool
        """
        self.y_marks.append((where, label, color))
        #plt.hlines([where], *self.xlim, linestyle='--', label=label)


    def mark_intersect(self, refrence, level, label=None):
        intersects = self.elements[refrence].find_intersects(level)

        if not some(intersects):
            self.pending.append((self.mark_intersect, [refrence, level, label]))
            return

        for intersect in intersects:
            self.mark_x(intersect, label)


    def linear_fit(self, refrence):
        return self.elements[refrence].linear_fit()


    def make_plot(self):
        """
        this should not be called manually.
        it handles the pyplot interactions
        """
        plt.xlim(self.xlim)
        plt.ylim(self.ylim)
        plt.grid()
        for element in self.elements:
            if element.needs_xrange:
                element.x_values(np.linspace(self.xlim[0], self.xlim[1], 1000))
            element.plot()

        for task in self.pending:
            task[0](*task[1])
        for mark in self.x_marks:
            where, label, color = mark
            plt.vlines([where], *self.ylim, linestyle='--', label=label, color=color)

        for mark in self.y_marks:
            where, label, color = mark
            plt.hlines([where], *self.ylim, linestyle='--', label=label, color=color)

        plt.legend()
        plt.title('Fig {}: {}'.format(self.num, self.title))

        if some(self.xlabel): plt.xlabel(self.xlabel)
        if some(self.ylabel): plt.ylabel(self.ylabel)




    def preview(self):
        self.make_plot()
        plt.show()
        reset_pyplot()


    def save(self, filename):
        self.make_plot()
        plt.savefig(
            filename,
            bbox_inches = 'tight',
            pad_inches = 0.2,
            dpi=self.dpi
        )
        reset_pyplot()


    def finish(self, preview, file):
        """
        show the plot if preview is true
        or save to file if not
        """
        if preview:
            self.preview()
        else:
            self.save(file)