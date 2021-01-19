import sys
import math
import time
from queue import *

#Sliding puzzle solver WITH HEURISTIC
#Should allow for solving bigger problems
#All comments explaining old code on other file, all comments here are for new items
#Heuristic speed up - 1234_5678 takes around 1.2 seconds on main, 0.05 seconds on SimpleHeuristic, 0.06 on Manhattan
#Heuristic moves - 1234_5678 takes 17 moves on main, 67 on Simple, and 17 on Manhattan

#Create the Node class
#Includes a value and a parent (Node that it is linked to in the tree)
class Node:
    def __init__(self, value, parent=None):
        self.value=value
        self.parent=parent
    def getValue(self):
        return self.value
    def getParent(self):
        return self.parent

#Checks to see if the puzzle inputted will fit the requirements for the program
def checkParams(puzzle):
    #Checks if the puzzle is a perfect square root (9 for 3x3, 16 for 4x4, etc.)
    if math.sqrt(len(puzzle))%1==0:
        space=False
        #Checks that there is only one underscore (Empty space in a puzzle)
        for x in range (0, len(puzzle)):
            if puzzle[x]=="_" and not space:
                space=True
            elif puzzle[x]!="_":
                continue
            else:
                return False
        #Return true if square root and only one empty space
        return True
    else:
        return False

#Checks if the puzzle is able to be solved
#Works on Inversions - An even number of inversions is able to be solved, odd is impossible
def checkSolvable(puzzle):
    puzzleNums=[]
    inversions=0
    #Get all numbers in the puzzle into an array
    for x in range (0, len(puzzle)):
        if puzzle[x]!="_":
            puzzleNums.append(puzzle[x])
    #Count Inversions - Go through puzzle
    for x in range (0, len(puzzle)-1):
        #Start counting at x and finish through the puzzle
        for y in range (x, len(puzzle)-1):
            #If puzzle[x] is a higher number than puzzle[y], add one to inversions
            if puzzleNums[x]>puzzleNums[y]:
                inversions+=1
    #Return if inversions is an even number
    return inversions%2==0

#Check if the puzzle is solved
def checkSolved(puzzle):
    #Go through puzzle
    for x in range (1, len(puzzle)-1):
        #If puzzle[x] is not the empty space
        if puzzle[x]!="_":
            #If puzzle[x-1] is not the empty space
            if puzzle[x-1]!="_":
                #If puzzle[x-1] is greater than puzzle[x] then the puzzle is not solved
                if puzzle[x]<puzzle[x-1]:
                    return False
            else:
                return False
        else:
            return False
    #Will return true only if all pieces are in ascending value and the empty space is in the bottom right
    return True

#Next four functions focus on checking if the moves in all four directions are available
#Important to note that the function names are move from (direction)
#For checkMoveRight, see if the spot to the left of the empty space is open, then return true if it is
#Math involved here focuses on the grid of numbers, not a string like the puzzle is passed in as
def checkMoveRight(puzzle, length):
    if puzzle.index("_")%length!=length-1:
        return True
    return False

def checkMoveLeft(puzzle, length):
    if puzzle.index("_")%length!=0:
        return True
    return False

def checkMoveUp(puzzle, length):
    if puzzle.index("_")<math.pow(length, 2)-length-1:
        return True
    return False

def checkMoveDown(puzzle, length):
    if puzzle.index("_")>length-1:
        return True
    return False

#The next four functions focus on returning the puzzle string with the correct pieces moved
#The returns are string slices - they look much more intimidating before thinking through what is being returned
#Likely given at the start due to complexity
def moveRight(puzzle):
    spot=puzzle.index("_")
    return puzzle[:spot]+puzzle[spot+1]+puzzle[spot]+puzzle[spot+2:]

def moveLeft(puzzle):
    spot=puzzle.index("_")
    return puzzle[:spot-1]+puzzle[spot]+puzzle[spot-1]+puzzle[spot+1:]

def moveUp(puzzle, length):
    spot=puzzle.index("_")
    return puzzle[:spot]+puzzle[int(spot+length)]+puzzle[spot+1:int(spot+length)]+puzzle[spot]+puzzle[int(spot+length+1):]

def moveDown(puzzle, length):
    spot=puzzle.index("_")
    return puzzle[:int(spot-length)]+puzzle[spot]+puzzle[int(spot-length+1):int(spot)]+puzzle[int(spot-length)]+puzzle[spot+1:]

