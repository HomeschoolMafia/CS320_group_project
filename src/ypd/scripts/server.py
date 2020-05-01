import os
import subprocess
import platform

from .. import relative_path, config

def main():
    port = config['server']['port']

    if platform.system() == 'Windows':
        subprocess.run(f'set FLASK_APP={relative_path}/server.py && flask run -p {port}', shell=True)
    else:
        subprocess.run(f'export FLASK_APP={relative_path}/server.py && flask run -p {port}', shell=True)
