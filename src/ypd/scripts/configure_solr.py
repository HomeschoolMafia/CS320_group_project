import argparse
import atexit
from pathlib import Path
import subprocess

import requests

from ypd import relative_path, config

def main():
    """Configures the local solr server"""
    subprocess.run(f'solr start -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)
    subprocess.run(f'solr delete -c {config["solr"]["collection"]} -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)
    subprocess.run(f'solr delete -c {config["solr"]["test_collection"]} -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)
    subprocess.run(f'solr create_core -c {config["solr"]["collection"]} -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)
    subprocess.run(f'solr create_core -c {config["solr"]["test_collection"]} -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)

    schema = Path(f'{relative_path}/config/solr_schema.json').read_bytes()

    #Set working schema
    response = requests.post(f'{config["solr"]["url"]}/solr/{config["solr"]["collection"]}/schema', data=schema)
    if response.status_code != 200:
        raise RuntimeError(response.content)
    else:
        print("Successfully set collection schema")
    sample_data = Path(f'{relative_path}/config/sample_index.xml').read_bytes()
    response = requests.post(f'{config["solr"]["url"]}/solr/{config["solr"]["collection"]}/update',
                                data=sample_data, headers={'Content-type': 'text/xml'})
    if response.status_code != 200:
        raise RuntimeError(response.content)
    else:
        print("Successfully set sample data")

    #Set test schema
    response = requests.post(f'{config["solr"]["url"]}/solr/{config["solr"]["test_collection"]}/schema', data=schema)
    if response.status_code != 200:
        raise RuntimeError(response.content)
    else:
        print("Successfully set test schema")

    test_data = Path(F'{relative_path}/config/test_index.xml').read_bytes()
    response = requests.post(f'{config["solr"]["url"]}/solr/{config["solr"]["test_collection"]}/update',
                             data=test_data, headers={'Content-type': 'text/xml'})
    if response.status_code != 200:
        raise RuntimeError(response.content)
    else:
        print("Successfully set test data")

@atexit.register
def shutdown_solr():
    subprocess.run(f'solr stop -p {config["solr"]["url"].rpartition(":")[2]}', shell=True)