#Displays the puzzle in a grid
def displayPuzzle(puzzle):
    side=int(math.sqrt(len(puzzle)))
    toPrint=""
    for x in range (0, side):
        for y in range (0, side):
            toPrint+=puzzle[x*side+y]+" "
        toPrint+="\n"
    print(toPrint)

#Prints the result path from a list of moves - tree not traveled here
def displayPath(solvePath):
    moves=0
    while solvePath:
        currentPuzzle=solvePath.pop()
        displayPuzzle(currentPuzzle)
        moves+=1
    print("Puzzle solved in "+str(moves)+" moves.")

#Gets equivalent letter when number is 10 or greater - needed for 4x4 and higher boards
#Going up to Z allows for 6x6 boards
def getSimpleNumValue(num):
    valueDict={"1":"1", "2":"2", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9",
               "10":"A", "11":"B", "12":"C", "13":"D", "14":"E", "15":"F", "16":"G", "17":"H", "18":"I", "19":"J",
               "20":"K", "21":"L", "22":"M", "23":"N", "24":"O", "25":"P", "26":"Q", "27":"R", "28":"S", "29":"T",
               "30":"U", "31":"V", "32":"W", "33":"X", "34":"Y", "35":"Z"}
    return valueDict[num]

#Simple Heuristic Value - most simple heuristic. Will not result in fewest possible moves
#but will give a dramatic speed increase in solving. Not used in main method below but left
#in as a possible example.
def getSimpleHeuristicValue(puzzle): #Creates heuristic value function
    value=int(len(puzzle))-1 #Initial value is length of puzzle - how many spaces in puzzle
    for x in range (0, len(puzzle)-1): #For every spot in puzzle
        #if puzzle[x]==getSimpleNumValue(str(x+1)): #If the tile that is there in the solved state is currently there
        if x+1==getNumValue(puzzle[x]): #Same as above if statement but only uses getNumValue()
            value-=1 #Remove one from the value
    if puzzle[int(len(puzzle)-1)]=="_": #If the space is in the bottom right
        value-=1 #Remove one from the value
    return value #Return heuristic value

#Same idea as getSimpleNumValue, only reversed to provide the int value of the letter
def getNumValue(num):
    valueDict={"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
               "A":10, "B":11, "C":12, "D":13, "E":14, "F":15, "G":16, "H":17, "I":18, "J":19,
               "K":20, "L":21, "M":22, "N":23, "O":24, "P":25, "Q":26, "R":27, "S":28, "T":29,
               "U":30, "V":31, "W":32, "X":33, "Y":34, "Z":35}
    return valueDict[num]

#Heuristic value featuring Manhattan distance heuristic. Slightly more complex than simple heuristic
#but gives solution in fewer moves and quicker than the simple heuristic.
def getHeuristicValue(puzzle, moves):
    size=int(math.sqrt(len(puzzle))) #get side length of puzzle
    manhattan=0
    for x in range (0, len(puzzle)):
        if puzzle[x]!="_":
            #Manhattan distance is calculated as (current row - solved row) + (current column - solved column)
            #For example, in a 4x4 grid, the tile '1' in the 3rd row, 3rd column has Manhattan distance 4 (as it should be in 1st row, 1st col)
            #Work with (puzzle[x]-1) because 1 is the lowest tile, not 0, and everything needs to move up to adjust
            manhattan+=int(abs(x/size-(getNumValue(puzzle[x])-1)/size)+abs(x%size-(getNumValue(puzzle[x])-1)%size))
        else:
            #Same idea, but with the space it goes in the bottom right -> (size-1, size-1) coords
            manhattan+=int(abs(x/size-(size-1))+abs(x%size-(size-1)))
    #Returning Manhattan+moves allows for cutting down on the moves in the given solution
    #For example, the puzzle 1234_5678 took 46 moves without +moves, then with +moves went to the optimal 17
    return manhattan+moves

#Adds a heuristic value - useful for Priority Queue, full explanation below
def updateHeuristicCount(heuristicCount, heuristicValue):
    if heuristicValue in heuristicCount:
        heuristicCount[heuristicValue]+=1
    else:
        heuristicCount[heuristicValue]=0
    return heuristicCount

