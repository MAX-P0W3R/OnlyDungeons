from typing import Dict, List
import random
from game.models.enemies import create_enemy_bank

ROOM_KEYS = {"Item", "Enemy", "Description"}

def create_treasure_list() -> List[str]:
    """Create a list of possible treasures"""
    return [
        "Crystal", "Staff", "Sword", "Skull", "Glass Eye of Mystery",
        "Heavy Shield", "Ancient Amulet", "Enchanted Dagger",
        "Golden Chalice", "Magic Scroll", "Spectral Orb", "Dragon Scale",
        "Mystic Gem", "Runic Tablet", "Treasure Chest"
    ]

def initialize_rooms() -> Dict:
    """Initialize the dungeon rooms"""
    rooms = {
        'Liminal Space': {
            'North': 'Mirror Maze',
            'South': 'Bat Cavern',
            'East': 'Bazaar',
            'Description': 'You step into the first chamber of the dungeon, your boots scraping against the rough, uneven stone floor. The air is damp and heavy, carrying the faint, metallic tang of rust and the acrid bite of mildew. The walls glisten faintly with moisture, their surfaces etched with marks of age and strange, cryptic symbols worn smooth by time. The faint sound of water dripping echoes through the chamber, rhythmic and hollow, as if the dungeon itself has a heartbeat.\n\nSomewhere in the distance, you think you hear the faint scuttle of claws on stone or the muted whisper of something unseen shifting in the shadows. A faint draft snakes through the room, cool and clammy against your skin, as though the dungeon is breathing, its cold exhale brushing past you. The dim light from your torch dances erratically, casting long, flickering shadows that seem to stretch and writhe across the walls.\n\nThis place feels alive...watching, waiting, testing your resolve. The adventure has begun! What will you do next?'
        },
        'Mirror Maze': {
            'South': 'Liminal Space',
            'Item': 'Crystal',
            'Description': 'A room full of dusty mirrors!'
        },
        'Bat Cavern': {
            'North': 'Liminal Space',
            'East': 'Great Hall',
            'Item': 'Staff',
            'Description': 'BATS! Everywhere! You are in bat country!'
        },
        'Great Hall': {
            'West': 'Bat Cavern',
            'Item': 'Sword',
            'Description': 'The Great Hall is dimly lit by candles placed on stone shelves around the perimeter. A large stone slab dominates the center of the room.'
        },
        'Bazaar': {
            'West': 'Liminal Space',
            'North': 'Pit of Pendulums',
            'East': 'The Rotten Temple Room',
            'Item': 'Skull',
            'Description': 'Abandoned merchant stalls line the walls of this once-bustling marketplace. The scent of exotic spices still lingers in the air.'
        },
        'Pit of Pendulums': {
            'South': 'Bazaar',
            'East': 'Tomb of the Forgotten',
            'Item': 'Glass Eye of Mystery',
            'Description': 'Massive metal pendulums swing silently back and forth across this chamber. The floor is lined with ominous dark stains.'
        },
        'Tomb of the Forgotten': {
            'West': 'Pit of Pendulums',
            'Item': 'Heavy Shield',
            'Description': 'Ancient sarcophagi line the walls of this dusty chamber. The names of the deceased have been worn away by time.'
        },
        'The Rotten Temple Room': {
            'West': 'Bazaar',
            'Item': 'Treasure Chest',
            'Description': 'The location description.',
            'Locked': True
        }
    }
    
    # Assign random treasures and enemies
    _assign_random_treasures(rooms)
    _assign_random_enemies(rooms)
    
    return rooms

def _assign_random_treasures(rooms):
    """Assign random treasures to rooms"""
    available_treasures = create_treasure_list()
    random.shuffle(available_treasures)
    
    # Always treasure chest in boss room
    rooms['The Rotten Temple Room']['Item'] = "Treasure Chest"
    
    # Assign to other rooms
    rooms_for_treasures = [
        room for room in rooms 
        if room != 'Liminal Space' and room != 'The Rotten Temple Room'
    ]
    
    for room_name in rooms_for_treasures:
        if available_treasures:
            treasure = available_treasures.pop()
            rooms[room_name]['Item'] = treasure

def _assign_random_enemies(rooms):
    """Assign random enemies to rooms"""
    enemy_bank = create_enemy_bank()
    
    # Final boss in boss room
    final_boss = next(e for e in enemy_bank if e.is_final_boss)
    enemy_bank.remove(final_boss)
    rooms['The Rotten Temple Room']['Enemy'] = final_boss.to_dict()
    
    # Key holder gets assigned
    key_holder = next(e for e in enemy_bank if e.has_key)
    
    rooms_needing_enemies = [
        room for room in rooms 
        if room != 'Liminal Space' and room != 'The Rotten Temple Room'
    ]
    
    # Assign key holder
    if rooms_needing_enemies:
        key_room = random.choice(rooms_needing_enemies)
        rooms[key_room]['Enemy'] = key_holder.to_dict()
        rooms_needing_enemies.remove(key_room)
        enemy_bank.remove(key_holder)
    
    # Assign remaining enemies
    for room_name in rooms_needing_enemies:
        if enemy_bank:
            enemy = enemy_bank.pop()
            rooms[room_name]['Enemy'] = enemy.to_dict()

def get_available_exits(rooms, room_name):
    """Get available exits from a room"""
    return [key for key in rooms[room_name] if key not in ROOM_KEYS]

def describe_room(rooms, room_name):
    """Generate a description of the current room"""
    room_data = rooms[room_name]
    description = room_data.get("Description", "Nothing special here.")
    exits = get_available_exits(rooms, room_name)
    exit_str = ", ".join(exits)
    msg = f"{description}\n\nExits: {exit_str}"

    if "Enemy" in room_data:
        enemy = room_data["Enemy"]
        msg += f"\n\nEnemy: {enemy['Name']} ({enemy['Health']} HP / {enemy['Strength']} STR)"

    if "Item" in room_data:
        item = room_data["Item"]
        msg += f"\nItem: {item}"

    return msg
