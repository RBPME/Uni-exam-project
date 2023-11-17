import math
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
    return not s in b.white and not s in b.black

# def x_change(m: Move) -> int:
#    """
#    Returns how much a peice is moved horizontally in a given move
#    >>>y_change(Move (src=1, trg=3))
#    2
#    """
#    return (target(m)-source(m))%5

# def y_change(m: Move) -> int:
#    """
#    Returns how much a peice is moved vertically in a given move
#    >>>x_change(Move (src=1, trg=11))
#    2
#    """
#    return math.ceil(target(m)/5)-math.ceil(source(m)/5)

def is_legal(m: Move, b: Board) -> bool:
    """
    Checks if a given move is legal or not
    """
    if b.is_whites_turn and not source(m) in b.white:
        return False
    elif not b.is_whites_turn and not source(m) in b.black:
        return False
    elif not free(b,target(m)):
        return False
    elif not source(m) in range(1,25) or not target(m) in range(1,25):
        return False
    elif b.is_whites_turn and m.src + 5 == m.trg:
        return True
    elif not b.is_whites_turn and m.src - 5 == m.trg:
        return True
    elif b.is_whites_turn and m.src % 2 == 1 and m.src + 4 == m.trg:
        return True
    elif b.is_whites_turn and m.src % 2 == 1 and m.src + 6 == m.trg:
        return True
    elif not b.is_whites_turn and m.src % 2 == 1 and m.src - 4 == m.trg:
        return True
    elif not b.is_whites_turn and m.src % 2 == 1 and m.src - 6 == m.trg:
        return True
    elif b.is_whites_turn and m.src + 5 in b.black and m.src + 10 == m.trg:
        return True
    elif not b.is_whites_turn and m.src + 5 in b.white and m.src + 10 == m.trg:
        return True
    elif b.is_whites_turn and m.src - 5 in b.black and m.src - 10 == m.trg:
        return True
    elif not b.is_whites_turn and m.src - 5 in b.white and m.src - 10 == m.trg:
        return True
    elif b.is_whites_turn and m.src + 1 in b.black and m.src + 2 == m.trg:
        return True
    elif not b.is_whites_turn and m.src + 1 in b.white and m.src + 2 == m.trg:
        return True
    elif b.is_whites_turn and m.src - 1 in b.black and m.src - 2 == m.trg:
        return True
    elif not b.is_whites_turn and m.src - 1 in b.white and m.src - 2 == m.trg:
        return True
    elif b.is_whites_turn and m.src + 6 in b.black and m.src + 12 == m.trg:
        return True
    elif not b.is_whites_turn and m.src + 6 in b.white and m.src + 12 == m.trg:
        return True
    elif b.is_whites_turn and m.src - 6 in b.black and m.src - 12 == m.trg:
        return True
    elif not b.is_whites_turn and m.src - 6 in b.white and m.src - 12 == m.trg:
        return True
    elif b.is_whites_turn and m.src + 4 in b.black and m.src + 8 == m.trg:
        return True
    elif not b.is_whites_turn and m.src + 4 in b.white and m.src + 8 == m.trg:
        return True
    elif b.is_whites_turn and m.src - 4 in b.black and m.src - 8 == m.trg:
        return True
    elif not b.is_whites_turn and m.src - 4 in b.white and m.src - 8 == m.trg:
        return True
    else:
        return False
    
def legal_moves(b: Board) -> list[Move]:
    """
    Returns a list of all legal moves on a given board
    """
    res=[]
    for x in range(1,25):
        res = res + [make_move(x,y) for y in range(1,25) if is_legal(make_move(x,y),b)]
    return res