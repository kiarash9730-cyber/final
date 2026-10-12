
from Entity.EVENT import EVENT
from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventCreate(BaseModel):
    event_time: str = Field()
    capacity: int = Field(gt=0)
    ticket_price: int = Field(ge=0)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value

class EventResponse(BaseModel):
    id: int
    event_time: str
    capacity: int
    ticket_price: int

    @classmethod
    def from_entity(cls, event: EVENT):
        return cls(
            id=event.id,
            event_time=event.time,
            capacity=event.capacity,
            ticket_price=event.price
        )




class EventDetailResponse(BaseModel):
    remaining_capacity: int

    @classmethod
    def from_entity(cls,event:EVENT):
        return cls(remaining_capacity = event.capacity)

    