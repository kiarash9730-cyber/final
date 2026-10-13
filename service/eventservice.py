from repository.event import EventRepository

class EventService:
    def __init__(self):
        self.repository = EventRepository()

    def show_all_events(self):
        events = self.repository.show_all_events()
        return events

    def make_event(self, time: str, capacity: int, price: float):
        event = self.repository.make_event(time, capacity, price)
        return event

    def show_event_by_id(self, event_id: int):
        event = self.repository.show_event_by_id(event_id)
        if event:
            return event
        else:
            raise ValueError("this user doesnt exist")