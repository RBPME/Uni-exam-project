from dataclasses import dataclass
from move import *


@dataclass
class Board:
    white: list[int]
    black: list[int]
    is_whites_turn: bool


def make_board() -> Board:
    """
    Makes a board with the start position
    >>>make_board()
    board (wihte=[1,2,3,4,5,6,7,8,9,10,11,12], black=[14,15,16,17,18,19,20,21,22,23,24,25], is_whites_turn=True)
    """
    return Board([x for x in range(14, 26)], [y for y in range(1, 13)], True)


def white_plays(b: Board) -> bool:
    """
    Checks if it is whites turn
    >>>white_plays(Board (white=[1,8,10], black=[13,18,20], is_whites_turn=True))
    True
    >>>white_plays(Board (white=[1,8,10], black=[13,18,20], is_whites_turn=False))
    False
    """
    return b.is_whites_turn


def white(b: Board) -> list[int]:
    """
    Returns a list of all indecies of spaces with white peices
    >>>white(Board (white=[1,8,10], black=[13,18,20], is_whites_turn=False))
    [1, 8, 10]
    """
    return b.white


def black(b: Board) -> list[int]:
    """
    Returns a list of all indcies of spaces with black peices
    >>>black(Board (white=[1,8,10], black=[13,18,20], is_whites_turn=False))
    [13, 18, 20]
    """
    return b.black


def free(b: Board, s: int) -> bool:
    """
    Precondition: s is a number between 1 and 25 (including 1 and 25)
    Checks if a given space on the board is free
    >>>free(Board (white=[1], black=[], is_whites_turn=True),1)
    False
    >>>free(Board (white=[1], black=[], is_whites_turn=True),10)
    True
    """
    return not s in white(b) and not s in black(b)


def moves_diagonal(m: Move) -> bool:
    """
    Checks if a peice moves diagonal
    >>>moves_diagonal(Move (src=1, trg=6))
    False
    >>>moves_diagonal(Move (src=1, trg=13))
    True
    """
    return difference(m) % 4 == 0 or difference(m) % 6 == 0


def moves_double(m: Move) -> bool:
    """
    Checks if a given move moves a peice 2 spaces in a straight line
    >>>moves_double(Move (src=1, trg=11))
    True
    >>>moves_double(Move (src=1, trg=6))
    False
    """
    if abs(difference(m)) > 12:
        return False
    elif abs(difference(m)) == 4 or abs(difference(m)) == 6:
        return False
    elif difference(m) % 2 == 1:
        return False
    else:
        return True


def attacked_space(m: Move) -> int:
    """
    Precondition: A peice is moved 2 spaces, i.e. moves_double(m) == True
    Returns the index of a space that is a attacked during a move
    >>>attacked_space(Move (src=1, trg=11))
    6
    """
    return difference(m)//2 + source(m)  # Note that difference(m)//2 is used instead of difference(m)/2 purely to avoid errors, it follows from the precondition that difference(m)/2 is an integer, and then difference(m)//2 == difference(m)/2


def moves_through_edge(m: Move) -> bool:
    """
    Precondition: A peice is moved at most 2 spaces
    Checks if a move goes through the edge of the board
    >>>moves_through_edge(src=5, trg=6)
    True
    >>>moves_through_edge(src=4, trg=5)
    False
    """
    if moves_double(m):
        if difference(m) == 12 or difference(m) == -8 or difference(m) == 2:
            return source(m) % 5 == 0 or source(m) % 5 == 4
        elif difference(m) == -12 or difference(m) == 8 or difference(m) == -2:
            return source(m) % 5 == 1 or source(m) % 5 == 2
        else:
            return False
    else:
        if difference(m) == -4 or difference(m) == 1 or difference(m) == 6:
            return source(m) % 5 == 0
        elif difference(m) == -6 or difference(m) == -1 or difference(m) == 4:
            return source(m) % 5 == 1
        else:
            return False


def is_legal(m: Move, b: Board) -> bool:
    """
    Checks if a given move is legal or not
    >>>is_legal(Move (src=1, trg=11), Board white=[1], black=[6], is_whites_turn=True)
    True
    >>>is_legal(Move (src=1, trg=11), Board white=[1], black=[], is_whites_turn=True)
    False
    """
    if not source(m) in range(1, 26) or not target(m) in range(1, 26):
        return False
    elif not free(b, target(m)):
        return False
    elif moves_diagonal(m) and source(m) % 2 != 1:
        return False
    elif white_plays(b):
        if not source(m) in white(b):
            return False
        elif difference(m) == -4 or difference(m) == -5 or difference(m) == -6:
            return not moves_through_edge(m)
        elif moves_double(m):
            return attacked_space(m) in black(b) and not moves_through_edge(m)
        else:
            return False
    else:
        if not source(m) in black(b):
            return False
        elif difference(m) == 4 or difference(m) == 5 or difference(m) == 6:
            return not moves_through_edge(m)
        elif moves_double(m):
            return attacked_space(m) in white(b) and not moves_through_edge(m)
        else:
            return False


def legal_moves(b: Board) -> list[Move]:
    """
    Returns a list of all legal moves on a given board
    >>>legal_moves(Board (white=[13], black=[1], is_whites_turn=True))
    [Move(src=13, trg=7), Move(src=13, trg=8), Move(src=13, trg=9)]
    """
    res = []
    for x in range(1, 26):
        res = res + [make_move(x, y) for y in range(1, 26)
                     if is_legal(make_move(x, y), b)]
    return res


def move(m: Move, b: Board) -> None:
    """
    Updates the board by simulating a move
    """
    if moves_double(m):
        b.white = [x for x in white(b) if x != attacked_space(m)]
        b.black = [x for x in black(b) if x != attacked_space(m)]
    if white_plays(b):
        b.white = [x for x in white(b) if x != source(m)] + [target(m)]
    else:
        b.black = [x for x in black(b) if x != source(m)] + [target(m)]
    b.is_whites_turn = not b.is_whites_turn


def is_game_over(b: Board) -> bool:
    """
    Checks if the game is over or not
    >>>is_game_over(Board (white=[], black=[], is_whites_turn=True))
    True
    """
    if white(b) == [] or black(b) == []:
        return True
    elif legal_moves(b) == []:
        return True
    else:
        return False


def copy(b: Board) -> Board:
    """
    Returns a copy of a board
    >>>copy(Board (white=[], black=[], is_whites_turn=True))
    Board (white=[], black=[], is_whites_turn=True)
    """
    return b
