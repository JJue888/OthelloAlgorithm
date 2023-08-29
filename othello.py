from operator import truediv
from threading import currentThread
import turtle
import math
import copy
import random


# Constants
boardsize = 600
margin = 50

playerColors = {
    'w': 'white',
    'b': 'black'
}

# Turtle Initialization
t = turtle.Turtle()
t1 = turtle.Turtle()
t2 = turtle.Turtle()
t3 = turtle.Turtle()
s = turtle.Screen()
s.bgcolor('forest green')
s.setup(boardsize, boardsize)
t2.penup()
t.hideturtle()
t1.hideturtle()
t2.hideturtle()
t3.hideturtle()
t.speed(0)

ai_col = '?'
opp_col = '?'

# Data Structure Setup
gameBoard = [[0 for _ in range(8)] for _ in range(8)]
gameBoard[3][3] = 'w'
gameBoard[3][4] = 'b'
gameBoard[4][4] = 'w'
gameBoard[4][3] = 'b'
currentPlayer = 'b'


def drawBoard():
    t.penup()
    t.goto(-200, 200)
    t.pendown()
    t.goto(-200, -200)
    t.goto(200, -200)
    t.goto(200, 200)
    t.goto(-200, 200)
    for x in range(8):
        t.penup()
        t.goto(-200, 200 - margin * x)
        t.pendown()
        t.goto(200, 200 - margin * x)
    for x in range(8):
        t.penup()
        t.goto(200 - margin * x, -200)
        t.pendown()
        t.goto(200 - margin * x, 200)
    t.penup()


def whichRow(y):
    return int(math.ceil((y * -1) / margin + 4) - 1)


def whichColumn(x):
    return int(math.ceil((x / margin + 4)) - 1)


def xFromColumn(col):
    return -200 + margin / 2 + margin * col


def yFromRow(row):
    return 200 - margin / 2 - margin * row


def stampPlayer(row, col, player):
    t2.shape('circle')
    t2.shapesize(2, 2, 2)
    t2.color(player)
    t2.goto(xFromColumn(col), yFromRow(row))
    t2.showturtle()
    t2.stamp()
    t2.hideturtle()


def updateBoard(board, player, row, col):
    board[row][col] = player


def calculateScore(board, player):
    i = 0
    for j in board:
        for k in j:
            if k == player:
                i = i + 1
    return i


def updateScore():
    whi = 'White: ' + str(calculateScore(gameBoard, 'w'))
    bla = 'Black:' + str(calculateScore(gameBoard, 'b'))
    global currentPlayer
    t1.clear()
    t1.penup()
    t1.goto(-250, -250)
    t1.write(whi + '   ' + bla + '          ' + playerColors[currentPlayer], font=("Verdana", 15, 'normal'))


def chooseB(x, y):
    global ai_col, opp_col
    ai_col = 'w'
    opp_col = 'b'
    b1.hideturtle()
    b2.hideturtle()
    initialize()


def chooseW(x, y):
    global ai_col, opp_col, currentPlayer
    ai_col = 'b'
    opp_col = 'w'
    b1.hideturtle()
    b2.hideturtle()
    initialize()
    nextBoard(gameBoard, ai_col, ai_move(gameBoard, ai_col))
    updateScore()
    currentPlayer = reverse(currentPlayer)


b1 = turtle.Turtle()
b2 = turtle.Turtle()
b1.shapesize(4, 4, 4)
b2.shapesize(4, 4, 4)
b1.shape('circle')
b2.shape('circle')
b1.color('white')
b2.color('black')
b1.penup()
b2.penup()
b1.goto(-150, 0)
b2.goto(150, 0)
b1.onclick(chooseW)
b2.onclick(chooseB)


def initialize():
    drawBoard()
    stampPlayer(3, 3, 'white')
    stampPlayer(3, 4, 'black')
    stampPlayer(4, 4, 'white')
    stampPlayer(4, 3, 'black')
    updateScore()


def validMove(board, player, row, col):
    if not board[row][col] == 0:
        return False
    if row < 0 or row > 7 or col < 0 or col > 7:
        return False
    for y in range(-1, 2):
        for x in range(-1, 2):
            if checkDirections(board, row, col, player, y, x):
                return True
    return False


def checkDirections(board, row, col, player, directy, directx):
    if row + directy > 7 or row + directy < 0 or col + directx > 7 or col + directx < 0:
        return False
    if board[row + directy][col + directx] == 0 or board[row + directy][col + directx] == player:
        return False
    newy = 0
    newx = 0
    newy += directy
    newx += directx
    for _ in range(8):
        newy += directy
        newx += directx
        if row + newy < 0 or row + newy > 7 or col + newx < 0 or col + newx > 7:
            return False
        if board[row + newy][col + newx] == 0:
            return False
        if board[row + newy][col + newx] == player:
            return True
    return False


