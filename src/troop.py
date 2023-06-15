from src.GameMap import GameMap
from src import GlobalVariables
import copy
from src.building import Wall, Hut, TownHall, Building, Cannon
from time import time

class UserTroops:
    def __init__(self, Damage, Health, Speed, Coordinate, Symbol, Type):
        self.Damage = Damage
        self.Health = Health
        self.Hitpoints = Health         # The max health
        self.Speed = Speed
        self.Coordinate = Coordinate
        self.Symbol = Symbol
        self.Type = Type
        self.PrevDir = 'D'
        self.Alive = True
        self.PrevMoveTime = time()       # Contains the time when it moved/attacked last. Initialised with the time when it was spawned.
        self.ForeColour = "YELLOW"
        self.BackColour = "BLUE"

    def ReduceTroopHealth(self, reduction, cocMap):
        self.Health -= reduction

        if self.Health <= 0:
            self.Health = 0
            self.Alive = False
            GameMap.KillTroop(cocMap, self.Coordinate)
            self.ForeColour = "GREEN"
            self.BackColour = "GREEN"

        elif self.Health/float(self.Hitpoints) <= 0.3:
            self.BackColour = "RED"
            self.ForeColour = "BLUE" 
        elif self.Health/float(self.Hitpoints) <= 0.6:
            self.BackColour = "YELLOW"
            self.ForeColour = "BLUE"

class King(UserTroops):
    def __init__(self,cocMap):
        Damage = 100
        Health = 1000
        Speed = 0.2
        Coordinate = [14,1]
        Symbol = 'K'
        Type = 'King'
        super().__init__(Damage, Health, Speed, Coordinate, Symbol, Type)
        GameMap.InitialiseTroop(cocMap,self)

    def setPrev(self, dir):
        self.PrevDir = dir

    def getPrev(self):
        return self.PrevDir

    # Currently, moves only to empty spot. Doesn't move to another troop spot. Need to check for building instead of grass.
    def Move(self, inp, cocMap):
        oldKingCoords = copy.deepcopy(self.Coordinate)
        if inp == 'A' or inp == 'a':
            if self.Coordinate[1] != 1 and GameMap.isGrass(cocMap,self.Coordinate[0], self.Coordinate[1]-1):
                self.Coordinate[1] -= 1
        elif inp == 'W' or inp == 'w':
            if self.Coordinate[0] != 1 and GameMap.isGrass(cocMap,self.Coordinate[0]-1, self.Coordinate[1]):
                self.Coordinate[0] -= 1
        elif inp == 'D' or inp == 'd':
            if self.Coordinate[1] != GlobalVariables.MapNumColumns-2 and GameMap.isGrass(cocMap,self.Coordinate[0], self.Coordinate[1]+1):
                self.Coordinate[1] += 1
        elif inp == 'S' or inp == 's':
            if self.Coordinate[0] != GlobalVariables.MapNumRows-2 and GameMap.isGrass(cocMap,self.Coordinate[0]+1, self.Coordinate[1]):
                self.Coordinate[0] += 1

        GameMap.UpdateTroopPosition(cocMap, oldKingCoords, self.Coordinate, self)
        self.setPrev(inp)

    
    def Attack(self, cocMap):
        attackDir = self.getPrev()
        AttackCoords = copy.deepcopy(self.Coordinate)

        if(attackDir == 'a' or attackDir == 'A'):
            AttackCoords[1] -= 1
        elif (attackDir == 's' or attackDir == 'S'):
            AttackCoords[0] += 1
        elif (attackDir == 'd' or attackDir == 'D'):
            AttackCoords[1] += 1
        elif (attackDir == 'w' or attackDir == 'W'):
            AttackCoords[0] -= 1

        # EntityType = GameMap.GelLabel(cocMap,AttackCoords)
        AttackedBuilding = cocMap.GameMap[AttackCoords[0]][AttackCoords[1]][1] 
    
        if isinstance(AttackedBuilding, Building) and AttackedBuilding.Alive:
            AttackedBuilding.ReduceHealth(self.Damage,cocMap)


