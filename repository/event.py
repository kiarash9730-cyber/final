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

    def make_event(self, time: str, capacity: int, price: float):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("INSERT INTO events (time, capacity, price) VALUES (%s, %s, %s)", (time, capacity, price))
        self.connection.commit()
        

        user_id = cursor.lastrowid
        user = cursor.execute("SELECT * FROM events WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return EVENT(id=user['id'], time=user['time'], capacity=user['capacity'], price=user['price'])

    def show_event_by_id(self, event_id: int):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
        event = cursor.fetchone()
        cursor.close()
        if event:
            return EVENT(capacity=event['capacity'])
        else:
            return None


