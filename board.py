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
    return Board([x for x in range(1,13)], [y for y in range(14,26)], True)

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
        if source(m) % 5 == 0 or source(m) % 5 == 4:
            return difference(m) != 12 and difference(m) != -8 and difference(m) != 2
        elif source(m) % 5 == 1 or source(m) % 5 == 2:
            return difference(m) != 8 and difference(m) != -12 and difference(m) != -2
        else:
            return True

def is_legal(m: Move, b: Board) -> bool:
    """
    Checks if a given move is legal or not
    """
    if not free(b,target(m)):
        return False
    elif not source(m) in range(1,26) or not target(m) in range(1,26):
        return False
    elif white_plays(b):
        if not source(m) in white(b):
            return False
        elif difference(m) == 4:
            return source(m) % 2 == 1 and source(m) % 5 != 1
        elif difference(m) == 6:
            return source(m) % 2 == 1 and source(m) % 5 != 0
        elif moves_double(m):
            return difference(m)/2 + source(m) in black(b)
        else:
            return difference(m) == 5
    else:
        if not source(m) in black(b):
            return False
        elif difference(m) == -4:
            return source(m) % 2 == 1 and source(m) % 5 != 0
        elif difference(m) == -6:
            return source(m) % 2 == 1 and source(m) % 5 != 1
        elif moves_double(m):
            return difference(m)/2 + source(m) in white(b)
        else:
            return difference(m) == -5
    
def legal_moves(b: Board) -> list[Move]:
    """
    Returns a list of all legal moves on a given board
    """
    res=[]
    for x in range(1,26):
        res = res + [make_move(x,y) for y in range(1,26) if is_legal(make_move(x,y),b)]
    return res

def move(m: Move, b: Board) -> None:
    """
    Updates the board by simulating a move
    """
    if moves_double(m):
        b.white = [x for x in white(b) if x != difference(m)/2+source(m)]
        b.black = [x for x in black(b) if x != difference(m)/2+source(m)]
    if white_plays(b):
        b.white = [x for x in white(b) if x != source(m)] + [target(m)]
    else:
        b.black = [x for x in black(b) if x != source(m)] + [target(m)]
    b.is_whites_turn = not b.is_whites_turn

def is_game_over(b: Board) -> bool:
    """
    Checks if the game is over or not
    >>>is_game_over(Board (white=[], black=[], is_whites_turn=Tue))
    False
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