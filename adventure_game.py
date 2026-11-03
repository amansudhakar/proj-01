# creating a simple text choice based adventure game
import os
import random
import sys
import time


RANDOM_EVENTS = {
    "forest": (
        "A weathered pack hangs from a low branch.",
        "A raven drops a bright coin onto the trail.",
    ),
    "cave": (
        "A cracked supply crate rests beside the tunnel.",
        "Small glowing marks lead to a side passage.",
    ),
}

def get_choice(prompt, options):
    while True:
        choice = input(f"\n{prompt}").strip().upper()
        if choice in options:
            return choice
        print(f"Please choose one of: {', '.join(options)}.")


def show_notice(label, message):
    print(f"\n[{label}] {message}")


def loading_screen(stage, enabled=True):
    print(f"\n{stage}")
    if not enabled or not sys.stdin.isatty():
        return

    print("LOADING ", end="", flush=True)
    if os.name == "nt":
        print("[S to skip] ", end="", flush=True)
    for frame in range(9):
        print(".", end="", flush=True)
        time.sleep(0.12 if frame < 4 else 0.25)
        if os.name == "nt":
            import msvcrt

            if msvcrt.kbhit() and msvcrt.getwch().lower() == "s":
                print(" SKIPPED")
                return
    print(" READY")


def random_encounter(location, rng, state):
    event = rng.choice(RANDOM_EVENTS[location])
    show_notice("RANDOM EVENT", event)

    if state["lucky_charm"]:
        print("You already carry a lucky charm, so you move on.")
        return

    choice = get_choice(
        "Investigate (50% chance to find a lucky charm) [I] or move on [M]? >>> ",
        ("I", "M"),
    )
    if choice == "I" and rng.random() < 0.5:
        state["lucky_charm"] = True
        show_notice("ITEM", "You found a lucky charm. It can protect you from one fatal mistake.")
    elif choice == "I":
        print("You find nothing useful, but safely return to the trail.")
    else:
        print("You leave the event behind and continue safely.")


def survive_hazard(message, state):
    show_notice("THREAT", message)
    if not state["lucky_charm"]:
        return False

    state["lucky_charm"] = False
    show_notice("ITEM", "Your lucky charm breaks and shields you from the danger.")
    return True


def start_game(rng=None, animations=True):
    rng = rng or random.Random()

    while True:
        state = {"lucky_charm": False}
        print("\nWelcome player to 'The Adventure Game', an interactive choice-based RPG.")
        player = input("Enter challenger name: ").strip()
        print()
        print(f"Okay, challenger {player}, it's time to acquire lost treasure. Make your choice.")

        choice = get_choice("Explore the forest [F] or the cave [C]? >>> ", ("F", "C"))
        if choice == "F":
            loading_screen("ENTERING THE FOREST", animations)
            survived = forest_path(rng, state)
        else:
            loading_screen("ENTERING THE CAVE", animations)
            survived = cave_path(rng, state)

        if survived:
            loading_screen("APPROACHING THE ANCIENT GATE", animations)
            survived = ancient_gate(state)
        if survived:
            loading_screen("ENTERING THE TREASURE VAULT", animations)
            survived = treasure_vault(player, state)
        if survived:
            return

        print("\nGame over. Your journey has ended.")
        retry = get_choice("Try again [Y] or quit [Q]? >>> ", ("Y", "Q"))
        if retry == "Q":
            return

def forest_path(rng, state):
    print("\nYou enter the forest and hear rushing water nearby.")
    random_encounter("forest", rng, state)

    choice = get_choice("Follow the river [R] or climb a tree [T]? >>> ", ("R", "T"))
    if choice == "R":
        show_notice("THREAT", "The river is rushing fast, but you spot a marked crossing nearby.")
        crossing = get_choice("Use the marked crossing [M] or take a shortcut [S]? >>> ", ("M", "S"))
        if crossing == "S":
            if not survive_hazard("The current sweeps you toward the rapids.", state):
                return False
            print("The lucky charm pulls you toward the marked crossing.")
        print("You cross safely and continue along the trail.")
    else:
        show_notice("CLUE", "From the treetop, you spot a dry trail that avoids the river crossing.")

    show_notice("THREAT", "A startled wild animal blocks the trail.")
    choice = get_choice("Hide behind a fallen log [H] or run past it [R]? >>> ", ("H", "R"))
    if choice == "R":
        if not survive_hazard("The animal charges as you run.", state):
            return False
        print("The charm flashes, giving you time to reach the trail.")

    print("You stay hidden until the animal leaves, then follow its trail toward an ancient gate.")
    return True


def cave_path(rng, state):
    print("\nYou step into a dark cave and hear something moving deeper inside.")
    random_encounter("cave", rng, state)

    choice = get_choice("Light a torch [T] or proceed without one [W]? >>> ", ("T", "W"))
    if choice == "W":
        if not survive_hazard("A wild monster attacks from the darkness.", state):
            return False
        print("The charm flares brightly, revealing the cave passage.")
        show_notice("THREAT", "A deep chasm blocks the path.")
    else:
        show_notice("ITEM", "Your torch reveals a narrow path leading to a deep chasm.")
        show_notice("THREAT", "A deep chasm blocks the path.")
    choice = get_choice("Secure and test a rope [S] or leap across [L]? >>> ", ("S", "L"))
    if choice == "L":
        if not survive_hazard("You lose your footing at the edge of the chasm.", state):
            return False
        print("The charm's glow helps you find a safe foothold.")

    show_notice("ITEM", "The rope holds. You cross safely and find an ancient gate.")
    return True


def ancient_gate(state):
    show_notice("CLUE", 'The gate bears an inscription: "Patience reveals the way."')
    choice = get_choice("Study the inscription [S] or force the gate [F]? >>> ", ("S", "F"))
    if choice == "F":
        if not survive_hazard("The gate triggers a hidden trap.", state):
            return False
        print("The charm absorbs the trap's force, and the gate swings open.")

    print("The inscription reveals a pattern. The gate opens onto the treasure vault.")
    return True


def treasure_vault(player, state):
    print("\n" + "=" * 54)
    print("                 THE FINAL TRIAL")
    print("                  TREASURE VAULT")
    print("=" * 54)
    show_notice("CLUE", "Worn tiles form a safe path across the unstable floor.")
    choice = get_choice("Follow the marked tiles [M] or rush to the chest [R]? >>> ", ("M", "R"))
    if choice == "R":
        if not survive_hazard("The floor gives way beneath you.", state):
            return False
        print("The charm breaks your fall and leaves you beside the marked path.")

    print("\n" + "=" * 54)
    print("                 THE TREASURE IS YOURS")
    print("=" * 54)
    show_notice("TREASURE", "You uncover the Sunfire Crown, lost for a thousand years.")
    print(f"{player}, you followed the clues, survived every trial, and claimed the treasure!")
    print("                         YOU WIN")
    print("=" * 54)
    return True

if __name__ == "__main__":
    start_game()