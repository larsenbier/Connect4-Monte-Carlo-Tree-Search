import copy
import random

#####################################################################################
# 								Global Constants									#
#####################################################################################

BLANK = 0
RED = 1 
YELLOW = 2

ROWS = 6
COLS = 7
CONNECT_N = 4

#####################################################################################
# 									State Class										#
#####################################################################################

class State:

	def __init__(self, other = None, rows = ROWS, cols = COLS, connect_n = CONNECT_N):
		"""
		Docstring for __init__
		
		:param to_move: The player who should move next.
		:type to_move: int
		:param other: State to copy, if desired.
		"""
		if other is not None: # copy another state
			self.last_move = other.last_move
			self.rows = other.rows
			self.cols= other.cols
			self.board = copy.deepcopy(other.board)
			self.tops = copy.deepcopy(other.tops)
			self.to_move = other.to_move
			self.connect_n = other.connect_n
			return
	
		else: # initialize to initial game state
			self.last_move = None
			self.board=[[0 for i in range(cols)] for j in range(rows)]
			self.rows = len(self.board)
			self.cols = len(self.board[0])
			self.board = self.board
			self.tops = [0 for i in range(len(self.board[0]))] # list of index of place to insert next chip for each column
			self.to_move = RED
			self.connect_n = connect_n


	def addChip(self, col : int) -> bool:
		"""
		Adds a chip to the board in the specified column. Places a chip for the player self.to_move.
		Returns True if and only if a chip could be added in that column.

		:param col: The column to add the chip to.
		"""
		insert_row = self.tops[col]
		if insert_row < self.rows:
			self.board[insert_row][col] = self.to_move
			self.to_move = (1 if self.to_move == 2 else 2)
			self.tops[col] += 1
			self.last_move = (insert_row, col)
			return True
		return False
    
	
	def getChipAt(self, r, c):
		"""
		Returns the value of the chip at (r,c) on the board, or None if (r,c) is out of bounds.
		
		:param r: row to query from.
		:param c: column to query from.
		"""
		if r < self.rows and r >= 0 and c < self.cols and c >= 0:
			return self.board[r][c]
		return None
	
	def actions(self)-> list[int]:
		"""
		:param s: The state to get the actions for.
		:type s: State
		:return: A list of the possible actions in state s.
		:rtype: list[int]
		"""
		return [c for c in range(self.cols) if self.board[self.rows - 1][c]==0]


	def isTerminal(self) -> bool:
		"""
		Checks if a state is terminal
		
		:param s: The state to check.
		:type s: State
		:return: True if and only if the state is a terminal one.
		:rtype: bool
		"""
		if len(self.actions()) == 0: # tied game
			return True
		if self.last_move is None: # first move of game
			return False
		r, c = self.last_move
		player = (1 if self.to_move == 2 else 2) # the player who placed the previous chip
		winning_str = str(player) * self.connect_n # substring to check for win condition
		# check horizontal
		chip_str = ''
		for i in range(-self.connect_n + 1, self.connect_n):
			chip = self.getChipAt(r, c + i)
			if chip is not None:
				chip_str += str(chip)
		if winning_str in chip_str:
			return True
		# check vertical
		chip_str = ''
		for i in range(-self.connect_n + 1, self.connect_n):
			chip = self.getChipAt(r + i, c)
			if chip is not None:
				chip_str += str(chip)
		if winning_str in chip_str:
			return True
		# check diagonal (/)
		chip_str = ''
		for i in range(-self.connect_n + 1, self.connect_n):
			chip = self.getChipAt(r + i, c + i)
			if chip is not None:
				chip_str += str(chip)
		if winning_str in chip_str:
			return True
		# check diagonal (\)
		chip_str = ''
		for i in range(-self.connect_n + 1, self.connect_n):
			chip = self.getChipAt(r - i, c + i)
			if chip is not None:
				chip_str += str(chip)
		if winning_str in chip_str:
			return True
		
		return False

	def display(self):
		red_c = '\033[91m'
		yellow_c = '\033[93m'
		reset_c = '\033[0m'
		blue_c = '\033[94m'
		col_list = [i for i in range(self.cols)]
		col_str = '\t'
		for c in col_list:
			col_str += str(c + 1) + '    '
		print(col_str)
		print('\t' + '_____' * (self.cols - 1) + '_\n')
		rows, cols = len(self.board), len(self.board[0])
		for i in range(rows):
			print(rows - i, end = '\t')
			for j in range(cols):
				space = self.board[rows - i - 1][j]
				if space == 0:
					print(f'.', end='    ')
				elif space == 1:
					print(f'{red_c}\u25CF{reset_c}', end='    ')
				elif space == 2:
					print(f'{yellow_c}\u25CF{reset_c}', end='    ')
			print('\n')
		print('\t' + '_____' * (self.cols - 1) + '_\n')

