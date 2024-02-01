"""Reversegam has an 8*8 board and tiles that are black on one side and white
on the other (our game will use Os and Xs instead). Two players take turns 
placing tiles of their chosen color—black or white—on the board. When a player 
places a tile on the board, any of the opponent's tiles that are between 
the new tile and the other tiles of the player's color are flipped. The goal
of the game is to end with more tiles of your color than your opponent's color."""

import re
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


def get_scores(
    player_mark: str, opponent_mark: str, board: list[list[str]]
) -> tuple[int, int]:
    """returns scores"""

    flattened_board = [item for row in board for item in row]
    player_scores = flattened_board.count(player_mark)
    opponent_scores = flattened_board.count(opponent_mark)

    return (player_scores, opponent_scores)


def user_plays() -> str:
    """retrieves coordinates from user"""

    coordinate = ""
    while re.match("^[a-h][1-8]$", coordinate) is None:
        print("Where do you want to play? ([a~h][1~8]) eg. a1, b4, g7, etc.")
        coordinate = input()

    return coordinate


def computer_plays(ai_mark: str, board: list[list[str]]) -> str:
    """retrieves coordinates with highest score"""

    opponent_mark = "X" if ai_mark == "O" else "O"

    scores = {}
    for row in range(1, 9):
        for column in COLUMNS:
            coordinates = column + str(row)
            # copy of the playing board for simulation
            dummy_board = deepcopy(board)
            if valid_move(ai_mark, coordinates, dummy_board):
                scores[coordinates] = get_scores(ai_mark, opponent_mark, dummy_board)[0]

    # get coordinate with max score
    coordinate_max = max(scores, key=lambda x: scores[x], default="")
    # play with the max score on the playing board
    valid_move(ai_mark, coordinate_max, board)

    return coordinate_max


def check_direction(
    direction: str, coordinates: list[int], board: list[list[str]]
) -> tuple[list[int], str]:
    """returns coordinates of checked direction from selected position and the mark in the space"""

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


def not_within_the_board(row: int, column: int, direction: str) -> bool:
    """checks for movement outside the board"""

    if (
        (row == 0 and direction in ["up", "diagonal0", "diagonal3"])
        or (column == 0 and direction in ["left", "diagonal2", "diagonal3"])
        or (row == 7 and direction in ["down", "diagonal1", "diagonal2"])
        or (column == 7 and direction in ["right", "diagonal0", "diagonal1"])
    ):
        return True
    else:
        return False


def valid_move(player_mark: str, coordinates: str, board: list[list[str]]):
    """confirms whether selected position is a valid move and flips necessary tiles"""

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
            # starting from selected position check all directions for opponent's mark
            for direction in directions:
                # move within the board
                if not_within_the_board(row, column, direction):
                    continue
                new_coordinates, new_mark = check_direction(
                    direction, [row, column], board
                )

                may_be_flipped = []
                # if opponent's mark is found go further looking for player's mark
                while new_mark == opponent_mark:
                    # save each opponent's mark coordinates
                    may_be_flipped.append(new_coordinates)
                    # move within the board
                    if not_within_the_board(
                        new_coordinates[0], new_coordinates[1], direction
                    ):
                        break
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


def game_over(player_mark: str, board: list[list[str]]):
    """checks if there are any valid moves for the player"""

    for row in range(1, 9):
        for column in COLUMNS:
            coordinates = column + str(row)
            # copy of the playing board for simulation
            dummy_board = deepcopy(board)
            # board only gets changed if it's a valid move
            if valid_move(player_mark, coordinates, dummy_board):
                return False

    return True


def print_results(user_score: int, computer_score: int) -> None:
    """prints results at the end of the game"""

    print("GAME OVER!")
    if user_score > computer_score:
        print("YOU WON")
    elif user_score < computer_score:
        print("COMPUTER WINS")
    else:
        print("IT'S A TIE")


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

    while True:
        print("SCORES:")
        user_score, computer_score = get_scores(user_mark, computer_mark, playing_board)
        print(f"You: {user_score}")
        print(f"Computer: {computer_score}")
        print()

        # check if there is a valid move for the user
        if game_over(user_mark, playing_board):
            print_results(user_score, computer_score)
            break

        user_coordinate = ""
        while not valid_move(user_mark, user_coordinate, playing_board):
            user_coordinate = user_plays()
        draw_board(playing_board)

        # check if there is a valid move for the computer
        if game_over(computer_mark, playing_board):
            print_results(user_score, computer_score)
            break

        print("Computer plays...", end="\r")
        time.sleep(2)
        computer_coordinate = computer_plays(computer_mark, playing_board)
        print(f"Computer plays: {computer_coordinate}")
        draw_board(playing_board)
