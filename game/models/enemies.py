from dataclasses import dataclass
import random
from typing import Dict

@dataclass
class Enemy:
    name: str
    health: int = 0
    strength: int = 0
    is_final_boss: bool = False
    has_key: bool = False

    def roll_stats(self):
        """Roll random stats for the enemy"""
        self.health = random.randint(1, 6)
        self.strength = random.randint(1, 6)
        
    def to_dict(self) -> Dict:
        """Convert Enemy to dictionary for room storage"""
        return {
            'Name': self.name,
            'Health': self.health,
            'Strength': self.strength,
            'IsFinalBoss': self.is_final_boss,
            'HasKey': self.has_key
        }

def create_enemy_bank():
    """Create a bank of enemies that can be assigned to rooms"""
    enemies = [
        Enemy(name="Ghoul"),
        Enemy(name="Ghost"),
        Enemy(name="Goblin"),
        Enemy(name="Vampire"),
        Enemy(name="Skeleton"),
        Enemy(name="Zombie"),
        Enemy(name="Wraith"),
        Enemy(name="Brigand"),
        Enemy(name="Bandit"),
        Enemy(name="Ogre"),
        Enemy(name="Troll"),
        Enemy(name="Black Cat"),
        Enemy(name="Giant Rat"),
        Enemy(name="Slime"),
        Enemy(name="Dragon Butt", is_final_boss=True)
    ]
    
    # Roll random stats for each enemy
    for enemy in enemies:
        enemy.roll_stats()

    # Randomly select one non-boss enemy to have the key
    key_holder = random.choice([e for e in enemies if not e.is_final_boss])
    key_holder.has_key = True
        
    return enemies
