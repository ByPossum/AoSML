from MapGeneration import MapCreation

class MapMan:
    def __init__(self):
        self.map = MapCreation(5, 5)


    def GetMap(self):
        return self.map.map

    def BlockAction(self, action, pos):
        if self.GetMap()[pos[0]][pos[1]] == 'w':
            action = self.Knockback()
        elif self.GetMan()[pos[0]][pos[1]] == 'p':
            action += self.FallDownPit()
        return action

    def Knockback(self):
        pass

    def FallDownPit(self):
        print("You fell down a pit!")
        pass
