from env import State
from tree import Node
import time
import random

#####################################################################################
# 						Monte Carlo Tree Search Functions							#
#####################################################################################

def randomPlayout(s: State) -> int:
	"""
	Performs random move selection playout on state s. Does not modify s.
	
	:param s: The state to perform playout on.
	:type s: State
	:return: 0 if playout was a draw, else number of player who won (1 or 2).
	:rtype: int
	"""
	state = State(s)
	while not state.isTerminal():
		a = random.choice(state.actions())
		state.addChip(a)
	if len(state.actions()) == 0: # full board <==> tie
		return 0
	return (1 if state.to_move == 2 else 2) # player who last played wins
	

def selectNode(root: Node, s: State) -> tuple[Node, State]:
	"""
	Selects a node for simulation in MCTS according to the UCB applied to trees.
	Modifies s.
	
	:param root: The root of the Monte Carlo search tree.
	:type root: Node
	:param s: The game state corresponding to the root.
	:type s: State
	:return: The new child node generated and the state of the game corresponding to that node.
	:rtype: tuple[Node, State]
	"""
	# choose the root if its terminal
	if s.isTerminal():
		return root, s

    # stop if node not fully expanded
	possible_actions = s.actions()
	if len(root.children) < len(possible_actions):
		return root, s

	# recursively select best UCB child
	best_child = max(root.children, key = lambda c: c.UCB1())
	s.addChip(best_child.value)
	return selectNode(best_child, s)

	

def backprop(leaf: Node, winner : int):
	"""
	Backpropagates the win all the way up the Monte Carlo search tree.
	
	:param leaf: The leaf node we simulated the win from.
	:type leaf: Node
	:param winner: The result of the playout.
	:type winner: int
	"""
	if winner == leaf.player: # reward wins
		leaf.U += 1
	# if winner == 0: # currently using symmetric rewards, so no reward for tie
	# 	leaf.U += 0.0
	if winner == (1 if leaf.player == 2 else 2): # penalize losses
		leaf.U -= 1
	leaf.N += 1 # add to total visits
	if leaf.parent is not None: # recusrively update along branch of tree until reaching the root
		backprop(leaf.parent, winner)


def simulatePlayout(s: State) -> int:
	"""
	Simulates the playout from state s one time.
	
	:param s: The state to simulate playout from.
	:type s: State
	:return: The winner of the game (0 for tie, 1 or 2)
	:rtype: int
	"""
	return randomPlayout(s)
	

def updateSearchTree(root: Node, s: State):
	"""
	Performs one update step of Monte Carlo tree search.
	
	:param root: The root of the Monte Carlo search tree.
	:type root: Node
	:param s: The state corresponding to the root of the Monte Carlo Search tree.
	:type s: State
	"""
	# select node
	node, state = selectNode(root, State(s))

	# generate a new child (or skip if we selected a terminal node)
	if not state.isTerminal():
		visited_actions = {c.value for c in node.children}
		unvisited_actions = [a for a in state.actions() if a not in visited_actions]
		a = random.choice(unvisited_actions)
		state.addChip(a) # update state to correspond to generated child
		leaf = Node(value = a, parent = node) # generate child node and add to tree
		node.children.append(leaf) # add child to its parent's list of children
	else:
		leaf = node
	
	# determine winner through random play
	winner = simulatePlayout(state)

	# update search tree
	backprop(leaf, winner)



def MCTS(s: State, num_iterations = None, time_limit = None) -> int:
	"""
	Performs Monte Carlo tree search from state s to determine the next move.
	
	:param s: The game state to search from.
	:type s: State
	:param num_iterations: Maximum number of iterations to search for, or None if using time constraint.
	:param time_limit: Maximum time to search for, or None if using iteration constraint.
	:return: The best action according to MCTS.
	:rtype: int
	"""
	# input control
	if num_iterations is None and time_limit is None:
		raise ValueError('one of num_iterations or time_limit must not be None')
	if num_iterations is not None and time_limit is not None:
		raise ValueError('one of num_iterations and time_limit must be None')
	
	# root of the search tree
	# each node's player is the player who sent the game to that state (the last person who played)
	root = Node(value = 'root' if s.last_move is None else s.last_move[1], parent = None, player = (1 if s.to_move == 2 else 2))

	# iteration based constraint
	if num_iterations is not None:
		for i in range(num_iterations):
			updateSearchTree(root, s)

	# time based constraint
	if time_limit is not None:
		start = time.time()
		while time.time() - start < time_limit:
			updateSearchTree(root, s)

	# get the most visited child of the root
	visits = {}
	max_visits = -float('inf')
	max_idx = None
	for i,c in enumerate(root.children):
		visits[c.value] = c.N
		if c.N > max_visits:
			max_idx = i
			max_visits = c.N
	return root.children[max_idx].value
		


	
	









