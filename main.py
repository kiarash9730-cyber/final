import fastapi
from delivery.eventdelivery import event_delivery
from service.eventservice import EventService

app = fastapi.FastAPI()

service = EventService()
app.include_router(event_delivery(service))