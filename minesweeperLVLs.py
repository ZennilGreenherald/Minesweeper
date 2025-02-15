__author__ = 'ambivalentbunnie'

import random
import string

class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    END = "\033[0m"

red_x = f"{Color.RED}X{Color.END}"

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
        # finds coordinate of top left, top center, top right, left side, right side, bottom left, bottom center, bottom right surrounding the mine
        for space in self.neighbors(row, col):
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

    def neighbors(self, row, col):
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if r >= 0 and c >= 0 and r < self.board_rows and c < self.board_cols and (r != row or c != col):
                    yield r, c

    def get_user_move(self):
        s = input("Please enter '<row> <col>' to uncover a space or 'X <row> <col>' to place or remove a flag: ")
        ls = s.upper().translate(str.maketrans(string.punctuation, (" " * len(string.punctuation)))).split()
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
        while True:
            is_flagging, row, col = self.get_user_move()
            move_coord = row, col

            if move_coord not in self.dict_board:
                print("That's not even a space on the board >_>")
                break

            elif not is_flagging:
                self.check_move(move_coord)
                break
            elif is_flagging:
                is_first_move = self.countSpaces == self.board_rows * self.board_cols
                if is_first_move:
                    print("You really want to place a flag on your first move?")
                else:
                    self.toggle_flag(move_coord)
                    break
            else:
                print("Invalid input. Please try again.")
                self.print_board()

    def toggle_flag(self, move_coord):
            if self.dict_board[move_coord] == "O":
                if self.count_flags < self.num_mines:
                    self.dict_board[move_coord] = red_x
                    self.count_flags += 1
                    self.print_board()
                else:
                    print('You already placed as many flags as there are bombs.')
            elif self.dict_board[move_coord] == red_x:
                self.dict_board[move_coord] = "O"
                self.count_flags -= 1
                self.print_board()
            else:
                print("You want to waste flag on a space you already uncovered??? o_O")

    def check_move(self, move_coord):
        if self.dict_board[move_coord] == red_x:
            print("Uhmmm, you want to dig up a flag you put down??")

        elif self.dict_board[move_coord] != "O":
            print("You already uncovered this space -_-")
            self.print_board()

        elif self.dict_board[move_coord] == "O":
            if move_coord in self.mines_and_nums:
                # don't let user hit a bomb on the first move
                is_first_move = self.countSpaces == self.board_rows * self.board_cols
                if is_first_move and self.mines_and_nums[move_coord] == "*":
                    ls = [coord for coord, x in self.mines_and_nums.items() if x != '*']
                    random.shuffle(ls)
                    free_coord = ls[0]
                    self.mines_and_nums[move_coord] = ' '
                    self.mines_and_nums[free_coord] = '*'
                    self.place_nums(free_coord[0], free_coord[1])

                if self.mines_and_nums[move_coord] != "*":
                    self.dict_board[move_coord] = self.mines_and_nums[move_coord]
                    self.countSpaces -= 1
                    self.print_board()
                else:
                    # mine is at coordinate - game over, man
                    self.dict_board[move_coord] = self.mines_and_nums[move_coord]
                    self.print_board()
                    print("Game Over!")
                    raise SystemExit()
            else:
                self.dict_board[move_coord] = " "
                self.countSpaces -= 1
                self.uncover_space(move_coord[0], move_coord[1])
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
        self.print_board()
        while True:
            self.make_move()
            self.user_win()

minesweeper = Minesweeper()
minesweeper.start_game()
