from copy import deepcopy

side_length = 3
expandedNodes = 0
maxNodes = 0
goalDepth = 0
makeQueue = []

# EightPuzzle class, for printing the puzzle
class EightPuzzle:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        #self.goalState = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '.']]
        self.goalState = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', '.']]
    def print(self):
        for i in self.puzzle:
            print("\t" + " ".join([str(j) for j in i]))

# NodeState class, for each node state in the state tree
class NodeState:
    def __init__(self, eightPuzzle, gn, hn):
        self.eightPuzzle = eightPuzzle 
        self.gn = gn  # g(n)
        self.hn = hn  # h(n)
        self.fn = self.gn + self.hn  # f(n)
        self.goalState = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', '.']]  # Goal State

# Find the "." tile
def findDotTile(puzzle):
    for i in range(0, side_length):
        for j in range(0, side_length):
            if puzzle[i][j] == '.':
                return i, j

# Calculating hn value for misplaced tile
def misplacedTile(state):
    totalMisplaced = 0
    for i in range(3):
        for j in range(3):
            if state.eightPuzzle.puzzle[i][j] != state.eightPuzzle.goalState[i][j] and state.eightPuzzle.puzzle[i][j] != '.':
                totalMisplaced = totalMisplaced + 1  
    return totalMisplaced

# Calculating hn value for manhattan distance hn
def manhattanDistance(state):
    map_x = {}
    map_y = {}
    manhattan_sum = 0
    for i in range(3):
        for j in range(3):
            point = state.goalState[i][j]
            map_x[point],map_y[point]= i,j
    for i in range(3):
        for j in range(3):
            point = state.eightPuzzle.puzzle[i][j]
            manhattan_sum += abs(map_x[point] -i) + abs(map_y[point]-j)
    return manhattan_sum


# Operators to move the blank either left, right, up, or down.   'up': 0, 'down': 1, 'left': 2, 'right': 3
def moveBlankTile(puzzle_raw, puzzle, index):
    i, j = findDotTile(puzzle)
    move_i = [-1,1,0,0]
    move_j = [0,0,-1,1]
    target_i = i + move_i[index]
    target_j = j + move_j[index]
    if 0 <= target_i and target_i < side_length and 0 <= target_j and target_j < side_length:
        puzzle[i][j], puzzle[target_i][target_j] = puzzle[target_i][target_j], puzzle[i][j]
        makeQueue.append(puzzle_raw)


def expand(parentNode):
    gCost = str(parentNode.gn)  # cost g(n)
    hCost = str(parentNode.hn)  # cost h(n)
    bestStateStr = "The best state to expand: g(n) = " + gCost + " and h(n) = " + hCost + " is\n"
    print(bestStateStr)
    parentNode.eightPuzzle.print()
    print("Expanding this node")

    going_node_list = [deepcopy(parentNode) for _ in range(0,4)]
    for i in range(0,4):
        going_now = going_node_list[i]
        moveBlankTile(parentNode.eightPuzzle.puzzle,going_now.eightPuzzle.puzzle,i)
        going_now.gn = going_now.gn + 1
        going_now.fn = going_now.gn + going_now.hn
    return going_node_list

def removeFront(nodes):
    nodes.sort(key=lambda nodes: nodes.fn, reverse=True)
    headNode = nodes[0]
    index = 0
    for i in range(len(nodes)):
        if nodes[i].fn < headNode.fn:
            index = i
    headNode = nodes[index]
    nodes.pop(index)
    return headNode

def queueingFunction(node, algorithmName, nodes):
    global expandedNodes
    for i in node:
        if algorithmName == "UniformCostSearch":
            i.hn = 0
            if i.eightPuzzle.puzzle not in makeQueue:
                index = node.index(i)
                nodes.insert(index, i)
                makeQueue.append(i.eightPuzzle.puzzle)
                expandedNodes = expandedNodes + 1
        if algorithmName == "MisplacedTiles":
            i.hn = misplacedTile(i)
            if i.eightPuzzle.puzzle not in makeQueue:
                nodes.append(i)
                makeQueue.append(i.eightPuzzle.puzzle)
                expandedNodes = expandedNodes + 1
        if algorithmName == "ManhattanDistance":
            i.hn = manhattanDistance(i)
            if i.eightPuzzle.puzzle not in makeQueue:
                nodes.append(i)
                makeQueue.append(i.eightPuzzle.puzzle)
                expandedNodes = expandedNodes + 1
    return nodes

