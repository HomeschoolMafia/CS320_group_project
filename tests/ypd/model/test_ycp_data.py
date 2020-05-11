from unittest import TestCase

from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table, create_engine

from ypd.model import ycp_data


class TestUser(TestCase):
    @classmethod
    def setUpClass(self):
        self.ycp_engine = create_engine('sqlite:///')
        ycp_data.ycp_engine = self.ycp_engine
        metadata = MetaData()
        ycp_users = Table('users', metadata,
        Column('username', String), Column('current_student', Boolean), Column('current_faculty', Boolean),
        Column('name', String), Column('credits', Integer), Column('major', String))
        metadata.create_all(self.ycp_engine)
        ins = ycp_users.insert()
        self.ycp_engine.execute(ins.values(current_student=True, current_faculty=False, name='my name', username='mname4', credits=13, major='major'))

    def test_valid_user(self):
        ycp_data_object = ycp_data.YCPData('mname4')
        data = ycp_data_object.get_data()
        self.assertTrue(ycp_data_object.is_valid)
        self.assertTrue(data[0])
        self.assertFalse(data[1])
        self.assertEqual(data[2], 'my name')
        self.assertEqual(data[3], 13)
        self.assertEqual(data[4], 'major')

    def test_invalid_user(self):
        ycp_data_object = ycp_data.YCPData('invalid')
        self.assertFalse(ycp_data_object.is_valid)