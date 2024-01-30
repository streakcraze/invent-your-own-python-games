import re
import random
import time
from copy import deepcopy

NEW_BOARD = [list(" " * 8) for _ in range(8)]
COLUMNS = "abcdefgh"


def draw_board(board: list[list[str]]):
    """prints out board with moves from the passed list"""

    print()
    print("  a b c d e f g h  ")
    print(" +-+-+-+-+-+-+-+-+ ")

    for row in range(len(board)):
        print(f"{row + 1}|", end="")
        for column in range(len(board[row])):
            print(board[row][column] + "|", end="")
        print()
        print(" +-+-+-+-+-+-+-+-+ ")

    print()


def user_plays() -> str:
    coordinate = ""
    while re.match("^[a-i][1-9]$", coordinate) is None:
        print("Where do you want to play? ([a~i][1~9]) eg. a1, b4, g7, etc.")
        coordinate = input()

    return coordinate


def computer_plays() -> str:
    coordinate = ""
    coordinate += random.choice(list(COLUMNS))
    coordinate += str(random.choice(list(range(1, 9))))

    return coordinate


def check_direction(
    direction: str, coordinates: list[int], board: list[list[str]]
) -> tuple[list[int], str]:
    row = coordinates[0]
    column = coordinates[1]

    if direction == "up":
        new_row = row - 1
        new_column = column
        new_mark = board[new_row][new_column]
    elif direction == "down":
        new_row = row + 1
        new_column = column
        new_mark = board[new_row][new_column]
    elif direction == "left":
        new_row = row
        new_column = column - 1
        new_mark = board[new_row][new_column]
    elif direction == "right":
        new_row = row
        new_column = column + 1
        new_mark = board[new_row][new_column]
    elif direction == "diagonal0":
        new_row = row - 1
        new_column = column + 1
        new_mark = board[new_row][new_column]
    elif direction == "diagonal1":
        new_row = row + 1
        new_column = column + 1
        new_mark = board[new_row][new_column]
    elif direction == "diagonal2":
        new_row = row + 1
        new_column = column - 1
        new_mark = board[new_row][new_column]
    elif direction == "diagonal3":
        new_row = row - 1
        new_column = column - 1
        new_mark = board[new_row][new_column]
    else:
        raise Exception

    return ([new_row, new_column], new_mark)


def valid_move(player_mark: str, coordinates: str, board: list[list[str]]):
    if len(coordinates) == 2:
        column = COLUMNS.index(coordinates[0])
        row = int(coordinates[1]) - 1

        if board[row][column] == " ":
            opponent_mark = "X" if player_mark == "O" else "O"
            directions = [
                "up",
                "down",
                "left",
                "right",
                "diagonal0",
                "diagonal1",
                "diagonal2",
                "diagonal3",
            ]

            found_valid_move = False
            for direction in directions:
                # move within the board
                if (
                    (row == 0 and direction in ["up", "diagonal0", "diagonal3"])
                    or (column == 0 and direction in ["left", "diagonal2", "diagonal3"])
                    or (row == 7 and direction in ["down", "diagonal1", "diagonal2"])
                    or (
                        column == 7 and direction in ["right", "diagonal0", "diagonal1"]
                    )
                ):
                    continue

                # starting from selected position check all directions for opponent's mark
                new_coordinates, new_mark = check_direction(
                    direction, [row, column], board
                )

                may_be_flipped = []
                while new_mark == opponent_mark:
                    # save each opponent's mark coordinates
                    may_be_flipped.append(new_coordinates)
                    # if opponent's mark is found go further looking for player's mark
                    new_coordinates, new_mark = check_direction(
                        direction, [new_coordinates[0], new_coordinates[1]], board
                    )

                    if new_mark == player_mark:
                        # if player's mark is found flip all opponent marks between it
                        # and the selected position
                        for x, y in may_be_flipped:
                            board[x][y] = player_mark

                        found_valid_move = True

            if found_valid_move:
                board[row][column] = player_mark
                return True

    return False


if __name__ == "__main__":
    playing_board = deepcopy(NEW_BOARD)

    centers = {"X": [[3, 3], [4, 4]], "O": [[3, 4], [4, 3]]}
    for key, value in centers.items():
        playing_board[value[0][0]][value[0][1]] = key
        playing_board[value[1][0]][value[1][1]] = key

    print("R E V E R S E G A M")
    time.sleep(2)

    print("LET'S BEGIN")
    draw_board(playing_board)

    user_mark = ""
    while user_mark != "X" and user_mark != "O":
        print("Choose X or O:")
        user_mark = input().upper()
    computer_mark = "X" if user_mark == "O" else "O"

    play_time = 5
    while play_time > 0:
        user_coordinate = ""
        while not valid_move(user_mark, user_coordinate, playing_board):
            user_coordinate = user_plays()

        draw_board(playing_board)

        print("Computer plays...", end="\r")
        time.sleep(2)

        computer_coordinate = ""
        while not valid_move(computer_mark, computer_coordinate, playing_board):
            computer_coordinate = computer_plays()

        print(f"Computer plays: {computer_coordinate}")
        draw_board(playing_board)

        play_time -= 1
