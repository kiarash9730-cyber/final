import mysql.connector
import redis

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

class Redis:
    def __init__(self):
        self.redis = redis.Redis(
            host="127.0.0.1",
            port=6379,
            db=0,
            decode_responses=True
        )
    def check_conn(self):
        return self.redis.ping()

    def get_connection(self):
        return self.redis