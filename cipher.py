"""Caesar's cipher encrypts a message by replacing each symbol 
with another symbol from a shifted symbol table. The table is
shifted using a key which is a number representing how many times
the symbol table should be shifted to the left.
SYMBOL TABLE: |A|B|C|D|E|F|
KEY: 1
SHIFTED SYMBOL TABLE: |B|C|D|E|F|A|
KEY: 2
SHIFTED SYMBOL TABLE: |C|D|E|F|A|B|
"""

import re
from typing import List, Tuple

SYMBOLS = list(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !?@#$%^&*()"
)


def get_message_and_key() -> Tuple[str, int]:
    """requests user message and key, validates the key, and returns them"""

    print("Enter message:")
    user_message = input()

    user_key = ""
    while re.match("^[1-9][0-9]*$", user_key) is None or int(user_key) > len(SYMBOLS):
        print(f"Enter key: (1~{len(SYMBOLS)})")
        user_key = input()
    user_key = int(user_key)

    return (user_message, user_key)


def rotate_chars(chars_list: List[str], key) -> List[str]:
    """shifts symbol table to the left by number of times provided by key"""

    for _ in range(key):
        chars_list.append(chars_list.pop(0))

    return chars_list


def encrypt_message(original_message: str, shifted_symbols: List[str]) -> str:
    """encrypts message using symbols rotated by user key"""

    shifted_message = ""
    for i in range(len(message)):
        shifted_message += shifted_symbols[SYMBOLS.index(original_message[i])]

    return shifted_message


def decrypt_message(shifted_message: str, shifted_symbols: List[str]) -> str:
    """receives encrypted message and reconstructs the original message from it"""

    original_message = ""
    for i in range(len(message)):
        original_message += SYMBOLS[shifted_symbols.index(shifted_message[i])]

    return original_message


print("C A E S A R' S  C I P H E R")
message, key = get_message_and_key()
rotated_chars = rotate_chars(SYMBOLS.copy(), key)

# choose to encrypt or decrypt message
user_option = ""
while user_option != "encrypt" and user_option != "decrypt":
    print("Do you want to encrypt or decrypt?")
    user_option = input().lower()

# receive encrypted or decrypted message
if user_option == "encrypt":
    new_message = encrypt_message(message, rotated_chars)
    print(f"Encrypted message: {new_message}")
else:
    new_message = decrypt_message(message, rotated_chars)
    print(f"Decrypted message: {new_message}")
