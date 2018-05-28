#coding=utf-8
import sqlite3
import logging
import traceback
from pprint import pprint
from logconfig import logger
class MyDataBase (object):

    def __init__(self, database_name="test.db"):
        self.conn = sqlite3.connect(database_name)

    def _commit(self):
        self.conn.commit()

    # class Cursor():
    #     def __init__(self, conn):
    #         self.conn = conn
    #
    #     def __enter__(self):
    #         self.cursor = self.conn.cursor()
    #         return self.cursor
    #
    #     def __exit__(self, exc_type, exc_val, exc_tb):
    #
    #         if exc_tb is None:
    #             self.cursor.close()
    #         else:
    #             self.cursor.close()
    #             # raise sqlite3.OperationalError

    def _execute(self, sql):
       """execute sql command."""
       try:
            self.conn.execute(sql)
            self.conn.commit()
       except:
            self.conn.rollback()
            raise

    def create_table(self, table_name):
        """create table in database.
        table_name:type:string
        """
        sql = "CREATE TABLE IF NOT EXISTS " + str(table_name) + " (IMSI INTEGER PRIMARY KEY NOT NULL);"
        try:
            self._execute(sql)
        except:
            raise

    def drop_table(self, table_name):
        """drop table from database.
        table_name:type:string
        """
        sql = "DROP TABLE IF EXISTS " + str(table_name) + ";"
        try:
            self._execute(sql)
        except:
            raise

    def insert(self, table_name, value):
        """insert data to database table.
        table_name:type:string
        value:type:string
        """
        sql = "INSERT INTO " + str(table_name) + " (IMSI) VALUES(" + str(value) + ");"
        try:
            self._execute(sql)
        except:
            raise

    def delete(self, table_name, value):
        """delete data from database table.
        table_name:type:string
        value:type:string
        """
        sql = "DELETE FROM " + str(table_name) + " (IMSI) VALUES(" + str(value) + ");"
        try:
            self._execute(sql)
        except:
            raise

    def update(self, table_name, value):
        """update database table.
        table_name:type:string
        value:type:string
        """
        sql = "UPDATE " + str(table_name) + " SET " + "IMSI = " + str(value) + ";"
        try:
            self._execute(sql)
        except:
            raise

    # def query(self, table_name, value):
    #     """query database table.
    #     table_name:type:string
    #     value:type:string
    #     """
    #     sql = "SELECT IMSI FROM " + str(table_name) + " WHERE IMSI=%s" % value
    #     try:
    #         with self.Cursor(self.conn) as cur:
    #             cursor = cur.execute(sql)
    #             row = cursor.fetchone()
    #         return row
    #     except:
    #         raise

    def query(self, table_name, value):
        """query database table.
        table_name:type:string
        value:type:string
        """
        sql = "SELECT IMSI FROM " + str(table_name) + " WHERE IMSI=%s" % value
        try:
            cu = self.conn.cursor()
            cu.execute(sql)
            row = cu.fetchone()
            return row
        except Exception as e:
            logger.error(e)
            cu.close()


    def close(self):
        """close the connection of database."""
        self.conn.close()



if __name__ == '__main__':
    db = MyDataBase()
    row = db.query('mobilecomm', '11111111111')
    if row is not None:
        print("existed!")






