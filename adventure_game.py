# creating a simple text choice based adventure game

def get_choice(prompt, options):
    while True:
        choice = input(f"\n{prompt}").strip().upper()
        if choice in options:
            return choice
        print(f"Please choose one of: {', '.join(options)}.")


def show_notice(label, message):
    print(f"\n[{label}] {message}")


def start_game():
    while True:
        print("\nWelcome player to 'The Adventure Game', an interactive choice-based RPG.")
        player = input("Enter challenger name: ").strip()
        print()
        print(f"Okay, challenger {player}, it's time to acquire lost treasure. Make your choice.")

        choice = get_choice("Explore the forest [F] or the cave [C]? >>> ", ("F", "C"))
        if choice == "F":
            survived = forest_path()
        else:
            survived = cave_path()

        if survived:
            survived = ancient_gate()
        if survived:
            survived = treasure_vault(player)
        if survived:
            return

        print("\nGame over. Your journey has ended.")
        retry = get_choice("Try again [Y] or quit [Q]? >>> ", ("Y", "Q"))
        if retry == "Q":
            return

def forest_path():
    print("\nYou enter the forest and hear rushing water nearby.")

    choice = get_choice("Follow the river [R] or climb a tree [T]? >>> ", ("R", "T"))
    if choice == "R":
        show_notice("THREAT", "The river is rushing fast, but you spot a marked crossing nearby.")
        crossing = get_choice("Use the marked crossing [M] or take a shortcut [S]? >>> ", ("M", "S"))
        if crossing == "S":
            show_notice("THREAT", "The current sweeps you away before you can reach the other bank.")
            return False
        print("You cross safely and continue along the trail.")
    else:
        show_notice("CLUE", "From the treetop, you spot a dry trail that avoids the river crossing.")

    show_notice("THREAT", "A startled wild animal blocks the trail.")
    choice = get_choice("Hide behind a fallen log [H] or run past it [R]? >>> ", ("H", "R"))
    if choice == "R":
        show_notice("THREAT", "The animal charges as you run. Your journey ends in the forest.")
        return False

    print("You stay hidden until the animal leaves, then follow its trail toward an ancient gate.")
    return True


def cave_path():
    print("\nYou step into a dark cave and hear something moving deeper inside.")

    choice = get_choice("Light a torch [T] or proceed without one [W]? >>> ", ("T", "W"))
    if choice == "W":
        show_notice("THREAT", "A wild monster attacks from the darkness. Your journey ends in the cave.")
        return False

    show_notice("ITEM", "Your torch reveals a narrow path leading to a deep chasm.")
    show_notice("THREAT", "A deep chasm blocks the path.")
    choice = get_choice("Secure and test a rope [S] or leap across [L]? >>> ", ("S", "L"))
    if choice == "L":
        show_notice("THREAT", "You fall into the chasm. Your journey ends in the cave.")
        return False

    show_notice("ITEM", "The rope holds. You cross safely and find an ancient gate.")
    return True


def ancient_gate():
    show_notice("CLUE", 'The gate bears an inscription: "Patience reveals the way."')
    choice = get_choice("Study the inscription [S] or force the gate [F]? >>> ", ("S", "F"))
    if choice == "F":
        show_notice("THREAT", "The gate triggers a hidden trap. Your journey ends at the gate.")
        return False

    print("The inscription reveals a pattern. The gate opens onto the treasure vault.")
    return True


def treasure_vault(player):
    print("\n" + "=" * 54)
    print("                 THE FINAL TRIAL")
    print("                  TREASURE VAULT")
    print("=" * 54)
    show_notice("CLUE", "Worn tiles form a safe path across the unstable floor.")
    choice = get_choice("Follow the marked tiles [M] or rush to the chest [R]? >>> ", ("M", "R"))
    if choice == "R":
        show_notice("THREAT", "The floor gives way beneath you. Your journey ends in the vault.")
        return False

    print("\n" + "=" * 54)
    print("                 THE TREASURE IS YOURS")
    print("=" * 54)
    show_notice("TREASURE", "You uncover the Sunfire Crown, lost for a thousand years.")
    print(f"{player}, you followed the clues, survived every trial, and claimed the treasure!")
    print("                         YOU WIN")
    print("=" * 54)
    return True

start_game()