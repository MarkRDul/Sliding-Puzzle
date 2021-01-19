# 1234_5678 -> 3.9 Seconds No Heuristic, 17 Moves
# 1234_5678 -> 0.385 Seconds Simple Heuristic, 21 Moves
# 1234_5678 -> 0.309 Seconds Manhattan, 17 Moves
import sys
import math
import time
from queue import *

class Node:
    def __init__(self, value, parent=None):
        self.value=value
        self.parent=parent
    def getValue(self):
        return self.value
    def getParent(self):
        return self.parent

def checkParams(puzzle):
    if math.sqrt(len(puzzle))%1==0:
        space=False
        for x in range (0, len(puzzle)):
            if puzzle[x]=="_" and not space:
                space=True
            elif puzzle[x]=="_" and space:
                return False
            else:
                continue
        return space
    else:
        return False

def checkSolveable(puzzle):
    puzzleNums=[]
    inversions=0
    for x in range (0, len(puzzle)):
        if puzzle[x]!="_":
            puzzleNums.append(puzzle[x])
    for x in range (0, len(puzzle)-1):
        for y in range (x, len(puzzle)-1):
            if puzzleNums[x]>puzzleNums[y]:
                inversions+=1
    return inversions%2==0

def checkSolved(puzzle):
    for x in range (1, len(puzzle)-1):
        if puzzle[x]!="_":
            if puzzle[x-1]!="_":
                if puzzle[x]<puzzle[x-1]:
                    return False
            else:
                return False
        else:
            return False
    return True

def checkMoveRight(puzzle, length):
    if puzzle.index("_")%length!=length-1:
        return True
    return False

def checkMoveLeft(puzzle, length):
    if puzzle.index("_")%length!=0:
        return True
    return False

def checkMoveDown(puzzle, length):
    if puzzle.index("_")>length-1:
        return True
    return False

def checkMoveUp(puzzle, length):
    if puzzle.index("_")<math.pow(length, 2)-length-1:
        return True
    return False

#These five functions are given to you - do not change them!
#The first four functions are what "moves" the puzzle - the math is worked out on them
def moveRight(puzzle):
    spot=puzzle.index("_")
    #The moving works on a Python concept called string slicing - the bracket notation tells Python how to divide and replace the string
    #String slicing works on a [start:end:steps] notation:
    #The first is the starting spot in the string - If empty it assumes 0
    #The second spot is where it stops copying the string - If empty it assumes the end of the string
    #The third is the steps - for example, [::2] takes every other character, while [::-1] reverses the string
    #If empty, the third assumes a value of 1 (copy the string as is)
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

#This function helps for puzzles bigger than 3x3 - we run out of numbers at 10, so we use letters
#This simply returns the number value when given the letter the puzzle uses - now we can go up to 6x6
def getNumValue(num):
    valueDict={"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9,
               "A":10, "B":11, "C":12, "D":13, "E":14, "F":15, "G":16, "H":17, "I":18, "J":19,
               "K":20, "L":21, "M":22, "N":23, "O":24, "P":25, "Q":26, "R":27, "S":28, "T":29,
               "U":30, "V":31, "W":32, "X":33, "Y":34, "Z":35}
    return valueDict[num]

def displayPuzzle(puzzle):
    side=int(math.sqrt(len(puzzle)))
    toPrint=""
    for x in range (0, side):
        for y in range(0, side):
            toPrint+=puzzle[x*side+y]+" "
        toPrint+="\n"
    print(toPrint)

def displayPath(solvePath):
    moves=0
    while solvePath:
        currentPuzzle=solvePath.pop()
        displayPuzzle(currentPuzzle)
        moves+=1
    print("Puzzle solved in "+str(moves)+" moves.")

def getSimpleHeuristicValue(puzzle):
    value=int(len(puzzle))-1
    for x in range(0, len(puzzle)-1):
        if puzzle[x]!="_":
            if x+1==getNumValue(puzzle[x]):
                value-=1
    if puzzle[int(len(puzzle)-1)]=="_":
        value-=1
    return value

