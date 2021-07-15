
import numpy as np
import train

y, x = 6, 7


def test_check_connect_4():
    TOPPED_OUT = []
    NOT_TOPPED_OUT = [i for i in range(x)]
    train.gameboard = [ [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 7, 0, 0, 0, 5, 0],
                        [0, 7, 0, 0, 5, 7, 0],
                        [0, 7, 0, 5, 5, 7, 0],
                        [0, 7, 5, 7, 7, 7, 7],
                ]

    assert train.check_connect_4(4, 3) == '4connected'
    assert train.check_connect_4(2, 4) == False
    assert train.check_connect_4(6, 5) == '4connected'
    assert train.check_connect_4(1, 2) == '4connected'


def test_probable_move():
    TOPPED_OUT = []
    NOT_TOPPED_OUT = [i for i in range(x)]
    train.gameboard = [[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 5, 0],
                       [0, 7, 0, 0, 0, 7, 0],
                       [0, 7, 0, 5, 5, 7, 0],
                       [0, 7, 5, 7, 7, 7, 7],
                       ]

    assert train.probable_move(4, 3) == '4connected'
    assert train.probable_move(0, 5) == False
    assert train.probable_move(1, 2) == '4connected'


def test_is_creating_4_above():
    TOPPED_OUT = []
    NOT_TOPPED_OUT = [i for i in range(x)]
    train.top = [5, 2, 4, 3, 4, 1, 4]
    train.gameboard = [[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 5, 0],
                       [0, 7, 0, 0, 0, 7, 0],
                       [0, 7, 0, 5, 0, 7, 0],
                       [0, 7, 5, 7, 7, 7, 7],
                       ]

    assert train.is_creating_4_above(4) == True
    assert train.is_creating_4_above(3) == False

def test_add_coin():
    
    train.top = [5, 2, 4, 3, 4, 1, 4]
    train.gameboard = [[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 5, 0],
                       [0, 7, 0, 0, 0, 7, 0],
                       [0, 7, 0, 5, 0, 7, 0],
                       [0, 7, 5, 7, 7, 7, 7],
                       ]
    train.COIN = 5
    train.add_coin(0)

    assert train.gameboard == [[0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 5, 0],
                               [0, 7, 0, 0, 0, 7, 0],
                               [0, 7, 0, 5, 0, 7, 0],
                               [5, 7, 5, 7, 7, 7, 7],
                               ]
    TOPPED_OUT = [0]
    NOT_TOPPED_OUT = [1, 2, 3, 4, 5, 6]
    train.top = [0, 2, 4, 3, 4, 1, 4]
    train.gameboard = [[7, 0, 0, 0, 0, 0, 0],
                       [5, 0, 0, 0, 0, 0, 0],
                       [7, 0, 0, 0, 0, 5, 0],
                       [5, 7, 0, 0, 0, 7, 0],
                       [5, 7, 0, 5, 0, 7, 0],
                       [5, 7, 5, 7, 7, 7, 7],
                       ]
    train.COIN = 5
    train.add_coin(0)

    assert train.gameboard == [[7, 0, 0, 0, 0, 0, 0],
                               [5, 0, 0, 0, 0, 0, 0],
                               [7, 0, 0, 0, 0, 5, 0],
                               [5, 7, 0, 0, 0, 7, 0],
                               [5, 7, 0, 5, 0, 7, 0],
                               [5, 7, 5, 7, 7, 7, 7],
                               ]
