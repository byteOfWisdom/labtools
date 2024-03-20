# these are basically just the typical
# top level bindings i'd import in my lab
# data crunching things.
from labtools.libs import numpy as np
from labtools.plutils import Plot, mod_plot_num
from labtools.perror import ev, unzip, value, error
from labtools.math import fit_func
from labtools.misc import sq, some, unpack_data
from labtools.easyparse import write_printable, merge_all
from labtools.notetaking import note, note_var, write_notes, print_notes
from labtools.task_list import run_task_list
from labtools.settings import set_setting