import fastapi
from delivery.eventdelivery import event_delivery
from delivery.reservedelivery import reservation_delivery

from service.eventservice import EventService
from service.reserveservice import ReserveService

app = fastapi.FastAPI()

event_service = EventService()
reservation_service = ReserveService()

app.include_router(event_delivery(event_service))
app.include_router(reservation_delivery(reservation_service))