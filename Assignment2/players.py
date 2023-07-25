import random
import time
import pygame
import math
import numpy as np
from copy import deepcopy


class connect4Player(object):
    def __init__(self, position, seed=0):
        self.position = position
        self.opponent = None
        self.seed = seed
        random.seed(seed)

    def play(self, env, move):
        move = [-1]



class human(connect4Player):

    def play(self, env, move):
        move[:] = [int(input('Select next move: '))]
        while True:
            if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
                break
            move[:] = [int(input('Index invalid. Select next move: '))]


class human2(connect4Player):

    def play(self, env, move):
        done = False
        while (not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.position == 1:
                        pygame.draw.circle(
                            screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                    else:
                        pygame.draw.circle(
                            screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    move[:] = [col]
                    done = True


class randomAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        move[:] = [random.choice(indices)]


class stupidAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p:
                indices.append(i)
        if 3 in indices:
            move[:] = [3]
        elif 2 in indices:
            move[:] = [2]
        elif 1 in indices:
            move[:] = [1]
        elif 5 in indices:
            move[:] = [5]
        elif 6 in indices:
            move[:] = [6]
        else:
            move[:] = [0]


class minimaxAI(connect4Player):

    def __init__(self, position, seed=0):
        super().__init__(position, seed)
        self.currentPlayer = position

    def play(self, env, move):
        envCopy = deepcopy(env)
        envCopy.visualize = False
        player = self.position
        depth = 1
        #Hardcoded first move if player 1
        if not np.any(env.board):
            move[:] = [player]
            env.board[5][3] = player
            #env.board[5,3] = 1
            print("had to make the first move")
            env.topPosition[3] -= 1
        


        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)

        possibleMoves = [float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf') ]

        for i in indices:
            current = i
            newEnv = self.simulateNextMove(envCopy, current, player)
            possibleMoves[i] = self.aiMin(newEnv, current, player, depth - 1)

        print("minimaxAI made a move")
        move[:] = [np.argmax(possibleMoves)]

    def aiMax(self, env, move, player, depth):
        if env.gameOver(move, player) or depth == 0:
            return self.myEval(env, player)
        
        value = float('-inf')
        env = deepcopy(env)
        env.visualize = False

        possible = env.topPosition >= 0

        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)

        for i in indices:
            currentMove = i
            newEnv = self.simulateNextMove(deepcopy(env), currentMove, player)
            value = max(value, self.aiMin(newEnv, currentMove, player, depth - 1))
        return value 
    
    def aiMin(self, env, move, player, depth):
        if env.gameOver(move, player) or depth == 0:
            #print("player", player, "value is:", self.myEval(env,player), "on this board:", env.getBoard())
            #print(depth)
            return self.myEval(env, player)
        
        value = float('inf')
        env = deepcopy(env)
        env.visualize = False

        possible = env.topPosition >= 0

        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        for i in indices:
            currentMove = i
            newEnv = self.simulateNextMove(deepcopy(env), currentMove, player)
            value = min(value, self.aiMax(newEnv, currentMove, player, depth))
        return value 
    
    def simulateNextMove(self, env, move, player):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        return env

    #This function takes a connect4 board and manipulates the array in various ways to 
    #view each 4-space as a sliding window. Does it horizontally, vertically, and both diagonals.
    #sends the array to a another function that sums up each potential win condition - enemy win conditions.
    #returns the value
    ##THIS VERSION ISN'T CORRECT BUT AB AI IS. JUST NEED TO USE THAT EVAL
    def myEval(self, env, player):
        arr = env.getBoard()

        #create size of area to check at a time, in this case 1x4 window: [0 0 0 0]
        window_shape = (1,4)

        #Create the horizontal view matrix of the board.
        arr_view = np.lib.stride_tricks.sliding_window_view(arr, window_shape)

        #Create the vertical view matrix of the board.
        arr_transposed = np.transpose(arr)
        arr_transposed_view = np.lib.stride_tricks.sliding_window_view(arr_transposed, window_shape)

        #Create the matrix of diagnoal pieces (top left to bottom right).

        #This should get the diagonal starting at [0,0]
        diag = arr.diagonal()
        #This should get the diagonal starting at [0,1]
        diag1 = arr.diagonal(1)
        #This should get the diagonal starting at [0,2], this also adds in a filler number to keep the array the same size.
        diag2 = np.append(arr.diagonal(2), 9)
        #This should get the diagonal starting at [0,3], this also adds in a filler number to keep the array the same size.
        diag3 = np.append(arr.diagonal(3), [9,9])
        #This should get the diagonal starting at (1,0), also adds a filler number
        diagneg1 = np.append(arr.diagonal(-1), 9)
        #This should get the diagonal starting at (-2,0), also adds filler numbers. 
        diagneg2 = np.append(arr.diagonal(-2), [9,9])
        alldiagonals = np.array((diagneg2, diagneg1, diag, diag1, diag2, diag3), dtype=object)
        arr_diagonals_view = np.lib.stride_tricks.sliding_window_view(alldiagonals, window_shape)

        #Create the diagonal view matrix of the board.
        arr_diagonals_view = np.lib.stride_tricks.sliding_window_view(alldiagonals, window_shape)

        #Create the matrix of diagonal pieces going the other way (top right to bottom left).
        flipped_board = np.flip(arr, 1)

        flippedDiag = flipped_board.diagonal()
        flippedDiag1 = flipped_board.diagonal(1)
        flippedDiag2 = np.append(flipped_board.diagonal(2), 9)
        flippedDiag3 = np.append(flipped_board.diagonal(3), [9,9])
        flippedDiagneg1 = np.append(flipped_board.diagonal(-1), 9)
        flippedDiagneg2 = np.append(flipped_board.diagonal(-2), [9,9])
        flippedAlldiagonals = np.array((flippedDiagneg2, flippedDiagneg1, flippedDiag, flippedDiag1, flippedDiag2, flippedDiag3), dtype=object)
        flipped_arr_diagonals_view = np.lib.stride_tricks.sliding_window_view(flippedAlldiagonals, window_shape)

        #Create the flipped diagonal view matrix of the board.
        flipped_arr_diagonals_view = np.lib.stride_tricks.sliding_window_view(alldiagonals, window_shape)

        #Check the score of each 4-space in the board, summing up your score - enemy score.
        score = 0.0
        score += self.scorechecker(arr_view, player)
        score += self.scorechecker(arr_transposed_view, player)
        score += self.scorechecker(arr_diagonals_view, player)
        score += self.scorechecker(flipped_arr_diagonals_view, player)
        return score
    ##THIS ISN'T CORRECT BUT AB AI IS    
    def scorechecker(self, arr, player):
        minimaxplayer1score = 0.0
        minimaxplayer2score = 0.0
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                for k in range(arr.shape[2]):
                    #print(arr_view[i,j,k])
                    if all(elem == 0 for elem in arr[i,j,k]):
                        pass
                        #print("array has only 0s, nothing done here")
                    elif set(arr[i,j,k]) == {0, 1}:
                        #print("increment friendly score")
                        tempScore = sum(arr[i,j,k])
                        if tempScore == 1:
                            minimaxplayer1score += 1
                        elif tempScore == 2:
                            minimaxplayer1score += 3
                        elif tempScore == 3:
                            minimaxplayer1score += 9
                        elif tempScore == 4:
                            minimaxplayer1score += 9999
                        print("temp score is ", tempScore, "for player", player, "on sequence", arr[i,j,k])
                    elif set(arr[i,j,k]) == {0, 1, 2} or set(arr[i,j,k]) == {1, 2}:
                        #print("array is a block")
                        pass
                    elif set(arr[i,j,k]) == {0, 2}:
                        tempScore = sum(arr[i,j,k])
                        if tempScore == 2:
                            minimaxplayer2score += 1
                        elif tempScore == 4:
                            minimaxplayer2score += 3
                        elif tempScore == 6:
                            minimaxplayer2score += 9
                        elif tempScore == 8:
                            minimaxplayer2score += 9999
        if player == 1:
            return minimaxplayer1score - minimaxplayer2score
        elif player == 2:
            return minimaxplayer2score - minimaxplayer1score

class alphaBetaAI(connect4Player):

    def __init__(self, position, seed=0):
        super().__init__(position, seed)
        self.currentPlayer = position

    def play(self, env, move):
        player = self.position
        depth = 2
        alpha = float('-inf')
        beta = float('inf')
    
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)

        possibleMoves = [float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf'), float('-inf') ]


        for i in indices:
            copyEnv = deepcopy(env)
            copyEnv.visualize = False
            current = i
            newEnv = self.simulateNextMove(copyEnv, current, player)
            possibleMoves[i] = self.aiMin(newEnv, current, player, depth - 1, alpha, beta)

            

        move[:] = [np.argmax(possibleMoves)]
        print("AB AI made a move")
        print("I think I'm player", player)


    def aiMax(self, env, move, player, depth, alpha, beta):

        if env.gameOver(move, player) or depth == 0:
            return self.myEval(env, player)
        
        value = float('-inf')


        possible = env.topPosition >= 0

        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)

        for i in indices:
            currentMove = i
            copyEnv = deepcopy(env)
            copyEnv.visualize = False
            newEnv = self.simulateNextMove(copyEnv, currentMove, player)
            value = max(value, self.aiMin(newEnv, currentMove, player, depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if value >= beta:
                return value

        return value 
    
    def aiMin(self, env, move, player, depth, alpha, beta):
        if env.gameOver(move, player) or depth == 0:
            return self.myEval(env, player)
        
        value = float('inf')

        possible = env.topPosition >= 0

        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)

        for i in indices:
            currentMove = i
            copyEnv = deepcopy(env)
            copyEnv.visualize = False
            newEnv = self.simulateNextMove(copyEnv, currentMove, player)
            value = min(value, self.aiMax(newEnv, currentMove, player, depth-1, alpha, beta))
            beta = min(beta, value)
            if value <= alpha:
                return value

        return value 
    
    def simulateNextMove(self, env, move, player):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        return env

    #This function takes a connect4 board and manipulates the array in various ways to 
    #view each 4-space as a sliding window. It does this horizontally, vertically, and both diagonals.
    #sends the array to a another function that sums up each potential win condition - enemy win conditions.
    #returns the value
    def myEval(self, env, player):
        arr = env.getBoard()
        #==============Diagonals============#
        diagonal_window_shape = (4,4)
        flipped_board = np.flip(arr, 1)

        #Create 4x4 view matrix array of the board.
        fourbyfour = np.lib.stride_tricks.sliding_window_view(arr, diagonal_window_shape)
        flipped_fourbyfour = np.lib.stride_tricks.sliding_window_view(flipped_board, diagonal_window_shape)

        diagonals = []
        for i in range(3):
            for j in range(4):
                diagonals.append(fourbyfour[i][j].diagonal())


        flipped_diagonals = []
        for i in range(3):
            for j in range(4):
                flipped_diagonals.append(flipped_fourbyfour[i][j].diagonal())

        allDiagonals = diagonals + flipped_diagonals
        allDiagonals = np.array(allDiagonals)

        #=========Horizontals & Verticals=========#
        #Create the horizontal view matrix of the board.
        horizontal_window_shape = (1,4)
        arr_view = np.lib.stride_tricks.sliding_window_view(arr, horizontal_window_shape)

        #Create the vertical view matrix of the board.
        vertical_window_shape = (1,4)
        transposed_arr = np.transpose(arr)
        arr_vertical_view = np.lib.stride_tricks.sliding_window_view(transposed_arr, vertical_window_shape)

        #=========Return Score======#
        score = 0.0

        allDiagonals1 = allDiagonals.reshape(6,4,1,4)
        score += self.diagScoreChecker(allDiagonals1, player)
        score += self.scorechecker(arr_view, player)
        score += self.scorechecker(arr_vertical_view, player)
        return(score)
    
    def scorechecker(self, arr, player):
        player1score = 0.0
        player2score = 0.0
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                for k in range(arr.shape[2]):
                    if set(arr[i,j,k]) == {1} or set(arr[i,j,k]) =={2}:
                        tempScore = sum(arr[i,j,k])
                        if tempScore == 4:
                            player1score = float('inf')
                        elif tempScore == 8:
                            player2score = float('inf')
                    elif set(arr[i,j,k]) == {0, 1}:
                        #Increment player 1 score.
                        p1tempScore = sum(arr[i,j,k])
                        if p1tempScore == 1:
                            player1score += 1
                        elif p1tempScore == 2:
                            player1score += 6
                        elif p1tempScore == 3:
                            player1score += 50
                    elif set(arr[i,j,k]) == {0, 1, 2} or set(arr[i,j,k]) == {1, 2}:
                        #This is a blocked array, no one can connect 4 here.
                        pass
                    elif set(arr[i,j,k]) == {0, 2}:
                        #Increment player 2's score.
                        p2tempScore = sum(arr[i,j,k])
                        if p2tempScore == 2:
                            player2score += 1
                        elif p2tempScore == 4:
                            player2score += 6
                        elif p2tempScore == 6:
                            player2score += 50
        if player == 1:
            return player1score - player2score
        elif player == 2:
            return player2score - player1score

    def diagScoreChecker(self, arr, player):
        player1score = 0.0
        player2score = 0.0
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                    if set(arr[i,j,0]) == {1} or set(arr[i,j,0]) =={2}:
                        tempScore = sum(arr[i,j,0])
                        if tempScore == 4:
                            player1score = float('inf')
                        elif tempScore == 8:
                            player2score = float('inf')
                    elif set(arr[i,j,0]) == {0, 1}:
                            #Increment player 1 score.
                            p1tempScore = sum(arr[i,j,0])
                            if p1tempScore == 1:
                                player1score += 1
                            elif p1tempScore == 2:
                                player1score += 6
                            elif p1tempScore == 3:
                                player1score += 50
                            elif p1tempScore == 4:
                                player1score = float('inf')
                    elif set(arr[i,j,0]) == {0, 1, 2} or set(arr[i,j,0]) == {1, 2}:
                            #This is a blocked array, no one can connect 4 here.
                            pass
                    elif set(arr[i,j,0]) == {0, 2}:
                            #Increment player 2's score.
                            p2tempScore = sum(arr[i,j,0])
                            if p2tempScore == 2:
                                player2score += 1
                            elif p2tempScore == 4:
                                player2score += 6
                            elif p2tempScore == 6:
                                player2score += 50
                            elif p2tempScore == 8:
                                player2score += 100
        if player == 1:
            return player1score - player2score
        elif player == 2:
            return player2score - player1score

SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