def allMoves(board, player):
    possible = []
    for x in range(8):
        for y in range(8):
            if board[y][x] == 0:
                if validMove(board, player, y, x):
                    possible.append([y, x])
    return possible


def reverse(player):
    p = 'b'
    if p == player:
        p = 'w'
    return p


def nextBoard(board, player, move):
    global currentPlayer
    print(move)
    if validMove(board, player, move[0], move[1]):
        board[move[0]][move[1]] = player
        stampPlayer(move[0], move[1], playerColors[player])
        for y in range(-1, 2):
            for x in range(-1, 2):
                if checkDirections(board, move[0], move[1], player, y, x):
                    newy = 0
                    newx = 0
                    for _ in range(8):
                        newy += y
                        newx += x
                        if board[move[0] + newy][move[1] + newx] == player:
                            break
                        board[move[0] + newy][move[1] + newx] = player
                        stampPlayer(move[0] + newy, move[1] + newx, playerColors[player])
    currentPlayer = reverse(currentPlayer)
    return board


def posBoard(board, player, move):
    global currentPlayer
    copyBoard = copy.deepcopy(board)
    if validMove(copyBoard, player, move[0], move[1]):
        copyBoard[move[0]][move[1]] = player
        for y in range(-1, 2):
            for x in range(-1, 2):
                if checkDirections(copyBoard, move[0], move[1], player, y, x):
                    newy = 0
                    newx = 0
                    for _ in range(8):
                        newy += y
                        newx += x
                        if copyBoard[move[0] + newy][move[1] + newx] == player:
                            break
                        copyBoard[move[0] + newy][move[1] + newx] = player
    return copyBoard


def nextMove(x, y):
    row = whichRow(y)
    col = whichColumn(x)
    global ai_col, opp_col
    if validMove(gameBoard, opp_col, row, col):
        nextBoard(gameBoard, opp_col, [row, col])
        nextBoard(gameBoard, ai_col, ai_move(gameBoard, ai_col))
        updateScore()


def comp():
    pos = allMoves(gameBoard, currentPlayer)
    move = random.randint(0, len(pos) - 1)
    nextBoard(gameBoard, currentPlayer, pos[move])


def ai_move(board, player):
    _, move = minimax(board, player, 4)
    return move


def gameOver(board):
    global currentPlayer
    if not allMoves(board, currentPlayer):
        return True
    return False


def minimax(board, player, depth):
    global ai_col, opp_col
    if depth == 0 or not allMoves(board, player):
        return evaluate(board), None
    bestMove = None
    if player == ai_col:
        maxEval = -math.inf
        for move in allMoves(board, ai_col):
            child = posBoard(board, ai_col, move)
            val, _ = minimax(child, opp_col, depth - 1)
            if val > maxEval:
                maxEval = val
                bestMove = move
        return maxEval, bestMove
    else:
        minEval = math.inf
        for move in allMoves(board, opp_col):
            child = posBoard(board, opp_col, move)
            val, _ = minimax(child, ai_col, depth - 1)
            if val < minEval:
                minEval = val
                bestMove = move
        return minEval, bestMove


def evaluate(board):
    global ai_col, opp_col

    ai_tiles = 0
    opp_tiles = 0
    ai_front_tiles = 0
    opp_front_tiles = 0

    p = 0
    f = 0
    d = 0

    X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

    V = [
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ]

    for i in range(8):
        for j in range(8):
            if board[i][j] == ai_col:
                d += V[i][j]
                ai_tiles += 1
            elif board[i][j] == opp_col:
                d -= V[i][j]
                opp_tiles += 1

            if board[i][j] != ' ':
                for k in range(8):
                    x = i + X1[k]
                    y = j + Y1[k]
                    if 0 <= x < 8 and 0 <= y < 8 and board[x][y] == ' ':
                        if board[i][j] == ai_col:
                            ai_front_tiles += 1
                        else:
                            opp_front_tiles += 1
                        break

    if ai_tiles > opp_tiles:
        p = (100.0 * ai_tiles) / (ai_tiles + opp_tiles)
    elif ai_tiles < opp_tiles:
        p = -(100.0 * opp_tiles) / (ai_tiles + opp_tiles)
    else:
        p = 0

    if ai_front_tiles > opp_front_tiles:
        f = -(100.0 * ai_front_tiles) / (ai_front_tiles + opp_front_tiles)
    elif ai_front_tiles < opp_front_tiles:
        f = (100.0 * opp_front_tiles) / (ai_front_tiles + opp_front_tiles)
    else:
        f = 0

    return (10 * p) + (74.396 * f) + (10 * d)


# initialize()
s.onclick(nextMove)
s.mainloop()
