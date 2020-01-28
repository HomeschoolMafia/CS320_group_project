import subprocess
import platform

def main():
    if platform.system() == 'Windows':
        subprocess.run('set FLASK_APP=src/project_proposer/prototype_server.py && flask run', shell=True)
    else:
        subprocess.run('export FLASK_APP=src/project_proposer/prototype_server.py && flask run', shell=True)
