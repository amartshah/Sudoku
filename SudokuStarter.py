#!/usr/bin/env python
import struct, string, math
from copy import *
import copy
class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board


    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
                                                                  
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
    empty_row, empty_column = checkEmpty(initial_board, MRV, LCV)
    #potential values based on current constraints
    constraints = get_constraints(empty_row, empty_column, initial_board, LCV)
    
    if len(constraints) <= 0:
        print 'infeasible solution!' #print statement added
        #the problem for the 9x9 is that our backtracking reaches this point bc apparently there are no feasible lcoations left
        return False

    for v in constraints:
        temp_board = copy.deepcopy(initial_board)
        temp_board.set_value(empty_row, empty_column, v)
        print temp_board.print_board() #print statement added   
        solution = solve(temp_board, False, False, False, False)
        if solution == False:
            break
        else:
            print 'moving back up the recursion stack' #print statement added
            print solution.print_board() #print statement added
            return solution
    print initial_board.print_board() #print statement added
    print 'last case where no solution was found and we finished backtracking!' #print statement added
    return False



    print "Remember to return the final board (the SudokuBoard object)."
    print "I'm simply returning initial_board for demonstration purposes."
    return initial_board

def delc_for_others(empty_row, empty_column, v):
    """  """

def checkEmpty(board, MRV, LCV):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)

   #when MRV and LCV are false just find next empty position (row, column)
    if LCV == False and MRV == False:
        for i in range(size):
            for j in range(size):
                if BoardArray[i][j] == 0:
                    return i, j
               
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
        if BoardArray[i][column] != 0 and (BoardArray[i][column] in constraints):
            constraints.remove(BoardArray[i][column])

    #delete numbers already in the same row
    for j in range(size):
        if BoardArray[row][j] != 0 and (BoardArray[row][j] in constraints):
            constraints.remove(BoardArray[row][j])

    #delet numbers already in subsquare - reference is_complete
    for i in range(subsquare):
        for j in range(subsquare):
            if BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] != 0 and (BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] in constraints):
                constraints.remove(BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j])
    return constraints




               
               
               
               
               
               
               
               
               
               
