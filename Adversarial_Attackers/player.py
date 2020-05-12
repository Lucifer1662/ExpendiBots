from Adversarial_Attackers.board import Board
from Adversarial_Attackers.AI import determineMove
import json
import math
import random
import numpy as np

_BLACK_START_SQUARES = [(1,0,7), (1,1,7),   (1,3,7), (1,4,7),   (1,6,7), (1,7,7),
                        (1,0,6), (1,1,6),   (1,3,6), (1,4,6),   (1,6,6), (1,7,6)]
_WHITE_START_SQUARES = [(1,0,1), (1,1,1),   (1,3,1), (1,4,1),   (1,6,1), (1,7,1),
                        (1,0,0), (1,1,0),   (1,3,0), (1,4,0),   (1,6,0), (1,7,0)]



class MainPlayer:
    def __init__(self, colour):
        board = {"white":_WHITE_START_SQUARES, "black":_BLACK_START_SQUARES}
        self.board = Board(board, colour)
        self.colour = colour  
        self.visted = {}


    def action(self):
        bhash = self.board.to_hashable()
        #if previously visiten chosen the second action to avoid
        #repeated states
        if(bhash in self.visted):
            actions = self.visted[bhash]
            if(len(actions) > 1):
                action = actions[1][1]
            else:
                action = actions[0][1]
        
        #else use AI to determine Move
        else:
            actions = determineMove(self.board.copy())
            action = actions[0][1]
            self.visted[bhash] = actions

        if(action == None):
            return ("BOOM", ())
        if(action[0] == None):
            return ("BOOM", (action[1]))
        else:
            return ("MOVE",action[0],action[1],action[2])


    def update(self, colour, action):
        if(action[0] == "BOOM"):
            self.board.update_board(action[1], None, None)
        else:
            self.board.update_board(action[2], action[3], action[1])

