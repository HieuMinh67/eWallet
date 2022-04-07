import logging

import psycopg2

# TODO: move this to config file
DB_HOST = "localhost"
DATABASE = "e_wallet"
USER = "hocvien_dev"
PASSWORD = "123456"


class PostgreSQL:
    db_host = DB_HOST
    database = DATABASE
    user = USER
    password = PASSWORD

    def connect(self):
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return conn
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)
            raise e


# TODO: find better way to init session
session = PostgreSQL().connect()
