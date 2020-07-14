import mysql.connector

class DBConnector(object):

    def __init__(self, host="", user="", password="", database=""):

        self.dbConnect = {
            'host' : host,
            'user' : user,
            'password' : password,
            'database' : database
        }
        self.dbconn = None

    # creats new connection
    def create_connection(self):
        return mysql.connector.connect(**self.dbConnect)

    # For explicitly opening database connection
    def __enter__(self):
        self.dbconn = self.create_connection()
        return self.dbconn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbconn.close()
        