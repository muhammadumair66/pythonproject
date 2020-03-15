import numpy as np
import copy

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numberpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        alpha = -float('inf')
        depth = 4
        beta = float('inf')
        val = self.maximum_value(board, depth, alpha, beta)
        print(str(val[0]) + "," + str(val[1]))
        return val[1]
     #   raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, board):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numberpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        depth = 4
        val = self.exp_max_value(board, depth)
        print(str(val[0]) + "," + str(val[1]))
        return val[1]
      #  raise NotImplementedError('Whoops I don\'t know what to do')
    def maximum_value(self, board, depth, alpha, beta):
        if depth == 0 or term_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        val = -float('inf')
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)
        column = 0
        for i in valid_cols:
            new_board = copy.deepcopy(board)
            new_board = board_update(i, self.player_number, new_board)
           
            x = self.minimum_value(new_board, depth - 1, alpha, beta)[0]
            if x > val:
                val = x
                column = i
            if val >= beta: return (val, i)
            # alpha = max(alpha, v)
        print("max: " + str(val) + ", depth: " + str(depth))
        return (val, column)

    def minimum_value(self, board, depth, alpha, beta):
        if depth == 0 or term_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        val = float('inf')
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)
        column = 0
        for i in valid_cols:
            new_board = copy.deepcopy(board)
            new_board = board_update(i, self.player_number, new_board)
            # v = min(v, self.max_value(new_board, depth-1,alpha, beta)[0])
            x = self.maximum_value(new_board, depth - 1, alpha, beta)[0]
            if x < val:
                val = x
                column = i
            if val <= alpha: return (val, i)
            beta = min(beta, val)
        print("min: " + str(val) + ", depth: " + str(depth))
        return (val, column)

    def exp_max_value(self, board, depth):
        if depth == 0 or term_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        val = -float('inf')
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)
        column = 0
        for i in valid_cols:
            new_board = copy.deepcopy(board)
            new_board = board_update(i, self.player_number, new_board)
            # v = max(v, self.exp_value(new_board, depth-1)[0])
            x = self.exp_value(new_board, depth - 1)[0]
            if x > val:
                val = x
                column = i
        return (val, column)

    def exp_value(self, board, depth):
        if depth == 0 or term_test(self.player_number, board):
            return (self.evaluation_function(board), 0)
        val = 0
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:, col]:
                valid_cols.append(col)
        for i in valid_cols:
            new_board = copy.deepcopy(board)
            new_board = board_update(i, self.player_number, new_board)
            val = ((1 / 7) * self.exp_max_value(new_board, depth - 1)[0]) + val
        return (val, 0)




    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numberpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
        enemy_number = 0
        if 2 - self.player_number == 1:
            enemy_number = 2
        else:
            enemy_number = 1
       
        total_Points = 0
        for i in range(1, 5):
            my_Points = count_points(self.player_number, board, i)
            enemy_Points = count_points(enemy_number, board, i)
            total_Points = total_Points + (my_Points - enemy_Points)
        return total_Points

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numberpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)

def board_update(move, player_number, board):
        if 0 in board[:, move]:
            updated_row = -1
            for row in range(1, board.shape[0]):
                updated_row = -1
                if board[row, move] > 0 and board[row - 1, move] == 0:
                    updated_row = row - 1
                elif row == board.shape[0] - 1 and board[row, move] == 0:
                    updated_row = row

                if updated_row >= 0:
                    board[updated_row, move] = player_number
                    return board

def term_test(player_number, board):
        player_win_string = '{0}{0}{0}{0}'.format(player_number)
        to_string = lambda a: ''.join(a.astype(str))

        def check_horizontal(board):
            for row in board:
                if player_win_string in to_string(row):
                    return True
            return False

        def check_verticle(board):
            return check_horizontal(board.T)

        def check_diagonal(board):
            for operation in [None, np.fliplr]:
                operation_board = operation(board) if operation else board

                root_diag = np.diagonal(operation_board, offset=0).astype(np.int)
                if player_win_string in to_string(root_diag):
                    return True

                for i in range(1, board.shape[1] - 3):
                    for offset in [i, -i]:
                        diag = np.diagonal(operation_board, offset=offset)
                        diag = to_string(diag.astype(np.int))
                        if player_win_string in diag:
                            return True

            return False

        def check_available_spaces(board):
            valid_cols = []
            for col in range(board.shape[1]):
                if 0 in board[:, col]:
                    valid_cols.append(col)
            if len(valid_cols) == 0:
                return True
            return False

        return (check_horizontal(board) or
                check_verticle(board) or
                check_diagonal(board) or
                check_available_spaces(board))

def count_points(player_number, board, number):
        player_numb_string_array = []
        factor = 0
        if number == 1:
            player_numb_string_array.append('{1}{1}{1}{0}'.format(player_number, 0))
            player_numb_string_array.append('{0}{1}{1}{1}'.format(player_number, 0))
            player_numb_string_array.append('{1}{0}{1}{1}'.format(player_number, 0))
            player_numb_string_array.append('{1}{1}{0}{1}'.format(player_number, 0))
            factor = 15
        elif number == 2:
            player_numb_string_array.append('{1}{1}{0}{0}'.format(player_number, 0))
            player_numb_string_array.append('{0}{1}{1}{0}'.format(player_number, 0))
            player_numb_string_array.append('{0}{0}{1}{1}'.format(player_number, 0))
            player_numb_string_array.append('{1}{0}{0}{1}'.format(player_number, 0))
            player_numb_string_array.append('{0}{1}{1}{0}'.format(player_number, 0))
            player_numb_string_array.append('{1}{0}{1}{0}'.format(player_number, 0))
            player_numb_string_array.append('{0}{1}{0}{1}'.format(player_number, 0))
            factor = 35
        elif number == 3:
            player_numb_string_array.append('{0}{0}{0}{1}'.format(player_number, 0))
            player_numb_string_array.append('{0}{0}{1}{0}'.format(player_number, 0))
            player_numb_string_array.append('{0}{1}{0}{0}'.format(player_number, 0))
            player_numb_string_array.append('{1}{0}{0}{0}'.format(player_number, 0))
            factor = 75
        elif number == 4:
            player_numb_string_array.append('{0}{0}{0}{0}'.format(player_number))
            factor = 250
        to_string = lambda a: ''.join(a.astype(str))

        def check_horizontal(board, factor):
            counts = 0
            for row in board:
                for i in player_numb_string_array:
                    if i in to_string(row):
                        counts = counts + factor
            return counts

        def check_verticle(board, factor):
            return check_horizontal(board.T, factor)

        def check_diagonal(board, factor):
            counts = 0
            for operation in [None, np.fliplr]:
                operation_board = operation(board) if operation else board

                root_diag = np.diagonal(operation_board, offset=0).astype(np.int)
                for lin in player_numb_string_array:
                    if lin in to_string(root_diag):
                        counts = counts + factor

                for i in range(1, board.shape[1] - 3):
                    for offset in [i, -i]:
                        diag = np.diagonal(operation_board, offset=offset)
                        diag = to_string(diag.astype(np.int))
                        for lon in player_numb_string_array:
                            if lon in diag:
                                counts = counts + factor

            return counts

        return (check_horizontal(board, factor) +
                check_verticle(board, factor) +
                check_diagonal(board, factor))


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numberpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

