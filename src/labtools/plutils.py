from enum import Enum

from labtools import perror

from labtools.libs import pyplot as plt # for the actualy plotting part
from labtools.libs import numpy as np

from labtools.misc import some, pairs, is_real, fit_func

from labtools.settings import get_setting
from labtools.pdf_maker import queue_chart


import locale


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
        _, res = func_fit(lambda x, a, b: a * x + b, self.x, self.y)
        return res[0].value, res[1].value, res[0].error, res[1].error


class Spectrum:
    def __init__(self, wavelenghts):
        self.needs_xrange = False #this should be constant for this type
        self.wavelenghts = np.array(list(map(float, wavelenghts)))
        self.width = 2.5
    
    def plot(self):
        cmap = plt.get_cmap('rainbow')
        colors = cmap((self.wavelenghts - 400) / (250))
        plt.bar(self.wavelenghts, 1, width=self.width, label=self.wavelenghts, color=colors)

    def lims(self):
        return ([400, 700], [0, 1])


class Heatmap:
    def __init__(self, x, y, z, label=''):
        self.x_grid = x
        self.y_grid = y
        self.z = z
        self.label = label
        self.needs_xrange = False

    def plot(self):
        dimx = max(self.x_grid) - min(self.x_grid) + 1
        dimy = max(self.y_grid) - min(self.y_grid) + 1
        data = np.zeros((dimy, dimx), dtype=np.float64)
        for x, y, value in zip(self.x_grid, self.y_grid, self.z):
            data[y][x] = value

        plt.imshow(data)
        plt.colorbar(shrink=0.5, label=self.label)
        plt.grid(False)
        plt.legend('',frameon=False)
        plt.xticks(np.arange(dimx), labels=list(range(dimx)))
        plt.yticks(np.arange(dimy), labels=list(range(dimy)))

        for i in range(dimx):
            for j in range(dimy):
                if data[j][i] != 0.0:
                    text = plt.text(i, j, round(data[j][i], 1),
                       ha="center", va="center", color="w")


    def lims(self):
        dimx = max(self.x_grid) - min(self.x_grid) + 1
        dimy = max(self.y_grid) - min(self.y_grid) + 1
        return ([-0.5, dimx - 0.5], [-0.5, dimy -0.5])



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
    if type(args[0]) == str and args[0] == 'spectrum':
        return Spectrum(args[1])
    elif type(args[0]) == str and args[0] == 'spectrum_w':
        spec = Spectrum(args[1])
        spec.width = 1.0
        return spec
    elif type(args[0]) == str and args[0] == 'heatmap':
        label = ''
        if 'label' in kwds.keys(): 
            label = kwds['label']
        return Heatmap(args[1], args[2], args[3], label)


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


def mod_plot_num():
    global pnum
    pnum += 0.1


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
        
        self.xlabel = ''
        self.ylabel = ''

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

        # here comes the localization for THAT tutor who insists
        # on commas for decimal points... cause GERMANY...

        if some(get_setting('localization')):
            locale.setlocale(locale.LC_ALL, get_setting('localization'))
            plt.rcdefaults()

            # Tell matplotlib to use the locale we set above
            plt.rcParams['axes.formatter.use_locale'] = True


        # and here comes actual code

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
            plt.hlines([where], *self.xlim, linestyle='--', label=label, color=color)

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
            queue_chart(file)