import os
#from PIL import Image

# Show map
#img = Image.open('Map.png')
#img.show()

# Display the start menu.
def prompt():
    print("\t\t\tWelcome to the Dungeon\n\n"
        "You must collect all six treasures from each enemy to defeat the final Boss.\n"
        "Movement:\t'go {direction}' (travel north,south,east,or west)\n"
        "\t'get {item}' (add nearby item to inventory)\n")

    input("Press any key to continue ... ")

# Clear the terminal.
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Map
rooms = {
    'Liminal Space' : {'North':'Mirror Maze','South':'Bat Cavern'},
    'Mirror Maze' : {'South':'Liminal Space','Item':'Crystal'},
    'Bat Cavern' : {'North':'Liminal Space','East':'Great Hall','Item':'Staff'},
    'Great Hall' : {'West':'Bat Cavern','Enemy':'Goblin'},
    'Bazaar' : {'West':'Liminal Space','North':'Location Four','East':'Location Six','Item':'Skull'},
    'Location Four' : {'South':'Bazaar','East':'Location Five','Enemy':'Brigand'},
    'Location Five' : {'West':'Location Four','Enemy':'Ghoul'},
    'Location Six' : {'East':'Bazaar','Enemy':'Final Boss'}
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
    print(f"You are in {current_room}\nInventory : {inventory}\n{'-' * 27}")

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

# Enemy encounter -- TO DO

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

    # Add Attack action

    # Add random dice roll

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

#if mainMenu == 'rules':
#    print("Objective: In todays dungeon you will adventure deep into the Unknown void to attempt")
#    print("to defeat your foes, destroy their lairs, and loot their treasure hordes. You will need")
#    print("a lucky roll of the dice and a bit of cunning.")

#elif mainMenu == 'begin':
    # Introduce heroes.
#    print("Let's meet your party:")
#    print('')
#   print('Hero #1: Watchman')
#    print('Health: 5')
#    print('Power: 3')
#    print('')
#    print('Hero #1: Assassin')
#    print('Health: 4')
#    print('Power: 4')
#    print('')
#    print('Hero #1: Alchemist')
#    print('Health: 3')
#    print('Power: 5')

#else:
#    print('Invalid response!')
#    quit()


