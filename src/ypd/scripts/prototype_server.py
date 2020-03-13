import subprocess
import platform

from .. import relative_path

def main():
    if platform.system() == 'Windows':
        subprocess.run(f'set FLASK_APP={relative_path}/prototype_server.py && flask run', shell=True)
    else:
        subprocess.run(f'export FLASK_APP={relative_path}/prototype_server.py && flask run -p 2080', shell=True)