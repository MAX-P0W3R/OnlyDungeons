# Game Engine (game/engine.py)

class GameEngine:
    @staticmethod
    def new_game():
        return {
            'current_room': 'entrance',
            'inventory': [],
            'health': 100,
            'score': 0,
            'visited_rooms': set(),
            'flags': {}
        }
    
    @staticmethod
    def get_intro():
        return """
        ADVENTURE GAME
        ==============
        
        You wake up in a dark room. The air is musty and cold.
        A single beam of light filters through a crack in the ceiling.
        
        Type 'help' for a list of commands.
        Type 'look' to examine your surroundings.
        """
    
    @staticmethod
    def process_command(command, state):
        words = command.split()
        verb = words[0] if words else ''
        
        # Command routing
        if verb in ['look', 'l']:
            return Commands.look(state)
        elif verb in ['go', 'move', 'walk']:
            direction = words[1] if len(words) > 1 else None
            return Commands.go(direction, state)
        elif verb in ['take', 'get', 'grab']:
            item = ' '.join(words[1:])
            return Commands.take(item, state)
        elif verb in ['inventory', 'i']:
            return Commands.inventory(state)
        elif verb == 'help':
            return Commands.help(state)
        else:
            return {
                'output': "I don't understand that command. Type 'help' for options.",
                'state': state
            }

class Commands:
    @staticmethod
    def look(state):
        room = Rooms.get(state['current_room'])
        return {
            'output': room.description,
            'state': state
        }
    
    @staticmethod
    def go(direction, state):
        # Implement room navigation
        pass
    
    @staticmethod
    def take(item, state):
        # Implement item pickup
        pass
    
    @staticmethod
    def inventory(state):
        if not state['inventory']:
            return {'output': 'You are carrying nothing.', 'state': state}
        items = '\n'.join(f"- {item}" for item in state['inventory'])
        return {'output': f'You are carrying:\n{items}', 'state': state}
    
    @staticmethod
    def help(state):
        return {
            'output': """
            Available commands:
            - look/l: Examine your surroundings
            - go <direction>: Move in a direction (north, south, east, west)
            - take <item>: Pick up an item
            - use <item>: Use an item from inventory
            - inventory/i: Check what you're carrying
            - help: Show this message
            """,
            'state': state
        }