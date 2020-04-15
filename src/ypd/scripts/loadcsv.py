import csv 

from ypd import relative_path

def main():
    with open(f'{relative_path}/db/project.csv','r') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)