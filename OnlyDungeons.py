import os
import random
import sys
from colorama import Fore, init

init()

# Constants
ROOM_KEYS = ["Item", "Enemy", "Description"]

## Utility Functions ##
# Clear the terminal screen.  
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Simulate a D6 roll.
def roll_d6():
    return random.randint(1, 6)

# Helper for input prompts.
def input_with_prompt(prompt_text):
    input(Fore.YELLOW + prompt_text + Fore.RESET)

# Menu Functions
def main_menu():
    # Display the main menu and handle navigation.
    while True:
        clear()
        print(Fore.GREEN + "~~~~ Welcome to the Dungeon! ~~~~\n"
              "1. Begin the adventure\n"
              "2. Gameplay & Rules\n"
              "3. Commands\n"
              "4. Exit\n")
        choice = input("Enter your selection: ")

        if choice == "1":
            clear()
            print(Fore.YELLOW + "Starting your adventure...\n")
            prompt()
            return  # Exit the menu loop
        elif choice == "2":
            clear()
            display_rules()
        elif choice == "3":
            clear()
            display_commands()
        elif choice == "4":
            clear()
            print(Fore.RED + "Exiting the game. Goodbye!")
            sys.exit()
        else:
            clear()
            print(Fore.RED + "Invalid selection. Please choose a valid option.\n")

def prompt():
    print(Fore.GREEN + "\t\tWelcome, Brave Adventurer!\n\n\
\tYou stand at the threshold of the forgotten dungeon, a labyrinth of peril and mystery.\n\
Whispers speak of untold treasures guarded by ancient foes, each more deadly than the last.\n\
To claim victory, you must gather six legendary artifacts, hidden deep within the dungeon, each\n\
guarded by fearsome enemies.\n\n\
\tYour journey will test your courage, strategy, and skill. Armed with nothing but your wits, your dice,\n\
and your resolve, you must navigate through treacherous rooms, face off against monstrous enemies, and\n\
unearth the secrets of the dungeon.\n\n\
\tRoll the dice, make your move, and choose your actions wisely. Will you emerge victorious, or will the\n\
dungeon claim yet another soul?\n\n\
The dungeon awaits... let the adventure begin!\n")

    input("\t\tPress any key to continue ...\n")

def display_rules():
    print(Fore.CYAN + "~~~ Gameplay & Rules ~~~\n"
          "1. You have 30 rounds to explore the dungeon.\n"
          "2. Allocate dice rolls to movement, treasure, enemy, and location.\n"
          "3. Defeat enemies to collect gold and items.\n"
          "4. The game ends when you defeat the final boss or run out of rounds.\n")
    input_with_prompt("Press any key to continue...")

def display_commands():
    print(Fore.BLUE + "~~~ Commands ~~~\n"
          "- 'Look': Inspect your current room.\n"
          "- 'Go': Navigate to another room.\n"
          "- 'Attack': Engage in combat with an enemy.\n"
          "- 'Inventory': Check your collected items and gold.\n")
    input_with_prompt("Press any key to continue...")

# Gameplay Functions
def describe_room(current_room):
    #Generate a description of the current room.
    description = rooms[current_room].get("Description", "Nothing special here.")
    exits = [key for key in rooms[current_room] if key not in ROOM_KEYS]
    exit_str = ", ".join(exits)
    msg = f"{description}\nExits: {exit_str}"

    if "Enemy" in rooms[current_room]:
        enemy = rooms[current_room]["Enemy"]
        msg += f"\nEnemy: {enemy['Name']} {enemy['Health']}/{enemy['Strength']}"
    return msg

def combat(player, enemy_name, current_room):
    #Handle combat mechanics.
    enemy = rooms[current_room]["Enemy"]
    print(f"\nYou encounter {enemy_name}!")
    print(f"Player: {player['Health']}/{player['Strength']} | {enemy_name}: {enemy['Health']}/{enemy['Strength']}")

    while player["Health"] > 0 and enemy["Health"] > 0:
        # Player attacks
        input_with_prompt("Press Enter to roll for your attack...")
        player_damage = roll_d6() * player["Strength"]
        enemy["Health"] -= player_damage
        print(f"You deal {player_damage} damage.")

        if enemy["Health"] <= 0:
            print(f"You defeated the {enemy_name}!")
            player["Gold"] += 3 if enemy.get("IsFinalBoss") else 1
            print(f"You earned {player['Gold']} gold in total.")
            del rooms[current_room]["Enemy"]
            return True  # Victory

        # Enemy attacks
        input_with_prompt(f"The {enemy_name} attacks! Press Enter to defend...")
        enemy_damage = roll_d6() * enemy["Strength"]
        player["Health"] -= enemy_damage
        print(f"The {enemy_name} deals {enemy_damage} damage.")

        if enemy["Health"] <= 0:
            print(f"You defeated the {enemy_name}!")
            
            # Grant gold to the player
            if enemy.get("IsFinalBoss", False):
                player["Gold"] += 3
                print("You defeated the final boss! You earn 3 gold!")
            else:
                player["Gold"] += 1
                print("You earn 1 gold!")

            print(f"Your total gold: {player['Gold']}")

            # Add room item to inventory, if present
            if "Item" in rooms[current_room]:
                item = rooms[current_room]["Item"]
                if item not in inventory:
                    inventory.append(item)
                    print(f"You found and collected the {item}!")

            # Safely remove the enemy
            if "Enemy" in rooms[current_room]:
                del rooms[current_room]["Enemy"]

            return True  # Player wins
         # Show updated health
        print(f"\nYour Health: {player['Health']} | {enemy_name}'s Health: {enemy['Health']}")

        if player["Health"] <= 0:
            print("You have been defeated. Game over!")
            return False  # Loss

