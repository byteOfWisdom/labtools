notes_str = ''

def note(s):
    global notes_str
    notes_str += s + "\n"


def note_var(var, value, err=None, unit=''):
    if err == None:
        note('{} = {} {}'.format(var, value, unit))
    else:
        note('{} = ({} +- {}) {}'.format(var, value, err, unit))


def write_notes(file):
    global notes_str
    with open(file, 'w') as handle:
        handle.write(notes_str)


def print_notes():
    print(notes_str)


def clear_notes():
    global notes_str
    notes_str = ''