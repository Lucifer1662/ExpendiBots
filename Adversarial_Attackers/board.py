
from Adversarial_Attackers.tile import Tile
from Adversarial_Attackers.util import print_board

class Board:
    def __init__(self, data, myColour="white", tiles = None):
        self.myColour = myColour
        self.tiles = {}
        if(tiles!=None):
            self.tiles = tiles
        if(data != None):
            for key in data:
                for i, info in enumerate(data[key]):
                    self.tiles[(data[key][i][1], data[key][i][2])] = Tile(key == myColour, data[key][i][0])

    def at(self, pos: tuple) -> Tile:
        return self.tiles[pos]

    def __getitem__(self, key) -> Tile:
        return self.tiles.__getitem__(key)
    
    def new_tile_at(self, pos:tuple, tile: Tile):
        self.tiles[pos] = tile
    
    def make_blank(self, pos) -> Tile:
        self.tiles.pop(pos)
        
    def __contains__(self, key):
        return key in self.tiles
    
    def __iter__(self) -> tuple:
        return self.tiles.__iter__()

    def copy(self):
        tiles = {}
        for pos in self.tiles:
            tiles[pos] = self.tiles[pos].copy()

        return Board(None, self.myColour, tiles)
    
    def move_tokens_from_to(self, source, destination, numTokens):
        if(destination in self):
            self.at(destination).numTokens += numTokens
        else:
            self.new_tile_at(destination, Tile(self.at(source).isMyToken, numTokens))

        if(self.at(source).numTokens - numTokens == 0):
            self.make_blank(source)
        else:
            self.at(source).numTokens -= numTokens

    def recurse_explosion(self, pos, tiles):
        tiles.append(pos)
        for x in range(-1,2):
            for y in range(-1,2):
                neighborPos = (pos[0]+x,pos[1]+y)
                if(neighborPos in self and not neighborPos in tiles):
                    self.recurse_explosion(neighborPos, tiles)
        
    def update_explosion(self, pos):
        tiles = []
        self.recurse_explosion(pos, tiles)
        for tile in tiles:
            self.make_blank(tile)

    def update_board(self, source: tuple, destination: tuple, numTokens: int):
        if(numTokens != None):
            self.move_tokens_from_to(source, destination, numTokens)
        else:
            self.update_explosion(source)
        return self

    def amountOfTokensAtDestination(self, move):
        num = move[0]
        if(move[2] in self):
            num += self[move[2]].numTokens
        return num

    def no_enemies(self):
        for pos in self.tiles:
            if(self.at(pos).is_enemy()):
                return False
        return True

    def no_my_tokens(self):
        for pos in self.tiles:
            if(not self.at(pos).is_enemy()):
                return False
        return True
    
    def is_enemy(self, pos):
        return pos in self.tiles and self.at(pos).is_enemy()
    
    def is_my_token(self, pos):
        return pos in self.tiles and self.at(pos).isMyToken

    def can_move_here(self, pos):
        return not pos in self.tiles or self.is_my_token(pos)
                   
    def nearby_enemy(self, pos):
        for x in range(-1,2):
            for y in range(-1,2):
                neighborPos = (pos[0]+x,pos[1]+y)
                if(self.is_enemy(neighborPos)):
                    return True

    def to_tuple_at(self, pos):
        if(pos in self.tiles):
            return tuple([self.at(pos).to_tuple()])
        return tuple([tuple([None])])

    #turns the board state into a string so
    #it can easily be hashed
    def to_hashable(self):
        string = ""
        for y in range(0,8):
            for x in range(0,8):
                pos = self.to_tuple_at((x,y))[0]
                if(pos == tuple([None])):
                    string += chr(0)
                else:
                    (isMine, num) = pos
                    if(isMine):
                        string += chr(num)
                    else:
                        string += chr(12+num)
        return string

    def print(self):
        print_board(self.tiles)
    
    def update(self, move):
        self.update_board(move[1],move[2], move[0])


    def flipPlayer(self):
        if(self.myColour == "white"):
            self.myColour = "black"
        else:
            self.myColour = "white"

        for pos in self:
            self[pos].flipPlayer()
    
