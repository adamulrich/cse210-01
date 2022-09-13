

"""
Author: Adam Ulrich
File: TicTacToe.py

Overview
Tic-Tac-Toe is a game in which two players seek in alternate turns to complete a row, a column, or a diagonal with either three x's or three o's drawn in the spaces of a grid of nine squares.
 
Rules
Tic-Tac-Toe is played according to the following rules.

The game is played on a grid that is three squares by three squares.
Player one uses x's. Player two uses o's.
Players take turns putting their marks in empty squares.
The first player to get three of their marks in a row (vertically, horizontally, or diagonally) is the winner.
If all nine squares are full and neither player has three in a row, the game ends in a draw.

Requirements
Your program must also meet the following requirements.

The program must have a comment with assignment and author names.
The program must have at least one if/then block.
The program must have at least one while loop.
The program must have more than one function.
The program must have a function called main.
Suggestions
Make the game in any way you like. A few ideas are as follows.

Enhanced input validation with user-friendly messages.
Enhanced game over messages (x's, o's or draw).
Enhanced board size (4x4, 5x5, 6x6 grid, or user selected!)
Enhanced game display (different colors for each player)

"""

import os
from time import sleep
from termcolor import colored

PLAYER_1 = "X"
PLAYER_2 = "O"
CAT = "C"
current_user = PLAYER_1


#swap users
def swap_current_user():
    global current_user
    current_user = PLAYER_1 if current_user == PLAYER_2 else PLAYER_2


# draw board function
def draw_board(board_array,cell_format_length, row_separator):
    #clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    size = len(board_array)
    for column_iterator in range(size):
        row = board_array[column_iterator]
        for row_iterator in range(size):

            #set up cell in center for display
            #you have to do it this way because adding the color formatting changes the length, and so built in functions don't work right.
            cell = str(row[row_iterator])
            display_cell = cell.center(cell_format_length)

            #add color
            if cell == PLAYER_1:
                display_cell = display_cell.replace(PLAYER_1, colored(cell,"blue"))
            if cell == PLAYER_2:
                display_cell = display_cell.replace(PLAYER_2, colored(cell,"red"))
            
            print(f" {display_cell} ",end="")

            #if we aren't at the last item, print the cell separator
            if row_iterator != size - 1:
                print("|", end="")

        # if we aren't at the last row, print the row separator
        if column_iterator != size - 1:
            print()
            print(row_separator, end="")
            for x in range(size - 1):
                print("+" + row_separator,end="")
            print()
    print()

def check_list_for_win(row):
    #get the first cell
    first_cell = row[0]
    #if it has a player mark
    return_value = False
    if first_cell == PLAYER_1 or first_cell == PLAYER_2:
        return_value = first_cell
        #iterate over the rest of the row
        for cell in row[1:]:
            if cell != first_cell:
                #if it isn't equal, set false and bail
                return_value = False
                break
    
    return return_value

def check_for_win(board_array):
    #check rows
    for row in board_array:
        row_check = check_list_for_win(row)
        if row_check != False:
            return row_check
        
    #check columns
    for i in range(len(board_array)):
        #get column
        column = [item[i] for item in board_array]
        
        column_check = check_list_for_win(column)
        if column_check != False:
            return column_check

    #check diagonal
    diagonal1 = []
    diagonal2 = []
    diagonal_length = len(board_array[0])
    for x in range(len(board_array)):
        diagonal1.append(board_array[x][x])
        diagonal2.append(board_array[x][diagonal_length - 1 - x])

    diagonal_check = check_list_for_win(diagonal1)
    if diagonal_check != False:
        return diagonal_check


    diagonal_check = check_list_for_win(diagonal2)
    if diagonal_check != False:
        return diagonal_check

    #check for cat's game
    cat_flag = CAT
    for row in board_array:
        for cell in row:
            if isinstance(cell,int):
                cat_flag = False
                break
    
    return cat_flag

def get_valid_user_input(board_array, cell_count):
    
    while True:
        print()
        try:
            #get a number from the user for their move
            user_selection = int(input(f"{current_user}'s turn to choose a square (1 - {cell_count}): "))
        except:
            print("Invalid selection. Try again.")
            print()
            sleep(1)
            return

        #check to see if it's valid
        selected_cell_good = False
        for row in board_array:

            #if valid, set the location to the current user, and swap players and exit
            if user_selection in row:
                row[row.index(user_selection)] = current_user
                swap_current_user()
                return
    
        #we fell through, bad selection.
        print("Invalid selection. Try again.")
        print()
        sleep(1)
        return
            

def get_numeric_input(prompt: str, var_type, min = None, max = None, round_digits = None) :
    
    #they can pass in 'int' or int, and we will get the right context
    if type(var_type).__name__ != 'str':
        var_type = var_type.__name__
    while True:
        try:
            string_value = input(prompt)
            return_value = eval(var_type + "(string_value)")

            # don't bother checking if both are none.
            if min == None and max == None:
                return return_value
            else:                
                # set flags to true
                min_check = True
                max_check = True

                #check min
                if min != None:
                    if return_value < min:
                        min_check = False
                
                #check max
                if max != None:
                    if return_value > max:
                        max_check = False

                #if both check, return value
                if min_check and max_check:

                    # cast back to correct type, handle special case for int.
                    if var_type != 'int':
                        return_value = str(return_value)

                    return_value = eval(var_type + "(return_value)")
                    return return_value

                else:
                    print(f"Number not in range, try again.")

        except (ValueError) :
            print(f"Not a valid {var_type}, try again.")

# main 
def main():
    
    #get board size
    os.system('cls' if os.name == 'nt' else 'clear')
    board_size = get_numeric_input("Welcome to Tic Tac Toe. How big do you want your board to be? (3-10) -->",min=3,max=100,var_type=int)

    # create board data
    cell_format_length = len(str(board_size**2))
    row_separator = "-" * (cell_format_length + 2)
    cell_count = board_size**2

    # create board, fill with numbers
    row_list = []
    board_array = []
    counter = 1
    for row  in range(board_size):
        row_list = []
        for column in range(board_size):
            row_list.append(counter)
            counter += 1
        board_array.append(row_list)

    #main loop
    while True:
        draw_board(board_array,cell_format_length, row_separator)

        get_valid_user_input(board_array, cell_count)

        status = check_for_win(board_array)

        #if it returns CAT, then print the result and break
        if status == CAT:
            draw_board(board_array,cell_format_length, row_separator)
            print()
            print(f"Cat's game!")
            break

        #if a player has won, return the result and break
        if status == PLAYER_1 or status == PLAYER_2:
            draw_board(board_array,cell_format_length, row_separator)
            print()
            print(f"Player {status} wins!")
            break
    
        #else we stay in the loop and go again

# Call the main function so that
# this program will start executing.
if __name__ == "__main__":
    main()