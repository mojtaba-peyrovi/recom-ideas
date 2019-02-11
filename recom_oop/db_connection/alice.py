import os
import pymysql.cursors

alice_db_username = os.environ.get('ALICE_DB_USERNAME')
alice_db_password = os.environ.get('ALICE_DB_PASSWORD')
alice_db_url = os.environ.get('ALICE_DB_URL')

if alice_db_username is None or alice_db_password is None or alice_db_url is None:
    raise EnvironmentError(
        'Missing environment variable: ALICE_DB_USERNAME, ALICE_DB_PASSWORD, ALICE_DB_URL')


class alice_engine(object):
    def __init__(self, database_name):
        self.connection = pymysql.connect(
        host = alice_db_url,
        user = alice_db_username,
        password = alice_db_password,
        db = database_name,
        charset = 'utf8'
        )
