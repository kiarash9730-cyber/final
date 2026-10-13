from fastapi import APIRouter , HTTPException
from schema.eventschema import EventCreate, EventResponse,EventDetailResponse


def event_delivery(service):
    app = APIRouter(prefix="/events", tags=["Events"])

    @app.get("/", response_model=list[EventResponse])
    def show_all_events():
        events = service.show_all_events()
        return [EventResponse.from_entity(event) for event in events]

    @app.post("/post", response_model=EventResponse)
    def make_event(event: EventCreate):
        event = service.make_event(time=event.event_time, capacity=event.capacity, price=event.ticket_price)
        return EventResponse.from_entity(event)

    @app.get("/{event_id}", response_model=EventDetailResponse)
    def show_event_by_id(event_id: int):
        try :
            event = service.show_event_by_id(event_id)
        except ValueError as e:
            raise HTTPException(status_code=404,detail=str(e))


        return EventDetailResponse.from_entity(event)

    return app