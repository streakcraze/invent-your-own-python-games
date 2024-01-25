"""This game is called Dragon Realm. 
The player chooses between two caves, 
one which holds treasure 
or another which holds certain doom."""

import random
import time
from textwrap import dedent


def intro() -> str:
    """:return -> str: introduction text for the game"""

    intro_text = """
    You are in a land full of dragons.
    In front of you, there are two caves.
    One cave has a friendly dragon who will share his treasure with you.
    The other cave has a greedy and hungry dragon who will eat you on sight.
    """
    return dedent(intro_text)


def choose_cave() -> int:
    """:return -> int: cave chosen by player"""

    cave = 0
    while cave != 1 and cave != 2:
        print("Which cave will you go into? (1 or 2)")
        cave = int(input())

    return cave


def check_cave(cave_choice: int) -> None:
    """:cave_choice -> int: either cave 1 or 2 chosen by player"""

    print("You approach the cave...")
    time.sleep(3)
    print("It is dark and spooky...")
    time.sleep(3)
    print(
        "A large dragon jumps out in front of you! He opens his jaws and ..."
    )
    time.sleep(3)

    friendly_cave = random.randint(1, 2)

    if cave_choice == friendly_cave:
        print("Gives you his treasure.")
    else:
        print("Gobbles you down in one bite.")

    time.sleep(3)


if __name__ == "__main__":
    while True:
        print(intro())
        cave_choice = choose_cave()
        check_cave(cave_choice)

        print("Do you want to continue playing? (yes or no)")
        continue_playing = input().lower()

        if continue_playing == "no":
            break