def generalSearch(problem, algorithmName):
    global maxNodes
    global goalDepth
    node = NodeState(problem, 0, 0)  # The initial state of the puzzle
    nodes = [node]  # MAKE-QUEUE
    while True:
        maxNodes = max(len(nodes),maxNodes)
        if len(nodes) == 0:
            print("No solution found.")
            return 0
        node = removeFront(nodes)
        if problem.goalState == node.eightPuzzle.puzzle:
            goalDepth = node.gn
            expandedInStr = str(expandedNodes)
            maxInStr = str(maxNodes)
            goalInStr = str(goalDepth)

            print("Solution found!")
            node.eightPuzzle.print()
            print("expaned node: " + expandedInStr)
            print("max number of nodes in the queue: " + maxInStr)
            print("depth of the goal node: " + goalInStr)
            return node
        nodes = queueingFunction(expand(node), algorithmName, nodes)

def main():
    userInput = ""  
    userPuzzle = None  
    # Puzzle that will be used as default puzzle with user enters 1
    #defaultPuzzle = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', '.']]
    #defaultPuzzle = [['A', 'B', 'C'], ['D', 'E', 'F'], ['.', 'G', 'H']]
    defaultPuzzle = [['A', 'B', 'C'], ['E', '.', 'F'], ['D', 'G', 'H']]
    #defaultPuzzle = [['A', 'C', 'F'], ['E', '.', 'B'], ['D', 'G', 'H']]
    #defaultPuzzle = [['A', 'C', 'F'], ['E', '.', 'G'], ['D', 'H', 'B']]
    #defaultPuzzle = [['A', 'F', 'G'], ['E', '.', 'C'], ['D', 'H', 'B']]
    #defaultPuzzle = [['G', 'A', 'B'], ['D', 'H', 'E'], ['F', 'C', '.']]
    #defaultPuzzle = [['.', 'G', 'B'], ['D', 'F', 'A'], ['C', 'E', 'H']]

    print("Welcome to 8-Puzzle solver.")
    print("Type \"1\" to use default puzzle.")
    print("Type \"2\" to use your puzzle.")
    while userInput != "1" and userInput != "2": 
        userInput = input("Your choice:") 
        if userInput == "1":
            print("Using default puzzle now")
            userPuzzle = EightPuzzle(defaultPuzzle)  
            userPuzzle.print()  # Print the puzzle
        elif userInput == "2":
            print("Enter your puzzle")
            print("use \".\" to represent the blank")
            print("use space or tabs between letters")
            row_list = []
            for i in range(0,side_length):
                row_list.append([str(s) for s in input("Enter the row "+str(i+1)+": ").split()])
            userPuzzle = EightPuzzle(row_list)
            print("Your puzzle:")
            userPuzzle.print()  # Print the puzzle
    chooseAlgorithm(userPuzzle) 

def chooseAlgorithm(userPuzzle):
    userInput = 0
    algorithmName = ""
    algorithmNameList = ["","UniformCostSearch","MisplacedTiles","ManhattanDistance"]
    node = None
    while userInput <1 or userInput>3:
        print(R'''
Enter your choice of algorithm number
1. Uniform Cost Search
2. A* with the Misplaced Tile Heuristic
3. A* with the Manhattan distance Heuristic''')
        userInput = int(input("Your choice:"))
        if userInput <1 or userInput >3:
            continue
        algorithmName = algorithmNameList[userInput]
        print("initial state:")
        userPuzzle.print()
        node = generalSearch(userPuzzle,algorithmName) 
main()
