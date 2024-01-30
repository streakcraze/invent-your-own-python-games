"""This is a Guess the Number game."""

import re
import random

print("Hello! What is your name?")
username = input()

secret_number = random.randint(1, 20)

print(f"Well, {username}, I am thinking of a number between 1 and 20.")

for guesses_taken in range(1, 7):
    user_guess = ""
    while re.match("^[1-9][0-9]*$", user_guess) is None or int(user_guess) > 20:
        print("Take a guess. (1~20)")
        user_guess = input()
    user_guess = int(user_guess)

    if user_guess > secret_number:
        print("Your guess is too high.")
    elif user_guess < secret_number:
        print("Your guess is too low.")
    else:
        print(
            f"Good job, {username}! You guessed my number in {guesses_taken} {'try' if guesses_taken == 1 else 'tries'}"
        )
        break
else:
    print(
        f"You have run out of guesses! The number I was thinking of was {secret_number}"
    )
