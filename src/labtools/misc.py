def sq(x):
    return x ** 2


def list_like(var):
    return hasattr(var, "__getitem__") and hasattr(var, "__len__")