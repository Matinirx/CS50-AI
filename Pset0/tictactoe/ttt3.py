"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Typically 'X' starts the game.

    x_t = sum(row.count('X') for row in board)
    o_t = sum(row.count('O') for row in board)

    return 'X' if x_t <= o_t else 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # All possible actions in a 3x3 game
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is None}

def result(board, move):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Make a deep copy of the board
    new_board = [row[:] for row in board]
    i, j = move

    if not (0 <= i < len(board)) or not (0 <= j < len(board[0])):
        raise ValueError("Move out of bounds")
    if board[i][j] is not None:
        raise ValueError("Invalid move: Cell is already occupied")

    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check horizontal wins
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]

    # Check vertical wins
    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # Check diagonal wins
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # No winner
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Iteratively checking if the game is over
    return winner(board) is not None or all(cell is not None for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win = winner(board)

    # Assigns a score to a terminal board state.
    # 1 for 'X' win, -1 for 'O' win, 0 for a tie.
    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if (terminal(board) == True):
        return None
    else:
        bestScore = 1
        bestPlay = ()
        for play in actions(board):
            score = Min(result(board, play))
            if score < bestScore:
                bestScore = score
                bestPlay = play
        return bestPlay

def Min(board):
    if (terminal(board) == True):
        return utility(board)
    else:
        bestMinScore = 1
        for play in actions(board):
            bestMinScore = min(bestMinScore, Max(result(board, play)))
        return bestMinScore

def Max(board):
    if (terminal(board) == True):
        return utility(board)
    else:
        bestMaxScore = -1
        for play in actions(board):
            bestMaxScore = max(bestMaxScore, Min(result(board, play)))
        return bestMaxScore
