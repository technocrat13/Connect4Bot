'''main program to play a best of three with the AI trained or untrained, to train use train.py'''


import shelve
import train
import sys


y, x = 6, 7

def take_input_gamer(player):
    '''takes input if users chance, otherwise generates ai_move'''


#    if player == 9:
#        return random.choice(NOT_TOPPED_OUT)
#
    if player == 7:
        move = input('drop COIN at: ').rstrip()
        while train.valid_move_x(move) is False:
            move = input('last input invalid, go again: ').rstrip()
        return int(move) - 1

    print('AI is calculating its next move.....')
    #ai_move = stop_4_connecting()
    ai_move = train.generate_next_move(train.gameboard)
    #ai_move = random.randint(0, 6)
    print('Playing at: ' + str(ai_move + 1))
    return ai_move




key_press = input('start a best of 3 with the AI (Y/N): ')[0]
if key_press in ['y', 'Y']:
    print('loading AI...')
    train.q_table = shelve.open('q_table_shelf.db',  writeback=True)

    train.EPISODES = 3
    train.EPSILION = 1
    for e in range(train.EPISODES):
        print('----------------------------------new game------------------------------------')
        train.gameboard = [[0 for j in range(x)] for i in range(y)]
        train.TURN = 0
        train.COIN = 7
        train.top = [5 for i in range(x)]
        train.print_gameboard()

        while train.add_coin(take_input_gamer(train.COIN)) != '4connected':
            if train.TURN % 2 == 0:
                train.COIN = 5
            else:
                train.COIN = 7

            train.print_gameboard()
            train.TURN = train.TURN + 1

            if train.TURN == 42:
                print('omg a draw!!1! at game: ' +
                      str(e + 1) + '/' + str(train.EPISODES))
                train.DRAW = True
                break

        train.print_gameboard()

        train.MOVES = []
        train.TOPPED_OUT = []
        train.NOT_TOPPED_OUT = list(range(x))

        if train.DRAW is False:
            if train.COIN == 7:
                train.WINS_7 = train.WINS_7 + 1
            else:
                train.WINS_5 = train.WINS_5 + 1
            print('wow ' + str(train.COIN) + ' wins game ' + str(e + 1) + '/' + str(train.EPISODES))
        else:
            train.DRAWS = train.DRAWS + 1
            train.DRAW = False

    print('5 wins: ' + str(train.WINS_5) + ' | 7 wins: ' +
          str(train.WINS_7) + ' | draws: ' + str(train.DRAWS))
    print('5 win%: ' + str(train.WINS_5 * 100 / (e + 1)) + ' | 7 win%: ' +
          str(train.WINS_7 * 100 / (e + 1)) + ' | draw%: ' + str(train.DRAWS * 100 / (e + 1)))
    print(str(((e + 1) / train.EPISODES) * 100) + '%' + ' completion')

    print('quicksaving')
    train.q_table.sync()
    train.stamp_time()

    train.q_table.close()

else:
    sys.exit(0)

