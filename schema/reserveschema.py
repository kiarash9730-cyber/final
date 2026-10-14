from datetime import time, timedelta
from Entity.RESERVATION import RESERVATION
from pydantic import BaseModel, ConfigDict, Field, field_validator



class CreateReservationSchema(BaseModel):

    
    ticket_id : int = Field(..., description="The unique identifier for the ticket")
    number_of_tickets : int = Field(ge=1, le=4)
    

class ResponsesReservationSchema(BaseModel):

    id :int
    ticket_id: int
    number_of_tickets: int 
    status: str
    time: time

    @classmethod
    def from_entity(cls, reservation: list[RESERVATION]):
        value = reservation.event_time
        
        if isinstance(value, timedelta):
                total_seconds = int(value.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
        
                value = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        elif isinstance(value, time):
                value = value.strftime("%H:%M:%S")
                
        return cls(
            id = reservation.id,
            ticket_id=reservation.ticket_id,
            number_of_tickets=reservation.number_of_tickets,
            status=reservation.status,
            time=value
        )