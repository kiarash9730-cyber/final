from datetime import time, timedelta
from Entity.EVENT import EVENT
from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventCreate(BaseModel):
    event_time: int = Field(ge=0, le=24)
    capacity: int = Field(gt=0)
    ticket_price: int = Field(ge=0)




class EventResponse(BaseModel):
    id: int
    event_time: time
    capacity: int
    ticket_price: int

    @classmethod
    def from_entity(cls, event: EVENT):
        value = event.time

        if isinstance(value, timedelta):
            total_seconds = int(value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            value = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        elif isinstance(value, time):
            value = value.strftime("%H:%M:%S")

        else:
            value = str(value)
        return cls(
            id=event.id,
            event_time=value,
            capacity=event.capacity,
            ticket_price=event.price
        )




class EventDetailResponse(BaseModel):
    remaining_capacity: int

    @classmethod
    def from_entity(cls,event:EVENT):
        return cls(remaining_capacity = event.capacity)

    