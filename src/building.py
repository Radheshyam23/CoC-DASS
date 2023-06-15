'''
A general class for the different buildings and defences
'''

from src import GlobalVariables
from src.GameMap import GameMap
import copy
from time import time

class Building:

    # Class variables:
    NumWalls = 0
    NumHuts = 0
    NumCannons = 0
    NumWizards = 0

    TotCount = 0

    def __init__(self, TopLeft, BotRight, symbol, hitpoints, Type):
        self.TopLeft = TopLeft      # A tuple (x,y) having coordinates of top-left cell of the building
        self.BotRight = BotRight    # A tuple (x,y) having bottom-right coordinates
        self.Symbol = symbol
        self.Health = hitpoints     # Current health
        self.Hitpoints = hitpoints  # Max health
        self.Type = Type
        # self.Label = Label
        self.ForeColour = "YELLOW"
        self.BackColour = "BLACK"
        self.Alive = True

    # Some Getter functions 
    def RetTopLeft(self):
        return self.TopLeft
    
    def RetBotRight(self):
        return self.BotRight

    def RetSymbol(self):
        return self.symbol
    
    def RetColour(self):
        return self.colour

    def RetType(self):
        return self.Type

    def ReduceHealth(self, reduction, cocMap):
        self.Health -= reduction

        if self.Health <= 0:
            self.Health = 0
            
            if self.Type != 'Wall':
                Building.TotCount -= 1
            
            GameMap.RemoveBuilding(cocMap, self.TopLeft, self.BotRight)
            self.ForeColour = "GREEN"
            self.BackColour = "GREEN"
            self.Alive = False

        elif self.Health/float(self.Hitpoints) <= 0.3:
            self.BackColour = "RED"
            self.ForeColour = "YELLOW" 
        elif self.Health/float(self.Hitpoints) <= 0.6:
            self.BackColour = "YELLOW"
            self.ForeColour = "BLACK"

class Wall(Building):
    def __init__(self, Coordinate,cocMap):
        WallSymbol = '<'
        WallHitpoints = 250
        Type = "Wall"
        # Label = "W"+str(Building.NumWalls)
        Building.NumWalls += 1
        super().__init__(Coordinate, Coordinate, WallSymbol, WallHitpoints, Type)
        GameMap.AddBuildings(cocMap, self)

        # ColourCode["W"].append([WallColour,WallBackColour])


class Hut(Building):
    def __init__(self, TopLeft, BotRight, cocMap):
        HutSymbol = 'H'
        HutHitpoints = 150
        Type = "Hut"
        # Label = "H"+str(Building.NumHuts)
        Building.NumHuts += 1
        super().__init__(TopLeft, BotRight, HutSymbol, HutHitpoints, Type)
        GameMap.AddBuildings(cocMap, self)

        Building.TotCount += 1
        # ColourCode["H"].append([HutColour,HutBackColour])

class TownHall(Building):
    def __init__(self, TopLeft, BotRight, cocMap):
        TownSymbol = 'T'
        TownHitpoints = 700
        Type = "Town"
        # Label = "T"
        super().__init__(TopLeft, BotRight, TownSymbol, TownHitpoints, Type)
        GameMap.AddBuildings(cocMap, self)

        Building.TotCount += 1
        # ColourCode["T"] = [TownColour, TownBackColour]

