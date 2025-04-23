import os
import random
import copy
from random import choices

### The probability of the randomizer: ###
# 2 - 90%
# 4 - 10%

def start_game():
    matrix = []
    for i in range(4):
        line = []
        for j in range(4):
            line.append(0)
        matrix.append(line)
    return matrix

def random_2_4(matrix):
    r = random.randint(0, 3) # generating a random position of row
    c = random.randint(0, 3) # generating a random position of column

    while matrix[r][c] != 0:
        r = random.randint(0, 3)
        c = random.randint(0, 3)

    matrix[r][c] = choices([2, 4], [0.9, 0.1])[0]
    return matrix

def left(matrix):
    # Merging the sums
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                for k in range(j+1, len(matrix[i])):
                    if (matrix[i][j] != matrix[i][k]) and (matrix[i][k] != 0):
                        break
                    if (matrix[i][j] == matrix[i][k]):
                        matrix[i][j] = matrix[i][j]*2
                        matrix[i][k] = 0
                        break
    # Aligning to left
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                for k in range(j+1, len(matrix[i])):
                    if matrix[i][k] != 0:
                        matrix[i][j] = matrix[i][k]
                        matrix[i][k] = 0
                        break
    return matrix

def up(matrix):
    # Merging the sums
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            if matrix[j][i] != 0:
                for k in range(j+1, len(matrix)):
                    if (matrix[j][i] != matrix[k][i]) and (matrix[k][i] != 0):
                        break
                    if (matrix[j][i] == matrix[k][i]):
                        matrix[j][i] = matrix[j][i]*2
                        matrix[k][i] = 0
                        break
    # Aligning up
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            if matrix[j][i] == 0:
                for k in range(j+1, len(matrix)):
                    if matrix[k][i] != 0:
                        matrix[j][i] = matrix[k][i]
                        matrix[k][i] = 0
                        break
    return matrix

def right(matrix):
    # Merging the sums
    for i in range(len(matrix)):
        for j in range(len(matrix[i])-1, -1, -1):
            if matrix[i][j] != 0:
                for k in range(j-1, -1, -1):
                    if (matrix[i][j] != matrix[i][k]) and (matrix[i][k] != 0):
                        break
                    if (matrix[i][j] == matrix[i][k]):
                        matrix[i][j] = matrix[i][j]*2
                        matrix[i][k] = 0
                        break
    # Aligning to right
    for i in range(len(matrix)):
        for j in range(len(matrix[i])-1, -1, -1):
            if matrix[i][j] == 0:
                for k in range(j-1, -1, -1):
                    if matrix[i][k] != 0:
                        matrix[i][j] = matrix[i][k]
                        matrix[i][k] = 0
                        break
    return matrix

def down(matrix):
    # Merging the sums
    for i in range(len(matrix[0])):
        for j in range(len(matrix)-1, -1, -1):
            if matrix[j][i] != 0:
                for k in range(j-1, -1, -1):
                    if (matrix[j][i] != matrix[k][i]) and (matrix[k][i] != 0):
                        break
                    if (matrix[j][i] == matrix[k][i]):
                        matrix[j][i] = matrix[j][i]*2
                        matrix[k][i] = 0
                        break
    # Aligning down
    for i in range(len(matrix[0])):
        for j in range(len(matrix)-1, -1, -1):
            if matrix[j][i] == 0:
                for k in range(j-1, -1, -1):
                    if matrix[k][i] != 0:
                        matrix[j][i] = matrix[k][i]
                        matrix[k][i] = 0
                        break
    return matrix

def mov_direction(matrix, dir):

    # a or A - left
    # d or D - right
    # w or W - up
    # s or S - down

    if (dir == 'a') or (dir == 'A'):
        matrix = left(matrix)
    if (dir == 'd') or (dir == 'D'):
        matrix = right(matrix)
    if (dir == 'w') or (dir == 'W'):
        matrix = up(matrix)
    if (dir == 's') or (dir == 'S'):
        matrix = down(matrix)
    return matrix

def win_game(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2048:
                return True
    else:
        return False

def lose_game(matrix):
    # if there are cells with 0 the game is not over
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                return False

    # if there are cells
    for i in range(len(matrix)-1):
        for j in range(len(matrix[0])-1):
            if (matrix[i][j] == matrix[i+1][j]) or (matrix[i][j] == matrix[i][j+1]):
                return False

    for j in range(3):
        if(matrix[3][j]== matrix[3][j + 1]):
            return False

    for i in range(3):
        if(matrix[i][3]== matrix[i + 1][3]):
            return False

    else:
        return True

def same_state(matrix1, matrix2):
    for i in range(4):
        for j in range(4):
            if matrix1[i][j] != matrix2[i][j]:
                return False
    return True


def print_board(matrix):

    for i in range(len(matrix)):
        print("+------+------+------+------+")
        print("|", end="")
        for j in range(len(matrix[0])):
            cell = f"{matrix[i][j]}" if matrix[i][j] != 0 else ""
            print(f" {cell:^4} |", end="")
        print()
    print("+------+------+------+------+")

##### THE MAIN PROGRAM #####

matrix = random_2_4(random_2_4(start_game()))
print_board(matrix)

while (lose_game(matrix) == False) and (win_game(matrix) == False):

    direction = input()

    previous = copy.deepcopy(matrix)  # save current state
    matrix = mov_direction(matrix, direction)

    if not same_state(previous, matrix):
        matrix = random_2_4(matrix)

    os.system('cls' if os.name == 'nt' else 'clear')

    print_board(matrix)

if lose_game:
    print("GAME OVER!")
if win_game:
    print("YOU WON!")