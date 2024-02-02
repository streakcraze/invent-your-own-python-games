"""Runs simulation of different algorithms multiple times"""

import re
import time
import random
from copy import deepcopy
from textwrap import dedent

NEW_BOARD = [list(" " * 8) for _ in range(8)]
COLUMNS = "abcdefgh"


def get_scores(
    player_mark: str, opponent_mark: str, board: list[list[str]]
) -> tuple[int, int]:
    """returns scores"""

    flattened_board = [item for row in board for item in row]
    player_scores = flattened_board.count(player_mark)
    opponent_scores = flattened_board.count(opponent_mark)

    return (player_scores, opponent_scores)


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


def get_allowed_moves(player_mark: str, board: list[list[str]]) -> list[str]:
    """returns list of coordinates that are allowed moves for the player"""

    allowed_moves = []

    for row in range(1, 9):
        for column in COLUMNS:
            coordinates = column + str(row)
            # copy of the playing board for simulation
            dummy_board = deepcopy(board)
            # board only gets changed if it's a valid move
            if valid_move(player_mark, coordinates, dummy_board):
                allowed_moves.append(coordinates)

    return allowed_moves


def corner_first_computer(
    player_mark: str, allowed_moves: list[str], board: list[list[str]]
):
    """applies corner moves otherwise retrieves coordinates with highest score
    and plays with it"""

    opponent_mark = "X" if player_mark == "O" else "O"
    corners = ["a1", "h1", "a8", "h8"]

    for corner in corners:
        if corner in allowed_moves:
            # play with the corner on the playing board
            valid_move(player_mark, corner, board)
            break
    else:
        # if none of the corners are in allowed_moves use the best score
        scores = {}
        for coordinates in allowed_moves:
            # copy of the playing board for simulation
            dummy_board = deepcopy(board)
            # play with the valid move on the simulation board
            valid_move(player_mark, coordinates, dummy_board)
            # get the score of the move and store them
            scores[coordinates] = get_scores(player_mark, opponent_mark, dummy_board)[0]

        # get coordinate with max score
        coordinate_max = max(scores, key=lambda x: scores[x], default="")
        # play with the max score on the playing board
        valid_move(player_mark, coordinate_max, board)


def side_first_computer(
    player_mark: str, allowed_moves: list[str], board: list[list[str]]
):
    """applies side moves otherwise retrieves coordinates with highest score
    and plays with it"""

    opponent_mark = "X" if player_mark == "O" else "O"

    for coordinate in allowed_moves:
        # side coordinate has to have "a" or "1" or "h" or "7"
        if any(side_indicator in coordinate for side_indicator in ["a", "1", "h", "7"]):
            # play with the corner on the playing board
            valid_move(player_mark, coordinate, board)
            break
    else:
        # if none of the corners are in allowed_moves use the best score
        scores = {}
        for coordinates in allowed_moves:
            # copy of the playing board for simulation
            dummy_board = deepcopy(board)
            # play with the valid move on the simulation board
            valid_move(player_mark, coordinates, dummy_board)
            # get the score of the move and store them
            scores[coordinates] = get_scores(player_mark, opponent_mark, dummy_board)[0]

        # get coordinate with max score
        coordinate_max = max(scores, key=lambda x: scores[x], default="")
        # play with the max score on the playing board
        valid_move(player_mark, coordinate_max, board)


def best_scoring_computer(
    player_mark: str, allowed_moves: list[str], board: list[list[str]]
):
    """retrieves coordinates with highest score and plays with it"""

    opponent_mark = "X" if player_mark == "O" else "O"

    scores = {}
    for coordinates in allowed_moves:
        # copy of the playing board for simulation
        dummy_board = deepcopy(board)
        # play with the valid move on the simulation board
        valid_move(player_mark, coordinates, dummy_board)
        # get the score of the move and store them
        scores[coordinates] = get_scores(player_mark, opponent_mark, dummy_board)[0]

    # get coordinate with max score
    coordinate_max = max(scores, key=lambda x: scores[x], default="")
    # play with the max score on the playing board
    valid_move(player_mark, coordinate_max, board)