class Cannon(Building):
    def __init__(self, TopLeft, BotRight, cocMap):
        CannonSymbol = '%'
        CannonHitpoints = 500
        self.CannonDamage = 100 # Damage caused per shot of the cannon
        self.CannonCoolDown = 1 # interval of 0.5s per shot

        self.CannonPrevTime = time()

        self.Target = ""    # It will be a troop object

        Type = "Cannon"
        # Label = "C"+str(Building.NumCannons)
        Building.NumCannons += 1
        super().__init__(TopLeft, BotRight, CannonSymbol, CannonHitpoints, Type)
        GameMap.AddBuildings(cocMap, self)

        Building.TotCount += 1
        # ColourCode["C"].append([CannonColour,CannonBackColour])

    def InCannonRange(self, targetCoord):
        CannonTopLeft = self.TopLeft
        CannonBotright = self.BotRight
        CannonTopRight = (CannonTopLeft[0],CannonTopLeft[1]+1)
        CannonBotLeft = (CannonBotright[0],CannonBotright[1]-1)

        if min(GlobalVariables.CalcDist(CannonTopLeft,targetCoord), GlobalVariables.CalcDist(CannonTopRight,targetCoord), GlobalVariables.CalcDist(CannonBotright,targetCoord), GlobalVariables.CalcDist(CannonBotLeft,targetCoord)) <= GlobalVariables.CannonRange:
            return True
        else:
            return False

    def FindTarget(self, Troops):
        for troop in Troops:
            if self.InCannonRange(troop.Coordinate) and troop.Alive:
                self.Target = troop
                return troop
        self.Target = ""
        return ""

    def AttackTarget(self, Target, cocMap):
        Target.ReduceTroopHealth(self.CannonDamage, cocMap)


class WizardTower(Building):
    def __init__(self, TopLeft, BotRight, cocMap):
        WizardSymbol = '^'
        WizardHitpoints = 500
        self.WizardDamage = 100 # Damage caused per shot of the cannon
        self.WizardCoolDown = 1 # interval of 0.5s per shot

        self.WizardPrevTime = time()

        self.Target = ""    # It will be a troop object

        Type = "Wizard"
        Building.NumWizards += 1
        super().__init__(TopLeft, BotRight, WizardSymbol, WizardHitpoints, Type)
        GameMap.AddBuildings(cocMap, self)

        Building.TotCount += 1

    def InWizardRange(self, targetCoord):
        WizardTopLeft = self.TopLeft
        WizardBotright = self.BotRight
        WizardTopRight = (WizardTopLeft[0],WizardTopLeft[1]+1)
        WizardBotLeft = (WizardBotright[0],WizardBotright[1]-1)

        if min(GlobalVariables.CalcDist(WizardTopLeft,targetCoord), GlobalVariables.CalcDist(WizardTopRight,targetCoord), GlobalVariables.CalcDist(WizardBotright,targetCoord), GlobalVariables.CalcDist(WizardBotLeft,targetCoord)) <= GlobalVariables.WizardRange:
            return True
        else:
            return False

    def FindTarget(self, Troops):
        for troop in Troops:
            if self.InWizardRange(troop.Coordinate) and troop.Alive:
                self.Target = troop
                return troop
        self.Target = ""
        return ""

    def AreaAttackTarget(self, Target, cocMap, AllTroops):
        Range = GlobalVariables.WizardArea
        CentreCoords = Target.Coordinate

        TopLeft = copy.deepcopy(CentreCoords)
        TopLeft[0] -= int(Range/2)
        TopLeft[1] -= int(Range/2) 

        BotRight = copy.deepcopy(CentreCoords)
        BotRight[0] += int(Range/2)
        BotRight[1] += int(Range/2)
        
        if TopLeft[0] < 0:
            TopLeft[0] = 0
        if TopLeft[1] < 0:
            TopLeft[1] = 0
        if BotRight[0] >= GlobalVariables.MapNumRows:
            BotRight[0] = GlobalVariables.MapNumRows-1
        if BotRight[1] >= GlobalVariables.MapNumColumns:
            BotRight[1] = GlobalVariables.MapNumColumns-1

        for i in range(TopLeft[0],BotRight[0]+1):
            for j in range(TopLeft[1],BotRight[1]+1):
                if cocMap.GameMap[i][j][1] in AllTroops and cocMap.GameMap[i][j][1].Alive:
                    cocMap.GameMap[i][j][1].ReduceTroopHealth(self.WizardDamage, cocMap)