def getHeuristicValue(puzzle, moves):
    size=int(math.sqrt(len(puzzle)))
    manhattan=0
    for x in range (0, len(puzzle)):
        if puzzle[x]!="_":
            manhattan+=int(abs(x/size-(int(getNumValue(puzzle[x]))-1)/size)+abs(x%size-(int(getNumValue(puzzle[x])-1)%size)))
        else:
            manhattan += int(abs(x / size - (size - 1) / size) + abs(x % size - (size - 1) % size))
    return manhattan+moves


def updateHeuristicCount(heuristicCount, heuristicValue):
    if heuristicValue in heuristicCount:
        heuristicCount[heuristicValue]+=1
    else:
        heuristicCount[heuristicValue]=0
    return heuristicCount

def main():
    startTime = time.time()  # Measure time
    # Read puzzle from command prompt, create string, replace space with underscore
    puzzle = ''.join(sys.argv[1:]).replace(" ", "_")
    if not checkParams(puzzle):
        print("Puzzle does not meet requirements - Parameters.")
        exit()
    if not checkSolveable(puzzle):
        print("Puzzle does not meet requirements - Not solveable.")
        exit()
    size=math.sqrt(len(puzzle))
    states=set()
    root=Node(puzzle)
    queue=PriorityQueue()
    heuristicCount={}
    queue.put((getHeuristicValue(puzzle, 0), 0, 0, root))
    while 1==1:
        if queue.qsize()==0:
            print("Queue Error")
            exit()
        current=queue.get()
        puzzleNode=current[3]
        puzzle=puzzleNode.getValue()
        moves=current[1]
        print(puzzle)
        if checkMoveLeft(puzzle, size):
            newState=moveLeft(puzzle)
            if newState not in states:
                states.add(newState)
                heuristicValue=getHeuristicValue(newState, moves)
                updateHeuristicCount(heuristicCount, heuristicValue)
                queue.put((heuristicValue, moves+1, heuristicCount[heuristicValue], Node(newState, puzzleNode)))
                if checkSolved(newState):
                    solvedNode=Node(newState, puzzleNode)
                    break
        if checkMoveRight(puzzle, size):
            newState = moveRight(puzzle)
            if newState not in states:
                states.add(newState)
                heuristicValue = getHeuristicValue(newState, moves)
                updateHeuristicCount(heuristicCount, heuristicValue)
                queue.put((heuristicValue, moves + 1, heuristicCount[heuristicValue], Node(newState, puzzleNode)))
                if checkSolved(newState):
                    solvedNode = Node(newState, puzzleNode)
                    break
        if checkMoveDown(puzzle, size):
            newState = moveDown(puzzle, size)
            if newState not in states:
                states.add(newState)
                heuristicValue = getHeuristicValue(newState, moves)
                updateHeuristicCount(heuristicCount, heuristicValue)
                queue.put((heuristicValue, moves + 1, heuristicCount[heuristicValue], Node(newState, puzzleNode)))
                if checkSolved(newState):
                    solvedNode = Node(newState, puzzleNode)
                    break
        if checkMoveUp(puzzle, size):
            newState = moveUp(puzzle, size)
            if newState not in states:
                states.add(newState)
                heuristicValue = getHeuristicValue(newState, moves)
                updateHeuristicCount(heuristicCount, heuristicValue)
                queue.put((heuristicValue, moves + 1, heuristicCount[heuristicValue], Node(newState, puzzleNode)))
                if checkSolved(newState):
                    solvedNode = Node(newState, puzzleNode)
                    break
    print("\n\n")
    solvePath=[solvedNode.getValue()]
    parent=solvedNode.getParent()
    while parent!=None:
        solvePath.append(parent.getValue())
        parent=parent.getParent()
    displayPath(solvePath)
    print("Time elapsed: "+"{:.3f}".format(time.time()-startTime)+" seconds.")

if __name__ == "__main__":
    main()