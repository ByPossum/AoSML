from MapGeneration import MapCreation
from PlayerActions import PlayerAction

class MapMan:
    def __init__(self):
        self.map = MapCreation(20, 20)


    def GetMap(self):
        return self.map.map

    def GetStartPos(self):
        return self.map.GetStartPos()

    def CheckNextBlock(self, pos):
        mapChar = self.map.map[pos[0]][pos[1]]
        if mapChar == 'f':
            return PlayerAction.move
        if mapChar == 'w' or mapChar == 's':
            print("Hit a wall")
            return PlayerAction.none
        if mapChar == 'p':
            print("Hit a pit")
            return PlayerAction.pit
