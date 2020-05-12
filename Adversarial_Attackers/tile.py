

class Tile:
    def __init__(self, isMyToken, numTokens):
        self.isMyToken = isMyToken
        self.numTokens = numTokens
    
    def is_enemy(self):
        return not self.isMyToken
    
    def to_tuple(self):
        return (self.isMyToken, self.numTokens)
        
    def __str__(self):
        if(self.isMyToken):
            return 'w ' + self.numTokens.__str__()
        else:
            return 'b ' + self.numTokens.__str__()
    
    def copy(self):
        return Tile(self.isMyToken, self.numTokens)

    def flipPlayer(self):
        self.isMyToken = not self.isMyToken