from database.database import DB
from Entity.EVENT import EVENT

db = DB()

class EventRepository:
    def __init__(self):
        self.connection = db.get_connection()

    def show_all_events(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        cursor.close()
        return [EVENT(id=event['id'], time=event['time'], capacity=event['capacity'], price=event['price']) for event in events]

    def make_event(self, time: int, capacity: int, price: float):
        cursor = self.connection.cursor(dictionary=True)
        event_time = f"{time:02d}:00:00"
        cursor.execute("INSERT INTO events (time, capacity, price) VALUES (%s, %s, %s)", (event_time, capacity, price))
        self.connection.commit()
        

        user_id = cursor.lastrowid
        user = cursor.execute("SELECT * FROM events WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return EVENT(id=user['id'], time=user['time'], capacity=user['capacity'], price=user['price'])

    def show_event_by_id(self, event_id: int):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return EVENT(id=user['id'], time=user['time'], capacity=user['capacity'], price=user['price'])
        else:
            return None


