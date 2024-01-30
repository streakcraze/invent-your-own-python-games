"""Tic-Tac-Toe is played by two players on a 3*3 matrix.
One player is X and the other is O. Players take turns
placing Xs and Os on the matrix. If a player marks 3 spaces
either in a row, column or diagonal, they win. Otherwise,
the game ends in a draw.
-+-+-
X|O|X
-+-+-
O|X|O
-+-+-
X|O|X
-+-+-
"""

import re
import random
import time


def draw_board(board: list[str]):
    """prints out board with moves from the passed list"""

    print("+-+-+-+")
    print("|" + board[0] + "|" + board[1] + "|" + board[2] + "|")
    print("+-+-+-+")
    print("|" + board[3] + "|" + board[4] + "|" + board[5] + "|")
    print("+-+-+-+")
    print("|" + board[6] + "|" + board[7] + "|" + board[8] + "|")
    print("+-+-+-+")
    print()


def player_chooses_mark() -> tuple[str, str]:
    """returns letters for player and computer"""

    player_letter = ""
    while player_letter != "X" and player_letter != "O":
        print("Choose X or O")
        player_letter = input().upper()
    computer_letter = "X" if player_letter == "O" else "O"

    return (player_letter, computer_letter)


def check_for_win(current_play: list[str]) -> tuple[bool, str]:
    """checks the current play for any winner and returns tuple of
    True/False and the winner"""

    Xs = []
    Os = []

    for index, val in enumerate(current_play):
        if val == "X":
            Xs.append(index)
        elif val == "O":
            Os.append(index)
        else:
            pass

    wins = [
        [0, 1, 2],  # row 0
        [3, 4, 5],  # row 1
        [6, 7, 8],  # row 2
        [0, 3, 6],  # column 0
        [1, 4, 7],  # column 1
        [2, 5, 8],  # column 2
        [0, 4, 8],  # diagonal 0
        [2, 4, 6],  # diagonal 1
    ]

    for element in wins:
        if all(value in Xs for value in element):
            return (True, "X")
        elif all(value in Os for value in element):
            return (True, "O")
        else:
            pass
    else:
        return (False, "None")


def get_player_move(player_mark: str, current_play: list[str]) -> list[str]:
    """receives list of already made moves, asks player for new move, and returns
    a new list with the new move"""

    player_move = ""

    while (
        re.match("^[1-9]$", player_move) is None
        or current_play[int(player_move) - 1] != " "
    ):
        print("Choose where to mark. (1~9)")
        player_move = input()

    new_play = current_play.copy()
    new_play[int(player_move) - 1] = player_mark

    return new_play


def get_computer_move(computer_mark: str, current_play: list[str]) -> list[str]:
    """the computer's AI algorithm for playing"""

    empty_spaces = [index for index, val in enumerate(current_play) if val == " "]
    new_play = current_play.copy()

    # 1. make winning move
    for move in empty_spaces:
        new_play[move] = computer_mark
        if check_for_win(new_play)[0]:
            return new_play
        else:
            new_play[move] = " "

    # 2. block opponent's winning move
    for move in empty_spaces:
        new_play[move] = "X" if computer_mark == "O" else "O"
        if check_for_win(new_play)[0]:
            new_play[move] = computer_mark
            return new_play
        else:
            new_play[move] = " "

    # 3. take one of the corners
    corners = [0, 2, 6, 8]
    for move in corners:
        if move in empty_spaces:
            new_play[move] = computer_mark
            return new_play

    # 4. take the center
    if 4 in empty_spaces:
        new_play[4] = computer_mark
        return new_play

    # 5. take any of the remaining spots
    new_play[random.choice(empty_spaces)] = computer_mark
    return new_play


if __name__ == "__main__":
    print("T I C - T A C - T O E")
    print()
    time.sleep(2)

    print("Coordinates for the board:")
    numbered = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    draw_board(numbered)
    time.sleep(2)

    print("Let's begin.")
    empty = [" " for _ in numbered]
    draw_board(empty)
    player, computer = player_chooses_mark()

    ongoing_play = empty.copy()
    while True:
        # player makes a move
        ongoing_play = get_player_move(player, ongoing_play)
        draw_board(ongoing_play)
        # check if player won
        if check_for_win(ongoing_play)[0]:
            break

        # check if board is empty
        if not any(pos == " " for pos in ongoing_play):
            break

        # computer makes a move
        ongoing_play = get_computer_move(computer, ongoing_play)
        draw_board(ongoing_play)
        # check if computer won
        if check_for_win(ongoing_play)[0]:
            break

    # post results
    print(check_for_win(ongoing_play)[1] + " wins")
