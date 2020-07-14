import sqlite3

from DB.dbConnector import DBConnector

class DBConnection(object):
    connection = None

    @classmethod
    def get_connection(cls):
        """Creates return new Singleton database connection"""
        if cls.connection == None:
            cls.connection = DBConnector('', '', '', '').create_connection() #put your credentianls here
        return cls.connection

    @classmethod
    def execute_query(cls, query, data):
        """execute query on singleton db connection"""
        connection = cls.get_connection()
        result = None

        try:
            cursor = connection.cursor(buffered=True)

            if (data != 0):
                cursor.execute(query, data)
            else:
                cursor.execute(query)
                result = cursor.fetchall()

        except sqlite3.ProgrammingError:
            print("Programming Error!")
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()
            
        cursor.close()

        if result != None:
            return result