class ArcherQueen(UserTroops):
    def __init__(self,cocMap):
        Damage = 50
        Health = 500
        Speed = 0.2
        Coordinate = [14,1]
        Symbol = 'Q'
        Type = 'Queen'

        self.Range = 8
        self.AttackArea = 5

        super().__init__(Damage, Health, Speed, Coordinate, Symbol, Type)
        GameMap.InitialiseTroop(cocMap,self)

    def setPrev(self, dir):
        self.PrevDir = dir

    def getPrev(self):
        return self.PrevDir

    # Currently, moves only to empty spot. Doesn't move to another troop spot. Need to check for building instead of grass.
    def Move(self, inp, cocMap):
        oldQueenCoords = copy.deepcopy(self.Coordinate)
        if inp == 'A' or inp == 'a':
            if self.Coordinate[1] != 1 and GameMap.isGrass(cocMap,self.Coordinate[0], self.Coordinate[1]-1):
                self.Coordinate[1] -= 1
        elif inp == 'W' or inp == 'w':
            if self.Coordinate[0] != 1 and GameMap.isGrass(cocMap,self.Coordinate[0]-1, self.Coordinate[1]):
                self.Coordinate[0] -= 1
        elif inp == 'D' or inp == 'd':
            if self.Coordinate[1] != GlobalVariables.MapNumColumns-2 and GameMap.isGrass(cocMap,self.Coordinate[0], self.Coordinate[1]+1):
                self.Coordinate[1] += 1
        elif inp == 'S' or inp == 's':
            if self.Coordinate[0] != GlobalVariables.MapNumRows-2 and GameMap.isGrass(cocMap,self.Coordinate[0]+1, self.Coordinate[1]):
                self.Coordinate[0] += 1

        GameMap.UpdateTroopPosition(cocMap, oldQueenCoords, self.Coordinate, self)
        self.setPrev(inp)

    
    def Attack(self, cocMap, AllBuildings):
        Range = self.Range

        attackDir = self.getPrev()
        AttackCoords = copy.deepcopy(self.Coordinate)

        if(attackDir == 'a' or attackDir == 'A'):
            AttackCoords[1] -= Range
        elif (attackDir == 's' or attackDir == 'S'):
            AttackCoords[0] += Range
        elif (attackDir == 'd' or attackDir == 'D'):
            AttackCoords[1] += Range
        elif (attackDir == 'w' or attackDir == 'W'):
            AttackCoords[0] -= Range
        
        AttackTopLeft = copy.deepcopy(AttackCoords)
        AttackTopLeft[0] -= int(self.AttackArea/2)
        AttackTopLeft[1] -= int(self.AttackArea/2)

        AttackBotRight = copy.deepcopy(AttackCoords)
        AttackBotRight[0] += int(self.AttackArea/2)
        AttackBotRight[1] += int(self.AttackArea/2)

        if AttackTopLeft[0] < 0:
            AttackTopLeft[0] = 0
        if AttackTopLeft[1] < 0:
            AttackTopLeft[1] = 0
        if AttackBotRight[0] >= GlobalVariables.MapNumRows:
            AttackBotRight[0] = GlobalVariables.MapNumRows-1
        if AttackBotRight[1] >= GlobalVariables.MapNumColumns:
            AttackBotRight[1] = GlobalVariables.MapNumColumns-1

        for i in range(AttackTopLeft[0],AttackBotRight[0]+1):
            for j in range(AttackTopLeft[1],AttackBotRight[1]+1):
                if cocMap.GameMap[i][j][1] in AllBuildings and cocMap.GameMap[i][j][1].Alive:
                    cocMap.GameMap[i][j][1].ReduceHealth(self.Damage, cocMap)


