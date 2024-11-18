import os

from colorama import Fore, Back, Style, init

#from PIL import Image

# Show map
#img = Image.open('Map.png')
#img.show()
init()

# Display the start menu.
def prompt():
    print(Fore.GREEN + "\t\tWelcome to OnlyDungeons!\n\n\
        Objective: In todays dungeon you will adventure deep into the Unknown void to attempt\n\
        to defeat your foes, destroy their lairs, and loot their treasure hordes. You will need\n\
        a lucky roll of the dice and a bit of cunning.\n\n\
        You must defeat all six enemies to collect their treasure. One will possess the key\n\
        to unlock the final chamber.\n\
        You must find each enemy lair, slay the enemy, loot any treasure and escape the dungeon.\n\
        You will have 30 rounds to fulfill your quest. Good luck!\n\n\
        \tHere's a few tips to help you on your way:\n\
        Roll the Dice: 'roll' This will roll four D6(six sided dice).\n\
        Movement: 'go {direction}' Travel north,south,east,or west.\n\
        Collect items from a room: 'get {item}': Add nearby item to inventory.\n\
        Have a look around: 'look' To see the room description.\n\
        Attack: 'attack {enemy}' Any enemy within range may be attacked.\n\n\
        \tTo leave the game at any time type EXIT")

    input("\t\tPress any key to continue ...\n")


# Clear the terminal.
def clear():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print("\n" * 50)

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
        'Enemy':'Ghoull'
    },
    'Bat Cavern': {
        'North':'Liminal Space',
        'East':'Great Hall',
        'Item':'Staff',
        'Description':'BAts! Everywhere! We are in bat country!',
        'Enemy':'Ghost'
    },
    'Great Hall': {
        'West':'Bat Cavern',
        'Item':'Sword',
        'Description':'The Great Hall location description.',
        'Enemy':'Goblin'
    },
    'Bazaar': {
        'West':'Liminal Space',
        'North':'Location Four',
        'East':'Location Six',
        'Item':'Skull',
        'Description':'The bazaar location description.',
        'Enemy':'Vampire'
    },
    'Location Four': {
        'South':'Bazaar',
        'East':'Location Five',
        'Item':'',
        'Description':'The four location description.',
        'Enemy':'Brigand'
    },
    'Location Five': {
        'West':'Location Four',
        'Item':'',
        'Description':'The fifth location description.',
        'Enemy':'Ghoul'
    },
    'Location Six': {
        'East':'Bazaar',
        'Item':'Treasure Chest',
        'Description':'The sixth location description.',
        'Enemy':'Final Boss'
    }
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
    print(f"You are in {current_room}\nInventory : {inventory}\n{'~' * 27}")

    # Dispaly msg
    print(msg)

    # Item indicator
    if "Item" in rooms[current_room].keys():

        nearby_item = rooms[current_room]["Item"]

        if nearby_item not in inventory:

            # Plural
            if nearby_item[-1] == 's':
                print(f"You see {nearby_item}")

            # Singular starts with vowel
            elif nearby_item[0] in vowels:
                print(f"You see an {nearby_item}")

            # Singular starts with consanent
            else:
                print(f"You see a {nearby_item}")

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

        # Get Exits
        exits = [key for key in rooms[current_room].keys() if key not in ["Item", "Enemy", "Description"]]
        exit_str = ", ".join(exits)

        # Add description to mesaage.
        msg = f"{description}\nExits: {exit_str}"

        # Add item deets if present.
        if "Item" in rooms[current_room]:
            item = rooms[current_room]["Item"]
            msg += f"\nItem: {item}"

        # Add enemy deets if present.
        if "Enemy" in rooms[current_room]:
            enemy = rooms[current_room]["Enemy"]
            msg += f"\nEnemy: {enemy}"

    # Add Attack action
    elif action == "Attack":
        try:
            if "Enemy" in rooms[current_room]:
                enemy = rooms[current_room]["Enemy"]
                msg = f"You attack the {enemy}! It's defeated!"
                # Remove enemy after attack
                del rooms[current_room]["Enemy"]
            else:
                msg = "No enemy here to attack."
        except:
            msg = "Attack failed."

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




################################
#name = input('Enter your name: ')
#print(f'Greetings {name}! Welcome to the Dungeon!')
#start = input('Would you like to enter the Dungeon or quit and die? ')
#if start == 'enter':
#    print("Great! Let's get on with the adventure!")
#    mainMenu = input('Would you like to read the Rules or Begin the adventure? ')
#else:
#    print("Lame. You have died at the gates of the unknown...")
#    quit()

#elif mainMenu == 'begin':


#else:
#    print('Invalid response!')
#    quit()


