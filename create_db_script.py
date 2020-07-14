from DB.dbConnection import DBConnection as db

result = db.execute_query("""CREATE TABLE IF NOT EXISTS sensores (
                                registerdate date,
                                temperature INTEGER,
                                humedity INTEGER
                            )""", 0)
