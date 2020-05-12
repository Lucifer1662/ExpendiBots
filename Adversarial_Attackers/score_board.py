from Adversarial_Attackers.board import Board
from Adversarial_Attackers.path_finding import possible_moves
import numpy as np
from scipy.ndimage import gaussian_filter

#returns a list of the current players pieces
def myPieces(board: Board):
    pieces = []
    for pos in board:
        if(board[pos].isMyToken):
            pieces.append(pos)
    return pieces


#If there is a tie in score then rank them using heuristic
#for ordering
def breakTiesWithRankPieceHeuristic(board: Board, moves):
    bmap = createbmap(board)
    topSame = []
    notTop = []
    topRes = moves[0][0]
    for (res, move) in moves:
        if(topRes == res):
            if(move[0]==None):
                newres = scoreBlowUp(board, move[1])
            else:
                newres = rankPiece(board.amountOfTokensAtDestination(move), move[2], bmap)
            
            topSame.append(((res, move), newres))
        else:
            notTop.append((res,move))
    
    topSame.sort(key=lambda x: x[1], reverse = True)
    result = []
    for move in topSame:
        result.append(move[0])
    
    result.extend(notTop)
    return result

#orders the moves base on scoreBlowUp and rank piece
def bestMoves(board: Board):
    bmap = createbmap(board)
    pieces = myPieces(board)
    moves = []
    for pos in pieces:
        if(board.nearby_enemy(pos)):
            moves.append((scoreBlowUp(board, pos), (None, pos, None)))

        for move in possible_moves(board[pos].numTokens, pos, board):
            res = rankPiece(board.amountOfTokensAtDestination(move), move[2], bmap)
            moves.append((res, move))
    
    moves.sort(key=lambda x:x[0], reverse=True)
    m = []
    for move in moves:
        m.append(move[1])
    return m



#returns a list of moves where the 
#player can blow up and enemy
def blowUps(board: Board):
    pieces = myPieces(board)
    moves = []
    for pos in pieces:
        if(board.nearby_enemy(pos)):
               moves.append((None, pos, None))
    return moves

def create_islands(board:Board):
    """
    Input  Board

    Output: A dictionary of islands with the key being an integer representing the island id
            and the value being a list of tuples, representing the pieces in that island.

            Example: {0: [(3, 5)], 1: [(4, 3)], 2: [(0, 7)], 3: [(4, 1)], 4: [(6, 2), (7, 3)]}
            means there are 5 islands, and island 4 has two pieces in it: (6, 2) and (7, 3)
    """
    islands = {}
    island_no = 0
    for pos in board:
        if not pos in islands:
            recurseIslands(island_no, pos, board, islands)
            island_no += 1

    ret_islands = {}
    for pos in islands:
        if islands[pos] not in ret_islands:
            ret_islands[islands[pos]] = [pos]
        else:
            ret_islands[islands[pos]].append(pos)
    return ret_islands

def recurseIslands(id, pos, board, islands):
    islands[pos] = id
    for x in range(-1,2):
        for y in range(-1,2):
            neighborPos = (pos[0]+x,pos[1]+y)
            if(neighborPos in board and not neighborPos in islands):
                recurseIslands(id, neighborPos, board, islands)


#creates a blow up mape for the board using islands
def blowUpMap(board:Board, isMyToken, islands):
    blowUpMap = np.zeros((8,8), dtype=float)

    for id in islands:
        l = 0
        for pos in islands[id]:
            if(board[pos].isMyToken != isMyToken):
                l += board[pos].numTokens

        for pos in islands[id]:
            if(board[pos].isMyToken != isMyToken):
                blowUpMap[pos[0]][pos[1]] = l

    return blowUpMap




#calculate
#(number friend + 1)/(number enemy + 1)
#and if can see win/draw/lose return very big/small number
def enemiesVsPlayerHeuristic(board: Board):
    white = 1
    black = 1
    for pos in board.tiles:
        if(board[pos].is_enemy()):
            black = black + board[pos].numTokens
        else:
            white = white + board[pos].numTokens

    if(black == 1 and white != 1):
        return 10000000
    if(white == 1 and black != 1):
        return -10000000
    if(white == 1 and black == 1):
        return 0
    return white/black


#ranks the move based on how effectily the blow up
#increase the score
def scoreBlowUp(board: Board, pos):
    board = board.copy()
    before = enemiesVsPlayerHeuristic(board)
    board.update_explosion(pos)
    after = enemiesVsPlayerHeuristic(board)
    #times 100 to ensure it is above movement moves
    return (after-before)*100




def createbmap(board: Board):
    islands = create_islands(board)
    bmap = blowUpMap(board, True, islands)
    zeros = np.zeros((8,8))
    bmap = np.maximum(zeros, bmap)
    return bmap


bluredCache = {}
def resetBluredCache():
    global bluredCache
    bluredCache = {}

def rankPiece(numTokens, pos, bmap):
    global bluredCache
    key = (numTokens, pos)
    if(not key in bluredCache):
        moveMap = np.zeros((8,8))
        moveMap[pos[0]][pos[1]] = numTokens
        blured = gaussian_filter(moveMap, sigma = numTokens, mode="constant", cval=0)
        bluredCache[key] = blured
    else:
        blured = bluredCache[key]

    return np.sum(np.multiply(blured, bmap))

#assigns a number for the board that represent
#how benefitial its current state is
def rankBoard(board: Board):
    score = enemiesVsPlayerHeuristic(board)*1000  
    return score
   