class Barbarians(UserTroops):
    def __init__(self,cocMap, Coordinate):
        Damage = 50
        Health = 300
        Speed = 0.5
        Symbol = 'B'
        Type = 'Barbarian'

        self.PrevTime = time()

        super().__init__(Damage, Health, Speed, Coordinate, Symbol, Type)
        GameMap.InitialiseTroop(cocMap,self)

    def setPrev(self, dir):
        self.PrevDir = dir

    def getPrev(self):
        return self.PrevDir

    def FindTarget(self, AllBuildings):
        # Search for the nearest building except walls
        minDist = 100
        minObj = None
        for building in AllBuildings:
            if building.Alive and building.Type !='Wall':

                TopLeft = building.TopLeft
                Botright = building.BotRight
                TopRight = (TopLeft[0],TopLeft[1]+1)
                BotLeft = (Botright[0],Botright[1]-1)

                dist = min(GlobalVariables.CalcDist(TopLeft,self.Coordinate), GlobalVariables.CalcDist(TopRight,self.Coordinate), GlobalVariables.CalcDist(Botright,self.Coordinate), GlobalVariables.CalcDist(BotLeft,self.Coordinate))
                if dist < minDist:
                    minDist = dist
                    minObj = building

        self.Target = minObj

        if minObj == None:
            return None

        TopLeft = minObj.TopLeft
        Botright = minObj.BotRight
        TopRight = (TopLeft[0],TopLeft[1]+1)
        BotLeft = (Botright[0],Botright[1]-1)

        if GlobalVariables.CalcDist(TopLeft,self.Coordinate) == minDist:
            return TopLeft
        elif GlobalVariables.CalcDist(Botright,self.Coordinate) == minDist:
            return Botright
        elif GlobalVariables.CalcDist(TopRight,self.Coordinate) == minDist:
            return TopRight
        else: return BotLeft  

    def Attack(self, cocMap):
        attackDir = self.getPrev()
        AttackCoords = copy.deepcopy(self.Coordinate)

        if(attackDir == 'a' or attackDir == 'A'):
            AttackCoords[1] -= 1
        elif (attackDir == 's' or attackDir == 'S'):
            AttackCoords[0] += 1
        elif (attackDir == 'd' or attackDir == 'D'):
            AttackCoords[1] += 1
        elif (attackDir == 'w' or attackDir == 'W'):
            AttackCoords[0] -= 1

        # EntityType = GameMap.GelLabel(cocMap,AttackCoords)
        AttackedBuilding = cocMap.GameMap[AttackCoords[0]][AttackCoords[1]][1] 
    
        if isinstance(AttackedBuilding, Building):
            AttackedBuilding.ReduceHealth(self.Damage,cocMap)

    
    def Move(self, AllBuildings, AllTroops, cocMap):
        # Update target and return the closest corner to the troop.
        TargetCorner = self.FindTarget(AllBuildings)
        if TargetCorner == None:
            return

        OldCoords = copy.deepcopy(self.Coordinate)

        if TargetCorner[1] - self.Coordinate[1] < 0:
            if cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1].Alive:
                # Call Attack Function
                self.PrevDir = 'a'
                self.Attack(cocMap)

            elif cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1].Alive:
                return
            else:
                self.Coordinate[1] -= 1
                self.prev = 'a'
        
        elif TargetCorner[1] - self.Coordinate[1] > 0:
            if cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1].Alive:
                # Call Attack Function
                self.PrevDir = 'd'
                self.Attack(cocMap)

            elif cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1].Alive:
                return
            
            else:
                self.Coordinate[1] += 1
                self.prev = 'd'
        
        else:
            # Now move in the Y direction
            if TargetCorner[0] - self.Coordinate[0] < 0:
                if cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1].Alive:
                    # Call Attack Function
                    self.PrevDir = 'w'
                    self.Attack(cocMap)

                elif cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1].Alive:
                    return
                
                else:
                    self.Coordinate[0] -= 1
                    self.prev = 'w'
            
            elif TargetCorner[0] - self.Coordinate[0] > 0:
                if cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1].Alive:
                    # Call Attack Function
                    self.PrevDir = 's'
                    self.Attack(cocMap)

                elif cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1].Alive:
                    return

                else:
                    self.Coordinate[0] += 1
                    self.prev = 's'
            else:
                # Target reached. Attack Target
                # call attack function
                self.Attack(cocMap)

        GameMap.UpdateTroopPosition(cocMap, OldCoords, self.Coordinate, self)


