import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

# Constants
ROOM_KEYS = {"Item", "Enemy", "Description"}  # Using a set for faster lookups

# ANSI Color Codes
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'  
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[92m'  

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

@dataclass
class Player:
    health: int
    strength: int
    gold: int
    inventory: List[str]
    has_key: bool = False

class DungeonGame:
    def __init__(self):
        self.player = Player(health=5, strength=5, gold=0, inventory=[])
        self.current_room = "Liminal Space"
        self.round_number = 1
        self.total_rounds = 30
        self.message = ""
        self.treasures = self._create_treasure_list()
        self.enemy_bank = self._create_enemy_bank()
        self.rooms = self._initialize_rooms()

    def _create_treasure_list(self) -> List[str]:
        """Create a list of possible treasures to be randomly assigned to rooms"""
        return [
            "Crystal",
            "Staff",
            "Sword",
            "Skull",
            "Glass Eye of Mystery",
            "Heavy Shield",
            "Ancient Amulet",
            "Enchanted Dagger",
            "Golden Chalice",
            "Magic Scroll",
            "Spectral Orb",
            "Dragon Scale",
            "Mystic Gem",
            "Runic Tablet",
            "Treasure Chest"
        ]

    def _create_enemy_bank(self) -> List[Enemy]:
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
            # Final boss is always the same
            Enemy(name="Dragon Butt", is_final_boss=True)
        ]
        
        # Roll random stats for each enemy
        for enemy in enemies:
            enemy.roll_stats()

        # Randomly select one non-boss enemy to have the key
        key_holder = random.choice([e for e in enemies if not e.is_final_boss])
        key_holder.has_key = True
            
        return enemies
        
    def _initialize_rooms(self) -> Dict:
        """Initialize the dungeon rooms and set enemy stats."""
        rooms = {
            'Liminal Space': {
                'North': 'Mirror Maze',
                'South': 'Bat Cavern',
                'East': 'Bazaar',
                'Description': 'You step into the first chamber of the dungeon, your boots scraping against the rough, uneven stone floor. The air is damp\n'
                'and heavy, carrying the faint, metallic tang of rust and the acrid bite of mildew. The walls glisten faintly with\n'
                'moisture, their surfaces etched with marks of age and strange, cryptic symbols worn smooth by time.\n'
                'The faint sound of water dripping echoes through the chamber, rhythmic and hollow, as if the dungeon itself has a heartbeat.\n\n'
                'Somewhere in the distance, you think you hear the faint scuttle of claws on stone or the muted whisper of something unseen\n'
                'shifting in the shadows. A faint draft snakes through the room, cool and clammy against your skin, as though the\n'
                'dungeon is breathing, its cold exhale brushing past you. The dim light from your torch dances erratically,\n'
                'casting long, flickering shadows that seem to stretch and writhe across the walls.\n\n'
                'This place feels alive...watching, waiting, testing your resolve. The adventure has begun!\n'
                'What will you do next?\n'
            },
            'Mirror Maze': {
                'South': 'Liminal Space',
                'Item': 'Crystal',
                'Description': 'A room full of dusty mirrors!',
                #'Enemy': {'Name': 'Ghoul', 'Health': 0, 'Strength': 0},
            },
            'Bat Cavern': {
                'North': 'Liminal Space',
                'East': 'Great Hall',
                'Item': 'Staff',
                'Description': 'BATS! Everywhere! You are in bat country!',
                #'Enemy': {'Name': 'Ghost', 'Health': 0, 'Strength': 0},
            },
            'Great Hall': {
                'West': 'Bat Cavern',
                'Item': 'Sword',
                'Description': 'The Great Hall is dimly lit by candles placed on stone shelves around the perimeter. '
                'A large stone slab dominates the center of the room.',
                #'Enemy': {'Name': 'Goblin', 'Health': 0, 'Strength': 0},
            },
            'Bazaar': {
                'West': 'Liminal Space',
                'North': 'Pit of Pendulums',
                'East': 'The Rotten Temple Room',
                'Item': 'Skull',
                'Description': 'Abandoned merchant stalls line the walls of this once-bustling marketplace. '
                'The scent of exotic spices still lingers in the air.',
                #'Enemy': {'Name': 'Vampire', 'Health': 0, 'Strength': 0},
            },
            'Pit of Pendulums': {
                'South': 'Bazaar',
                'East': 'Tomb of the Forgotten',
                'Item': 'Glass Eye of Mystery',
                'Description': 'Massive metal pendulums swing silently back and forth across this chamber. '
                'The floor is lined with ominous dark stains.',
                #'Enemy': {'Name': 'Brigand', 'Health': 0, 'Strength': 0},
            },
            'Tomb of the Forgotten': {
                'West': 'Pit of Pendulums',
                'Item': 'Heavy Shield',
                'Description': 'Ancient sarcophagi line the walls of this dusty chamber. '
                'The names of the deceased have been worn away by time.',
                #'Enemy': {'Name': 'Black Cat', 'Health': 0, 'Strength': 0},
            },
            'The Rotten Temple Room': {
                'West': 'Bazaar',
                'Item': 'Treasure Chest',
                'Description': 'The location description.',
                #'Enemy': {'Name': 'Dragon Butt', 'Health': 0, 'Strength': 0, 'IsFinalBoss': True},
            }
        }
        
        # Assign random treasures to rooms (excluding starting room and final boss room)
        self._assign_random_treasures(rooms)

        # Assign random enemies to rooms (excluding starting room)
        self._assign_random_enemies(rooms)
                
        return rooms

    def _assign_random_treasures(self, rooms):
        """Assign random treasures to rooms"""
        # Create a copy of treasures that we can shuffle and pop from
        available_treasures = self.treasures.copy()
        random.shuffle(available_treasures)
        
        # Always put a special treasure in the final boss room
        if available_treasures:
            final_treasure = "Treasure Chest"  # Always a treasure chest in the boss room
            rooms['The Rotten Temple Room']['Item'] = final_treasure
            if final_treasure in available_treasures:
                available_treasures.remove(final_treasure)
        
        # Assign other treasures randomly to the remaining rooms (excluding starting room)
        rooms_for_treasures = [
            room for room in rooms 
            if room != 'Liminal Space' and room != 'The Rotten Temple Room'
        ]
        
        for room_name in rooms_for_treasures:
            if available_treasures:
                treasure = available_treasures.pop()
                rooms[room_name]['Item'] = treasure

    def _assign_random_enemies(self, rooms):
        """Assign random enemies to rooms from the enemy bank"""
        # Create a copy of enemies that we can shuffle and pop from
        available_enemies = self.enemy_bank.copy()
        
        # Always put the final boss in the Rotten Temple Room
        final_boss = next(enemy for enemy in available_enemies if enemy.is_final_boss)
        available_enemies.remove(final_boss)
        rooms['The Rotten Temple Room']['Enemy'] = final_boss.to_dict()
        
        # Find the enemy with the key
        key_holder = next(enemy for enemy in available_enemies if enemy.has_key)
        
        # Shuffle the remaining enemies
        random.shuffle([e for e in available_enemies if e != key_holder])
        
        # Assign other enemies randomly to the remaining rooms (excluding starting room)
        rooms_needing_enemies = [
            room for room in rooms 
            if room != 'Liminal Space' and room != 'The Rotten Temple Room'
        ]
        
        # Make sure key holder is assigned to a random room
        if rooms_needing_enemies:
            key_room = random.choice(rooms_needing_enemies)
            rooms[key_room]['Enemy'] = key_holder.to_dict()
            rooms_needing_enemies.remove(key_room)
            available_enemies.remove(key_holder)
        
        # Assign remaining enemies
        for room_name in rooms_needing_enemies:
            if available_enemies:
                enemy = available_enemies.pop()
                rooms[room_name]['Enemy'] = enemy.to_dict()
            else:
                # If we run out of enemies, create a new random one
                new_enemy = Enemy(name=f"Unknown {random.choice(['Creature', 'Monster', 'Beast'])}")
                new_enemy.roll_stats()
                rooms[room_name]['Enemy'] = new_enemy.to_dict()

    @staticmethod
    def clear():
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def roll_d6():
        """Simulate a D6 roll."""
        return random.randint(1, 6)

    @staticmethod
    def print_slow(text, delay=0.05):
        """Print text slowly to simulate a typing effect."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def main_menu(self):
        """Display the main menu and handle navigation."""
        while True:
            self.clear()
            print(f"{Colors.GREEN}~~~~ Welcome to the Dungeon! ~~~~\n"
                  "1. Begin the adventure\n"
                  "2. Gameplay & Rules\n"
                  "3. Commands\n"
                  "4. Exit\n")
            choice = input("Enter your selection: ")

            if choice == "1":
                self.clear()
                self.prompt()
                return  # Exit the menu loop
            elif choice == "2":
                self.clear()
                self.display_rules()
            elif choice == "3":
                self.clear()
                self.display_commands()
            elif choice == "4":
                self.clear()
                print(f"{Colors.RED}Exiting the game. Goodbye!{Colors.RESET}")
                sys.exit()
            else:
                self.clear()
                print(f"{Colors.RED}Invalid selection. Please choose a valid option.\n{Colors.RESET}")

    def prompt(self):
        """Display the introductory prompt."""
        print(f"{Colors.GREEN}\tWelcome, Brave Adventurer!\n\n\
\tYou stand at the threshold of the forgotten dungeon, a labyrinth of peril and mystery.\n\
Whispers speak of untold treasures guarded by ancient foes, each more deadly than the last.\n\
To claim victory, you must gather six legendary artifacts, hidden deep within the dungeon, each\n\
guarded by fearsome enemies.\n\n\
\tYour journey will test your courage, strategy, and skill. Armed with nothing but your wits, your dice,\n\
and your resolve, you must navigate through treacherous rooms, face off against monstrous enemies, and\n\
unearth the secrets of the dungeon.\n\n\
\tRoll the dice, make your move, and choose your actions wisely. Will you emerge victorious, or will the\n\
dungeon claim yet another soul?\n\n\
The dungeon awaits... let the adventure begin!\n{Colors.RESET}")

        input(f"{Colors.YELLOW}\tPress ENTER to continue ...\n{Colors.RESET}")

    def display_rules(self):
        """Display game rules."""
        print(f"{Colors.CYAN} <<< Gameplay & Rules >>>\n"
              " ~ You have 30 rounds to explore the dungeon.\n"
              " ~ Navigate the dungeon to find monsters, treasure, and adventure.\n"
              " ~ Defeat enemies to collect gold and items.\n"
              " ~ The game ends when you defeat the final boss or run out of rounds.\n"
              " ~ In order to unlock the door to the final boss, you must find the key first.\n")
        input("Press ENTER to continue...")

    def display_commands(self):
        """Display available commands."""
        print(f"{Colors.CYAN} <<< Commands >>>\n"
              " ~ 'Look': Inspect your current room.\n"
              " ~ 'Go [direction]': Navigate to another room (North, South, East, West).\n"
              " ~ 'Attack': Engage in combat with an enemy in the room.\n"
              " ~ 'Get [item]': Pick up an item if there's no enemy in the room.\n"
              " ~ 'Roll': Roll some dice for fun.\n"
              " ~ 'Help': Display these commands.\n"
              " ~ 'Rules': Display game rules.\n"
              " ~ 'Exit': Quit the game.\n")
        input("Press ENTER to continue...")

    def get_available_exits(self, room_name):
        """Get available exits from a room."""
        return [key for key in self.rooms[room_name] if key not in ROOM_KEYS]

    def describe_room(self, room_name):
        """Generate a description of the current room."""
        room_data = self.rooms[room_name]
        description = room_data.get("Description", "Nothing special here.")
        exits = self.get_available_exits(room_name)
        exit_str = ", ".join(exits)
        msg = f"{description}\nExits: {exit_str}"

        if "Enemy" in room_data:
            enemy = room_data["Enemy"]
            msg += f"\nEnemy: {enemy['Name']} {enemy['Health']}/{enemy['Strength']}"

        if "Item" in room_data:
            item = room_data["Item"]
            msg += f"\nItem: {item}"

        return msg

    def combat(self, enemy_name, room_name):
        """Handle combat between player and enemy."""
        room_data = self.rooms[room_name]
        if "Enemy" not in room_data:
            return False, f"No enemy named {enemy_name} is present in this room."

        enemy = room_data["Enemy"]
        print(f"{Colors.RED}You have encountered a {enemy_name}!")
        print(f"Player: {self.player.health} HP / {self.player.strength} STR | {enemy_name}: {enemy['Health']} HP / {enemy['Strength']} STR{Colors.RESET}")

        # Initiative Roll
        input(f"{Colors.YELLOW}Press Enter to roll for initiative...{Colors.RESET}")
        player_initiative = self.roll_d6()
        enemy_initiative = self.roll_d6()
        print(f"\nYou rolled {player_initiative} for initiative!")
        print(f"The {enemy_name} rolled {enemy_initiative} for initiative!")

        # Determine who attacks first
        player_turn = player_initiative >= enemy_initiative  # Player goes first on a tie
        if player_turn:
            print("You have the initiative and will attack first!")
        else:
            print(f"The {enemy_name} has the initiative and will attack first!")

        # Combat Loop
        while self.player.health > 0 and enemy["Health"] > 0:
            if player_turn:
                # Player's attack
                input("Press Enter to roll for your attack...")
                player_roll = self.roll_d6()
                player_damage = player_roll * self.player.strength
                enemy["Health"] -= player_damage
                print(f"You rolled {player_roll}! You deal {player_damage} damage to the {enemy_name}.")

                if enemy["Health"] <= 0:
                    print(f"You defeated the {enemy_name}!")
                    # Grant gold to the player
                    if enemy.get("IsFinalBoss", False):
                        self.player.gold += 3
                        print("You defeated the final boss! You earn 3 gold!")
                    else:
                        self.player.gold += 1
                        print("You earn 1 gold!")
                    print(f"Your total gold: {self.player.gold}")

                    # Check if enemy had the key
                    if enemy.get("HasKey", False):
                        self.player.has_key = True
                        self.player.inventory.append("Dungeon Key")
                        print(f"{Colors.YELLOW}You found a key on the {enemy_name}! This will allow you to enter the final boss room.{Colors.RESET}")

                    # Add room item to inventory, if present
                    if "Item" in room_data:
                        item = room_data["Item"]
                        if item not in self.player.inventory:
                            self.player.inventory.append(item)
                            print(f"You found and collected the {item}!")

                    # Remove the enemy from the room
                    del room_data["Enemy"]
                    return True, f"You defeated the {enemy_name}!"  # Player wins
            else:
                # Enemy's attack
                input(f"The {enemy_name} attacks! Press Enter to roll for defense...")
                enemy_roll = self.roll_d6()
                enemy_damage = enemy_roll * enemy["Strength"]
                self.player.health -= enemy_damage
                print(f"The {enemy_name} rolled {enemy_roll}! It deals {enemy_damage} damage to you.")

                if self.player.health <= 0:
                    print(f"\nYou have succumbed to a fatal blow and been defeated by the {enemy_name}!")
                    print("~~~ Game Over ~~~")
                    sys.exit()

            # Switch turns
            player_turn = not player_turn

            # Show updated health after each round
            print(f"\nYour Health: {self.player.health} | {enemy_name}'s Health: {enemy['Health']}")

        return False, "Combat ended unexpectedly."  # Failsafe if combat ends unexpectedly

    def process_action(self, action, params=None):
        """Process player action."""
        if action == "Go":
            if params and params[0] in self.get_available_exits(self.current_room):
                direction = params[0]
                next_room = self.rooms[self.current_room][direction]
                
                # Check if the player is trying to enter the locked boss room
                if next_room == "The Rotten Temple Room" and self.rooms[next_room].get("Locked", False):
                    if not self.player.has_key:
                        return f"{Colors.RED}The door to {next_room} is locked. You need to find a key.{Colors.RESET}"
                    else:
                        print(f"{Colors.GREEN}You use the key to unlock the door to {next_room}.{Colors.RESET}")
                        self.rooms[next_room]["Locked"] = False
                
                self.current_room = next_room
                self.round_number += 1
                return f"You have traveled {direction} to the {self.current_room}."
            return "You can't go that way."

        elif action == "Help":
            self.display_commands()
            return "Commands displayed."

        elif action == "Rules":
            self.display_rules()
            return "Rules displayed."

        elif action == "Look":
            description = self.describe_room(self.current_room)
            return f"{Colors.CYAN}{description}{Colors.RESET}"

        elif action == "Attack":
            if "Enemy" in self.rooms[self.current_room]:
                enemy = self.rooms[self.current_room]["Enemy"]
                item = self.rooms[self.current_room].get("Item", "unknown treasure")
                victory, combat_msg = self.combat(enemy["Name"], self.current_room)
                self.round_number += 1
                if victory:
                    if "HasKey" in enemy and enemy["HasKey"]:
                        return f"You defeated the {enemy['Name']}! \nYou found a key and claimed the {item}!"
                    else:
                        return f"You defeated the {enemy['Name']}! \nYour reward for victory is one gold and you have claimed the {item}!"
                return combat_msg
            return "No enemy here to attack."

        elif action == "Roll":
            rolls = [self.roll_d6() for _ in range(4)]
            return f"Dice Rolls: {', '.join(map(str, rolls))}"

        elif action == "Get":
            if params and "Item" in self.rooms[self.current_room]:
                item = self.rooms[self.current_room]["Item"]
                if ' '.join(params).title() == item:
                    if item not in self.player.inventory:
                        if "Enemy" in self.rooms[self.current_room]:
                            return "You must defeat the enemy first!"
                        self.player.inventory.append(item)
                        return f"{item} retrieved!"
                    return f"You already have the {item}."
            return f"Can't find that item."

        elif action == "Exit":
            self.clear()
            print(f"{Colors.RED}Exiting the game. Goodbye!{Colors.RESET}")
            sys.exit()

        elif action == "Inventory" or action == "I":
            if self.player.inventory:
                return f"Your inventory: {', '.join(self.player.inventory)}"
            return "Your inventory is empty."

        return "Invalid Command"

    def restart_game(self):
        """Reset the game with new random enemies"""
        self.player = Player(health=5, strength=5, gold=0, inventory=[])
        self.current_room = "Liminal Space"
        self.round_number = 1
        self.message = ""
        self.treasures = self._create_treasure_list()
        self.enemy_bank = self._create_enemy_bank()
        self.rooms = self._initialize_rooms()

    def game_loop(self):
        """Main game loop."""
        while self.round_number <= self.total_rounds:
            self.clear()
            
            # Display room information
            description = self.rooms[self.current_room].get("Description", "You see nothing special here.")
            print(description + f"\n{'--' * 17}")

            # Display player information
            print(f"{Colors.GREEN}Current Room: {self.current_room} \nRound: {self.round_number}/{self.total_rounds}\n"
                  f"Health: {self.player.health} Strength: {self.player.strength} Gold: {self.player.gold}\n"
                  f"Loot: {self.player.inventory} Key: {'Yes' if self.player.has_key else 'No'}\n{'--' * 17}\n{Colors.RESET} ")
                  

            # Display the latest message
            print(self.message)

            # Accept player input for move
            user_input = input(f"{Colors.YELLOW}Enter your move: \n{Colors.RESET}")
            
            # Split move into words and parse
            parts = user_input.split()
            if not parts:
                self.message = "Please enter a command."
                continue
                
            action = parts[0].title()
            params = [p.title() for p in parts[1:]] if len(parts) > 1 else None
            
            self.message = self.process_action(action, params)
            
            # Check if the game is over
            if self.round_number > self.total_rounds:
                print("Game over! You've completed all 30 rounds.")

                play_again = input("Would you like to play again? (y/n): ")
                if play_again.lower() == 'y':
                    self.restart_game()
                else:
                    break
                
            # Check if player has defeated the final boss
            if "The Rotten Temple Room" in self.rooms and "Enemy" not in self.rooms["The Rotten Temple Room"]:
                print(f"{Colors.GREEN}Congratulations! You've defeated the final boss and won the game!{Colors.RESET}")
                
                play_again = input("Would you like to play again? (y/n): ")
                if play_again.lower() == 'y':
                    self.restart_game()
                else:
                    break

def main():
    game = DungeonGame()
    game.main_menu()
    game.game_loop()

if __name__ == "__main__":
    main()