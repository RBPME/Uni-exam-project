from dataclasses import dataclass

@dataclass 
class Move:
    src: int
    trg: int

def make_move(src: int, trg: int) -> Move:
    """
    Precondition: src and trg are both numbers between 1 and 25 (including 1 and 25)
    Makes a move between two given spaces
    >>>make_move(1,6)
    Move (src=1, trg=6)
    """
    return Move(src,trg)

def source(m: Move) -> int:
    """
    Returns the space a move starts from
    >>>source(Move (src=1, trg=6))
    1
    """
    return m.src

def target(m: Move) -> int:
    """
    Returns the space a move ends on
    >>>source(Move (src=1, trg=6))
    6
    """
    return m.trg