def main():
    #Start timing the program
    starttime=time.time()
    #Create puzzle string
    puzzle=''.join(sys.argv[1:]).replace(" ","_")
    #Check if it fits the parameters of the problem and if it is able to be solved
    if not checkParams(puzzle):
        print("Puzzle does not meet requirements.")
    if not checkSolvable(puzzle):
        print("Puzzle is not able to be solved.")
    if checkParams(puzzle) and checkSolvable(puzzle):
        #Get the size of the puzzle
        size=math.sqrt(len(puzzle))
        #Start an empty array with the states the puzzle is in - this helps to avoid double dipping already tried states of the puzzle
        states=set()
        #Set the root node
        root=Node(puzzle)
        # Creates a Priority Queue, with heuristic function as value
        queue=PriorityQueue()
        #Create heuristic count array - priority queue only allows one priority value per queue
        #By creating the heuristic count array, this allows multiple states with the same heuristic value
        #to be in the priority queue at one time.
        heuristicCount={}
        #Puts the first tuple into the PQ. Has four parts - the heuristic value, the number of moves made up to that point,
        #The heuristic count tie breaker, and the root for the tree. The queue will sort going from left to right, meaning that
        #the value gets sorted first, then if two have the same heuristic value the moves will be the tie breaker, and so on.
        queue.put((getHeuristicValue(puzzle, 0), 0, 0, root))
        while 1==1:
            #If the queue is 0, there was an error - exit the program
            if queue.qsize()==0:
                print("Queue error.")
                break
            #Get the current puzzle state we want to work with
            current=queue.get()
            #Get the current node on the tree for backtracing
            puzzleNode=current[3]
            #Get the puzzle we're working with from the value in the node
            puzzle=puzzleNode.getValue()
            #Get the number of moves this state has required
            moves=current[1]
            print(puzzle)
            #The next four if statements all work the same way, so comments are only on the first one
            if checkMoveLeft(puzzle, size): #If we can make a move to the left
                newState=moveLeft(puzzle) #Return what the puzzle would be like if we moved the piece from the left of the empty spot
                if newState not in states: #If the newState has not already been seen
                    states.add(newState) #Add the newState to the list
                    heuristicValue=getHeuristicValue(newState, moves) #Get heuristic value of the newState
                    updateHeuristicCount(heuristicCount, heuristicValue) #Update counter of heuristicValue
                    #Add this state to the Priority Queue
                    #Put in the Heuristic Value first, then the moves, then the tiebreaker if value and moves are the same, then a new Node
                    # with the newState and the current node as its parent
                    queue.put((heuristicValue, moves+1,heuristicCount[heuristicValue], Node(newState,puzzleNode)))
                    #Check if the puzzle is solved, if so save the solved node and break
                    if checkSolved(newState):
                        solvedNode=Node(newState, puzzleNode)
                        break
            if checkMoveRight(puzzle, size):
                newState=moveRight(puzzle)
                if newState not in states:
                    states.add(newState)
                    heuristicValue=getHeuristicValue(newState, moves)
                    updateHeuristicCount(heuristicCount, heuristicValue)
                    queue.put((heuristicValue, moves + 1, heuristicCount[heuristicValue], Node(newState, puzzleNode)))
                    if checkSolved(newState):
                        solvedNode=Node(newState, puzzleNode)
                        break
            if checkMoveUp(puzzle, size):
                newState=moveUp(puzzle, size)
                if newState not in states:
                    states.add(newState)
                    heuristicValue=getHeuristicValue(newState, moves)
                    updateHeuristicCount(heuristicCount, heuristicValue)
                    queue.put((heuristicValue, moves + 1, heuristicCount[heuristicValue], Node(newState, puzzleNode)))
                    if checkSolved(newState):
                        solvedNode=Node(newState, puzzleNode)
                        break
            if checkMoveDown(puzzle, size):
                newState=moveDown(puzzle, size)
                if newState not in states:
                    states.add(newState)
                    heuristicValue=getHeuristicValue(newState, moves)
                    updateHeuristicCount(heuristicCount, heuristicValue)
                    queue.put((heuristicValue, moves + 1, heuristicCount[heuristicValue], Node(newState, puzzleNode)))
                    if checkSolved(newState):
                        solvedNode=Node(newState, puzzleNode)
                        break
        #Now out of while loop
        print("\n\n")
        #Create the array to back track through the tree
        solvePath=[solvedNode.getValue()]
        parent=solvedNode.getParent()
        #The root's parent is None, so once we see None as the parent we know we've hit the root of the tree
        while parent != None:
            #Append the parent value to the solvePath while the node is not the root
            solvePath.append(parent.getValue())
            #Update the parent to get the next node up in the tree
            parent=parent.getParent()
        #Display the path and show the time elapsed
        displayPath(solvePath)
        print("Time elapsed: "+"{:.3f}".format(time.time()-starttime)+" seconds.") #Show time elapsed

if __name__ == "__main__":
    main()