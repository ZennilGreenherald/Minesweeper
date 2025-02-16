__author__ = 'ambivalentbunnie'

import random
import string

from enum import Enum, unique

@unique
class FlagResult(Enum):
    SPOT_CLEAR = 1
    NO_FLAGS_LEFT = 2
    OK = 3

@unique
class CheckResult(Enum):
    SPOT_FLAGGED = 1
    SPOT_ALREADY_SHOWN = 2
    OK = 3
    EXPLODE = 4

class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    END = "\033[0m"

class Board:
    red_x = f"{Color.RED}X{Color.END}"

    def __init__(self, rows, cols, mines):
        self.dict_board = {}
        self.mines_and_nums = {}
        self.count_flags = 0
        self.board_rows = rows
        self.board_cols = cols
        self.countSpaces = self.board_rows * self.board_cols
        self.num_mines = mines
        self.make_board()

    def make_board(self):
        for r in range(self.board_rows):
            for c in range(self.board_cols):
                self.dict_board[(r, c)] = "O"
        self.place_mines()

    def place_mines(self):
        mines_to_place = ['*'] * self.num_mines + [' '] * ((self.board_rows * self.board_cols) - self.num_mines)
        random.shuffle(mines_to_place)
        for r in range(self.board_rows):
            for c in range(self.board_cols):
                m = mines_to_place.pop()
                if m == '*':
                    coord = (r, c)
                    if coord not in self.mines_and_nums or self.mines_and_nums[coord] != "*":
                        self.mines_and_nums[coord] = "*"
                        self.place_nums(r, c)

    # method will use the coordinates of the mines that are placed
    def place_nums(self, row, col):
        for space in self.model_neighbors(row, col):
            # if the coordinate is not in the dictionary yet, adds key and value
            if space not in self.mines_and_nums:
                self.mines_and_nums[space] = 1
            # if the coordinate is already a key, increments the value up by 1
            elif space in self.mines_and_nums and self.mines_and_nums[space] != "*":
                self.mines_and_nums[space] += 1

    def print_board(self):
        max_row_num_width = len(str(self.board_rows - 1))
        print(' ' * (max_row_num_width + 3) + ' '.join(str(c // 10) if c >= 10 else ' ' for c in range(self.board_cols)))
        print(' ' * (max_row_num_width + 3) + ' '.join(str(c % 10) for c in range(self.board_cols)))
        print(' ' * (max_row_num_width + 1) + '-' * (self.board_cols * 2 + 1))

        for r in range(self.board_rows):
            row_prefix = f'{" " * max_row_num_width}{r} | '[-(max_row_num_width + 3):]
            print(row_prefix, end = '')
            for c in range(self.board_cols):
                print(self.dict_board[(r,c)], end = " ")
            print()

    def model_neighbors(self, row, col):
        # finds neighboring spots in all 8 directions
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r >= 0 and c >= 0 and r < self.board_rows and c < self.board_cols and (r != row or c != col):
                    yield r, c

    def model_toggle_flag(self, move_coord):
        if self.dict_board[move_coord] == "O":
            if self.count_flags < self.num_mines:
                self.dict_board[move_coord] = Board.red_x
                self.count_flags += 1
                return FlagResult.OK
            else:
                return FlagResult.NO_FLAGS_LEFT
        elif self.dict_board[move_coord] == Board.red_x:
            self.dict_board[move_coord] = "O"
            self.count_flags -= 1
            return FlagResult.OK
        else:
            return FlagResult.SPOT_CLEAR

    def model_check_move(self, move_coord):
        if self.dict_board[move_coord] == Board.red_x:
            return CheckResult.SPOT_FLAGGED

        elif self.dict_board[move_coord] != "O":
            return CheckResult.SPOT_ALREADY_SHOWN

        else:
            # if first move, don't let user hit a bomb
            is_first_move = self.countSpaces == self.board_rows * self.board_cols
            if is_first_move and move_coord in self.mines_and_nums and self.mines_and_nums[move_coord] == "*":
                ls = [coord for coord, x in self.mines_and_nums.items() if x != '*']
                random.shuffle(ls)
                free_coord = ls[0]
                self.mines_and_nums[move_coord] = ' '
                self.mines_and_nums[free_coord] = '*'
                self.place_nums(free_coord[0], free_coord[1])

            self.dict_board[move_coord] = self.mines_and_nums[move_coord] if move_coord in self.mines_and_nums else ' '
            self.countSpaces -= 1
            if move_coord not in self.mines_and_nums:
                self.uncover_space(move_coord[0], move_coord[1])
                return CheckResult.OK
            else:
                if self.mines_and_nums[move_coord] == "*":
                    return CheckResult.EXPLODE
                else:
                    return CheckResult.OK

    def uncover_space(self, row, col):
        for space in self.model_neighbors(row, col):
            if self.dict_board[space] == "O":
                if space not in self.mines_and_nums:
                    self.dict_board[space] = " "
                    self.countSpaces -= 1
                    self.uncover_space(space[0], space[1])
                elif space in self.mines_and_nums and self.mines_and_nums[space] != "*":
                    self.dict_board[space] = self.mines_and_nums[space]
                    self.countSpaces -= 1

    def move_in_range(self, coord):
        return coord in self.dict_board

    def has_moved(self):
        return self.countSpaces != self.board_rows * self.board_cols

    def isGameWon(self):
        # when all the blank spaces are uncovered - winner is pronounced!
        return self.countSpaces == self.num_mines


class Minesweeper:
    # beginner = 9x9 w/ 10 mines
    # intermediate = 16x16 w/ 40 mines
    # advanced = 30x16 w/ 99 mines
    board_size_settings = [
        {
            'board_rows': 9,
            'board_cols': 9,
            'num_mines': 10
        }, {
            'board_rows': 16,
            'board_cols': 16,
            'num_mines': 40
        }, {
            'board_rows': 16,
            'board_cols': 30,
            'num_mines': 99
        }
    ]
    levels = ["beginner", "intermediate", "advanced", "custom"]


    def __init__(self):
        self.board = None

    def get_level(self):
        while True:
            choice = input("Please choose a level (Beginner, Intermediate, Advanced, Custom, Quit): ").lower()
            if choice == 'quit':
                raise SystemExit()
            elif choice in Minesweeper.levels:
                return choice
            else:
                print("What kind of level is that?!?!?! >:O")

    def define_level(self):
        # Get dimensions and number of mines with which to construct the board
        choice = self.get_level()
        if choice in Minesweeper.levels[:3]:
            i = Minesweeper.levels.index(choice)
            settings = Minesweeper.board_size_settings
            rows  = settings[i]['board_rows']
            cols  = settings[i]['board_cols']
            mines = settings[i]['num_mines']
            self.board = Board(rows, cols, mines)
        # custom level
        else:
            while True:
                try:
                    rows = int(input("Please enter a number 1-80 for rows: "))
                    cols = int(input("Please enter a number 1-80 for columns: "))
                    mines = int(input("Please enter a number 1-99 for bombs: "))
                    if 0 < rows <= 80 and 0 < cols <= 80 and 0 < mines < min(100, (board_rows * board_cols) / 2):
                        self.board = Board(rows, cols, mines)
                        return
                    else: 
                        print("Can't make a board like that! D:")
                except:
                    print("Can't make a board like that! D:")

    def get_user_move(self):
        s = input("Please enter '<row> <col>' to uncover a space or 'X <row> <col>' to place or remove a flag: ")
        ls = s.upper().translate(str.maketrans(string.punctuation, " " * len(string.punctuation))).split()
        try:
            coords = tuple(map(int, ls[-2:]))
            if len(ls) == 2:
                return (False, ) + coords
            elif len(ls) == 3 and ls[0] == 'X':
                return (True, ) + coords
        except Exception as e:
            print(f'Bad input: {e}. Please try again.')
        return self.get_user_move()

    def make_move(self):
        self.board.print_board()

        is_flagging, row, col = self.get_user_move()
        move_coord = row, col

        if not self.board.move_in_range(move_coord):
            print("That's not even a space on the board >_>")
        elif not is_flagging:
            self.check_move(move_coord)
        else:
            if self.board.has_moved():
                self.toggle_flag(move_coord)
            else:
                print("You really want to place a flag on your first move?")
                self.make_move()

    def toggle_flag(self, move_coord):
        res = self.board.model_toggle_flag(move_coord)

        if res == FlagResult.NO_FLAGS_LEFT:
            print('You already placed as many flags as there are bombs.')

        elif res == FlagResult.SPOT_CLEAR:
            print("You want to waste flag on a space you already uncovered??? o_O")

    def check_move(self, move_coord):
        res = self.board.model_check_move(move_coord)

        if res == CheckResult.SPOT_FLAGGED:
            print("Uhmmm, you want to dig up a flag you put down??")

        elif res == CheckResult.SPOT_ALREADY_SHOWN:
            print("You already uncovered this space -_-")

        elif res == CheckResult.EXPLODE or (res == CheckResult.OK and self.board.isGameWon()):
            self.board.print_board()
            print("Game Over!" if res == CheckResult.EXPLODE else "Congrats you won! :D")
            raise SystemExit()

    def start_game(self):
        self.define_level()
        while True:
            self.make_move()

minesweeper = Minesweeper()
minesweeper.start_game()
