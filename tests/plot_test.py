#!python3
import labtools

def main():
    data = labtools.ep.parse('test.data')
    plot = labtools.Plot('random x data', 'some y values')

    elem = {
        'x': data['x'],
        'y': data['y'],
        'yerr': 0.5,
        'label': 'a fancy label thing',
        'color': 'green'
    }

    dataset = plot.add_element(**elem)

    function = plot.add_element(lambda x: x ** 2)
    plot.mark_intersect(dataset, 12.5)
    plot.mark_intersect(function, 12.5, 'function intersect')
    plot.preview()


    plot = labtools.Plot('an axis', 'another axis')
    x = labtools.np.linspace(0, 100, 100)
    y = labtools.p.ev(labtools.np.random.rand(100) * 10, labtools.np.random.rand(100) * 2)
    noise = plot.add_element(x, y)

    a, b, _, _ = plot.linear_fit(noise)
    plot.add_element(lambda x: a * x + b)

    plot.preview()


if __name__ == '__main__':
    main()