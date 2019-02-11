import os
import pymysql.cursors

ihub_db_username = os.environ.get('IHUB_DB_USERNAME')
ihub_db_password = os.environ.get('IHUB_DB_PASSWORD')
ihub_db_url = os.environ.get('IHUB_DB_URL')

if ihub_db_username is None or ihub_db_password is None or ihub_db_url is None:
    raise EnvironmentError(
        'Missing environment variable: IHUB_DB_USERNAME, IHUB_DB_PASSWORD, IHUB_DB_URL')


class iHub_engine(object):
    def __init__(self, database_name):
        self.connection = pymysql.connect(
        host = ihub_db_url,
        user = ihub_db_username,
        password = ihub_db_password,
        db = database_name,
        charset = 'utf8'
        )
