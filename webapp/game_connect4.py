'''enhanced  game interface with more coding expience actually AI using Q-Learning, cleaned up a lot of the previous code'''

import numpy as np


class Connect4:

    def __init__(self, Y = 6, X = 7):
        self.X = X
        self.Y = Y
        self.gameboard = np.array([[0] * X] * Y)
        self.topped_out = [False] * X

        self.top_row = np.array([Y-1] * X)
        
        self.is_game_ended = False
        self.coin = 1

    def print_gameboard(self):
        '''prints gameboard'''

        for i in self.gameboard:
            print(''.join(f'{x:3}' for x in i))


    def check_connect_4(self, x_pos, y_pos):
        '''checks if there is a 4 sequence from the recived x and y coord'''

        # Vertical check
        if y_pos <= 2 and np.sum(self.gameboard[y_pos: y_pos + 4, x_pos]) == 4 * self.coin:
            return True

        # Horizontal check
        for i in range(0, 4):
            curr_x_pos = x_pos - i
            if 0 <= curr_x_pos <= 3 and np.sum(self.gameboard[y_pos, curr_x_pos:curr_x_pos + 4]) == 4 * self.coin:
                return True

        # Diagonal \ check
        for i in range(0, 4):
            curr_x_pos = x_pos - i
            curr_y_pos = y_pos - i
            if 0 <= curr_x_pos <= 3 and 0 <= curr_y_pos <= 2 and np.sum(np.diag(self.gameboard[curr_y_pos:curr_y_pos+4, curr_x_pos:curr_x_pos+4])) == 4 * self.coin:
                return True
            
        # Diagonal / check
        for i in range(0, 4):
            curr_x_pos = x_pos - i
            curr_y_pos = y_pos + i
            if 0 <= curr_x_pos <= 3 and 4 <= curr_y_pos <= self.Y-1 and np.sum(np.flip(self.gameboard[curr_y_pos-3:curr_y_pos+1, curr_x_pos:curr_x_pos+4], axis=1).diagonal()) == 4 * self.coin:
                return True

        return False


    def add_coin(self, x_pos):
        '''adds a coin at given position, subtracts one to make it play nice with the array'''

        try:
            x_pos = int(x_pos) - 1
            if  x_pos < 0 or x_pos > 6:
                return 'ERR_inputoutofbounds'
            
        except ValueError:
            return 'ERR_valuenotcorrect'
        
        if self.top_row[x_pos] >= 0:

            self.gameboard[self.top_row[x_pos]][x_pos] = self.coin
            self.top_row[x_pos] = self.top_row[x_pos] - 1
            
            if self.check_connect_4(x_pos, self.top_row[x_pos] + 1):
                self.is_game_ended = True
                return 'GAME_OVER_4connected'
            
            if sum(self.top_row) == -self.X:
                return 'GAME_OVER_nomoremovesleft'

            self.coin = - self.coin
            return 'next_move'

        return 'ERR_rowtoppedout'
    
    def reset(self):
        '''reset all attributes about the current class instance'''


        self.gameboard = np.array([[0] * self.X] * self.Y)
        self.topped_out = [False] * self.X
        self.top_row = np.array([self.Y-1] * self.X)
        self.is_game_ended = False
        self.coin = 1
       
    def generate_move(self):

        choices = np.where(self.top_row >= 0)[0]
        # print(choices)
        
        return np.random.choice(choices, 1) + 1
    


def main():
    '''game enters here'''
    
    game = Connect4()
    game.print_gameboard()

    while not game.is_game_ended:
        print(game.add_coin(input().rstrip()))
        game.print_gameboard()
        print(game.add_coin(game.generate_move()))
        game.print_gameboard()

    print('game ended!', game.coin, 'wins!')

if __name__ == '__main__':
    main()