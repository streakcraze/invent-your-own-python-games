"""This is a Guess the Number game."""

import random

guesses_taken = 0

print("Hello! What is your name?")
username = input()

secret_number = random.randint(1, 20)

print(f"Well, {username}, I am thinking of a number between 1 and 20.")

for guesses_taken in range(6):
    print("Take a guess.")
    user_guess = input()
    user_guess = int(user_guess)

    if user_guess > secret_number:
        print("Your guess is too high.")
    elif user_guess < secret_number:
        print("Your guess is too low.")
    else:
        break

if user_guess == secret_number:
    guesses_taken += 1
    print(
        f"Good job, {username}! You guessed my number in {guesses_taken} {'try' if guesses_taken == 1 else 'tries'}"
    )
else:
    print(f"Nope! The number I was thinking of was {secret_number}")
