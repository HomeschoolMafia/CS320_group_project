import subprocess


def main():
    subprocess.run(
        "export FLASK_APP=src/project_proposer/prototype_server.py; flask run", shell=True)
