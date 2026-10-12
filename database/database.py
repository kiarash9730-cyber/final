import mysql.connector

class DB:
    def __init__(self):
        self.database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kiarash1010",
            database="ticket",
            port=330
        )

    def get_connection(self):
        return self.database