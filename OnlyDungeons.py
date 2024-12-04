import os
import random
import sys

from colorama import Fore, Back, Style, init


init()

# Display main menu.
def mainMenu():
    while True: # Keep showing the menu until player chooses to exit
        clear()
        print(Fore.GREEN + "~~~~ Welcome the Dungeon! ~~~~\n\
    1. Begin the adventure\n\
    2. Gameplay & Rules\n\
    3. Commands\n\
    4. Exit\n")

        choice = input("Enter your selection: \n")

 # Process the choice
        if choice == "1":
            clear()
            print(Fore.YELLOW + "\nStarting your adventure...\n")
            prompt()  # Call a function to begin the game
            break # Exits the menu loop
        elif choice == "2":
            clear()
            print(Fore.CYAN + "\n~~~ Gameplay & Rules ~~~")
            displayRules()  # Call a function to show rules
        elif choice == "3":
            clear()
            print(Fore.BLUE + "\n~~~ Commands ~~~")
            displayCommands()  # Call a function to list commands
        elif choice == "4":
            clear()
            print(Fore.RED + "\nExiting the game. Goodbye!")
            sys.exit()  # Exit the program
        else:
            clear()
            print(Fore.RED + "Invalid selection. Please choose a valid option.\n")

# Display the start menu.
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

def displayRules():
    print("Rules of the game:\n\
1. You have 30 rounds to explore the dungeon.\n\
2. Each turn, roll dice to allocate to movement, treasure, enemy, and location.\n\
3. Defeat enemies to collect gold and items.\n\
4. The game ends when you defeat the final boss or run out of rounds.\n")
    input("\t\tPress any key to continue ...\n")

def displayCommands():
    print("Available commands:\n\
- 'Look': Inspect your current room.\n\
- 'Go': Navigate to another room.\n\
- 'Attack': Engage in combat with an enemy.\n\
- 'Inventory': Check your collected items and gold.\n")
    input("\t\tPress any key to continue ...\n")

# Clear the terminal.
def clear():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print("\n" * 50)

# Define dice roll D6 & Combat function
def roll_d6():
    return random.randint(1,6)

# Combat description and mechanics
def combat(player, enemy_name, current_room):
    if "Enemy" not in rooms[current_room]:
        print(f"No enemy named {enemy_name} is present in this room.")
        return False

    enemy = rooms[current_room]["Enemy"]
    print(f"\nYou encounter a {enemy_name}!")
    print(f"Player: {player['Health']}/{player['Strength']} | {enemy_name}: {enemy['Health']}/{enemy['Strength']}")

    while player["Health"] > 0 and enemy["Health"] > 0:
        # Player's attack
        input("Press Enter to roll for your attack...")
        player_roll = roll_d6()
        player_damage = player_roll * player["Strength"]
        enemy["Health"] -= player_damage
        print(f"You rolled {player_roll}! You deal {player_damage} damage.")

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

        # Enemy's attack
        input(f"The {enemy_name} attacks! Press Enter to roll for defense...")
        enemy_roll = roll_d6()
        enemy_damage = enemy_roll * enemy["Strength"]
        player["Health"] -= enemy_damage
        print(f"The {enemy_name} rolled {enemy_roll}! It deals {enemy_damage} damage.")

        if player["Health"] <= 0:
            print("You have been defeated! Game over.")
            return False  # Enemy wins

        # Show updated health
        print(f"\nYour Health: {player['Health']} | {enemy_name}'s Health: {enemy['Health']}")

    return False  # Default fail-safe

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
        'Enemy':{'Name': 'Ghoul', 'Health':10, 'Strength': 0},
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

# Player and Enemy stats
player = {
    "Health": 5,
    "Strength": 5,
    "Gold":0
    }

# List of Vowels
vowels = ['a', 'e', 'i', 'o', 'u']

# List to track inventory
inventory = []

# List player gold
gold = 0

# Track current room
current_room = "Liminal Space"

# Result of last move
msg = ""

# Initialize the round number
round_number = 1  # Start at round 1

# Total rounds in the game
total_rounds = 30


clear()
mainMenu()
#prompt()

# Gameplay Loop
while True:

    clear()

    # Display info player
    print(f"You are in {current_room}\nRound: {round_number}/{total_rounds}\nHealth: {player['Health']}\n\
Strength: {player['Strength']}\nGold: {gold}\nLoot: {inventory}\n{'--' * 17}")

    # Dispaly msg
    print(msg)

    # Item indicator
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

    # You can also check if the player has completed the game or lost
    if round_number > total_rounds:
        print("Game over! You've completed all 30 rounds.")
        break

    # Moving between rooms
    if action == "Go":

        try:
            current_room = rooms[current_room][direction]
            msg = f"You have traveled {direction} to the {current_room}."

        except:
            msg = f"You can't go that way."
 
    # Picking up items
    elif action == "Get":

        try:
            if item == rooms[current_room]["Item"]:

                if item not in inventory:

                    inventory.append(rooms[current_room]["Item"])
                    msg = f"{item} retrieved!"

                else:
                    msg = f"You already have the {item}."

            else:
                msg = f"Can't find {item}."

        except:
            msg = f"Can't find {item}."

    # Add Look action
    elif action == "Look":
        # Get room description
        description = rooms[current_room].get("Description", "You see nothing special here.")

        # Get item description if present.


        # Get Exits
        exits = [key for key in rooms[current_room].keys() if key not in ["Item", "Enemy", "Description"]]
        exit_str = ", ".join(exits)

        # Add description to mesaage.
        msg = f"{description}\nExits: {exit_str}"

        # Add enemy description if present.
        if "Enemy" in rooms[current_room]:
            enemy = rooms[current_room]["Enemy"]
            if isinstance(enemy, dict):
                enemy_name = enemy["Name"]
                enemy_health = enemy["Health"]
                enemy_strength = enemy["Strength"]
                msg += f"\nEnemy: {enemy_name} {enemy_health}/{enemy_strength}"

    # Add Attack action
    elif action == "Attack":
        if "Enemy" in rooms[current_room]:
            enemy = rooms[current_room]["Enemy"]
            victory = combat(player, enemy["Name"], current_room)
#           if victory:
#                del rooms[current_room]["Enemy"]  # Remove defeated enemy
       
        else:
            print("No enemy here to attack.")

    # Add random dice roll
    elif action == "Roll":
        import random
        rolls = [random.randint(1, 6) for _ in range(4)]
        msg = f"Dice Rolls: {', '.join(map(str, rolls))}"

    # Exit game
    elif action == "Exit":
        break

    # Help commands

    else:
        msg = "Invalid Command"
