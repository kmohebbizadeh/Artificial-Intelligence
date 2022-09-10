"""
Tic Tac Toe Player
"""

import math
import copy

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
    # Count the number of moves present on the board
    count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is not EMPTY:
                count = count + 1
    # Odd is O and even is X
    if count == 0:
        return X

    if count % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # reaction is how the opponent will play after your move
    reactions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                reactions.add((i, j))
    return reactions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # If the move is not valid, raise exception
    if action not in actions(board):
        print(action)
        raise Exception("Error: Invalid Move")
    # Make a duplicate add the move to the board
    duplicate = copy.deepcopy(board)
    duplicate[action[0]][action[1]] = player(board)

    return duplicate


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][1] == X:
                return X
            if board[i][1] == O:
                return O

    for j in range(len(board[0])):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[1][j] == X:
                return X
            if board[1][j] == O:
                return O

    if board[0][0] == board[1][1] == board[2][2]:
        if board[1][1] == X:
            return X
        if board[1][1] == O:
            return O

    if board[2][0] == board[1][1] == board[0][2]:
        if board[1][1] == X:
            return X
        if board[1][1] == O:
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X:
        return True
    if winner(board) == O:
        return True
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    if winner(board) is None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    results = []
    moves = []
    if terminal(board):
        return None
    if player(board) == 'X':
        for action in actions(board):
            results.append(min_value(result(board, action)))
            moves.append(action)
        best_result = max(results)
        result_index = results.index(best_result)
        best_action = moves[result_index]
        return best_action
    if player(board) == 'O':
        for action in actions(board):
            results.append(max_value(result(board, action)))
            moves.append(action)
        best_result = min(results)
        result_index = results.index(best_result)
        best_action = moves[result_index]
        return best_action


def min_value(board):
    # pseudocode from Lecture 0 notes
    v = float('inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def max_value(board):
    # pseudocode from Lecture 0 notes
    v = float('-inf')
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v
