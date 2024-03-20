from setuptools import setup
from mypyc.build import mypycify

setup(
    name = "labtools",
    ext_modules = mypycify([
        "src/labtools/__init__.py", 
        "src/labtools/cassy_parser.py", 
        "src/labtools/defaults.py", 
        "src/labtools/easyparse.py", 
        "src/labtools/libs.py", 
        "src/labtools/math.py", 
        "src/labtools/misc.py", 
        "src/labtools/notetaking.py", 
        "src/labtools/pdf_maker.py", 
        "src/labtools/perror.py", 
        "src/labtools/plutils.py", 
        "src/labtools/settings.py", 
        "src/labtools/task_list.py"
    ]),
)