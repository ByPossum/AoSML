from MapGeneration import MapCreation
from PlayerActions import PlayerAction
import copy
class MapMan:
    def __init__(self):
        self.map = MapCreation(20, 20)


    def GetMap(self):
        return self.map.map

    def GetMapButMakeItNumbersWithPlayer(self, playerPos):
        trainingMap = copy.deepcopy(self.map.map)
        for i in range(self.map.width):
            for j in range(self.map.height):
                if trainingMap[i][j] == 'f':
                    trainingMap[i][j] = 0
                elif trainingMap[i][j] == 'w':
                    trainingMap[i][j] = 1
                elif trainingMap[i][j] == 'p':
                    trainingMap[i][j] = 2
                elif trainingMap[i][j] == 's':
                    trainingMap[i][j] = 3
                elif trainingMap[i][j] == 'e':
                    trainingMap[i][j] = 5
        trainingMap[playerPos[0]][playerPos[1]] = 4
        return trainingMap

    def GetStartPos(self):
        return self.map.GetStartPos()

    def CheckNextBlock(self, pos):
        mapChar = self.map.map[pos[0]][pos[1]]
        if mapChar == 'f':
            return PlayerAction.move
        if mapChar == 'w' or mapChar == 's':
            return PlayerAction.none
        if mapChar == 'p':
            return PlayerAction.pit

    def CheckCurrentBlock(self, pos):
        mapChar = self.map.map[pos[0],pos[1]]
        if mapChar == 'e':
            return True
        return False
