from fastapi import APIRouter , HTTPException
from schema.reserveschema import ResponsesReservationSchema, CreateReservationSchema

def reservation_delivery(service):
    app = APIRouter(prefix="/reservations", tags=["Reservations"])

    @app.post("/reserve")
    def reserve_ticket(reservation: CreateReservationSchema):
        result = service.reserve_ticket(reservation.ticket_id, reservation.number_of_tickets)
        if result == "Ticket already reserved":
            raise HTTPException(status_code=400, detail=result)
        elif result == "this event doesnt exist":
            raise HTTPException(status_code=404, detail=result)
        elif result == "Not enough capacity":
            raise HTTPException(status_code=400, detail=result)
        
        return {"message": "Reservation created successfully"}

    @app.post("/confirm/{ticket_id}")
    def confirm_reservation(ticket_id: int):
        result = service.confirm_reservation(ticket_id)
        if result == "expired":
            raise HTTPException(status_code=400, detail="Reservation has expired")
        elif result == "Reservation is not in a reserved state":
            raise HTTPException(status_code=400, detail=result)
        elif result == "Reservation does not exist":
            raise HTTPException(status_code=404, detail=result)
        return {"message": "Reservation confirmed successfully"}

    @app.post("/cancel/{ticket_id}")
    def cancel_reservation(ticket_id: int):
        result = service.cancel_reservation(ticket_id)
        if result == "expired":
            raise HTTPException(status_code=400, detail="Reservation has expired")
        elif result == "Reservation is not in a reserved state":
            raise HTTPException(status_code=400, detail=result)
        elif result == "Reservation does not exist":
            raise HTTPException(status_code=404, detail=result)
        
        return {"message": "Reservation canceled successfully"}

    @app.get("/show", response_model=list[ResponsesReservationSchema])
    def show_reservations():
        reservations = service.show_reservations()
        return [ResponsesReservationSchema.from_entity(reservation) for reservation in reservations]

    return app