import math

class Node:
    def __init__(self, value, parent, children = None, player = None):
        self.value = value
        self.parent = parent
        self.children = ([] if children is None else children)
        self.N:float = 0.0 # total playouts through node
        self.U:float = 0.0 # total wins through node
        if player is not None:
            self.player = player
        else:
            self.player = (1 if parent.player == 2 else 2)
        
    def UCB1(self) -> float:
        if self.N == 0.0:
            return float('inf')
        C = math.sqrt(2)
        return self.U / self.N + C * math.sqrt(math.log(self.parent.N) / self.N)
    
    def printTree(self):
        print('displaying tree...')
        queue = [self]
        while len(queue) > 0:
            node = queue.pop(0)
            print(f'\tnode: {node.value}, parent: {None if node.parent is None else node.parent.value}, at {node.parent}')
            for c in node.children:
                queue.append(c)
            
        
    

        

    
