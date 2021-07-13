'''enhanced AI using Q-Learning, cleaned up a lot of the previous code'''

import random
import shelve
import datetime
import numpy as np



y, x = 6, 7
gameboard = [[0 for j in range(x)] for i in range(y)]

COIN = 7
MOVES = []
TOPPED_OUT = []
NOT_TOPPED_OUT = [0, 1, 2, 3, 4, 5, 6]

#q_table = {}s
q_table = shelve.open('q_table_shelf.db',  writeback=True)

#with open("qtable.txt", "rb") as myFile:
#    q_table = pickle.load(myFile)


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


    for i in [7, 5]:
        gameboard[y_pos][x_pos] = i
        #print('probablemove')
        #print_gameboard()
        if check_connect_4(x_pos, y_pos) == '4connected':
            gameboard[y_pos][x_pos] = 0
            #if i == 7:
                #print('aha saved a connect4 at ' + str(x_pos + 1))
            #else:
                #print('i win in this simple move at ' + str(x_pos + 1))
            return '4connected'
        gameboard[y_pos][x_pos] = 0

    return False

def keywithmaxval(dic):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value
    https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary"""
    k = list(dic.keys())
    # boltzmann
    val = np.array(list(dic.values()))
    # If there are multiple max values, choose randomly
    return k[int(random.choice(np.argwhere(val == np.amax(val))))]


# the percentage of time when we should take the best action (instead of a random action)
EPSILION = 0.9
DISCOUNT_FACTOR = 0.9  # discount factor for future rewards
LEARNING_RATE = 0.9  # the rate at which the AI agent should learn


def is_creating_4_above(x_pos):
    '''checks if there is a connect 4 above current pos'''

    if top[x_pos] == 0:
        return False
    y_pos = top[x_pos]

    for i in [7, 5]:
        gameboard[y_pos - 1][x_pos] = i
        #print('probablemove')
        #print_gameboard()
        #print('is this working hello')
        #print_gameboard()
        if check_connect_4(x_pos, y_pos - 1) == '4connected':
            #print('is this working hello')
            gameboard[y_pos - 1][x_pos] = 0
            return True
        gameboard[y_pos - 1][x_pos] = 0


    if check_connect_4(x_pos, top[x_pos] - 1) == '4connected':
        print('checking above xpos')
        return True

    return False


def stop_4_connecting():
    '''check_connect_4(takes x_pos and then y_pos) to highest y_pos and check for every x_pos'''

    #(0, top[0])
    #print('top in stop4connecting: ', end='')
    #print(top)

    length = len(top)
    for i in range(length):
        if top[i] == -1:
            continue
        if probable_move(i, top[i]) == '4connected':
            if check_connect_4(i, top[i]) == '4connected':
                return i
            #good_move.append(i)
            return i

    move = random.choice(NOT_TOPPED_OUT)
    gameboard_as_key = ''.join(str(item) for innerlist in gameboard for item in innerlist)
    if np.random.random() < EPSILION:
        move = keywithmaxval(q_table[gameboard_as_key])

    #print('NOTTOPPEDOUT in stop4connecting: ', end='')
    #print(NOT_TOPPED_OUT)
    count = 0
    while is_creating_4_above(move) is True:
        if count == 5:
            move = random.choice(NOT_TOPPED_OUT)
            break
        move = random.choice(NOT_TOPPED_OUT)
        count = count + 1

    return move


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
            top[x_pos] = top[x_pos] - 1
            #print('top in addcoin: ', end='')
            #print(top)
            return check_connect_4(x_pos, y_pos)

    return 'not valid'


def get_move_reward(x_pos):
    '''calculates the reward for that move at the global board state'''

    y_pos = top[x_pos]
    for i in [7, 5]:
        gameboard[y_pos][x_pos] = i
        #print('calculating reward')
        #print_gameboard()

        if check_connect_4(x_pos, y_pos) == '4connected':
            gameboard[y_pos][x_pos] = 0
            if i == 7:
                print('aha saved a connect4 at ' + str(x_pos + 1))
                return -20
            print('i win in this simple move at ' + str(x_pos + 1))
            return 100
            #return '4connected'
        gameboard[y_pos][x_pos] = 0

    return -1


def generate_next_move(board_state):
    '''next move is generated either through random or highest q value, EPSILION mediates this'''

    gameboard_as_key = ''.join(str(item)
                                for innerlist in board_state for item in innerlist)

    #print(gameboard_as_key)

    if gameboard_as_key not in q_table:
        q_table[gameboard_as_key] = {el: 0 for el in NOT_TOPPED_OUT}

    action = stop_4_connecting()

    reward = get_move_reward(action)

    old_q_value = q_table[gameboard_as_key][action]
    temporal_difference = reward + \
        (DISCOUNT_FACTOR * q_table[gameboard_as_key]
         [keywithmaxval(q_table[gameboard_as_key])]) - old_q_value

    new_q_value = old_q_value + (LEARNING_RATE * temporal_difference)
    q_table[gameboard_as_key][action] = new_q_value

    print(q_table[gameboard_as_key])

    return action


def swap_gameboard():
    '''to change all the 5s to 7s and vice versa, used to calculatate board
    for AI2 but feed to the main db'''

    for i in range(x):
        for j in range(5, top[i], -1):
            if gameboard[j][i] == 7:
                gameboard[j][i] = 5
            else:
                gameboard[j][i] = 7


def take_input(player):
    '''takes input if users chance, otherwise generates ai_move'''


    if player == 6: #change to 7 for 
        if COIN == 7:
            COIN = 5
            #print_gameboard()
            swap_gameboard()
            #print('AI2 is calculating its next move.....')
            ai_2_move = generate_next_move(gameboard)
            #print('Playing at: ' + str(ai_2_move + 1))
            COIN = 7
            swap_gameboard()
            return ai_2_move


    if player == 9:
        return random.choice(NOT_TOPPED_OUT)

    if player == 7:
        move = input('drop COIN at: ').rstrip()
        while valid_move_x(move) is False:
            move = input('last input invalid, go again: ').rstrip()
        return int(move) - 1


    print('AI is calculating its next move.....')
    #ai_move = stop_4_connecting()
    ai_move = generate_next_move(gameboard)

    #ai_move = random.randint(0, 6)
    print('Playing at: ' + str(ai_move + 1))
    return ai_move


EPISODES = 3

WINS_7 = 0
WINS_5 = 0
DRAWS = 0
DRAW = False
first_time = datetime.datetime.now()

print_gameboard()


for e in range(EPISODES):
    print('---------------------------------------new game----------------------------------------')
    gameboard = [[0 for j in range(x)] for i in range(y)]
    TURN = 0
    COIN = 7
    top = [5, 5, 5, 5, 5, 5, 5]

    while add_coin(take_input(COIN)) != '4connected':
        if TURN % 2 == 0:
            COIN = 5
        else:
            COIN = 7

        print_gameboard()
        TURN = TURN + 1

        if TURN == 42:
            print('omg a draw!!1!')
            DRAW = True
            break

    print_gameboard()

    #with open('pastGames.txt', 'a') as f:
    #    f.write('\n')
    #    f.write(''.join(MOVES))
    #    f.close()

    MOVES = []
    TOPPED_OUT = []
    NOT_TOPPED_OUT = [0, 1, 2, 3, 4, 5, 6]

    if DRAW is False:
        if COIN == 7:
            WINS_7 = WINS_7 + 1
        else:
            WINS_5 = WINS_5 + 1
        print('wow ' + str(COIN) + ' wins game ' + str(e + 1) + '/' + str(EPISODES))
    else:
        DRAWS = DRAWS + 1
        DRAW = False

    print('5 wins: ' + str(WINS_5) + ' | 7 wins: ' +
          str(WINS_7) + ' | draws: ' + str(DRAWS))
    print('5 win%: ' + str(WINS_5 * 100 / (e + 1)) + ' | 7 win%: ' +
          str(WINS_7 * 100 / (e + 1)) + ' | draw%: ' + str(DRAWS * 100 / (e + 1)))
    print(str(((e + 1) / EPISODES) * 100) + '%' + ' completion')

    if (e + 1) % (EPISODES/100) == 0:
        print('quicksaving')
        q_table.sync()


q_table.close()

later_time = datetime.datetime.now()
difference = later_time - first_time
print(divmod((difference.days * 24 * 60 * 60) + difference.seconds, 60))
