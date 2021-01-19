import sys
import math
import time

#Sliding puzzle solver
#Able to work on any size (3x3, 4x4, 5x5, etc.) though it slows considerably on larger puzzles (BFS reasons)
#Note - while this works, it is still innefficient for puzzles with longer move requirements or puzzles bigger than 3x3
#Simple heuristic can be applied to dramatically speed up solve process in another file.

#Create Node class - creates tree, allows for backtracking after path to solved puzzle found
class Node:
    def __init__(self, value, parent=None):
        self.value=value
        self.parent=parent
    def getValue(self):
        return self.value
    def getParent(self):
        return self.parent

#Check parameters - checks if...
#Puzzle is a square (3x3, 4x4)
#Checks for only one empty space
def checkParams(puzzle):
    if math.sqrt(len(puzzle))%1==0:
        space=False
        for x in range (0, len(puzzle)):
            if puzzle[x]=="_" and not space:
                space=True
            elif puzzle[x]!="_":
                continue
            else:
                return False
        return True
    else:
        return False

#Checks if the given puzzle is able to be solved - checks by looking at inversions
#For example, puzzle "81234567_" has 7 inversions - the 8 is larger than seven pieces after it
#In "82134567_", there are 8 inversions - seven for the 8 piece and one for the 2 piece (larger than 1)
#If a sliding puzzle has an even number of inversions, it is solvable. It is impossible with an odd number of inversions.
def checkSolvable(puzzle):
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

#Checks if puzzle is solved. Goes through and checks that each piece is larger than the one before it.
#Stops at length-1 because it checks the blank piece is not in the middle. The empty spot at the end
#will not trigger if it goes up to length-1.
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

#Next four functions check if movement is available. If the blank spot exists at whatever
#index it logically falls in, it returns true. Important to note that this checks moving FROM
#the direction indicated - checkMoveRight checks if you can move a piece to the right to fill
#in the empty spot on its left.
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

#Next four functions deal with moving the string around in the appropriate direction.
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

#Displays puzzle in a grid shape you would find in a sliding puzzle.
def displayPuzzle(puzzle):
    side=int(math.sqrt(len(puzzle)))
    toPrint=""
    for x in range (0, side):
        for y in range (0, side):
            toPrint+=puzzle[x*side+y]+" "
        toPrint+="\n"
    print(toPrint)

#Takes in array of moves made from solved to original state, works from
#back to front of array by displaying them.
def displayPath(solvePath):
    moves=0
    while solvePath:
        currentPuzzle=solvePath.pop()
        displayPuzzle(currentPuzzle)
        moves+=1
    print("Puzzle solved in "+str(moves)+" moves.")

def main():
    starttime=time.time() #Measure time
    #Read puzzle from command prompt, create string, replace space with underscore
    puzzle=''.join(sys.argv[1:]).replace(" ","_")
    #Check params/if solvable
    if not checkParams(puzzle):
        print("Puzzle does not meet requirements.")
    #if not checkSolvable(puzzle):
    #    print("Puzzle is not able to be solved.")
    if checkParams(puzzle):# and checkSolvable(puzzle):
        size=math.sqrt(len(puzzle))
        states=set() #Used to store checked states to avoid duplicates, speeding up solving process
        solved=False
        root=Node(puzzle) #Create initial node in tree, parent is None by default
        queue=[root] #Create queue - will append subsequent states to queue.
        while not solved:
            if len(queue)==0: #Shouldn't happen but will escape an infinite while loop
                print("Queue error.")
                exit()
            puzzleNode=queue.pop(0) #Get current puzzle node - will provide the parent for new node
            puzzle=puzzleNode.getValue() #and value for current state
            print(puzzle)
            if checkMoveLeft(puzzle, size): #If a piece can be moved from the left to the right
                newState=moveLeft(puzzle) #Get new puzzle state with piece moved
                if newState not in states: #If the new puzzle state hasn't already been made
                    states.add(newState) #Add the new state to the list of all states
                    queue.append(Node(newState, puzzleNode)) #Append new node with new state to the queue
                    if checkSolved(newState): #Check if the new state is the solved puzzle
                        solvedNode=Node(newState, puzzleNode) #If it is, signify it is the solved node and stop the while loop
                        break
            if checkMoveRight(puzzle, size): #Repeat that above process for moves from right, up, and down
                newState=moveRight(puzzle)
                if newState not in states:
                    states.add(newState)
                    queue.append(Node(newState, puzzleNode))
                    if checkSolved(newState):
                        solvedNode=Node(newState, puzzleNode)
                        break
            if checkMoveUp(puzzle, size):
                newState=moveUp(puzzle, size)
                if newState not in states:
                    states.add(newState)
                    queue.append(Node(newState, puzzleNode))
                    if checkSolved(newState):
                        solvedNode=Node(newState, puzzleNode)
                        break
            if checkMoveDown(puzzle, size):
                newState=moveDown(puzzle, size)
                if newState not in states:
                    states.add(newState)
                    queue.append(Node(newState, puzzleNode))
                    if checkSolved(newState):
                        solvedNode=Node(newState, puzzleNode)
                        break
        #Now out of while loop
        print("\n\n")
        solvePath=[solvedNode.getValue()] #Begin making path from solved state to original state
        parent=solvedNode.getParent()
        while parent != None: #While there is a parent
            solvePath.append(parent.getValue()) #Append parent value to path
            parent=parent.getParent()
        displayPath(solvePath) #Display path and finish
        print("Time elapsed: "+"{:.3f}".format(time.time()-starttime)+" seconds.") #Show time elapsed

if __name__ == "__main__":
    main()