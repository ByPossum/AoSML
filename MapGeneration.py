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
        self.startDir = ()
        self.startPos = self.SetStart()
        self.endPos = self.SetEnd()
        self.allMoves = self.InitializeMovement()
        self.iterations = 0
        self.PlaceFloor(self.CreateMaze((self.startPos[0] - self.startDir[0], self.startPos[1] - self.startDir[1]),
                                        self.endPos, [], [self.startDir]))
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

    def InitializeMovement(self):
        allMovement = [[LEGAL_MOVES.copy()]*self.width for _ in range(self.height)]
        return allMovement

    def PlaceFloor(self, newMap):
        print(newMap)
        for i in range(0, len(newMap)):
            self.map[newMap[i][0]][newMap[i][1]] = 'f'

    def FindPath(self):
        newMap = None
        while newMap is None:
            pass

    def CreateMaze(self, startPos, endPos, maze, lastMoves):
        # Get current node
        print(self.iterations)
        self.iterations += 1
        currentNode = startPos
        # If there are no moves to be made from this node go back a node
        if len(self.allMoves[currentNode[0]][currentNode[1]]) <= 0:
            lastMove = lastMoves.pop()
            return self.CreateMaze((startPos[0] + lastMove[0], startPos[1] + lastMove[1]), endPos, maze, lastMoves)

        # Get a random direction and move in it
        moveIndex = random.randrange(0, len(LEGAL_MOVES)-1)
        direction = self.allMoves[currentNode[0]][currentNode[1]][moveIndex]
        row = self.allMoves[currentNode[0]][currentNode[1]].copy()
        row.pop(moveIndex)
        self.allMoves[currentNode[0]][currentNode[1]] = row
        nextMove = (currentNode[0] + direction[0], currentNode[1] + direction[1])

        # Check if you can actually move to the new

        if nextMove not in maze and self.TileInMap(nextMove):
            if self.ValidateTile(self.map[nextMove[0]][nextMove[1]]):
                # Add the current node to the list
                maze.append(nextMove)
                lastMoves.append(direction)
                for j in range(len(LEGAL_MOVES)):
                    # If you're at the end return the map
                    endChecker = (nextMove[0] + LEGAL_MOVES[j][0], nextMove[1] + LEGAL_MOVES[j][1])
                    if endChecker == endPos:
                        return maze
                return self.CreateMaze(nextMove, endPos, maze, lastMoves)
        # If you can't traverse to a new node restart
        return self.CreateMaze((currentNode[0], currentNode[1]), endPos, maze, lastMoves)

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
        self.startDir = (0 if zeroPos == 0 else 1, 0 if zeroPos == 0 else 1)
        print("(" + zeroPos.__str__() + "," + extreme.__str__() + ")")
        if extreme:
            self.startDir = (self.startDir[0] * -1, self.startDir[1] * -1)
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
        if _tile == 'w' or _tile == 'p' or _tile == 's' or _tile == 'e':
            return False
        else:
            return True

    def TileInMap(self, _tile):
        if _tile[0] >= 0 and _tile[0] <= self.width-1 and _tile[1] >= 0 and _tile[1] <= self.height-1:
            return True
        return False

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
