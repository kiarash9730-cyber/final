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

    def sub_capacity(self, event_id:int,number_of_tickets):
        cursor = self.connection.cursor(dictionary=True)
        capacity = cursor.execute("select * from events where id = %s", (event_id,))
        capacity = cursor.fetchone()

        if capacity["capacity"] < number_of_tickets:
            cursor.close()
            return "Not enough capacity"
        else:
        
            cursor.execute("UPDATE events SET capacity = capacity - %s WHERE id = %s", (number_of_tickets ,event_id))
            self.connection.commit()
            cursor.close()
            return "Capacity updated"

    def add_capacity(self,event_id):
        cursor = self.connection.cursor(dictionary=True)

        number_of_tickets = cursor.execute("select * from reserve where id = %s ", (event_id,)) 
        number_of_tickets = cursor.fetchone()

        cursor.execute("UPDATE events SET capacity = capacity + %s WHERE id = %s", (number_of_tickets["number_of_tickets"],number_of_tickets["ticket_id"]))
        self.connection.commit()

