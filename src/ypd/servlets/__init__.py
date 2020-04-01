
from os.path import join
from pathlib import Path
import glob

#Load all .py files in this directory so we can import them all at once in server.py
modules = Path(__file__).parent.glob('*.py')
__all__ = []
for module in modules:
    module_name = str(module).rpartition('.')[0].rpartition('/')[2]
    if module_name != '__init__':
        __all__.append(module_name)