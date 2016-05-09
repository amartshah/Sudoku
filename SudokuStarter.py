#!/usr/bin/env python
#All group members were present and contributing during all worked on this project.
#Sonia Nigam snk088 Amar Shah ats545 Armaan Shah asf408
import struct, string, math
from copy import *
import copy
import operator

counter = 0
class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
        """the constructor for the SudokuBoard"""
        self.BoardSize = size #the size of the board
        self.CurrentGameBoard= board #the current state of the game board

        constraints = []
        for x in range(1, size+1):
            constraints.append(x)
        #here we create an arary of arrays which has an array of all the constraints for each position on the board
        self.position_constraints = [[0 for x in range(size)] for y in range(size)]
        for i in range(size):
        # go through all the values for i
            for j in range(size):
            # go through all the values for i
                self.position_constraints[i][j] = get_constraints(i,j,self,False)
        #print self.position_constraints


    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        self.position_constraints[row][col] = []
        #print str(len(self.position_constraints)) + " that was the lenght of the position constraint array for the value just set = should be zerp"
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard).print_board()
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    
    #print "Your code will solve the initial_board here!"
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    
    #solution is found, return
    if is_complete(initial_board) == True:
        #print 'done, the board should be all finished!' #print statement added
        return initial_board
    
    #gets next empty row, column postion
    empty_row, empty_column = checkEmpty(initial_board, MRV, Degree)
    #potential values based on current constraints
    initial_board.position_constraints[empty_row][empty_column] = get_constraints(empty_row, empty_column, initial_board, LCV)

    if len(initial_board.position_constraints[empty_row][empty_column]) == 0:
        #print 'infeasible solution!' #print statement added
        #the problem for the 9x9 is that our backtracking reaches this point bc apparently there are no feasible lcoations left
        return False
    if LCV == True:#goes into this loop if lcv is true

        values = get_LCV(empty_row,empty_column,initial_board)
        #print values
        for v in values:

            temp_board = copy.deepcopy(initial_board)
            temp_board.set_value(empty_row, empty_column, v[0])
            global counter
            counter += 1
            
            if forward_checking == True:
                if forward_checking_get_constraints(empty_row,empty_column,temp_board,LCV) == False:
                    continue

                #print 'it is forward forward checking'
            
            #print temp_board.print_board() #print statement added
            
            solution = solve(temp_board, forward_checking, MRV, Degree, LCV)
            if solution == False:
                #print " solution was found as false @#$#%$@#$$@%@#$@#%@#$@#%@#$@#$%@%"
                continue
            else:
                #print 'moving back up the recursion stack' #print statement added
                #print solution.print_board() #print statement added
                print counter
                return solution
        
    else:
        for v in initial_board.position_constraints[empty_row][empty_column]:
            temp_board = copy.deepcopy(initial_board)
            temp_board.set_value(empty_row, empty_column, v)
            counter += 1

            if forward_checking == True:
                #print "called once"

                if forward_checking_get_constraints(empty_row,empty_column,temp_board,LCV) == False:
                    continue
                #print 'it is forward forward checking'
            
            #print temp_board.print_board() #print statement added   
            
            solution = solve(temp_board, forward_checking, MRV, Degree, LCV)
            if solution == False:
                continue
            else:
                #print 'moving back up the recursion stack' #print statement added
                #print solution.print_board() #print statement added
                print counter
                return solution
    
    #print initial_board.print_board() #print statement added
    #print 'last case where no solution was found and we finished backtracking!' #print statement added
    print counter
    return False

