#TODO - convert to Python 3

import os
import random


class Board(object):

  _HORIZONTAL = 0
  _NEW_HIT = "new_hit"
  _PAST_HIT = "past_hit"
  _NEW_MISS = "new_miss"
  _PAST_MISS = "past_miss"

  def __init__(self, board_size, ship_length):
    self.board_size = board_size
    self.ship_length = ship_length
    self._board = []
    for x in range(self.board_size):
      self._board.append(["+"] * self.board_size)
    self._ship_row = []
    self._ship_col = []
    # Decide vertical vs. horizontal (0 is horizontal (constant row), 1 is
    # vertical (constant col)):
    self._ship_orientation = random.randint(0, 1)
    self._ship_start_point()
    self._populate_ship()

  def _ship_start_point(self):
    if self._ship_orientation == self._HORIZONTAL:
      self.ship_start_row = random.randint(0, len(self._board[0]) - 1)
      self.ship_start_col = random.randint(0, len(self._board[0]) - (self.ship_length))
    else:
      self.ship_start_row = random.randint(0, len(self._board) - (self.ship_length))
      self.ship_start_col = random.randint(0, len(self._board[0]) - 1)

  def _populate_ship(self):
    self._ship_row = [self.ship_start_row]
    self._ship_col = [self.ship_start_col]
    self._ship_col_count = 0
    self._ship_row_count = 0
    if self._ship_orientation == self._HORIZONTAL:
      for i in range(1, self.ship_length):
        self._ship_col_count += 1
        self._ship_col.append(self.ship_start_col + self._ship_col_count)
        self._ship_row.append(self.ship_start_row)
    else:
      for i in range(1, self.ship_length):
        self._ship_row_count += 1
        self._ship_row.append(self.ship_start_row + self._ship_row_count)
        self._ship_col.append(self.ship_start_col)

  def clear_screen_print_board(self):
    os.system("clear")
    self.print_board()

  def print_board(self):
    for row in self._board:
      print " ".join(row)

  def check_hit(self, guess_row, guess_col):
    self._guess_row = guess_row
    self._guess_col = guess_col
    if (self._guess_row in self._ship_row and
        self._guess_col in self._ship_col):
      if self._board[self._guess_row][self._guess_col] == "X":
        return self._PAST_HIT
      else:
        return self._NEW_HIT
    else:
      if self._board[self._guess_row][self._guess_col] == "O":
        return self._PAST_MISS
      else:
        return self._NEW_MISS

  def update(self, row, col, cond):
    self._board[row][col] = cond

  def check_sunk(self):
    if (self._board[self._ship_row[0]][self._ship_col[0]] == "X" and
        self._board[self._ship_row[1]][self._ship_col[1]] == "X" and
        self._board[self._ship_row[2]][self._ship_col[2]] == "X" and
        self._board[self._ship_row[3]][self._ship_col[3]] == "X"):
      return True
    else:
      return False

class Game(object):

  def __init__(self, ship_length, board_size, turns_remaining):
    self._ship_length = ship_length
    self._board_size = board_size
    self._turns_remaining = turns_remaining
    self._pl1_board = Board(self._board_size, self._ship_length)

  def game_loop(self):
    self._pl1_board.clear_screen_print_board()
    print "Let's play Battleships!"
    while self._turns_remaining > 0:
      try:
        self.guess_row = int(raw_input("Guess Row:")) - 1
        self.guess_col = int(raw_input("Guess Col:")) - 1
      except ValueError:
        print "Invalid guess. has to be a number between 1 and %s" % self._board_size
        print "%s turns remaining." % self._turns_remaining
      if (self.guess_row in range(self._pl1_board.board_size) and
          self.guess_col in range(self._pl1_board.board_size)):
        for k in range(self._pl1_board.ship_length):
          if self._pl1_board.check_hit(self.guess_row, self.guess_col) == "past_hit":
            self._pl1_board.clear_screen_print_board()
            self._turns_remaining -= 1
            print "Already hit.\n%s turns remaining." % self._turns_remaining
            break
          elif self._pl1_board.check_hit(self.guess_row, self.guess_col) == "new_hit":
            self._pl1_board.update(self.guess_row, self.guess_col, "X")
            self._pl1_board.clear_screen_print_board()
            print "It's a hit!\n"
            if self._pl1_board.check_sunk() == True:
              print "You sank my battleship!"
              return "win"
            print "%s turns remaining." % self._turns_remaining
            break
          elif self._pl1_board.check_hit(self.guess_row, self.guess_col) == "past_miss":
            self._pl1_board.clear_screen_print_board()
            self._turns_remaining -= 1
            print "You already missed that one.\n%s turns remaining." % self._turns_remaining
            break
          elif self._pl1_board.check_hit(self.guess_row, self.guess_col) == "new_miss":
            self._pl1_board.update(self.guess_row, self.guess_col, "O")
            self._pl1_board.clear_screen_print_board()
            self._turns_remaining -= 1
            print "It's a miss.\n%s turns remaining." % self._turns_remaining
            break
          else:
            break
      else:
        self._pl1_board.clear_screen_print_board()
        print "Invalid guess. has to be a number between 1 and %s" % self._board_size
        print "%s turns remaining." % self._turns_remaining
    return "lose"

  def game_over(self):
    self._pl1_board.clear_screen_print_board()
    print "You're out of turns... \n Game Over"


def main():
  ship_length = 4
  board_size = 10
  turns = 5
  try:
    game1 = Game(ship_length, board_size, turns)
    if game1.game_loop() == "lose":
      game1.game_over()
  except KeyboardInterrupt:
    print "\nUser exit"
    raise SystemExit


if __name__ == "__main__":
  main()
