from time import gmtime, strftime

from DB.dbConnection import DBConnection as db

theTime = strftime("%Y-%m-%d", gmtime())
temperature = 10
humidity = 50

db.execute_query("INSERT INTO climate VALUES (?,?,?)", (theTime, temperature, humidity))
db.connection.commit()