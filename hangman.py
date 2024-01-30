"""Hangman is a game for two people in which one player thinks of a word
and then draws a blank line for each letter in the word. The second player 
then tries to guess a letter of the word. For each letter guessed correctly 
the first player writes the letter in the proper blank. However, for each letter 
guessed incorrectly the first player draws a single body part of a hanging man 
until he is complete, at which point the second player loses."""

import random
import time

HANGMAN_PICS = [
    """
  
     
     
     
    ===""",
    """

     |
     |
     |
    ===""",
    """
 +---+
     |
     |
     |
    ===""",
    """
 +---+
 0   |
     |
     |
    ===""",
    """
 +---+
 0   |
 |   |
     |
    ===""",
    """
 +---+
 0   |
/|   |
     |
    ===""",
    """
 +---+
 0   |
/|\\  |
     |
    ===""",
    """
 +---+
 0   |
/|\\  |
/    |
    ===""",
    """
 +---+
 0   |
/|\\  |
/ \\  |
    ===""",
    """
 +---+
[0   |
/|\\  |
/ \\  |
    ===""",
    """
 +---+
[0]  |
/|\\  |
/ \\  |
    ===""",
]

WORDS = {
    "animals": """bat bear beaver cat cougar crab deer dog donkey duck eagle
 fish frog goat leech lion lizard monkey moose mouse otter owl panda
 python rabbit rat shark sheep skunk squid tiger turkey turtle weasel
 whale wolf wombat zebra""".split(),
    "colors": "red orange yellow green blue indigo violet white black brown".split(),
    "fruits": """apple orange lemon lime pear watermelon grape grapefruit cherry
 banana cantaloupe mango strawberry tomato""".split(),
    "shapes": """square triangle rectangle circle ellipse rhombus trapezoid chevron 
 pentagon hexagon septagon octagon""".split(),
}


def random_word(word_dict: dict[str, list]) -> tuple[str, str]:
    """takes in a list of words and returns a random word from the list"""

    category: str = random.choice(list(word_dict.keys()))
    word: str = random.choice(word_dict[category])

    return (category, word)


def get_guess(already_guessed: str) -> str:
    """makes sure the player enters a single letter and returns it"""

    print("Guess a letter")

    while True:
        guess: str = input().lower()

        if len(guess) != 1:
            print("Please enter a single letter.")
        elif guess in already_guessed:
            print("You have already guessed that letter. Choose another one.")
        elif not guess.isalpha():
            print("Please enter a letter.")
        else:
            break

    return guess


if __name__ == "__main__":
    while True:
        print("H A N G M A N")
        time.sleep(2)

        difficulty_level = ""
        while difficulty_level not in ["E", "M", "H"]:
            print("Choose difficulty level. (E, M, or H)")
            print("E - easy, M - medium, H - hard")
            difficulty_level: str = input().upper()

        if difficulty_level == "M":
            HANGMAN_PICS_DIFF: list[str] = HANGMAN_PICS[:-2]
        elif difficulty_level == "H":
            HANGMAN_PICS_DIFF: list[str] = HANGMAN_PICS[2:-2]
        else:
            HANGMAN_PICS_DIFF: list[str] = HANGMAN_PICS

        category, secret_word = random_word(WORDS)
        print(f"The category is: {category}")

        matched_letters = ""
        mismatched_letters = ""

        fails = 0
        while fails < len(HANGMAN_PICS_DIFF):
            print("Secret word is:")
            for letter in secret_word:
                if letter in matched_letters:
                    print(letter, end="")
                else:
                    print("_", end="")
            print()

            guess: str = get_guess(matched_letters + mismatched_letters)

            if guess in secret_word:
                print("CORRECT!")
                matched_letters += guess
            else:
                print("WRONG!")
                mismatched_letters += guess
                print(HANGMAN_PICS_DIFF[fails])
                fails += 1

            if sorted(matched_letters) == sorted(set(secret_word)):
                print("CONGRATULATIONS! The secret word is complete. You have WON.")
                print("The Secret word is:")
                print(secret_word)
                break
        else:
            print("SORRY! The Hangman is complete. You have LOST.")
            print("The Secret word was:")
            print(secret_word)

        print("Do you want to play again? (yes or no)")
        continue_playing: str = input().lower()
        if continue_playing == "no":
            print("Thank you for playing. BYE!")
            break
