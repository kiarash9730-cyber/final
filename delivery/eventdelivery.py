from fastapi import APIRouter , HTTPException
from eventschema import EventCreate, EventResponse,EventDetailResponse


def event_delivery(service):
    app = APIRouter("/events", methods=["GET", "POST"])

    @app.get("/", response_model=list[EventResponse])
    def show_all_events():
        return service.show_all_events()

    @app.post("/post", response_model=EventCreate)
    def make_event(event: EventCreate):
        return service.make_event(time=event.event_time, capacity=event.capacity, price=event.ticket_price)

    @app.get("/events/{event_id}", response_model=EventDetailResponse)
    def show_event_by_id(event_id: int):
        return service.show_event_by_id(event_id)

    return app