import platform
import subprocess
from csv import DictReader
from pathlib import Path

from .. import config, relative_path
from ..model import Base, Session, engine
from ..model.user import User, UserType
from ..model.project import Provided, Solicited


def main():
    csv_dir=Path(f'{relative_path}/csv')

    print('Creating database')
    session = Session()
    Base.metadata.create_all(engine)

    #Load the users
    print('Adding users...')
    users_path = csv_dir.joinpath('users.csv')
    with users_path.open() as file:
        users_reader = DictReader(file)
        for row in users_reader:
            row['user_type'] = UserType[row['user_type']]
            User.sign_up(**row)

    print('Adding provided projects...')
    provided_path = csv_dir.joinpath('provided.csv')
    with provided_path.open() as file:
        provided_reader = DictReader(file)
        for row in provided_reader:
            row['poster'] = session.query(User).filter_by(username=row['poster']).one()
            Provided().post(**row)

    print('Adding solicited projects...')
    solicited_path = csv_dir.joinpath('solicited.csv')
    with solicited_path.open() as file:
        solicited_reader = DictReader(file)
        for row in solicited_reader:
            row['poster'] = session.query(User).filter_by(username=row['poster']).one()
            Solicited().post(**row)

    print('finished!')
    session.commit()
    session.close()
