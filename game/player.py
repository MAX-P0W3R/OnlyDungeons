from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Player:
    health: int
    strength: int
    gold: int
    inventory: List[str]
    has_key: bool = False
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def is_alive(self):
        return self.health > 0
