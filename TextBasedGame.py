# ==============================
# Cursed Manor — IT 140 project
# Author: Willow Magnante
# ==============================
import time
import random

# ---------- Game State ----------
state = {
    "hp": 25,                 # Base HP for normal players
    "inventory": {},          # item_name -> description
    "books": set(),           # {"lore1", "lore2", "lore3", "lore4", "lore5"}
    "allies": set(),          # {"Cursed Knight", "Mad Alchemist"}
    "trophies": set(),        # {"knight_trophy", "alchemist_trophy"}
    "hidden_found": set(),    # {"hidden1", "hidden2"}
    "current_room": "start",
    "king_defeated": False,
}

# ---------- Win requirements ----------
REQUIRED_ITEMS = {"dagger", "ring"}
REQUIRED_BOOKS = {"lore1", "lore2", "lore3"}  # lore4 & lore5 are optional for sparing King

# ---------- Map ----------
rooms = {
    "start": {"east": "hallway", "south": "kitchen"},
    "kitchen": {"north": "start", "west": "storage"},
    "storage": {"east": "kitchen"},
    "hallway": {"west": "start", "east": "cell1", "south": "cell2", "north": "laboratory"},
    "hidden1": {"up": "hallway"},
    "hidden2": {},  # added dynamically
    "cell1": {"west": "hallway"},  # hidden2 added dynamically
    "cell2": {"north": "hallway"},
    "laboratory": {"south": "hallway", "west": "boss"},
    "boss": {"east": "laboratory"},
}

room_actions = {
    "kitchen": ["search"],
    "storage": ["search"],
    "hallway": ["search"],
    "hidden1": ["search"],
    "hidden2": ["search"],
    "cell2": ["search"],
    "laboratory": ["search"],
    "cell1": ["search"],
    "boss": ["search"],
}

# ---------- Helper Functions ----------
def slow_print(text, delay=0.03):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def add_item(name, desc):
    if name not in state["inventory"]:
        state["inventory"][name] = desc
        slow_print(f"> You pick up {name}.")
        # TODO: flavor text
        slow_print(f"[TODO FLAVOR TEXT] You notice {name} in the room. {desc}")

def add_book(book_id, desc):
    if book_id not in state["books"]:
        state["books"].add(book_id)
        slow_print(f"> You found {book_id}! {desc}")
        # TODO: flavor text
        slow_print(f"[TODO FLAVOR TEXT] You read '{book_id}': {desc}")

def allies_attack():
    total_dmg = 0
    for ally in state["allies"]:
        dmg = random.randint(1, 3)
        slow_print(f"Your ally {ally} attacks for {dmg} damage!")
        # TODO: flavor text
        slow_print(f"[TODO FLAVOR TEXT] {ally} lunges forward, striking the enemy.")
        total_dmg += dmg
    return total_dmg

def allies_defend(incoming_damage):
    reduced = 0
    for ally in state["allies"]:
        if random.random() < 0.25:
            block = random.randint(1, 3)
            slow_print(f"Your ally {ally} blocks {block} damage!")
            # TODO: flavor text
            slow_print(f"[TODO FLAVOR TEXT] {ally} intercepts the blow skillfully!")
            reduced += block
    return max(0, incoming_damage - reduced)

def fight_enemy(enemy_name, enemy_hp, enemy_damage, trophy_name):
    slow_print(f"\nA {enemy_name} lunges at you!")
    # TODO: flavor text
    slow_print(f"[TODO FLAVOR TEXT] You feel a chill as the {enemy_name} approaches!")
    rounds = 0

    while enemy_hp > 0 and state["hp"] > 0:
        rounds += 1
        # Player attacks
        attack_bonus = 2 if "knife" in state["inventory"] else 0
        attack_bonus += len(state["allies"])
        dmg = random.randint(1, 4) + attack_bonus
        enemy_hp -= dmg
        slow_print(f"You strike the {enemy_name} for {dmg} damage!")
        # TODO: flavor text
        slow_print(f"[TODO FLAVOR TEXT] Your blow lands with force!")

        # Allies attack
        if state["allies"]:
            ally_dmg = allies_attack()
            enemy_hp -= ally_dmg

        # Check if enemy defeated
        if enemy_hp <= 0:
            slow_print(f"The {enemy_name} is on the ropes after {rounds} rounds!")
            choice = ""
            while choice not in ("spare", "kill"):
                choice = input(f"Do you SPARE or KILL the {enemy_name}? ").strip().lower()
            if choice == "spare":
                slow_print(f"You spare the {enemy_name}. It joins you as an ally!")
                state["allies"].add(enemy_name)
                state["hp"] += 2
                slow_print(f"{enemy_name} boosts your morale! HP is now {state['hp']}.")
                # TODO: flavor text
                slow_print(f"[TODO FLAVOR TEXT] {enemy_name} kneels and pledges their aid.")
            else:
                slow_print(f"You slay the {enemy_name}, claiming a trophy!")
                state["trophies"].add(trophy_name)
                # TODO: flavor text
                slow_print(f"[TODO FLAVOR TEXT] The {enemy_name} falls, leaving behind a grim token.")

        # Enemy attacks
        if enemy_hp > 0:
            edmg = random.randint(1, enemy_damage)
            edmg = allies_defend(edmg)
            state["hp"] -= edmg
            slow_print(f"The {enemy_name} hits you for {edmg} damage!")
            # TODO: flavor text
            slow_print(f"[TODO FLAVOR TEXT] Pain surges as the {enemy_name} lands its strike!")
            if state["hp"] <= 0:
                slow_print("You have been slain... Game over.")
                exit()

