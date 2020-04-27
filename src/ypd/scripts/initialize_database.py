import platform
import subprocess
from csv import DictReader
from pathlib import Path

from sqlalchemy import Boolean, Column, MetaData, String, Table, insert

from .. import config, relative_path
from ..model import Base, Session, engine, ycp_engine
from ..model.project import Provided, Solicited
from ..model.user import User


def main():
    csv_dir=Path(f'{relative_path}/csv')

    print('Creating ycp database')
    metadata = MetaData()
    ycp_users = Table('users', metadata,
    Column('username', String), Column('current_student', Boolean), Column('current_faculty', Boolean))
    metadata.create_all(ycp_engine)

    ycp_path = csv_dir.joinpath('ycp_users.csv')
    with ycp_path.open() as file:
        ycp_reader = DictReader(file)
        ins = ycp_users.insert()
        for row in ycp_reader:
            row['current_student'] = True if row['current_student'] == 'True' else False
            row['current_faculty'] = True if row['current_faculty'] == 'True' else False
            ycp_engine.execute(ins.values(**row))

    print('Creating ypd database')
    session = Session()
    Base.metadata.create_all(engine)

    #Load the users
    print('Adding users...')
    users_path = csv_dir.joinpath('users.csv')
    with users_path.open() as file:
        users_reader = DictReader(file)
        for row in users_reader:
            row['is_admin'] = True if row['is_admin'] == 'True' else False
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
