from dataclasses import dataclass

@dataclass
class EVENT:
    id :int
    time: str
    capacity: int
    price: int