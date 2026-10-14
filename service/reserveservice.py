from repository.reservation import ReservationRepository
from repository.event import EventRepository

class ReserveService:
    def __init__(self):
        self.reservation_repository = ReservationRepository()
        self.event_repository = EventRepository()

    def reserve_ticket(self, ticket_id , number_of_tickets):
        if not self.event_repository.show_event_by_id(ticket_id):
            return "this event doesnt exist"

        

        sub_capacity_result = self.event_repository.sub_capacity(
            ticket_id, number_of_tickets
        )

        if sub_capacity_result == "Not enough capacity":
            return "Not enough capacity"

        return self.reservation_repository.temporary_reservation(
            ticket_id, number_of_tickets
        )

    def confirm_reservation(self, ticket_id):
        # Confirm the reservation by removing it from Redis and updating the database
        check = self.reservation_repository.get_reservation_status(ticket_id)
    
        if check is not None:
            if check == "reserved":
                result = self.reservation_repository.confirm_reservation(ticket_id)
                if result == "expired":
                    self.event_repository.add_capacity(ticket_id)
                    return "expired"
                return result
            else:
                return "Reservation is not in a reserved state"
        else:
            return "Reservation does not exist"                                                                                     

    def cancel_reservation(self, ticket_id):

        # Cancel the reservation by removing it from Redis and updating the database
        check = self.reservation_repository.get_reservation_status(ticket_id)

        if check is not None:
            if check == "reserved":

                result = self.reservation_repository.cancel_reservation(ticket_id)
                self.event_repository.add_capacity(ticket_id)
                return result
            else:
                return "Reservation is not in a reserved state"
        else:
            return "Reservation does not exist"
    
    def show_reservations(self):
        return self.reservation_repository.show_reservations()



