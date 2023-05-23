'''enhanced  game interface with more coding expience actually AI using Q-Learning, cleaned up a lot of the previous code'''

import numpy as np
from copy import deepcopy


class Connect4:

    def __init__(self, Y = 6, X = 7):
        self.X = X
        self.Y = Y
        self.gameboard = np.array([[0] * X] * Y)
        self.topped_out = [False] * X

        self.top_row = np.array([Y-1] * X)
        
        self.is_game_ended = False
        self.coin = 1
        self.AI_PLAYER = None

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
            if 0 <= curr_x_pos <= 3 and 3 <= curr_y_pos <= self.Y-1 and np.sum(np.flip(self.gameboard[curr_y_pos-3:curr_y_pos+1, curr_x_pos:curr_x_pos+4], axis=1).diagonal()) == 4 * self.coin:
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
                self.is_game_ended = True
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
        self.AI_PLAYER = None
       
    def generate_move(self):

        self.AI_PLAYER = self.coin
        remaining_moves = np.count_nonzero(self.gameboard==0)

        depth = 13.513-0.224*remaining_moves
        depth = max(5, int(np.floor(depth)) - 2)

        print(f'{depth = }')
        return self.get_best_move(depth)
    
    def get_best_move(self, depth):
        score_dict = {}

        for move in self.get_valid_moves():
            new_board = deepcopy(self)
            if new_board.add_coin(move + 1) == 'GAME_OVER_4connected': # player changed
                return move + 1
            score = new_board.minimax(depth - 1, False, move, 0)
            score_dict[move] = score_dict.get(move, 0) + score


        print(score_dict)
        max_value = np.max(list(score_dict.values()))
        max_keys = [k for k, v in score_dict.items() if v == max_value]  # get all keys with max value
        move = np.random.choice(max_keys) + 1
        print(move)
        return move

    
    def evaluate(self, x_pos):
        multiplier = -1
        if self.coin == self.AI_PLAYER:
            multiplier = 1

        if not self.is_game_ended:

            return multiplier * sum(self.top_row + self.X)

        if not self.check_connect_4(x_pos, self.top_row[x_pos] + 1):
            # draw
            return 0

        return multiplier * 1000


    
    def get_valid_moves(self):
        # print(np.where(self.top_row >= 0)[0])
        return np.where(self.top_row >= 0)[0]

    def minimax(self, depth, is_maximizing_player, x_pos, running_score):
        # if is_maximizing_player is False:
        #     current_player = curr_coin
        #     self.AI_PLAYER = -curr_coin
        # else:
        #     current_player = -curr_coin
        #     self.AI_PLAYER = curr_coin

        
        if depth == 0 or self.is_game_ended:
            return self.evaluate(x_pos) + running_score

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.get_valid_moves():
                new_board = deepcopy(self)
                # new_board.coin = self.AI_PLAYER
                new_board.add_coin(move + 1)
                evals = new_board.minimax(depth - 1, False, move, self.evaluate(x_pos) + running_score)
                max_eval = max(max_eval, evals)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves():
                new_board = deepcopy(self)
                # new_board.coin = -self.AI_PLAYER
                new_board.add_coin(move + 1)
                evals = new_board.minimax(depth - 1, True, move, self.evaluate(x_pos) + running_score)
                min_eval = min(min_eval, evals)
            return min_eval


def main():
    '''game enters here'''
    
    game = Connect4()
    game.gameboard = np.array([ [ 0,  0,  0, -1, -1,  0,  0],
                                [ 0,  0, -1, -1,  0,  0,  0],
                                [ 0, -1, -1,  0,  0,  1,  0],
                                [-1, -1,  0,  0,  1, -1,  0],
                                [ 0, -1,  0,  1,  1, -1,  0],
                                [ 0, -1,  1, -1, -1, -1, -1],
                ])
    game.print_gameboard()

    # while not game.is_game_ended:
    #     print(game.add_coin(input().rstrip()))
    #     game.print_gameboard()
    #     print(game.add_coin(game.generate_move()))
    #     game.print_gameboard()
    game.coin = 1
    print(game.check_connect_4(3, 4))

    game.coin = -1
    print(game.check_connect_4(2, 2))
    print(game.check_connect_4(0, 3))

    print('game ended!', game.coin, 'wins!')

if __name__ == '__main__':
    main()