class Archers(UserTroops):
    def __init__(self,cocMap, Coordinate):
        Damage = 25
        Health = 150
        Speed = 0.3
        Symbol = 'A'
        Type = 'Archer'

        self.PrevTime = time()

        super().__init__(Damage, Health, Speed, Coordinate, Symbol, Type)
        GameMap.InitialiseTroop(cocMap,self)

    def setPrev(self, dir):
        self.PrevDir = dir

    def getPrev(self):
        return self.PrevDir

    def FindTarget(self, AllBuildings):
        # Search for the nearest building except walls
        minDist = 100
        minObj = None
        for building in AllBuildings:
            if building.Alive and building.Type !='Wall':

                TopLeft = building.TopLeft
                Botright = building.BotRight
                TopRight = (TopLeft[0],TopLeft[1]+1)
                BotLeft = (Botright[0],Botright[1]-1)

                dist = min(GlobalVariables.CalcDist(TopLeft,self.Coordinate), GlobalVariables.CalcDist(TopRight,self.Coordinate), GlobalVariables.CalcDist(Botright,self.Coordinate), GlobalVariables.CalcDist(BotLeft,self.Coordinate))
                if dist < minDist:
                    minDist = dist
                    minObj = building

        self.Target = minObj

        if minObj == None:
            return None

        TopLeft = minObj.TopLeft
        Botright = minObj.BotRight
        TopRight = (TopLeft[0],TopLeft[1]+1)
        BotLeft = (Botright[0],Botright[1]-1)

        if GlobalVariables.CalcDist(TopLeft,self.Coordinate) == minDist:
            return TopLeft
        elif GlobalVariables.CalcDist(Botright,self.Coordinate) == minDist:
            return Botright
        elif GlobalVariables.CalcDist(TopRight,self.Coordinate) == minDist:
            return TopRight
        else: return BotLeft

    def Attack(self, cocMap):
        Building.ReduceHealth(self.Target,self.Damage,cocMap)


    # def GroundAttack(self, cocMap):
    #     attackDir = self.getPrev()
    #     AttackCoords = copy.deepcopy(self.Coordinate)

    #     if(attackDir == 'a' or attackDir == 'A'):
    #         AttackCoords[1] -= 1
    #     elif (attackDir == 's' or attackDir == 'S'):
    #         AttackCoords[0] += 1
    #     elif (attackDir == 'd' or attackDir == 'D'):
    #         AttackCoords[1] += 1
    #     elif (attackDir == 'w' or attackDir == 'W'):
    #         AttackCoords[0] -= 1

    #     # EntityType = GameMap.GelLabel(cocMap,AttackCoords)
    #     AttackedBuilding = cocMap.GameMap[AttackCoords[0]][AttackCoords[1]][1] 
    
    #     if isinstance(AttackedBuilding, Building):
    #         AttackedBuilding.ReduceHealth(self.Damage,cocMap)

    
    def Move(self, AllBuildings, AllTroops, cocMap):
        # Update target and return the closest corner to the troop.
        TargetCorner = self.FindTarget(AllBuildings)
        if TargetCorner == None:
            return

        OldCoords = copy.deepcopy(self.Coordinate)

        if GlobalVariables.CalcDist(self.Coordinate,TargetCorner) <= GlobalVariables.ArcherRange:
            # Attack building
            self.Attack(cocMap)
        else:
            # move
            if TargetCorner[1] - self.Coordinate[1] < 0:
                if cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1].Alive:
                    # Call Attack Function
                    self.Target = cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1]
                    self.Attack(cocMap)

                elif cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]-1][1].Alive:
                    return
                else:
                    self.Coordinate[1] -= 1
                    self.prev = 'a'
            
            elif TargetCorner[1] - self.Coordinate[1] > 0:
                if cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1].Alive:
                    # Call Attack Function
                    self.PrevDir = 'd'
                    self.Target = cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1]
                    self.Attack(cocMap)

                elif cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]][self.Coordinate[1]+1][1].Alive:
                    return
                
                else:
                    self.Coordinate[1] += 1
                    self.prev = 'd'
            
            else:
                # Now move in the Y direction
                if TargetCorner[0] - self.Coordinate[0] < 0:
                    if cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1].Alive:
                        # Call Attack Function
                        self.PrevDir = 'w'
                        self.Target = cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1]
                        self.Attack(cocMap)

                    elif cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]-1][self.Coordinate[1]][1].Alive:
                        return
                    
                    else:
                        self.Coordinate[0] -= 1
                        self.prev = 'w'
                
                elif TargetCorner[0] - self.Coordinate[0] > 0:
                    if cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1] in AllBuildings and cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1].Alive:
                        # Call Attack Function
                        self.PrevDir = 's'
                        self.Target = cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1]
                        self.Attack(cocMap)

                    elif cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1] in AllTroops and cocMap.GameMap[self.Coordinate[0]+1][self.Coordinate[1]][1].Alive:
                        return

                    else:
                        self.Coordinate[0] += 1
                        self.prev = 's'
                else:
                    # Target reached. Attack Target
                    # call attack function
                    self.Attack(cocMap)

        GameMap.UpdateTroopPosition(cocMap, OldCoords, self.Coordinate, self)