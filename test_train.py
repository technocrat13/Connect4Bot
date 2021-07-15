
import numpy as np
from train import check_connect_4

y, x = 6, 7

def test_check_connect_4():
    TOPPED_OUT = []
    NOT_TOPPED_OUT = [i for i in range(x)]
    gameboard = [[0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 5, 7, 0],
                 [0, 0, 0, 5, 5, 7, 0],
                 [0, 0, 5, 7, 7, 7, 0],
                ]

    assert check_connect_4(5, 2) == '4connected'
