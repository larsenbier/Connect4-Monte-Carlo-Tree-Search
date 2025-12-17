import search
import os
from env import State
import readchar 

def isPositiveInteger(n: str) -> bool:
    try: 
        int(n) 
        if int(n) <= 0:
            return False
        return True
    except ValueError:
        return False
    
def clearWindow():
    os.system('cls' if os.name == 'nt' else 'clear')

def displayBoard(s: State, red_move, yellow_move, iter_limit, time_limit):
    clearWindow()
    print('CONTROLS:\n')
    print('Press "x" to exit')
    print('Press "r" to restart the game with the same settings.')
    print('Press "d" to adjust the difficulty of the AI.')
    print('Press the number of a playable column to make a move.' )
    print(f'\nAI level: {str(iter_limit) + ' iterations.' if iter_limit is not None else str(int(time_limit*1000)) + ' milliseconds.'} ')
    print('')
    s.display()
    print(f'\tRed Move: {red_move}\tYellow Move: {yellow_move}')


def playOneGame(rows, cols, connect_n, iter_limit, time_limit) -> str:

    # create initial game state
    s = State(rows = rows, cols = cols, connect_n = connect_n)

    # track player moves for printing
    red_move = None
    yellow_move = None

    while not s.isTerminal():

        # get player input
        key = None
        while key not in ['x', 'r', 'd'] + [str(i+1) for i in s.actions()]:
            # display initial gameboard and instructions
            displayBoard(s, red_move, yellow_move, iter_limit, time_limit)
            print('\n\tMove: ', end = '')
            key = readchar.readkey()

        # exit keys
        if key in ['x', 'r', 'd']:
            return key
        
        # player move
        red_move = int(key)
        s.addChip(red_move - 1)

        # human win
        if s.isTerminal():
            displayBoard(s, red_move, yellow_move, iter_limit, time_limit)
            print('\n\tRed wins!')
            print('\n\tPress any key to start a new game...')
            stall = readchar.readkey()
            return 'r'

        # CPU move
        
        yellow_move = search.MCTS(s, num_iterations = iter_limit, time_limit = time_limit) + 1
        s.addChip(yellow_move - 1)

        # CPU win
        if s.isTerminal():
            displayBoard(s, red_move, yellow_move, iter_limit, time_limit)
            print('\n\tYellow wins!')
            print('\n\tPress any key to start a new game...')
            stall = readchar.readkey()
            return 'r'

    # exited loop ==> tie
    displayBoard(s, red_move, yellow_move, iter_limit, time_limit)
    print('\tTie!')
    return 'r'


def play(num_iters = 100):
    clearWindow()
    again = True
    key = 'unassigned'
    while again:
        # customization setting
        print('\nWelcome to Monte Carlo tree search Connect 4 by Larsen Bier!\n')
        print('Press d to set the difficult of the AI.')
        print('Press any other key to play with the default AI difficulty (100 iterations).')
        
        # read user input
        if key != 'd':
            key=readchar.readkey()
        clearWindow()

        # get AI level
        time_limit = None # default
        iter_limit = 100 # default
        # user specified AI level
        if key == 'd':
            limit = 'unassigned'
            while True:
                clearWindow()
                print('AI DIFFICULTY:\n')
                print('Enter a positive integer number of iterations per move (e.g. 100),')
                print('or enter a positive integer number of milliseconds the AI spends thinking per move (e.g. 5ms). ')
                print('You must include the ms if you want to specify the thinking time.\n')
                limit = input('Limit: ')
                if len(limit) == 0: # handle empty inputs
                    continue
                if limit[-2:] == 'ms':
                    if isPositiveInteger(limit[:-2]):
                        time_limit = float(int(limit[:-2]))/1000
                        iter_limit = None
                        break
                if isPositiveInteger(limit):
                    iter_limit = int(limit)
                    time_limit = None
                    break

        # play game
        while True:
            key = playOneGame(rows = 6, cols = 7, connect_n = 4, iter_limit = iter_limit, time_limit = time_limit)
            
            # reassign AI difficulty
            if key == 'd':
                break

            # exit game completely
            if key == 'x': 
                again = False
                print('Gameplay terminated.')
                break
        

play()





