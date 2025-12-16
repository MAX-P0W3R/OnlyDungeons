import random
from typing import Dict, Tuple
from game.player import Player
from game.world import initialize_rooms, get_available_exits, describe_room

class GameEngine:
    @staticmethod
    def roll_d6():
        """Simulate a D6 roll"""
        return random.randint(1, 6)
    
    @staticmethod
    def new_game():
        """Create a new game state"""
        return {
            'player': Player(health=5, strength=5, gold=0, inventory=[]).to_dict(),
            'current_room': 'Liminal Space',
            'round_number': 1,
            'total_rounds': 30,
            'rooms': initialize_rooms(),
            'game_over': False,
            'victory': False
        }
    
    @staticmethod
    def process_command(command: str, state: Dict) -> Dict:
        """Process a player command and return updated state + message"""
        parts = command.strip().split()
        if not parts:
            return {'output': 'Please enter a command.', 'state': state}
        
        action = parts[0].lower()
        params = parts[1:] if len(parts) > 1 else []
        
        # Route to appropriate handler
        if action in ['look', 'l']:
            return GameEngine._look(state)
        elif action in ['go', 'move']:
            return GameEngine._go(params, state)
        elif action == 'attack':
            return GameEngine._attack(state)
        elif action in ['get', 'take']:
            return GameEngine._get(params, state)
        elif action in ['inventory', 'i']:
            return GameEngine._inventory(state)
        elif action == 'roll':
            return GameEngine._roll(state)
        elif action == 'help':
            return GameEngine._help(state)
        else:
            return {'output': "Invalid command. Type 'help' for available commands.", 'state': state}
    
    @staticmethod
    def _look(state):
        """Look around the current room"""
        description = describe_room(state['rooms'], state['current_room'])
        return {'output': description, 'state': state}
    
    @staticmethod
    def _go(params, state):
        """Move to another room"""
        if not params:
            return {'output': "Go where? Specify a direction (north, south, east, west).", 'state': state}
        
        direction = params[0].title()
        current_room = state['current_room']
        rooms = state['rooms']
        
        if direction not in get_available_exits(rooms, current_room):
            return {'output': f"You can't go {direction} from here.", 'state': state}
        
        next_room = rooms[current_room][direction]
        
        # Check if boss room is locked
        if next_room == "The Rotten Temple Room" and rooms[next_room].get("Locked", False):
            player = Player.from_dict(state['player'])
            if not player.has_key:
                return {'output': "The door to The Rotten Temple Room is locked. You need to find a key.", 'state': state}
            else:
                rooms[next_room]["Locked"] = False
                state['current_room'] = next_room
                state['round_number'] += 1
                return {'output': f"You use the key to unlock the door and enter {next_room}.", 'state': state}
        
        state['current_room'] = next_room
        state['round_number'] += 1
        
        # Auto-look at new room
        description = describe_room(rooms, next_room)
        return {'output': f"You travel {direction} to {next_room}.\n\n{description}", 'state': state}
    
    @staticmethod
    def _attack(state):
        """Attack an enemy in the current room"""
        current_room = state['current_room']
        room_data = state['rooms'][current_room]
        
        if 'Enemy' not in room_data:
            return {'output': "There's no enemy here to attack.", 'state': state}
        
        # Conduct combat
        result = GameEngine._combat(state)
        state['round_number'] += 1
        
        return result
    
    @staticmethod
    def _combat(state):
        """Handle combat between player and enemy"""
        player = Player.from_dict(state['player'])
        current_room = state['current_room']
        enemy = state['rooms'][current_room]['Enemy']
        
        combat_log = [f"⚔️ Combat with {enemy['Name']}!"]
        combat_log.append(f"You: {player.health} HP / {player.strength} STR | {enemy['Name']}: {enemy['Health']} HP / {enemy['Strength']} STR\n")
        
        # Initiative
        player_init = GameEngine.roll_d6()
        enemy_init = GameEngine.roll_d6()
        combat_log.append(f"Initiative - You: {player_init} | Enemy: {enemy_init}")
        
        player_turn = player_init >= enemy_init
        if player_turn:
            combat_log.append("You strike first!\n")
        else:
            combat_log.append("The enemy strikes first!\n")
        
        # Combat loop
        round_num = 1
        while player.health > 0 and enemy['Health'] > 0:
            combat_log.append(f"--- Round {round_num} ---")
            
            if player_turn:
                # Player attacks
                roll = GameEngine.roll_d6()
                damage = roll * player.strength
                enemy['Health'] -= damage
                combat_log.append(f"You roll {roll}! You deal {damage} damage to {enemy['Name']}.")
                
                if enemy['Health'] <= 0:
                    combat_log.append(f"\n✅ Victory! You defeated the {enemy['Name']}!")
                    
                    # Rewards
                    if enemy.get('IsFinalBoss', False):
                        player.gold += 3
                        combat_log.append("🏆 Final boss defeated! You earn 3 gold!")
                        state['victory'] = True
                        state['game_over'] = True
                    else:
                        player.gold += 1
                        combat_log.append("💰 You earn 1 gold!")
                    
                    # Check for key
                    if enemy.get('HasKey', False):
                        player.has_key = True
                        player.inventory.append("Dungeon Key")
                        combat_log.append("🔑 You found a key! This unlocks the final boss room.")
                    
                    # Collect item
                    if 'Item' in state['rooms'][current_room]:
                        item = state['rooms'][current_room]['Item']
                        if item not in player.inventory:
                            player.inventory.append(item)
                            combat_log.append(f"📦 You collected the {item}!")
                    
                    # Remove enemy
                    del state['rooms'][current_room]['Enemy']
                    break
            else:
                # Enemy attacks
                roll = GameEngine.roll_d6()
                damage = roll * enemy['Strength']
                player.health -= damage
                combat_log.append(f"{enemy['Name']} rolls {roll}! It deals {damage} damage to you.")
                
                if player.health <= 0:
                    combat_log.append("\n💀 You have been defeated! Game Over.")
                    state['game_over'] = True
                    break
            
            player_turn = not player_turn
            combat_log.append(f"Your HP: {player.health} | {enemy['Name']} HP: {enemy['Health']}\n")
            round_num += 1
        
        # Update state
        state['player'] = player.to_dict()
        return {'output': '\n'.join(combat_log), 'state': state}
    
    @staticmethod
    def _get(params, state):
        """Pick up an item"""
        if not params:
            return {'output': "Get what? Specify an item.", 'state': state}
        
        item_name = ' '.join(params).title()
        current_room = state['current_room']
        room_data = state['rooms'][current_room]
        
        if 'Enemy' in room_data:
            return {'output': "You must defeat the enemy first!", 'state': state}
        
        if 'Item' not in room_data:
            return {'output': "There's no item here to get.", 'state': state}
        
        item = room_data['Item']
        player = Player.from_dict(state['player'])
        
        if item_name != item:
            return {'output': f"Can't find '{item_name}' here.", 'state': state}
        
        if item in player.inventory:
            return {'output': f"You already have the {item}.", 'state': state}
        
        player.inventory.append(item)
        state['player'] = player.to_dict()
        
        return {'output': f"✅ {item} retrieved!", 'state': state}
    
    @staticmethod
    def _inventory(state):
        """Check inventory"""
        player = Player.from_dict(state['player'])
        if not player.inventory:
            return {'output': "Your inventory is empty.", 'state': state}
        
        inv_list = '\n'.join(f"  • {item}" for item in player.inventory)
        return {'output': f"Your inventory:\n{inv_list}", 'state': state}
    
    @staticmethod
    def _roll(state):
        """Roll dice for fun"""
        rolls = [GameEngine.roll_d6() for _ in range(4)]
        return {'output': f"🎲 Dice rolls: {', '.join(map(str, rolls))}", 'state': state}
    
    @staticmethod
    def _help(state):
        """Show help"""
        help_text = """Available Commands:
- look (l) - Examine your current room
- go [direction] - Move (north, south, east, west)
- attack - Fight an enemy in the room
- get [item] - Pick up an item
- inventory (i) - Check your items
- roll - Roll some dice
- help - Show this message"""
        return {'output': help_text, 'state': state}
