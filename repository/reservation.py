from database.database import DB, Redis
from Entity.RESERVATION import RESERVATION



class ReservationRepository:
    def __init__(self):
        self.conn = DB().get_connection()
        self.redis = Redis().get_connection()

    def temporary_reservation(self, ticket_id, number_of_tickets ):
        # Store the reservation in Redis with a TTL of 5 minutes
        
          # 300 seconds 

        cursor = self.conn.cursor()

        cursor.execute("insert into reserve (ticket_id, number_of_tickets, status) values (%s, %s, %s)", (ticket_id, number_of_tickets, "reserved"))
        self.conn.commit()

        ticket_id = cursor.lastrowid

        cursor.close()
        key = f"reservation:{ticket_id}"
        self.redis.set(key, "reserved", ex=300)

        return "success"

    def show_reservations(self):
        # Show all reservations from the database
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("select r.id, r.ticket_id, r.status , e.time , r.number_of_tickets from reserve as r join events as e on r.ticket_id = e.id")
        result = cursor.fetchall()
        cursor.close()

        return [RESERVATION(id=row['id'], ticket_id=row['ticket_id'], status=row['status'], event_time=row['time'], number_of_tickets=row['number_of_tickets']) for row in result]

    def confirm_reservation(self, ticket_id):
        # Confirm the reservation by removing it from Redis and updating the database
        check_expired = self.is_expired(ticket_id)
        cursor = self.conn.cursor()
        if not check_expired:
            key = f"reservation:{ticket_id}"
            self.redis.delete(key)

            
            cursor.execute("update reserve set status=%s where id=%s and status=%s", ("confirmed", ticket_id, "reserved"))
            self.conn.commit()
            cursor.close()
            return "success"
        else:
            key = f"reservation:{ticket_id}"
            self.redis.delete(key)
            
            cursor.execute("update reserve set status=%s where id=%s and status=%s", ("expired", ticket_id, "reserved"))
            self.conn.commit()
            cursor.close()
            return "expired"

    def cancel_reservation(self, ticket_id):
        # Cancel the reservation by removing it from Redis and updating the database
        check = self.is_expired(ticket_id)
        cursor = self.conn.cursor()
        if not check:
            key = f"reservation:{ticket_id}"
            self.redis.delete(key)


            
            cursor.execute("update reserve set status=%s where id=%s and status=%s", ("canceled", ticket_id, "reserved"))
            self.conn.commit()
            cursor.close()
            return "success"
        else:
            key = f"reservation:{ticket_id}"
            self.redis.delete(key)
            
            cursor.execute("update reserve set status=%s where id=%s and status=%s", ("expired", ticket_id, "reserved"))
            self.conn.commit()
            cursor.close()
            return "expired"

    def get_reservation_status(self, ticket_id):
        # Get the reservation status from the database
        cursor = self.conn.cursor(buffered=True)
        cursor.execute("select status from reserve where id=%s order by id desc limit 1", (ticket_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None

    def is_expired(self, reservation_id: int) -> bool:
        key = f"reservation:{reservation_id}"
        remaining = self.redis.ttl(key)

        if remaining <= 0:
            return True

        return False

    def get_reservation(self, ticket_id):
        # Check if the reservation exists in Redis
        key = f"reservation:{ticket_id}"
        if self.redis.exists(key):
            return True
        else:
            return False

    


        