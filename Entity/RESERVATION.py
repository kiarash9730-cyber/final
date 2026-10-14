from dataclasses import dataclass

@dataclass
class RESERVATION:
    id :int
    ticket_id: int
    status: str
    event_time:str
    number_of_tickets:int