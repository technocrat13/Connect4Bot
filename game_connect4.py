'''enhanced  game interface with more coding expience actually AI using Q-Learning, cleaned up a lot of the previous code'''

import numpy as np


class Connect4:

    def __init__(self, Y = 6, X = 7):
        self.X = X
        self.Y = Y
        self.gameboard = np.array([[0] * X] * Y)
        self.topped_out = [False] * X
        # self.not_topped_out = list(range(X))
        self.top_row = [Y-1] * X
        
        self.is_game_ended = False
        self.coin = 1

    def print_gameboard(self):
        '''prints gameboard'''

        for i in self.gameboard:
            print(i)


    def check_connect_4(self, x_pos, y_pos):
        '''checks if there is a 4 sequence from the recived x and y coord'''

        # Vertical check
        if y_pos <= 2 and np.sum(self.gameboard[y_pos: y_pos + 4][x_pos]) == 4 * self.coin:
            return True

        # Horizontal check
        for i in range(0, 4):
            curr_x_pos = x_pos - i
            if 0 <= curr_x_pos <= 3 and np.sum(self.gameboard[y_pos][curr_x_pos:curr_x_pos + 4] == 4 * self.coin):
                return True

        # Diagonal \ check
        for i in range(0, 4):
            curr_x_pos = x_pos - i
            curr_y_pos = y_pos - i
            if 0 <= curr_x_pos <= 3 and 0 <= curr_y_pos <= 2 and np.sum(np.diag(self.gameboard[curr_y_pos:curr_y_pos+4][curr_x_pos:curr_x_pos+4])) == 4 * self.coin:
                return True
            
        # Diagonal / check
        for i in range(0, 4):
            curr_x_pos = x_pos - i
            curr_y_pos = y_pos - i
            if 0 <= curr_x_pos <= 3 and 0 <= curr_y_pos <= 2 and np.sum(np.flip(self.gameboard[curr_y_pos:curr_y_pos+4][curr_x_pos-3:curr_x_pos+1], axis=1).diagonal()) == 4 * self.coin:
                return True

        return False


    def add_coin(self, x_pos):
        '''adds a coin at given position'''

        # if self.topped_out[x_pos]:
        #     return False # still need to handle this
        try:
            x_pos = int(x_pos) - 1
        except ValueError:
            return 'ERR_valuenotcorrect'
        


        if self.top_row[x_pos] >= 0:

            self.gameboard[self.top_row[x_pos]][x_pos] = self.coin
            self.top_row[x_pos] = self.top_row[x_pos] - 1
            
            if self.check_connect_4(x_pos, self.top_row[x_pos] - 1):
                self.is_game_ended = True
                return '4connected'
            
            

            self.coin = - self.coin

            return False


        return 'ERR_rowtoppedout'


    def take_input(self, x_pos):
        '''sanitizes and checks if given position is valid or not'''

        


def main():
    '''game enters here'''
    return 0

if __name__ == '__main__':
    main()