def can_fight_boss():
    # Required items
    has_items = REQUIRED_ITEMS.union({"knife"}).issubset(state["inventory"].keys())
    # Required books
    has_books = REQUIRED_BOOKS.issubset(state["books"])
    # Enemy contributions
    enemies = {"Cursed Knight", "Mad Alchemist"}
    allies_have = state["allies"].intersection(enemies)
    trophies_have = state["trophies"].intersection({"knight_trophy", "alchemist_trophy"})
    
    enemy_condition = (
        allies_have == enemies or                 # both spared
        trophies_have == {"knight_trophy", "alchemist_trophy"} or  # both killed
        len(allies_have) + len(trophies_have) == 2  # one spared, one killed
    )
    return has_items and has_books and enemy_condition

def boss_encounter():
    slow_print("\nYou stand before the corrupted King.")
    # TODO: flavor text
    slow_print("[TODO FLAVOR TEXT] The air grows thick, the shadows deep, as the King glares at you.")
    has_bonus_books = {"lore4", "lore5"}.issubset(state["books"])

    if has_bonus_books:
        choice = input("Do you ATTACK or SPARE the King? ").strip().lower()
        if choice == "spare":
            slow_print("You spare the King, breaking the curse with compassion...")
            # TODO: flavor text
            slow_print("[TODO FLAVOR TEXT] A wave of light and relief washes over the chamber.")
            state["king_defeated"] = True
            ending(True)
            return

    fight_enemy("King", 35, 8, "king_trophy")
    state["king_defeated"] = True
    ending(False)

def ending(spared):
    slow_print("\n=== GAME OVER ===")
    if spared:
        slow_print("With the two hidden lore books, you learned the King was a victim. Your mercy frees him.")
        # TODO: flavor text
        slow_print("[TODO FLAVOR TEXT] Peace returns to the manor, the shadows recede.")
    else:
        slow_print("The King lies dead, the curse broken... but perhaps the true evil still lurks.")
        # TODO: flavor text
        slow_print("[TODO FLAVOR TEXT] A chill remains in the air, hinting at unseen threats.")
    exit()

# ---------- Start Game ----------
player_name = input("Enter your name, brave adventurer: ").strip().lower()
if player_name in ("archy", "archebald"):
    state["hp"] = 1000
    slow_print("Ah, the legendary Archy! You feel invincible! HP set to 1000.")
elif player_name == "inmate":
    state["hp"] = 35
    slow_print("You are an inmate with just enough strength to endure the cursed manor. Tread carefully.")
else:
    slow_print(f"Welcome, {player_name.capitalize()}. May your wits guide you through the manor.")

# ---------- Main Loop ----------
current_room = "start"
bad_inputs = 0

while not state["king_defeated"]:
    print(f"\nYou are in {current_room}.")
    # TODO: flavor text for room description
    slow_print(f"[TODO FLAVOR TEXT] You look around the {current_room} carefully.")
    time.sleep(0.5)
    print("Available moves:")
    for direction, dest in rooms[current_room].items():
        print(f" - {direction} -> {dest}")
    print(" - exit")

    if current_room in room_actions:
        print("You can also: " + ", ".join(room_actions[current_room]))

    user_input = input("\nWhat do you do? ").strip().lower()

    if user_input == "exit":
        slow_print("Thanks for playing!")
        break

    elif user_input in rooms[current_room]:
        current_room = rooms[current_room][user_input]
        bad_inputs = 0

    elif user_input in room_actions.get(current_room, []):
        bad_inputs = 0
        slow_print(f"You search the {current_room}...")

        # Kitchen
        if current_room == "kitchen":
            add_item("knife", "A sharp kitchen knife (+2 attack).")

        # Storage
        elif current_room == "storage":
            add_book("lore1", "[Lore 1 placeholder: Required book text goes here]")

        # Hallway
        elif current_room == "hallway":
            add_book("lore2", "[Lore 2 placeholder: Required book text goes here]")
            if "hidden1" not in state["hidden_found"]:
                state["hidden_found"].add("hidden1")
                slow_print("You press a loose brick... a hidden door opens below the hallway (hidden1)!")
                rooms["hallway"]["down"] = "hidden1"

        # Hidden1
        elif current_room == "hidden1":
            add_book("lore4", "[Lore 4 placeholder: Optional book text goes here]")

        # Cell1
        elif current_room == "cell1":
            fight_enemy("Cursed Knight", 12, 5, "knight_trophy")
            if "hidden2" not in state["hidden_found"]:
                state["hidden_found"].add("hidden2")
                slow_print("A hidden door opens to the east (hidden2)!")
                rooms["cell1"]["east"] = "hidden2"
                rooms["hidden2"]["west"] = "cell1"  # <-- Fixed return path

        # Hidden2
        elif current_room == "hidden2":
            add_book("lore5", "[Lore 5 placeholder: Optional book text goes here]")

        # Cell2
        elif current_room == "cell2":
            add_book("lore3", "[Lore 3 placeholder: Required book text goes here]")

        # Laboratory
        elif current_room == "laboratory":
            fight_enemy("Mad Alchemist", 14, 5, "alchemist_trophy")

        # Boss
        elif current_room == "boss":
            add_item("dagger", "A dagger, cold to the touch. You know what it’s for.")
            if can_fight_boss():
                boss_encounter()
            else:
                slow_print("You feel unprepared to face the King... perhaps you need more items or allies.")

    else:
        first_dir, first_room = next(iter(rooms[current_room].items()))
        if bad_inputs == 0:
            slow_print("That's not an option...")
        elif bad_inputs == 1:
            slow_print("Seriously... I literally gave you the options right there.")
        elif bad_inputs >= 2:
            slow_print(f"Ok, fine. When I say '{first_dir} -> {first_room}', just type '{first_dir}'. Easy.")
        bad_inputs += 1
