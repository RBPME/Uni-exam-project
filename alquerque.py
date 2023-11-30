from move import *
from board import *
from minimax import next_move


def white_player() -> bool:
    """
    Asks the user if they want to play as the white peices
    >>>white_player()
    Do you want to play as the white peices (YES/NO)
    YES
    True

    >>>white_player()
    Do you want to play as the white peices (YES/NO)
    NO
    False
    """
    print("Do you want to play as the white peices (YES/NO)")
    answer = input()
    if answer == "YES":
        return True
    elif answer == "NO":
        return False
    else:
        print("Error: please type either YES or NO (Remember to use capital letters)")
        return white_player()
    
def black_player() -> bool:
    """
    Asks the user if they want to play as the black peices
    >>>black_player()
    Do you want to play as the black peices (YES/NO)
    YES
    True

    >>>black_player()
    Do you want to play as the black peices (YES/NO)
    NO
    False
    """
    print("Do you want to play as the black peices (YES/NO)")
    answer = input()
    if answer == "YES":
        return True
    elif answer == "NO":
        return False
    else:
        print("Error: please type either YES or NO (Remember to use capital letters)")
        return black_player()

def white_strength() -> int:
    """
    Precondition: the user writes a number
    Asks how smart the white AI should play
    >>>white_strength()
    How smart should the white peices play? (1-7)
    4
    4
    """
    print("How smart should the white peices play? (1-7)")
    answer = input()
    if int(answer) >= 1 and int(answer) <= 7:
        return int(answer)
    else:
        print("Error: please write a number between 1 and 7")
        return white_strength()

def black_strength() -> int:
    """
    Precondition: the user writes a number
    Asks how smart the black AI should play
    >>>white_strength()
    How smart should the black peices play? (1-7)
    4
    4
    """
    print("How smart should the black peices play? (1-7)")
    answer = input()
    if int(answer) >= 1 and int(answer) <= 7:
        return int(answer)
    else:
        print("Error: please write a number between 1 and 7")
        return black_strength()

def space(n: int, b: Board) -> str:
    """
    Makes the UI string for a single space on the board
    >>>space(1, Board (white=[1], black=[2], is_whites_turn=True))
    'O'
    >>>space(2, Board (white=[1], black=[2], is_whites_turn=True))
    '*'
    >>>space(3, Board (white=[1], black=[2], is_whites_turn=True))
    ' '
    """
    if n in white(b):
        return "O"
    elif n in black(b):
        return "*"
    else:
        return " "
    
def combine_row(v: list[str]) -> str:
    """
    Combines a list of spaces into a single row on the board
    >>>combine_row(["*", "*", "O", " ", "O"])
    '* - * - O -   - O'
    """
    if v == []:
        return ""
    elif len(v) == 1:
        return v[0]
    else:
        return v[0] + " - " + combine_row(v[1:])
    
def _draw_board(v: list[str], n: int) -> None:
    """
    Helperfunction for draw_board
    """
    if n % 2 == 0 and len(v) >= 2:
        print(v[0])
        print("| \\ | / | \\ | / |") #Note that \\ is used instead of \ as \ is an escape character
        _draw_board(v[1:], n+1)
    elif n % 2 == 1 and len(v) >= 2:
        print(v[0])
        print("| / | \\ | / | \\ |") #Note that \\ is used instead of \ as \ is an escape character
        _draw_board(v[1:], n+1)
    elif len(v) == 1:
        print(v[0])


def draw_board(v: list[str]) -> None:
    """
    Draws an alquerque board based on a list of rows
    >>>draw_board(["* - * - * - * - *", "* - * - * - * - *", "* - * -   - O - O", "O - O - O - O - O", "O - O - O - O - O"])
    * - * - * - * - *
    | \ | / | \ | / |
    * - * - * - * - *
    | / | \ | / | \ |
    * - * -   - O - O
    | \ | / | \ | / |
    O - O - O - O - O
    | / | \ | / | \ |
    O - O - O - O - O
    """
    _draw_board(v, 0)

def show_board(b: Board) -> None:
    """
    Draws an alquerque board in the terminal
    >>>show_board(Board (white=[1, 8], black=[2, 20], is_whites_turn=True))
    O - * -   -   -  
    | \ | / | \ | / |
      -   - O -   -  
    | / | \ | / | \ |
      -   -   -   -  
    | \ | / | \ | / |
      -   -   -   - *
    | / | \ | / | \ |
      -   -   -   -  
    """
    res = []
    for i in range(5):
        res = res + [combine_row([space(n, b) for n in range(1+5*i,6+5*i)])]
    draw_board(res)

def input_move() -> Move:
    """
    Precondition: the user only writes numbers in the terminal
    Returns a move inputted in the terminal by the user
    >>>input_move()
    What space would you like to move from? (1-25)
    2
    What space would you like to move to? (1-25)
    6
    Move (src=2, trg=6)
    """
    print("What space would you like to move from? (1-25)")
    src = input()
    while int(src) not in range(1,26):
        print("Error: please write a number between 1 and 25")
        print("What space would you like to move from? (1-25)")
        src = input()
    print("What space would you like to move to? (1-25)")
    trg = input()
    while int(trg) not in range(1,26):
        print("Error: please write a number between 1 and 25")
        print("What space would you like to move to? (1-25)")
        trg = input()
    return make_move(int(src), int(trg))

WHITE_PLAYER = white_player()
BLACK_PLAYER = black_player()
WHITE_STRENGTH = 1
BLACK_STRENGTH = 1

if not WHITE_PLAYER:
    WHITE_STRENGTH = white_strength()
if not BLACK_PLAYER:
    BLACK_STRENGTH = black_strength()

b = make_board()

while not is_game_over(b):
    show_board(b)
    if white_plays(b) and WHITE_PLAYER:
        m = input_move()
        while not is_legal(m, b):
            print("Your move is illegal, please enter a legal move")
            m = input_move()
        move(m, b)
    elif white_plays(b) and not WHITE_PLAYER:
        move(next_move(b, WHITE_STRENGTH), b)
    elif not white_plays(b) and BLACK_PLAYER:
        m = input_move()
        while not is_legal(m, b):
            print("Your move is illegal, please enter a legal move")
            m = input_move()
        move(m, b)
    else:
        move(next_move(b, BLACK_STRENGTH), b)
    print() #makes space between each move, so it is easier to see what happened on which turn

if white(b) == []:
    print("Black won the game")
elif black(b) == []:
    print("White won the game")
else:
    print("The game was a draw")