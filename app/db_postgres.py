import logging

import psycopg2

from app.config import Config


class PostgreSQL(Config):
    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                host=self.DB_HOST,
                database=self.DATABASE,
                user=self.USER,
                password=self.PASSWORD
            )
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)
            raise e
        return self.connection, self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

