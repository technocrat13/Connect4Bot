'''this program plays connect 4 against you'''

import random


y, x = 6, 7
gameboard = [[0 for j in range(x)] for i in range(y)]


MOVES = []
TOPPED_OUT = []
NOT_TOPPED_OUT = [0, 1, 2, 3, 4, 5, 6]


def print_gameboard():
    '''prints gameboard'''

    for i in gameboard:
        print(i)


def check_connect_list(list_to_check):
    '''checks if sent list has a 4 of the same coins'''

    if len(list_to_check) != 4 or 0 in list_to_check:
        return False

    #print(list_to_check)

    if sum(list_to_check) in [20, 28]:
        return True
    return False

def check_diagonals(x_pos, y_pos):
    '''checks for 4 connect4 on x, y'''

    index_error_count = 0
    for j in range(0, 4):
        list_diagonal_top = []
        list_diagonal_bottom = []
        for i in range(1 + j, 5 + j):
            if y_pos - 4 + i >= 0 and x_pos - 4 + i >= 0:
                try:
                    list_diagonal_top.append(
                        gameboard[y_pos - 4 + i][x_pos - 4 + i])
                    #list_diagonal_bottom.append(gameboard[y_pos + 4 - i][x_pos - 4 + i])
                except IndexError:
                    index_error_count = index_error_count + 1

            if y_pos + 4 - i >= 0 and x_pos - 4 + i >= 0:
                try:
                    #list_diagonal_top.append(gameboard[y_pos - 4 + i][x_pos - 4 + i])
                    list_diagonal_bottom.append(
                        gameboard[y_pos + 4 - i][x_pos - 4 + i])
                except IndexError:
                    index_error_count = index_error_count + 1

        #print('checking diagonal top down ', end=' ')

        if check_connect_list(list_diagonal_top) is True:
            return '4connected'

        #print('checking diagonal bottom up ', end=' ')
        if check_connect_list(list_diagonal_bottom) is True:
            return '4connected'

    return False



def check_connect_4(x_pos, y_pos):
    '''checks if there is a 4 sequence from the recived x and y coord'''

    index_error_count = 0
    # checking x axis

    #print('checking x axis ', end=' ')
    for i in range(1, 5):
        try:
            if check_connect_list(gameboard[y_pos][x_pos - 4 + i: x_pos + i]) is True:
                return '4connected'
        except IndexError:
            index_error_count = index_error_count + 1

    # checking bellow x_pos

    #print('checking x to up ', end=' ')
    try:
        if check_connect_list([gameboard[i][x_pos] for i in range(y_pos - 0, y_pos + 4)]) is True:
            return '4connected'
    except IndexError:
        index_error_count = index_error_count + 1
        #print('col not tall enough')

    # checking diagonals
    return check_diagonals(x_pos, y_pos)

    # check bottom up diagonals

    #for j in range(0, 4):
    #    list_diagonal = []
    #    for i in range(1 + j, 5 + j):
    #        try:
    #            list_diagonal.append(gameboard[y_pos + 4 - i][x_pos - 4 + i])
    #        except IndexError:
    #            index_error_count = index_error_count + 1

    #    if check_connect_list(list_diagonal) is True:
    #        return '4connected'



def probable_move(x_pos, y_pos):
    '''checks if coin placed at this position connects4'''

    for i in [5, 7]:
        gameboard[y_pos][x_pos] = i
        if check_connect_4(x_pos, y_pos) == '4connected':
            gameboard[y_pos][x_pos] = 0
            if i == 7:
                print('aha saved a connect4 at ' + str(x_pos + 1))
            else:
                print('i win in this simple move at ' + str(x_pos + 1))
            return '4connected'
        gameboard[y_pos][x_pos] = 0

    return False


def stop_4_connecting():
    '''check_connect_4(takes x_pos and then y_pos) to highest y_pos and check for every x_pos'''

    top = []
    for i in range(0, x):
        for j in range(y - 1, -1, -1):
            if gameboard[j][i] == 0:
                top.append(j)
                break


    for j, i in zip(top, range(0, x)):
        if probable_move(i, j) == '4connected':
            return i

    return random.choice(NOT_TOPPED_OUT)


def valid_move(x_pos, y_pos):
    '''checks if position is a valid move or not'''

    if x_pos in TOPPED_OUT:
        return False

    if y_pos == 0:
        TOPPED_OUT.append(x_pos)
        NOT_TOPPED_OUT.remove(x_pos)

    return True


def valid_move_x(x_pos):
    '''sanitizes input and checks if given position is valid or not'''

    try:
        x_pos = int(x_pos) - 1
    except ValueError:
        return False

    if x_pos in NOT_TOPPED_OUT:
        return True
    return False


def add_coin(x_pos):
    '''adds a coin at given position'''

    MOVES.append(str(x_pos))
    for j in range(y - 1, -1, -1):
        if gameboard[j][x_pos] == 0 and valid_move(x_pos, j) is True:
            gameboard[j][x_pos] = COIN
            y_pos = j
            break
    return check_connect_4(x_pos, y_pos)


def take_input():
    '''takes input if users chance, otherwise generates ai_move'''

    if COIN == 7:
        move = input('drop COIN at: ').rstrip()
        while valid_move_x(move) is False:
            move = input('last input invalid, go again: ').rstrip()
        return int(move) - 1

    print('AI is calculating its next move.....')
    ai_move = stop_4_connecting()
    #ai_move = random.randint(0, 6)
    print('Playing at: ' + str(ai_move + 1))
    return ai_move



TURN = 0
COIN = 7

while add_coin(take_input()) != '4connected':
    if TURN % 2 == 0:
        COIN = 5
    else:
        COIN = 7

    print_gameboard()
    TURN = TURN + 1

    if TURN == 42:
        print('omg a draw!!1!')
        break

print_gameboard()
with open('pastGames.txt', 'a') as f:
    f.write('\n')
    f.write(''.join(MOVES))
    f.close()

print('wow ' + str(COIN) + ' wins!!1!!!!1111!')
