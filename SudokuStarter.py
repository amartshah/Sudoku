#!/usr/bin/env python
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

        self.position_constraints = [[0 for x in range(size)] for y in range(size)]
        for i in range(size):
        # print i
            for j in range(size):
            # print j
                self.position_constraints[i][j] = get_constraints(i,j,self,False)
        #print self.position_constraints


    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        self.position_constraints[row][col] = []
        print str(len(self.position_constraints)) + " that was the lenght of the position constraint array for the value just set = should be zerp"
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
    
    print "Your code will solve the initial_board here!"
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    
    #solution is found, return
    if is_complete(initial_board) == True:
        print 'done, the board should be all finished!' #print statement added
        return initial_board
    
    #gets next empty row, column postion
    empty_row, empty_column = checkEmpty(initial_board, MRV, Degree)
    #potential values based on current constraints
    initial_board.position_constraints[empty_row][empty_column] = get_constraints(empty_row, empty_column, initial_board, LCV)

    if len(initial_board.position_constraints[empty_row][empty_column]) == 0:
        print 'infeasible solution!' #print statement added
        #the problem for the 9x9 is that our backtracking reaches this point bc apparently there are no feasible lcoations left
        return False
    if LCV == True:

        values = get_LCV(empty_row,empty_column,initial_board)
        print values
        for v in values:

            temp_board = copy.deepcopy(initial_board)
            temp_board.set_value(empty_row, empty_column, v[0])
            global counter
            counter += 1
            
            if forward_checking == True:
                if forward_checking_get_constraints(empty_row,empty_column,temp_board,LCV) == False:
                    continue

                print 'it is forward forward checking'
            
            print temp_board.print_board() #print statement added
            
            solution = solve(temp_board, forward_checking, MRV, Degree, LCV)
            if solution == False:
                print " solution was found as false @#$#%$@#$$@%@#$@#%@#$@#%@#$@#$%@%"
                continue
            else:
                print 'moving back up the recursion stack' #print statement added
                print solution.print_board() #print statement added
                return solution
        
    else:
        for v in initial_board.position_constraints[empty_row][empty_column]:
            temp_board = copy.deepcopy(initial_board)
            temp_board.set_value(empty_row, empty_column, v)
            counter += 1

            if forward_checking == True:
                if forward_checking_get_constraints(empty_row,empty_column,temp_board,LCV) == False:
                    continue
                print 'it is forward forward checking'
            
            print temp_board.print_board() #print statement added   
            
            solution = solve(temp_board, forward_checking, MRV, Degree, LCV)
            if solution == False:
                continue
            else:
                print 'moving back up the recursion stack' #print statement added
                print solution.print_board() #print statement added
                print counter
                return solution
    
    print initial_board.print_board() #print statement added
    print 'last case where no solution was found and we finished backtracking!' #print statement added
    print counter
    return False

def forward_checking_get_constraints(row, column, board, lcv):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = column // subsquare
    #delete numbers already in the same column
    for i in range(size):
        if BoardArray[i][column] == 0 and BoardArray[row][column] in board.position_constraints[i][column]:
            board.position_constraints[i][column].remove(BoardArray[row][column])
            if len(board.position_constraints[i][column]) == 0:
                return False            
            if len(board.position_constraints[i][column]) == 1:
                board.set_value(i,column,board.position_constraints[i][column].pop())
                forward_checking_get_constraints(i,column,board,lcv)
            print BoardArray[row][column]

    #delete numbers already in the same row
    for j in range(size):
        if BoardArray[row][j] == 0 and BoardArray[row][column] in board.position_constraints[row][j]:
            board.position_constraints[row][j].remove(BoardArray[row][column])
            if len(board.position_constraints[i][column]) == 0:
                print "asdjfaksldjfhlwthaslkgjhaslkfjhsdlkajshglaksjhfalskdjfhasldkfjh  "
                return False   
            if len(board.position_constraints[row][j]) == 1:
                board.set_value(i,column,board.position_constraints[row][j].pop())
                forward_checking_get_constraints(row,j,board,lcv)
            print BoardArray[row][column]

    #delet numbers already in subsquare - reference is_complete
    for i in range(subsquare):
        for j in range(subsquare):
            if BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == 0 and BoardArray[row][column] in board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j]:
                board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j].remove(BoardArray[row][column])
                if len(board.position_constraints[i][column]) == 0:
                    return False   
                if len(board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j]) == 1:
                    board.set_value(SquareRow*subsquare+i,SquareCol*subsquare+j,board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j].pop())
                    forward_checking_get_constraints(SquareRow*subsquare+i,SquareCol*subsquare+j,board,lcv)
                print BoardArray[row][column]
    return True