# Function to handle enemy defeat
def defeat_enemy(current_room):
    global gold
    
    # Check if the room has an enemy
    if 'Enemy' in rooms[current_room]:
        enemy = rooms[current_room]['Enemy']
        # Check if it's the final boss
        if enemy.get('IsFinalBoss', False):
            gold += 3
            print(f"You defeated the final boss! You earned 3 gold. Total gold: {gold}")
        else:
            gold += 1
            print(f"You defeated {enemy['Name']}! You earned 1 gold. Total gold: {gold}")
        
        # Remove the defeated enemy
        del rooms[current_room]['Enemy']
    else:
        print("There is no enemy here to defeat.")

# Initialization
# Map
rooms = {
    'Liminal Space': {
        'North':'Mirror Maze',
        'South':'Bat Cavern',
        'East':'Bazaar',
        'Description':'Starting point. Grand entrance'
    },
    'Mirror Maze': {
        'South':'Liminal Space',
        'Item':'Crystal',
        'Description':'A room full of dusty mirrors!',
        'Enemy':{'Name': 'Ghoul', 'Health':0, 'Strength': 0},
    },
    'Bat Cavern': {
        'North':'Liminal Space',
        'East':'Great Hall',
        'Item':'Staff',
        'Description':'BATS! Everywhere! You are in bat country!',
        'Enemy':{'Name': 'Ghost', 'Health':0, 'Strength': 0},
    },
    'Great Hall': {
        'West':'Bat Cavern',
        'Item':'Sword',
        'Description':'The Great Hall is dimly lit by candles placed on stone shelves around the perimeter.'
        'You see a Goblin seated on large stone slab. He\'s seen you and you make eye contact.',
        'Enemy':{'Name': 'Goblin', 'Health':0, 'Strength': 0},
    },
    'Bazaar': {
        'West':'Liminal Space',
        'North':'Pit of Pendulums',
        'East':'The Rotten Temlpe Room',
        'Item':'Skull',
        'Description':'The bazaar location description.',
        'Enemy':{'Name': 'Vampire', 'Health': 0, 'Strength': 0},
    },
    'Pit of Pendulums': {
        'South':'Bazaar',
        'East':'Tomb of the Forgotten',
        'Item':'Glass Eye of Mystery',
        'Description':'The location description.',
        'Enemy':{'Name': 'Brigand', 'Health': 0, 'Strength': 0},
    },
    'Tomb of the Forgotten': {
        'West':'Pit of Pendulums',
        'Item':'Heavy Shield',
        'Description':'The location description.',
        'Enemy':{'Name': 'Black Cat', 'Health': 0, 'Strength': 0},
    },
    'The Rotten Temlpe Room': {
        'East':'Bazaar',
        'Item':'Treasure Chest',
        'Description':'The location description.',
        'Enemy':{'Name': 'Dragon Butt', 'Health': 0, 'Strength': 0, 'IsFinalBoss':True},
    }
    }

# Initialize enemy stats
for room, details in rooms.items():
    if 'Enemy' in details:
        details['Enemy']['Health'] = roll_d6()
        details['Enemy']['Strength'] = roll_d6()

player = {"Health": 5, "Strength": 5, "Gold": 0}
inventory = []
current_room = "Liminal Space"
round_number = 1
total_rounds = 30

# Game Loop
def game_loop():
    global round_number
    global current_room
    global msg 
    global gold 

    while round_number <= total_rounds:
        clear()
        print(f"Room: {current_room}\nRound: {round_number}/{total_rounds}\n"
              f"Health: {player['Health']} | Strength: {player['Strength']} | Gold: {player['Gold']}\n"
              f"Loot: {inventory}\n{'-' * 34}")
        print(describe_room(current_room))

        user_input = input("Enter your action: ").strip().title().split()
        action = user_input[0]
        direction = user_input[1] if len(user_input) > 1 else None

        if action == "Go" and direction:
            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
                print(f"You move {direction} to {current_room}.")
            else:
                print("You can't go that way.")
        elif action == "Look":
            print(describe_room(current_room))
        elif action == "Attack":
            if "Enemy" in rooms[current_room]:
                combat(player, rooms[current_room]["Enemy"]["Name"], current_room)
            else:
                print("No enemy here.")
        elif action == "Inventory":
            print(f"Inventory: {inventory}\nGold: {player['Gold']}")
        elif action == "Exit":
            break
        else:
            print("Invalid command.")
        round_number += 1

main_menu()
game_loop()
