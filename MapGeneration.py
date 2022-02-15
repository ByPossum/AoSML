import random
import sys

LEGAL_MOVES = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]

class MapCreation:
    def __init__(self, startWidth, startHeight):
        sys.setrecursionlimit(1600)
        self.recursionCounter = 0
        self.width = startWidth
        self.height = startHeight
        self.fillArr = ['f', 'w', 'p']
        self.map = self.InitializeMap()
        self.SurroundMapInWall()
        self.startPos = self.SetStart()
        self.endPos = self.SetEnd()
        self.closedSet = []
        self.openSet = []
        self.PlaceFloor(self.random_walk(self.startPos))
        self.DebugMap()
        #self.DebugMap()
        #self.FillMap()
        #self.DebugMap()

    def GetMap(self):
        return self.map

    def InitializeMap(self):
        newMap = []
        for x in range(self.height):
            newMap.append(['n']*self.width)
        return newMap

    def PlaceFloor(self, newMap):
        for x in range(0, self.width):
            for y in range(0, self.height):
                if len(newMap[x * self.height + y]) == 1:
                    direction = newMap[x * self.height + y][0]
                    chosen_pos = x + direction[0], y + direction[1]
                    self.map[chosen_pos[0]][chosen_pos[1]] = 'f'

    def FindPath(self):
        newMap = None
        while newMap is None:
            pass

    def Backtrack(self, _start, _end):
        # Found the path
        if _start[0] == _end:
            return self.openSet
        else:
            # If something is a wall or a pit, it's not a valid tile
            _closedSet = []
            if _start[1] is None:
                _closedSet = self.GetValidTiles(_start[0])
            else:
                _closedSet = _start[1]
            if len(_closedSet) > 0:
                nodeToExplore = _closedSet[random.randrange(0, len(_closedSet), 1)]
                _closedSet.remove(nodeToExplore)
                if len(self.openSet) > 0:
                    self.openSet[len(self.openSet)-1] = (_start[0], _closedSet)
                # Proceeds to the next node
                self.openSet.append((nodeToExplore, None))
                self.Backtrack((self.openSet[len(self.openSet)-1]), _end)
            else:
                # Return to the last explored node.
                self.openSet.pop()
                self.Backtrack(self.openSet[len(self.openSet)-1], _end)

    def fill_grid(self, sx, sy):
        legal_grid = []
        for i in range(0, sx*sy):
            legal_grid.append( LEGAL_MOVES )
        return legal_grid

    def random_walk(self, curr):
        legal_grid = self.fill_grid(self.width, self.height)
        self.func_recursive(curr, legal_grid)
        return legal_grid

    def func_recursive(self, curr, legal_grid):
        moves = random.sample(LEGAL_MOVES, len(LEGAL_MOVES))
        for move in moves:
            new = curr[0] + move[0], curr[1] + move[1]

            if self.is_legal_move(new) and len(legal_grid[new[0] * self.height + new[1]]) == 4:
                legal_grid[curr[0] * self.height + curr[1]] = [move]
                legal_grid[new[0] * self.height + new[1]] = [ (move[0] * -1, move[1] * -1) ]
                self.func_recursive(new, legal_grid)

    def is_legal_move(self, curr):
        if 0 <= curr[0] < self.width:
            if 0 <= curr[1] < self.height:
                #return False
                return self.map[curr[0]][curr[1]] in ('n', 's', 'e')
        return False

    def IsInOpenSet(self, _currentPos):
        for i in self.openSet:
            if i[0] == _currentPos:
                return True
        return False

    def GetValidTiles(self, _currentPos):
        newSet = []

        if _currentPos[0] + 1 < self.width:
            rightPos = (_currentPos[0]+1, _currentPos[1])
            if self.ValidateTile(self.map[rightPos[0]][rightPos[1]]) and not self.IsInOpenSet(rightPos):
                newSet.append((_currentPos[0] + 1, _currentPos[1]))
        if _currentPos[0] - 1 > 0:
            leftPos = (_currentPos[0]-1, _currentPos[1])
            if self.ValidateTile(self.map[leftPos[0]][leftPos[1]]) and not self.IsInOpenSet(leftPos):
                newSet.append((_currentPos[0] - 1, _currentPos[1]))
        if _currentPos[1] + 1 < self.height:
            upPos = (_currentPos[0], _currentPos[1]+1)
            if self.ValidateTile(self.map[upPos[0]][upPos[1]]) and not self.IsInOpenSet(upPos):
                newSet.append((_currentPos[0], _currentPos[1] + 1))
        if _currentPos[1] - 1 > 0:
            downPos = (_currentPos[0],_currentPos[1]-1)
            if self.ValidateTile(self.map[downPos[0]][downPos[1]]) and not self.IsInOpenSet(downPos):
                newSet.append((_currentPos[0], _currentPos[1]))
        return newSet

    def SurroundMapInWall(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height-1:
                    self.map[x][y] = 'w'


    def DoSomeCoinFlips(self):
        # Essentially coin flip
        zeroPos = random.getrandbits(1)
        extreme = random.getrandbits(1)
        return zeroPos, extreme

    def GetPositionAlongWall(self, zeroPos, extreme):
        # X or Y has to be at position 0 and the opposite has to be accessible to the player
        # (between 1 and 1 less than maximum) I.E. not in the corner
        if zeroPos == 0:
            x = 0 if extreme == 0 else self.width - 1
            y = random.randrange(1, self.height - 2, 1)
        elif zeroPos == 1:
            x = random.randrange(1, self.width - 2, 1)
            y = 0 if extreme == 0 else self.height - 1
        return x, y

    def SetStart(self):
        zeroPos, extreme = self.DoSomeCoinFlips()
        x, y = self.GetPositionAlongWall(zeroPos, extreme)
        self.map[x][y] = 's'
        return x, y

    def SetEnd(self):
        zeroPos, extreme = self.DoSomeCoinFlips()
        x, y = self.GetPositionAlongWall(zeroPos, extreme)
        if x == self.startPos[0] or y == self.startPos[1]:
            return self.SetEnd()
        self.map[x][y] = 'e'
        return x, y

    def ValidateTile(self, _tile):
        if _tile == 'w' or _tile == 'p':
            return False
        else:
            return True

    def FillMap(self):
        for x in range(0, len(self.map)):
            for y in range (0, len(self.map[x])):
                if self.map[x][y] == 'n':
                    self.map[x][y] = self.fillArr[random.randrange(0, len(self.fillArr))-1]

    def DebugMap(self):
        textMap = ""
        for x in range(self.width):
            for y in range(self.height):
                textMap += self.map[x][y]
            print(textMap)
            textMap = ""
        print("")