def checkEmpty(board, MRV, degree):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
   #when MRV and LCV are false just find next empty position (row, column)
    print "WEEEEEEEEEE ITERATINGGGGG"
    print "the value of MRV issssss " + str(MRV)
    print "the value of Degree issssss " + str(degree)

    if degree == False and MRV == False:
        for i in range(size):
            for j in range(size):
                if BoardArray[i][j] == 0:
                    print i,j
                    return i, j
        print "hello2"

    if MRV == True:
        row, column = get_MRV(board)
        print row, column
        print "hello MRV"
        return row, column

    if degree ==True:
        return get_degree(board)

def get_constraints(row, column, board, lcv):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = column // subsquare
    
    constraints = []
    for x in range(1, size+1):
        constraints.append(x)


    #delete numbers already in the same column
    for i in range(size):
        if (BoardArray[i][column] in constraints):
            constraints.remove(BoardArray[i][column])

    #delete numbers already in the same row
    for j in range(size):
        if (BoardArray[row][j] in constraints):
            constraints.remove(BoardArray[row][j])

    #delet numbers already in subsquare - reference is_complete
    for i in range(subsquare):
        for j in range(subsquare):
            if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] in constraints):
                constraints.remove(BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j])
    return constraints

def get_MRV(board):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    # init_row, init_col = checkEmpty(board,True, False)
    # least = len(board.position_constraints[init_row][init_col])
    least = float('inf')
    print "the startoff value for the min remaining values in constraints is " + str(least)
    row = 0
    column = 0

    for i in range(size):
        for j in range(size):
            print "the number of constraints in this position is " + str(len(board.position_constraints[i][j]))
            print "compared to the least variable which has " + str(least) + " number of remaining values"
            # if len(board.position_constraints[i][j]) != 0: #if that position is already set then empty constraint array

            if(BoardArray[i][j] == 0):
                print "#######the number of constraints in this position is " + str(len(board.position_constraints[i][j]))
                print "#######compared to the least variable which has " + str(least) + " number of remaining values"
                if least > len(board.position_constraints[i][j]):
                    least = len(board.position_constraints[i][j])
                    print "as shown by the above two lines, the least variable is larger then the #of constratins at that position so we are setting that pos cons to the least var"
                    row = i
                    column = j
    print "i returned row and column pair: " + str(row) + ", " + str(column)
    return row, column

def get_degree(board):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
 
    
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

                #delet numbers already in subsquare - reference is_complete
                for i in range(subsquare):
                    for j in range(subsquare):
                        if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] ==0 and SquareRow*subsquare+i != row and SquareCol*subsquare+j != column):
                            empty+=1
                if most_empty  < empty:
                    best_row = row
                    best_column = column
                    most_empty = empty
    return best_row,best_column

def get_LCV(row, column, board):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    SquareRow = row // subsquare
    SquareCol = column // subsquare
    output = dict()
    
    least_constrained = float('inf')
    
    #if that position is already set then empty constraint array
    if(BoardArray[row][column] == 0):
        for x in board.position_constraints[row][column]:
            constrained = 0

            for i in range(size): #each position in column
                if (BoardArray[i][column] == 0):
                    if (x in board.position_constraints[i][column]):
                        constrained+=1

            for j in range(size):
                if (BoardArray[row][j] == 0):
                    if (x in board.position_constraints[row][j] and j != column):
                        constrained+=1

            for i in range(subsquare):
                for j in range(subsquare):
                    if (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] ==0):
                        if (x in board.position_constraints[SquareRow*subsquare+i][SquareCol*subsquare+j] and (SquareRow*subsquare+i) != i and (SquareCol*subsquare+j) != j ):
                            constrained+=1

            output[x] = constrained
    sorted_x = sorted(output.items(), key=operator.itemgetter(1), reverse = False)
    print sorted_x
    return sorted_x


# #look at the doc string
#def find_LCV(row, column, board):
#     """
#     returns the coordinates of the blank square in the grid that is
#     involved in the fewest number of constraints with unassigned variables
#     """
#     BoardArray = board.CurrentGameBoard
#     size = len(BoardArray)
#     subsquare = int(math.sqrt(size))
#     SquareRow = row // subsquare
#     SquareCol = column // subsquare
#     coords = 0
#     low_constraints = size*size  # the max number of constraints, default to first open square
#
#     for row in range(size):
#         for col in range(size):
#             if BoardArray[row][col] == 0:
#                 constraints = 0
#                 for i in range(size):  # first check row + column constraints
#                     if BoardArray[row][i] == 0: constraints += 1
#                     if BoardArray[i][col] == 0: constraints += 1
#                 for i in range(subsquare):  # lastly check subsquare constraints
#                     for j in range(subsquare):
#                         if ((BoardArray[SquareRow * subsquare + i][SquareCol * subsquare + j]
#                                  == 0)
#                             and (SquareRow * subsquare + i != row)
#                             and (SquareCol * subsquare + j != col)): constraints += 1
#
#                 if constraints < low_constraints:
#                     low_constraints = constraints
#                     coords = BoardArray[row][column]
#     print board
##if low_constraints == size*size: return False
#
#     return coords

               
               
               
               
               
               
               
               
