import os
import random

from colorama import Fore, Back, Style, init


init()

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
    print(f"Your Health: {player['Health']} | Enemy Health: {enemy['Health']}")

    while player["Health"] > 0 and enemy["Health"] > 0:
        # Player's attack
        input("Press Enter to roll for your attack...")
        player_roll = roll_d6()
        player_damage = player_roll * player["Strength"]
        enemy["Health"] -= player_damage
        print(f"You rolled {player_roll}! You deal {player_damage} damage.")

        if enemy["Health"] <= 0:
            print(f"You defeated the {enemy_name}!")

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
        'Enemy':{'Name': 'Ghoul', 'Health':11, 'Strength': 3},
    },
    'Bat Cavern': {
        'North':'Liminal Space',
        'East':'Great Hall',
        'Item':'Staff',
        'Description':'BATS! Everywhere! You are in bat country!',
        'Enemy':{'Name': 'Ghost', 'Health':12, 'Strength': 4},
    },
    'Great Hall': {
        'West':'Bat Cavern',
        'Item':'Sword',
        'Description':'The Great Hall is dimly lit by candles placed on stone shelves around the perimeter.'
        'You see a Goblin seated on large stone slab. He\'s seen you and you make eye contact.',
        'Enemy':{'Name': 'Goblin', 'Health':12, 'Strength': 4},
    },
    'Bazaar': {
        'West':'Liminal Space',
        'North':'Pit of Pendulums',
        'East':'The Rotten Temlpe Room',
        'Item':'Skull',
        'Description':'The bazaar location description.',
        'Enemy':{'Name': 'Vampire', 'Health': 0, 'Strength': 0},
    },
    'Pit Of Pendulums': {
        'South':'Bazaar',
        'East':'Tomb of the Forgotten',
        'Item':'NULL',
        'Description':'The location description.',
        'Enemy':{'Name': 'Brigand', 'Health': 0, 'Strength': 0},
    },
    'Tomb of the Forgotten': {
        'West':'Pit Of Pendulums',
        'Item':'Sword',
        'Description':'The location description.',
        'Enemy':{'Name': 'Black Cat', 'Health': 0, 'Strength': 0},
    },
    'The Rotten Temlpe Room': {
        'East':'Bazaar',
        'Item':'Treasure Chest',
        'Description':'The location description.',
        'Enemy':{'Name': 'The Final Boss', 'Health': 0, 'Strength': 0},
    }
    }


# Initialize enemy stats
for room, details in rooms.items():
    if 'Enemy' in details:
        details['Enemy']['Health'] = roll_d6()
        details['Enemy']['Strength'] = roll_d6()


# Player and Enemy stats
player = {
    "Health": 20,
    "Strength": 6
    }

enemies = {
    "Goblin": {"Health":5, "Strength":2},
    "Brigand": {"Health":5, "Strength":3},
    "Ghoul": {"Health":5, "Strength":3},
    "Black Cat": {"Health":5, "Strength":3},
    "Vampire": {"Health":5, "Strength":3},
    "Fianl Boss": {"Health":5, "Strength":3},
    }


# List of Vowels
vowels = ['a', 'e', 'i', 'o', 'u']

# List to track inventory
inventory = []

# Track current room
current_room = "Liminal Space"

# Result of last move
msg = ""

clear()
prompt()

# Gameplay Loop
while True:

    clear()

    # Display info player
    print(f"You are in {current_room}\nHealth: {player['Health']}\nStrength: {player['Strength']}\nInventory : {inventory}\n{'--' * 17}")

    # Dispaly msg
    print(msg)

    # Item indicator
    if "Item" in rooms[current_room].keys():

        nearby_item = rooms[current_room]["Item"]

        # if nearby_item not in inventory:

        #     # Plural
        #     if nearby_item[-1] == 's':
        #         print(f"You see {nearby_item}")

        #     # Singular starts with vowel
        #     elif nearby_item[0] in vowels:
        #         print(f"You see an {nearby_item}")

        #     # Singular starts with consanent
        #     else:
        #         print(f"You see a {nearby_item}")

    # Accept player input for move
    user_input = input("Enter your move: \n")

    # Split move into words
    next_move = user_input.split(' ')

    # First word is action
    action = next_move[0].title()

    if len(next_move) > 1:
        item = next_move[1:]
        direction = next_move[1].title()

        item = ' '.join(item).title()


    # Moving between rooms
    if action == "Go":

        try:
            current_room = rooms[current_room][direction]
            msg = f"You have traveled {direction}."

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

    else:
        msg = "Invalid Command"
