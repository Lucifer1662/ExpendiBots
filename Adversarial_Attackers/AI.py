from Adversarial_Attackers.board import Board
from Adversarial_Attackers.path_finding import all_possible_moves, possible_moves,vector_addition,nextTo
from Adversarial_Attackers.score_board import bestMoves, breakTiesWithRankPieceHeuristic, blowUps, \
    createbmap, rankBoard, enemiesVsPlayerHeuristic
import operator
import math
import numpy as np
import random
import copy
import time
 
 

def InplaceMove(board, move):
    moveBoard = board
    #if is movement move, inplace make move
    if(move[0] != None):
            moveBoard.update_board(move[1], move[2], move[0])
    #else copy board to perform boom
    else:
        moveBoard = board.copy()
        moveBoard.update_board(move[1],move[2], move[0])

    #flip the board to be the other person
    moveBoard.flipPlayer()  
    return moveBoard   

def InplaceMoveBack(board, move):
    #if the action was a movement move, undo the movement
    if(move[0] != None):
        #flip it back to this current person
        board.flipPlayer()  
        board.update_board(move[2], move[1], move[0])


#Blows up all neighbouring pieces that are next to an enemy
#This is an approximation to a Quiescence Search and causes 
#the board to be in a stablier state
def BlowUp(board: Board, isMax:bool):    

    moveBoard = board.copy()
    moves = blowUps(moveBoard)
    #blow up all pieces next to enemies
    while(len(moves) > 0):
        move = moves[0]
        moveBoard.update_board(move[1],move[2], move[0])
        moves = blowUps(moveBoard)
    
    
    #if min then flip so we rank the board
    #relative to max
    if(not isMax):
        moveBoard.flipPlayer()

    bestRes = rankBoard(moveBoard)
    return bestRes
    



#The top of the Min Max search that returns a list of moves
#in order of which is the best and their relative score found
def MinMax0(board: Board, depth, isMax:bool, minRes, maxRes, cutoff):
    if(depth > cutoff):
        return (BlowUp(board, isMax), None)


    moves = bestMoves(board)

    rankedMoves = []
    for move in moves:

        moveBoard = InplaceMove(board, move)

        #recurse to find resulting score of this move
        (res, _) = MinMax(moveBoard, depth+1, not isMax, minRes, maxRes, cutoff)
        
        InplaceMoveBack(moveBoard, move)


        if(isMax and res > minRes):
            #if i am max, then always grab the best res as the min
            minRes = res

        if(not isMax and res < maxRes):
            #Since i am min, if this res < my maxRes, i will
            #take it as it make my max lower
            maxRes = res

        if(minRes >= maxRes):
            break

        
        rankedMoves.append((res, move))

    #sort by resulting score descending
    rankedMoves.sort(key = lambda x:x[0], reverse = True)
    
    moves = breakTiesWithRankPieceHeuristic(board, rankedMoves)
    return moves




#finds the best move and its resultant score from
#a current board state
def MinMax(board: Board, depth, isMax:bool, minRes, maxRes, cutoff):

    if(depth > cutoff):
        return (BlowUp(board, isMax), None)

    moves = bestMoves(board)

    bestMove = None
    for move in moves:
        moveBoard = InplaceMove(board, move)

        #recurse to find resulting score of this move
        (res, _) = MinMax(moveBoard, depth+1, not isMax, minRes, maxRes, cutoff)
        
        InplaceMoveBack(moveBoard, move)       
     
        if(isMax and res > minRes):
            #if i am max, then always grab the best res as the min
            minRes = res
            bestMove = move


        if(not isMax and res < maxRes):
            #Since i am min, if this res < my maxRes, i will
            #take it as it make my max lower
            maxRes = res
            bestMove = move

        if(minRes >= maxRes):
            break

    
    bestRes = None
    if(isMax):
        bestRes = minRes
    else:
        bestRes = maxRes

    #if no move was performed then just 
    #rank the current board state
    if(bestMove == None):
        bestRes = BlowUp(board, isMax)

    
    return (bestRes, bestMove)


#counts the number of pieces on the board
def numberOfPieces(board: Board):
    count = 0
    for pos in board:
        count += board[pos].numTokens
    return count

#picks a good depth based on how many pieces
#are on the board
def goodCutOff(board: Board):
    num = numberOfPieces(board)
    if(num > 20):
        return 2

    if(num > 15):
        return 2
    
    if(num > 10):
        return 3
    
    if(num > 8):
        return 4
    
    if(num > 5):
        return 4
    return 5



#a wrapper to make it easier to call the AI
def determineMove(board):
    return MinMax0(board, 0, True, -math.inf, math.inf, goodCutOff(board))
    


def determineMoveRes(board):
    return MinMax0(board, 0, True, -math.inf, math.inf, 2)


