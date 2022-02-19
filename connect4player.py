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
                #Last try
                new_value = self.value
                new_value -= self._all_quartets(col,j)
                new_value += self._all_quartets(col,j,new_rack)
                return ComputerPlayer.State(new_rack, (self.id%2)+1,new_value)
            return None

        def evaluate_rack(self):
            width = len(self.rack)
            height = len(self.rack[0])
            #Explore +3 in 4 non-opposite directions from each source (if possible).
            return sum([self._explore(i,j) for i in range(width) for j in range(height)])

        def _quartet(self,i,j,x,y,rack=None):
            if rack is None:
                rack = self.rack
            left = 3 if x == -1 else 0
            right = len(rack) - 3 if x == 1 else len(rack)
            bottom = 3 if y == -1 else 0
            top = len(rack[0]) - 3 if y == 1 else len(rack[0])
            if i < left or i >= right or j < bottom or j >= top:
                return 0
            id = 0
            count = 0
            for k in range(4):
                token = rack[i + x*k][j + y*k]
                if id == 0:
                    id = token
                if token != 0: 
                    if id != token:
                        return 0
                    else:
                        count += 1
            if count == 0:
                return 0 
            multiplier = 1 if id == 1 else -1
            if count < 4:
                value = 10 ** (count-1)
                return multiplier*value
            else:
                return multiplier*float("inf")

        def _all_quartets(self,i,j,rack=None):
            directions = [(x,y) for x in (-1,0,1) for y in (-1,0,1) if x != 0 or y != 0]
            out = 0
            for direction in directions:
                x = direction[0]
                y = direction[1]
                out += self._quartet(i,j,x,y,rack)
                out += self._quartet(i-x,j-y,x,y,rack)
            return out
                
        def _explore(self,i, j):
            out = 0
            for direction in [(-1,1),(0,1),(1,1),(1,0)]:
                x = direction[0]
                y = direction[1]
                out += self._quartet(i,j,x,y)
            return out