def forward_checking_get_constraints(row, column, board, lcv):
    '''takes a SudokuBoard and solves more of based on a position using forward checking'''
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare #this is to check the subsquare, we use a floor to reference it
    SquareCol = column // subsquare #this is to check the subsquare, we use a floor to reference it
    
    update(row, column, board)
    
    flag = True #this creates a flag here to kick out of the loop
    
    while flag == True: #get into the loop if flag is true
        flag = False #start off as false
        for i in range(size): #go through all possible bumbers
            for j in range(size):
                if len(board.position_constraints[i][j])  == 1 and BoardArray[i][j] == 0: #check to see if only 1 constraint
                    board.set_value(i, j, board.position_constraints[i][j][0]) #set the value
                    global counter #use our global counter to increase the check
                    counter += 1 #actually increase the check when we use set value
                    flag = True
                    update(i, j, board) #the function below will update the board 
                    #print "update"
                elif len(board.position_constraints[i][j])  == 0 and BoardArray[i][j] == 0:#if constraints is empty which is false then go through the loop again
                    return False
                if is_complete(board) == True: #just speeds things up if it is the optimal solution
                    #print 'special done, the board should be all finished!' #print statement added
                    return True
    return True

def update(row, column, board):
    '''Takes a SudokuBoard and updates the contraints of the position constraints matrix given a value addition'''
    if is_complete(board) == True:
        #print 'special done, the board should be all finished!' #print statement added
        return True

    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = column // subsquare
    #delete numbers already in the same column
    for i in range(size):
        if BoardArray[i][column] == 0 and BoardArray[row][column] in board.position_constraints[i][column]:
            board.position_constraints[i][column].remove(BoardArray[row][column])

    #delete numbers already in the same row
    for j in range(size):
        if BoardArray[row][j] == 0 and BoardArray[row][column] in board.position_constraints[row][j]:
            board.position_constraints[row][j].remove(BoardArray[row][column])
        
        #delet numbers already in subsquare - reference is_complete
        for i in range(subsquare):
            for j in range(subsquare):
                if BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == 0 and BoardArray[row][column] in board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j]:
                    board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j].remove(BoardArray[row][column])
    return

def checkEmpty(board, MRV, degree):
    '''Takes a sudokuboard and finds the next position that should be allocated a value based on the next empty slot, MRV and degree heuristics'''
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
   #when MRV and LCV are false just find next empty position (row, column)
    #print "WEEEEEEEEEE ITERATINGGGGG"
    #print "the value of MRV issssss " + str(MRV)
    #print "the value of Degree issssss " + str(degree)

    if degree == False and MRV == False: #you just simply return the element if it is empty
        for i in range(size):
            for j in range(size):
                if BoardArray[i][j] == 0:
                    #print i,j
                    return i, j
        #print "hello2"

    if MRV == True:
        row, column = get_MRV(board) #here you actually use the MRV
        #print row, column
        #print "hello MRV"
        return row, column

    if degree ==True: #here you actually use degree
        return get_degree(board)

def get_constraints(row, column, board, lcv):#this function here gets the constraints for a given spot
    '''returns the constraints (remaining values that are allowed) for a given position'''
    BoardArray = board.CurrentGameBoard #this is our current game board
    size = len(BoardArray) #get the size of the array
    subsquare = int(math.sqrt(size)) #square root of number so we can reference the smaller squares
    SquareRow = row // subsquare #get the floor I defined this up above
    SquareCol = column // subsquare #same thing as we have been doing
    
    constraints = [] #create an empty list
    for x in range(1, size+1): #fill empty list with possible values
        constraints.append(x) #start off with all posibbile values as contstraints


    #delete numbers already in the same column
    for i in range(size): #for number of possible values
        if (BoardArray[i][column] in constraints): #check columns
            constraints.remove(BoardArray[i][column]) #remove the constraint

    #delete numbers already in the same row
    for j in range(size):
        if (BoardArray[row][j] in constraints):
            constraints.remove(BoardArray[row][j])#remove a possible constraint

    #delet numbers already in subsquare - reference is_complete
    for i in range(subsquare):
        for j in range(subsquare):
            if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] in constraints): #check subsquare
                constraints.remove(BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j])
    return constraints

