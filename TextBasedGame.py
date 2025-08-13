# ==============================
# Cursed Manor — IT 140 project
# Author: Willow Magnante
# ==============================
import time
import random

# ---------- Game State ----------
state = {
    "hp": 12,
    "inventory": {},          # item_name -> description
    "books": set(),           # {"lore1", "lore2", "lore3", "lore4", "lore5"}
    "allies": set(),          # {"enemy1", "enemy2"}
    "trophies": set(),        # {"enemy1_trophy", "enemy2_trophy"}
    "hidden_found": set(),    # {"hidden1", "hidden2"}
    "current_room": "start",
    "king_defeated": False,
}

# ---------- Win requirements ----------
REQUIRED_ITEMS = {"dagger", "ring"}
REQUIRED_BOOKS = {"lore1", "lore2", "lore3"}  # lore4 & lore5 are bonus

# ---------- Map ----------
rooms = {
    "start": {"east": "hallway", "south": "kitchen"},
    "kitchen": {"north": "start", "west": "storage"},
    "storage": {"east": "kitchen"},
    "hallway": {"west": "start", "east": "cell1", "south": "cell2", "north": "laboratory"},
    "cell1": {"west": "hallway"},         
    "cell2": {"north": "hallway"},
    "laboratory": {"south": "hallway", "north": "boss"},
    "boss": {"south": "laboratory"},
    # Hidden rooms (locked until found)
    "hidden1": {"up": "hallway"},
    "hidden2": {"west": "cell1"},
}

# Rooms where search does something
room_actions = {
    "kitchen": ["search"],
    "hallway": ["search"],
    "cell1": ["search"],
    "cell2": ["search"],
    "storage": ["search"],
    "laboratory": ["search"],
    "boss": ["search"],
    "hidden1": ["search"],
    "hidden2": ["search"],
}

# ---------- Helper functions ----------
def slow_print(text, delay=0.03):
    """Print text one character at a time."""
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def add_item(name, desc):
    if name not in state["inventory"]:
        state["inventory"][name] = desc
        slow_print(f"> You pick up {name}.")

def add_book(book_id, desc):
    if book_id not in state["books"]:
        state["books"].add(book_id)
        slow_print(f"> You found {book_id}! {desc}")

def fight_enemy(enemy_name, enemy_hp, enemy_damage, trophy_name):
    slow_print(f"\nA {enemy_name} lunges at you!")
    attack_bonus = 2 if "knife" in state["inventory"] else 0

    while enemy_hp > 0 and state["hp"] > 0:
        dmg = random.randint(1, 4) + attack_bonus
        enemy_hp -= dmg
        slow_print(f"You strike the {enemy_name} for {dmg} damage!")
        if enemy_hp <= 0:
            slow_print(f"The {enemy_name} is defeated!")
            state["trophies"].add(trophy_name)
            return

        edmg = random.randint(1, enemy_damage)
        state["hp"] -= edmg
        slow_print(f"The {enemy_name} hits you for {edmg} damage!")
        if state["hp"] <= 0:
            slow_print("You have been slain... Game over.")
            exit()

def boss_encounter():
    slow_print("\nYou stand before the corrupted King.")
    has_bonus_books = {"lore4", "lore5"}.issubset(state["books"])

    if has_bonus_books:
        choice = input("Do you ATTACK or SPARE the King? ").strip().lower()
        if choice == "spare":
            slow_print("You spare the King, breaking the curse with compassion...")
            state["king_defeated"] = True
            ending(True)
            return

    fight_enemy("King", 12, 5, "king_trophy")
    state["king_defeated"] = True
    ending(False)

def ending(spared):
    slow_print("\n=== GAME OVER ===")
    if spared:
        slow_print("With the two hidden lore books, you learned the King was a victim. Your mercy frees him.")
    else:
        slow_print("The King lies dead, the curse broken... but perhaps the true evil still lurks.")
    exit()

# ---------- Main Loop ----------
current_room = "start"
bad_inputs = 0

while not state["king_defeated"]:
    print(f"\nYou are in {current_room}.")
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
        bad_inputs = 0  # Reset on valid input

    elif user_input in room_actions.get(current_room, []):
        bad_inputs = 0  # Reset on valid input
        slow_print(f"You search the {current_room}...")

        # Search logic per room
        if current_room == "kitchen":
            add_item("knife", "A sharp kitchen knife (+2 attack).")

        elif current_room == "hallway" and "hidden2" not in state["hidden_found"]:
            state["hidden_found"].add("hidden2")
            slow_print("You press a loose brick... a hidden door opens to a secret chamber (hidden2)!")
            rooms["hallway"]["secret"] = "hidden2"

        elif current_room == "cell1" and "hidden1" not in state["hidden_found"]:
            state["hidden_found"].add("hidden1")
            slow_print("You find a concealed switch... a hidden staircase leads to a secret room (hidden1)!")
            rooms["cell1"]["secret"] = "hidden1"

        elif current_room == "hidden1":
            add_book("lore4", "[Lore 4 placeholder: Optional book text goes here]")

        elif current_room == "hidden2":
            add_book("lore5", "[Lore 5 placeholder: Optional book text goes here]")

        elif current_room == "storage":
            add_item("ring", "An enchanted ring to resist the curse.")
            state["hp"] += 10
            slow_print(f"You feel stronger. HP is now {state['hp']}.")

        elif current_room == "cell2":
            fight_enemy("Cursed Guard", 6, 3, "guard_trophy")

        elif current_room == "laboratory":
            add_book("lore1", "[Lore 1 placeholder: Required book text goes here]")

        elif current_room == "boss":
            add_item("dagger", "A dagger, cold to the touch. You know what it’s for.")
            if REQUIRED_ITEMS.issubset(state["inventory"].keys()) and REQUIRED_BOOKS.issubset(state["books"]):
                boss_encounter()

    else:
        first_dir, first_room = next(iter(rooms[current_room].items()))
        if bad_inputs == 0:
            slow_print("That's not an option...")
        elif bad_inputs == 1:
            slow_print("Seriously... I literally gave you the options right there.")
        elif bad_inputs >= 2:
            slow_print(f"Ok, fine. When I say '{first_dir} -> {first_room}', just type '{first_dir}'. Easy.")
        bad_inputs += 1
