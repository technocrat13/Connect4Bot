'''to test all core functions of connect4'''

import webapp.game_connect4 as game_connect4
import numpy as np

train = game_connect4.Connect4()

def test_check_connect_4():
    '''tests 4 points for connect 4s'''

    train.gameboard = np.array([ [ 0,  0,  0,  0,  0,  0,  0],
                        [ 0,  0,  0,  0,  0,  0,  0],
                        [ 0, -1,  0,  0,  0,  1,  0],
                        [ 0, -1,  0,  0,  1, -1,  0],
                        [ 0, -1,  0,  1,  1, -1,  0],
                        [ 0, -1,  1, -1, -1, -1, -1],
                ])

    assert train.check_connect_4(4, 3) == True
    assert train.check_connect_4(2, 4) is False
    assert train.check_connect_4(6, 5) == True
    assert train.check_connect_4(1, 2) == True


# def test_probable_move():
#     '''tests 3 points for stopping or making 4s'''


#     train.gameboard = [[ 0,  0,  0,  0,  0,  0,  0],
#                        [ 0,  0,  0,  0,  0,  0,  0],
#                        [ 0,  0,  0,  0,  0,  1,  0],
#                        [ 0, -1,  0,  0,  0, -1,  0],
#                        [ 0, -1,  0,  1,  1, -1,  0],
#                        [ 0, -1,  1, -1, -1, -1, -1],
#                        ]

#     assert train.probable_move(4, 3) == '4connected'
#     assert train.probable_move(0,  1) is False
#     assert train.probable_move(1, 2) == '4connected'


# def test_is_creating_4_above():
#     '''tests 2 points for dangerous wells (if coin placed here, opp wins) 4s'''


#     train.top = [ 1, 2, 4, 3, 4, 1, 4]
#     train.gameboard = [[ 0,  0,  0,  0,  0,  0,  0],
#                        [ 0,  0,  0,  0,  0,  0,  0],
#                        [ 0,  0,  0,  0,  0,  1,  0],
#                        [ 0, -1,  0,  0,  0, -1,  0],
#                        [ 0, -1,  0,  1,  0, -1,  0],
#                        [ 0, -1,  1, -1, -1, -1, -1],
#                        ]

#     assert train.is_creating_4_above(4) is True
#     assert train.is_creating_4_above(3) is False


"""
def test_add_coin():
    '''testing 1 point of adding a coin and 1 point for topping out'''

    train.top = [ 1, 2, 4, 3, 4, 1, 4]
    train.gameboard = [[ 0,  0,  0,  0,  0,  0,  0],
                       [ 0,  0,  0,  0,  0,  0,  0],
                       [ 0,  0,  0,  0,  0,  1,  0],
                       [ 0, -1,  0,  0,  0, -1,  0],
                       [ 0, -1,  0,  1,  0, -1,  0],
                       [ 0, -1,  1, -1, -1, -1, -1],
                       ]
    train.COIN =  1
    train.add_coin( 0)

    assert train.gameboard == [[ 0,  0,  0,  0,  0,  0,  0],
                               [ 0,  0,  0,  0,  0,  0,  0],
                               [ 0,  0,  0,  0,  0,  1,  0],
                               [ 0, -1,  0,  0,  0, -1,  0],
                               [ 0, -1,  0,  1,  0, -1,  0],
                               [ 1, -1,  1, -1, -1, -1, -1],
                               ]
    train.TOPPED_OUT = [ 0]
    train.NOT_TOPPED_OUT = [1, 2, 3, 4,  1, 6]
    train.top = [ 0, 2, 4, 3, 4, 1, 4]
    train.gameboard = [[-1,  0,  0,  0,  0,  0,  0],
                       [ 1,  0,  0,  0,  0,  0,  0],
                       [-1,  0,  0,  0,  0,  1,  0],
                       [ 1, -1,  0,  0,  0, -1,  0],
                       [ 1, -1,  0,  1,  0, -1,  0],
                       [ 1, -1,  1, -1, -1, -1, -1],
                       ]
    train.COIN =  1
    train.add_coin( 0)

    assert train.gameboard == [[-1,  0,  0,  0,  0,  0,  0],
                               [ 1,  0,  0,  0,  0,  0,  0],
                               [-1,  0,  0,  0,  0,  1,  0],
                               [ 1, -1,  0,  0,  0, -1,  0],
                               [ 1, -1,  0,  1,  0, -1,  0],
                               [ 1, -1,  1, -1, -1, -1, -1],
                               ]
"""