def get_MRV(board):
    '''takes a sudokuboard and returns the next position that should be allocated a value based on the MRV heuristic'''
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    # init_row, init_col = checkEmpty(board,True, False)
    # least = len(board.position_constraints[init_row][init_col])
    least = float('inf') #set to positive infitity
    #print "the startoff value for the min remaining values in constraints is " + str(least)
    row = 0
    column = 0

    for i in range(size):#check if in size
        for j in range(size): #check if in size
            #print "the number of constraints in this position is " + str(len(board.position_constraints[i][j]))
            #print "compared to the least variable which has " + str(least) + " number of remaining values"
            # if len(board.position_constraints[i][j]) != 0: #if that position is already set then empty constraint array

            if(BoardArray[i][j] == 0):#if the element is empty
                #print "#######the number of constraints in this position is " + str(len(board.position_constraints[i][j]))
                #print "#######compared to the least variable which has " + str(least) + " number of remaining values"
                if least > len(board.position_constraints[i][j]): #check to see how lease affects possible constraints
                    least = len(board.position_constraints[i][j]) #set a new least value
                    #print "as shown by the above two lines, the least variable is larger then the #of constratins at that position so we are setting that pos cons to the least var"
                    row = i
                    column = j
    #print "i returned row and column pair: " + str(row) + ", " + str(column)
    return row, column

def get_degree(board):
    '''takes a sudokuboard and returns the next position that should be allocated a value based on the degree heuristic'''

    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
 
    #initializes counter and position variables to keep track of the value with the higest number of constriants it is involved in
    most_empty = 0
    best_row = 0
    best_column = 0
    for row in range(size): #for each row
        for column in range(size): #in each column
            SquareRow = row // subsquare
            SquareCol = column // subsquare
            empty = 0
            if BoardArray[row][column] == 0:
                #count empty positions in that column 
                for i in range(size): #each position in column
                    if (BoardArray[i][column] == 0):
                        empty+=1

                #count empty positions in that row
                for j in range(size):
                    if (BoardArray[row][j] == 0):
                        empty+=1

                #count empty positions in same subsquare, make sure not to doublecount ones from row and column 
                for i in range(subsquare):
                    for j in range(subsquare):
                        if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] ==0 and SquareRow*subsquare+i != row and SquareCol*subsquare+j != column):
                            empty+=1
                #if given variable has more empty positions than present most_empty, reset variables to make this the new most_empty
                if most_empty  < empty:
                    best_row = row
                    best_column = column
                    most_empty = empty

    #returns position with most empty positions
    return best_row,best_column

def get_LCV(row, column, board):
    '''Takes a sudokuboard and returns an array with values in increasing order based on the LCV heuristic'''
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = column // subsquare
    output = dict() #initialize dict that will keep track of values and corresponding involvement with other variable's constraints
    least_constrained = float('inf')
    
    #check that the position is empty
    if(BoardArray[row][column] == 0):
        #iterate through potential values based on constraints matrix
        for x in board.position_constraints[row][column]:
            constrained = 0

            for i in range(size): #increments based on column positions' constraints
                if (BoardArray[i][column] == 0):
                    if (x in board.position_constraints[i][column]):
                        constrained+=1

            for j in range(size):
                if (BoardArray[row][j] == 0): #increments based on row positions' constraints
                    if (x in board.position_constraints[row][j] and j != column):
                        constrained+=1

            for i in range(subsquare):
                for j in range(subsquare):#increments based on subsquare's positions' constraints
                    if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] ==0):
                        if (x in board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j] and (SquareRow*subsquare+i) != i and (SquareCol*subsquare+j) != j ):
                            constrained+=1
            #add value and count to output dict
            output[x] = constrained
    #sort dict based on increasing keys
    sorted_x = sorted(output.items(), key=operator.itemgetter(1), reverse = False)
    #return sorted list of tuples
    return sorted_x

               
               
               
               