def worst_scoring_computer(
    player_mark: str, allowed_moves: list[str], board: list[list[str]]
):
    """retrieves coordinates with lowest score and plays with it"""

    opponent_mark = "X" if player_mark == "O" else "O"

    scores = {}
    for coordinates in allowed_moves:
        # copy of the playing board for simulation
        dummy_board = deepcopy(board)
        # play with the valid move on the simulation board
        valid_move(player_mark, coordinates, dummy_board)
        # get the score of the move and store them
        scores[coordinates] = get_scores(player_mark, opponent_mark, dummy_board)[0]

    # get coordinate with min score
    coordinate_min = min(scores, key=lambda x: scores[x], default="")
    # play with the min score on the playing board
    valid_move(player_mark, coordinate_min, board)


def random_move_computer(
    player_mark: str, allowed_moves: list[str], board: list[list[str]]
):
    """retrieves random coordinate and plays with it"""

    random_coordinate = random.choice(allowed_moves)
    # play with the min score on the playing board
    valid_move(player_mark, random_coordinate, board)


def chosen_algorithm(
    identifier: str, player_mark: str, allowed_moves: list[str], board: list[list[str]]
):
    match identifier:
        case "1":
            corner_first_computer(player_mark, allowed_moves, board)
        case "2":
            side_first_computer(player_mark, allowed_moves, board)
        case "3":
            best_scoring_computer(player_mark, allowed_moves, board)
        case "4":
            worst_scoring_computer(player_mark, allowed_moves, board)
        case "5":
            random_move_computer(player_mark, allowed_moves, board)


if __name__ == "__main__":
    playing_board = deepcopy(NEW_BOARD)

    centers = {"X": [[3, 3], [4, 4]], "O": [[3, 4], [4, 3]]}
    for key, value in centers.items():
        playing_board[value[0][0]][value[0][1]] = key
        playing_board[value[1][0]][value[1][1]] = key

    print("R E V E R S E G A M : AI SIMULATION")
    print()
    time.sleep(2)

    print("LET'S BEGIN")
    print(
        dedent(
            """
    1. corner_first_computer:   applies corner moves otherwise retrieves coordinates with highest score
                                and plays with it
    2. side_first_computer:     applies side moves otherwise retrieves coordinates with highest score
                                and plays with it
    3. best_scoring_computer:   retrieves coordinates with highest score and plays with it
    4. worst_scoring_computer:  retrieves coordinates with lowest score and plays with it
    5. random_move_computer:    retrieves random coordinates and plays with it
    """
        )
    )

    ai1 = ""
    while re.match("^[1-5]$", ai1) is None:
        print("Choose the first algorithm: (1~5)")
        ai1 = input()
    ai2 = ""
    while re.match("^[1-5]$", ai2) is None:
        print("Choose the second algorithm: (1~5)")
        ai2 = input()
    runs = ""
    while re.match("^[0-9]+$", runs) is None:
        print("How many times do you want to run the simulation?")
        runs = input()

    ai1_mark, ai2_mark = "X", "O"
    ai1_wins, ai2_wins = 0, 0
    ties = 0

    total_runs = runs = int(runs)
    while runs > 0:
        while True:
            allowed_ai1_moves = get_allowed_moves(ai1_mark, playing_board)
            if allowed_ai1_moves:
                chosen_algorithm(ai1, ai1_mark, allowed_ai1_moves, playing_board)
            else:
                ai1_score, ai2_score = get_scores(ai1_mark, ai2_mark, playing_board)
                if ai1_score > ai2_score:
                    ai1_wins += 1
                elif ai1_score < ai2_score:
                    ai2_wins += 1
                else:
                    ties += 1
                break

            allowed_ai2_moves = get_allowed_moves(ai2_mark, playing_board)
            if allowed_ai2_moves:
                chosen_algorithm(ai2, ai2_mark, allowed_ai2_moves, playing_board)
            else:
                ai1_score, ai2_score = get_scores(ai1_mark, ai2_mark, playing_board)
                if ai1_score > ai2_score:
                    ai1_wins += 1
                elif ai1_score < ai2_score:
                    ai2_wins += 1
                else:
                    ties += 1
                break

        runs -= 1

    print(f"Algorithm 1 has {ai1_wins} wins ({round((ai1_wins//total_runs)*100, 2)}%).")
    print(f"Algorithm 2 has {ai2_wins} wins ({round((ai2_wins//total_runs)*100, 2)}%).")
    print(f"{ties} games were tied ({round((ties//total_runs)*100, 2)}%).")
