"""
This Connect Four player just picks a random spot to play. It's pretty dumb.
"""
__author__ = "Tristan Gaeta" 

class ComputerPlayer:
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.id = id
        self.difficulty_level = difficulty_level

    def pick_move(self, rack):
        state = ComputerPlayer.State(rack,self.id)
        ans = self.minimax(state,self.difficulty_level)
        return ans["src"]

    def minimax(self, state, plies):
        if plies == 0 or state.value == float("inf") or state.value == float("-inf"):
            if self.id != 1:
                state.value *= -1
            return {"val":state.value,"depth":self.difficulty_level-plies}
        
        best = {"val":float("-inf"),"depth":float("inf")}
        sign = 1 if self.id == state.id else -1
        for col in range(state.width):
            child = state.make_move(col)
            if child is not None:
                minimax_substate = self.minimax(child,plies-1)
                minimax_val = minimax_substate["val"] * sign
                if (minimax_val >= best["val"]):
                    if minimax_val == best["val"] and minimax_substate["depth"] > best["depth"]:
                        continue
                    best = {"val":minimax_val,"src":col,"depth":minimax_substate["depth"]}      
        best["val"] *= sign
        return best
        

    class State:
        def __init__(self, rack, id, value=None):
            self.width = len(rack)
            self.height = len(rack[0])
            self.rack = rack
            self.id = id
            self.value = self.evaluate_rack() if value is None else value

        def make_move(self, col):
            if 0 <= col < self.width and self.rack[col][self.height-1] == 0:
                j = self.rack[col].index(0)
                #Create new rack
                new_rack = [tuple(col[:]) for col in self.rack]
                new_col = list(new_rack[col][:])
                new_col[j] = self.id
                new_rack[col] = tuple(new_col)
                new_rack = tuple(new_rack)
                #determine value
                new_value = self.value
                new_value -= self._explore(col,j,True)
                new_value += self._explore(col,j,True,new_rack)
                return ComputerPlayer.State(new_rack, (self.id%2)+1,new_value)
            return None

        def evaluate_rack(self):
            width = len(self.rack)
            height = len(self.rack[0])
            #Explore +3 in 4 non-opposite directions from source (if possible).
            return  sum([self._explore(i,j) for i in range(width) for j in range(height)])
                
        def _explore(self, i, j, bi_directional=False, rack=None):   
            if rack is None:
                rack = self.rack
            width = len(rack)
            height = len(rack[0])
            value = 0
            multipliers = [-1,1] if bi_directional else [1]
            for direction in [(-1,1),(0,1),(1,1),(1,0)]:
                for multiplier in multipliers:
                    x = direction[0] * multiplier
                    y = direction[1] * multiplier
                    #Check if valid quatret
                    if (0 <= j + y*3 < height) and (0 <= i + x*3 < width):
                        p1_tokens = 0
                        p2_tokens = 0
                        #Count tokens in quartet
                        for k in range(4):
                            token = rack[i + x*k][j + y*k]
                            if token == 1:
                                p1_tokens += 1
                            elif token == 2:
                                p2_tokens += 1
                        if p1_tokens != 0 and p2_tokens != 0:
                            continue    #No value
                        elif p1_tokens != 0:
                            if p1_tokens < 4:
                                value += 10 ** (p1_tokens-1)
                            else:
                                return float("inf")
                        elif p2_tokens != 0:
                            if p2_tokens < 4:
                                value -= 10 ** (p2_tokens-1)
                            else:
                                return float("-inf")
            return value