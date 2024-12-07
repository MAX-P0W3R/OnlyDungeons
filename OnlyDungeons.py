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
    if "Enemy" not in rooms[current_room]:
        print(f"No enemy named {enemy_name} is present in this room.")
        return False

    enemy = rooms[current_room]["Enemy"]
    print(f"\nYou encounter a {enemy_name}!")
    print(f"Player: {player['Health']} HP / {player['Strength']} STR | {enemy_name}: {enemy['Health']} HP / {enemy['Strength']} STR")

    # Initiative Roll
    input("Press Enter to roll for initiative...")
    player_initiative = roll_d6()
    enemy_initiative = roll_d6()
    print(f"\nYou rolled {player_initiative} for initiative!")
    print(f"The {enemy_name} rolled {enemy_initiative} for initiative!")

    # Determine who attacks first
    player_turn = player_initiative >= enemy_initiative  # Player goes first on a tie
    if player_turn:
        print("You have the initiative and will attack first!")
    else:
        print(f"The {enemy_name} has the initiative and will attack first!")

    # Combat Loop
    while player["Health"] > 0 and enemy["Health"] > 0:
        if player_turn:
            # Player's attack
            input("Press Enter to roll for your attack...")
            player_roll = roll_d6()
            player_damage = player_roll * player["Strength"]
            enemy["Health"] -= player_damage
            print(f"You rolled {player_roll}! You deal {player_damage} damage to the {enemy_name}.")

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

                # Remove the enemy from the room
                del rooms[current_room]["Enemy"]
                return True  # Player wins
        else:
            # Enemy's attack
            input(f"The {enemy_name} attacks! Press Enter to roll for defense...")
            enemy_roll = roll_d6()
            enemy_damage = enemy_roll * enemy["Strength"]
            player["Health"] -= enemy_damage
            print(f"The {enemy_name} rolled {enemy_roll}! It deals {enemy_damage} damage to you.")

            if player["Health"] <= 0:
                print("You have been defeated! Game over.")
                return False  # Enemy wins

        # Switch turns
        player_turn = not player_turn

        # Show updated health after each round
        print(f"\nYour Health: {player['Health']} | {enemy_name}'s Health: {enemy['Health']}")

    return False  # Failsafe if combat ends unexpectedly

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
msg= "" 


# Game Loop
def game_loop():
    global round_number  # Use the global round number
    global current_room
    global msg
    global gold

    while round_number <= total_rounds:  # Loop until all rounds are completed
        clear()

        # Display player information
        print(f"You are in {current_room}\nRound: {round_number}/{total_rounds}\nHealth: {player['Health']}\n\
Strength: {player['Strength']}\nGold: {player['Gold']}\nLoot: {inventory}\n{'--' * 17}")

        # Display the latest message
        print(msg)

        # Handle nearby items
        if "Item" in rooms[current_room].keys():
            nearby_item = rooms[current_room]["Item"]

        # Accept player input for move
        user_input = input("Enter your move: \n")

        # Split move into words
        next_move = user_input.split(' ')

        # First word is action
        action = next_move[0].title()

        # Increment the round number after the action
        round_number += 1

        if len(next_move) > 1:
            item = next_move[1:]
            direction = next_move[1].title()

            item = ' '.join(item).title()

        # Check if the game is over
        if round_number > total_rounds:
            print("Game over! You've completed all 30 rounds.")
            break

        # Handle actions
        if action == "Go":
            try:
                current_room = rooms[current_room][direction]
                msg = f"You have traveled {direction} to the {current_room}."
            except KeyError:
                msg = f"You can't go that way."

        elif action == "Get":
            try:
                if item == rooms[current_room]["Item"]:
                    if item not in inventory:
                        inventory.append(item)
                        msg = f"{item} retrieved!"
                    else:
                        msg = f"You already have the {item}."
                else:
                    msg = f"Can't find {item}."
            except KeyError:
                msg = f"Can't find {item}."

        elif action == "Look":
            description = rooms[current_room].get("Description", "You see nothing special here.")
            exits = [key for key in rooms[current_room].keys() if key not in ["Item", "Enemy", "Description"]]
            exit_str = ", ".join(exits)
            msg = f"{description}\nExits: {exit_str}"

            if "Item" in rooms[current_room]:
                item = rooms[current_room]["Item"]
                msg += f"\nYou see a {item} here."

            if "Enemy" in rooms[current_room]:
                enemy = rooms[current_room]["Enemy"]
                if isinstance(enemy, dict):
                    msg += f"\nEnemy: {enemy['Name']} {enemy['Health']}/{enemy['Strength']}"

        elif action == "Attack":
            if "Enemy" in rooms[current_room]:
                enemy = rooms[current_room]["Enemy"]
                victory = combat(player, enemy["Name"], current_room)
                if victory:
                    msg = f"You defeated {enemy['Name']} and claimed the room's treasure!"
            else:
                msg = "No enemy here to attack."

        elif action == "Roll":
            rolls = [random.randint(1, 6) for _ in range(4)]
            msg = f"Dice Rolls: {', '.join(map(str, rolls))}"

        elif action == "Exit":
            break

        else:
            msg = "Invalid Command"
main_menu()
game_loop()
