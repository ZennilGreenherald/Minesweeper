__author__ = 'ambivalentbunnie'

import random
import string

class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    END = "\033[0m"

levels = ["beginner", "intermediate", "advanced", "custom"]

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

class Minesweeper:
    # build board and define how many mines/level
    def __init__(self):
        self.dict_board = {}
        self.mines_and_nums = {}
        self.count_mines = 0
        self.count_flags = 0
        self.board_rows = 0
        self.board_cols = 0
        self.num_mines = 0

    def get_level(self):
        while True:
            choice = input("Please choose a level (Beginner, Intermediate, Advanced, Custom, Quit): ").lower()
            if choice == 'quit':
                raise SystemExit()
            elif choice in levels:
                return choice
            else:
                print("What kind of level is that?!?!?! >:O")

    def define_level(self):
        choice = self.get_level()
        if choice in levels[:3]:
            i = levels.index(choice)
            self.board_rows = board_size_settings[i]['board_rows']
            self.board_cols = board_size_settings[i]['board_cols']
            self.num_mines  = board_size_settings[i]['num_mines']
        # custom level
        else:
            while True:
                try:
                    self.board_rows = int(input("Please enter a number 1-80 for rows: "))
                    self.board_cols = int(input("Please enter a number 1-80 for columns: "))
                    self.num_mines = int(input("Please enter a number 1-99 for bombs: "))
                    if 0 < self.board_rows <= 80 and 0 < self.board_cols <= 80 and 0 < self.num_mines <= 99 and self.num_mines < (self.board_rows * self.board_cols) / 2:
                        break
                    else: 
                        print("Can't make a board like that! D:")
                except:
                    print("Can't make a board like that! D:")

    def make_board(self):
        for r in range(self.board_rows):
            for c in range(self.board_cols):
                self.dict_board[(r, c)] = "O"
        self.countSpaces = self.board_rows * self.board_cols
        self.place_mines()
        self.print_board()
    
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
                        self.count_mines += 1

    def print_board(self):
        print('    ' + ' '.join(str(c) for c in range(self.board_cols)))
        print('  ' + '-' * (self.board_cols * 2 + 1))

        for r in range(self.board_rows):
            print(r, end = ' | ')
            for c in range(self.board_cols):
                print(self.dict_board[(r,c)], end = " ")
            print()

    def get_user_move(self):
        # when coordinate is inputed (row x column) checks the space
        return (input("Please enter a 'coordinate' to uncover a space or 'X, coordinate' to place or remove a flag: ")
                    .upper()
                    .translate(str.maketrans(string.punctuation, (" " * len(string.punctuation))))
                    .split())

    def make_move(self):
        while True:
            user = self.get_user_move()
            # determines if the user is inputting a space
            if len(user) == 2:
                try:
                    self.move = tuple(map(int, user))
                    if self.move in self.dict_board:
                        self.is_flagging = False
                        break
                    else:
                        print("That's not even a space on the board >_>")
                except:
                    print("NO! >:O")
            # determines if a user is inputting a flag
            elif len(user) == 3 and user[0] == "X":
                try:
                    self.flag = tuple(map(int, user[1:]))
                    if self.count_mines == 0:
                        print("You really want to place a flag on your first move?")
                    elif self.flag in self.dict_board:
                        self.toggle_flag()
                        self.is_flagging = True
                        break
                    else:
                        print("Sure. I can place a flag in the middle of nowhere for you! :D")
                except:
                    print("*BOOM* No flag for you! >:D")
            else:
                print("Invalid input.  Please try again.")
                self.print_board()

    def toggle_flag(self):
        if self.count_flags <= self.num_mines:
            if self.dict_board[self.flag] == "O":
                self.dict_board[self.flag] = f"{Color.RED}X{Color.END}"
                self.count_flags += 1
                self.print_board()
            elif self.dict_board[self.flag] == f"{Color.RED}X{Color.END}":
                self.dict_board[self.flag] = "O"
                self.count_flags -= 1
                self.print_board()
            else:
                print("You want to waste flag on a space you already uncovered??? o_O")

    def neighbors(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r >= 0 and c >= 0 and r < self.board_rows and c < self.board_cols and (r != row or c != col):
                    yield r, c

    # method will use the coordinates of the mines that are placed
    def place_nums(self, row, col):
        # finds coordinate of top left, top center, top right, left side, right side, bottom left, bottom center, bottom right surrounding the mine
        for space in self.neighbors(row, col):
            # if the coordinate is not in the dictionary yet, adds key and value
            if space not in self.mines_and_nums:
                self.mines_and_nums[space] = 1
            # if the coordinate is already a key, increments the value up by 1
            elif space in self.mines_and_nums and self.mines_and_nums[space] != "*":
                self.mines_and_nums[space] += 1

    def check_move(self):
        if self.is_flagging == False:
            # if mine is there at coordinate - game over
            if self.dict_board[self.move] == "O":
                if self.move in self.mines_and_nums:
                    # don't let user hit a bomb on the first move
                    is_first_move = self.countSpaces == self.board_rows * self.board_cols
                    if is_first_move and self.mines_and_nums[self.move] == "*":
                        ls = [coord for coord, x in self.mines_and_nums.items() if x != '*']
                        random.shuffle(ls)
                        free_coord = ls[0]
                        self.mines_and_nums[self.move] = ' '
                        self.mines_and_nums[free_coord] = '*'
                        self.place_nums(free_coord[0], free_coord[1])

                    if self.mines_and_nums[self.move] != "*":
                        self.dict_board[self.move] = self.mines_and_nums[self.move]
                        self.countSpaces -= 1
                        self.print_board()
                    else:
                        self.dict_board[self.move] = self.mines_and_nums[self.move]
                        self.print_board()
                        print("Game Over!")
                        raise SystemExit()
                else:
                    self.dict_board[self.move] = " "
                    self.countSpaces -= 1
                    self.uncover_space(self.move[0], self.move[1])
                    self.print_board()
            elif self.dict_board[self.move] == f"{Color.RED}X{Color.END}":
                print("Uhmmm, you want to dig up a flag you put down??")
            elif self.dict_board[self.move] != "O":
                print("You already uncovered this space -_-")
                self.print_board()


    def uncover_space(self, row, col):
        for space in self.neighbors(row, col):
            if self.dict_board[space] == "O":
                if space not in self.mines_and_nums:
                    self.dict_board[space] = " "
                    self.countSpaces -= 1
                    self.uncover_space(space[0], space[1])
                elif space in self.mines_and_nums and self.mines_and_nums[space] != "*":
                    self.dict_board[space] = self.mines_and_nums[space]
                    self.countSpaces -= 1

    def user_win(self):
        # when all the blank spaces are uncovered - winner is pronounced!
        if self.countSpaces == self.num_mines:
            print("Congrats you won! :D")
            raise SystemExit()

    def start_game(self):
        self.define_level()
        self.make_board()
        while True:
            self.make_move()
            self.check_move()
            self.user_win()

minesweeper = Minesweeper()
minesweeper.start_game()
