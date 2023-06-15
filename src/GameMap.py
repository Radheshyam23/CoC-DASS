from colorama import init, Fore, Back, Style
import copy
from src import GlobalVariables

'''
NOTE: We are using matrix/array indexing. NOT cartesian based indexing!!!
'''

init()

class GameMap:
    def __init__(self) -> None:
        self.cols = GlobalVariables.MapNumColumns
        self.rows = GlobalVariables.MapNumRows
        self.GameMap = []
        
        row = [["|", "Boundary"]]
        for j in range(self.cols-2):
            row.append([' ', "Grass"])
        row.append(["|", "Boundary"])

        row0 = [['-', "Boundary"] for i in range(self.cols)]
        self.GameMap.append(copy.deepcopy(row0))    # Deepcopy creates new copy of the elements too.

        for i in range(self.rows-2):
            self.GameMap.append(copy.deepcopy(row))                        
        
        self.GameMap.append(copy.deepcopy(row0))

        # HealthBar = ["|"]
        # HealthBar.append("King Health: ")
        # 14
        # for i in range(self.cols-15):
        #     HealthBar.append(" ")
        # HealthBar.append("|")

        # self.GameMap.append(copy.deepcopy(HealthBar))
        
        # Need to add health display functionality
        # Need to add num troop bar
        # Need to add Num Buildings baer 


    def RetSize(self):
        return [self.rows,self.cols]

    def DispMap(self):
        for i in self.GameMap:
            for j in i:
                if j[1] == 'Grass':
                    print(Back.GREEN+j[0],end='')
                elif j[1] == 'Boundary':
                    print(Back.BLACK+Fore.GREEN+j[0], end='')
                else:
                    print(getattr(Back,j[1].BackColour)+getattr(Fore,j[1].ForeColour)+j[0],end='')
                # elif j[1] == 'King':
                #     print(getattr(Back,GlobalVariables.ColourCode['King']["Back"])+getattr(Fore,GlobalVariables.ColourCode['King']["Fore"])+j[0], end='')
                # elif j[1] == "T":
                #     print(getattr(Back,GlobalVariables.ColourCode['T'][1])+getattr(Fore,GlobalVariables.ColourCode['T'][0])+j[0], end = '')                    
                # else:
                #     print(getattr(Back,GlobalVariables.ColourCode[j[1][0]][int(j[1][1:])][1])+getattr(Fore,GlobalVariables.ColourCode[j[1][0]][int(j[1][1:])][0])+j[0], end = '')
            print(Style.RESET_ALL)


    def AddBuildings(self, BuildingObj):
        TopLeft = BuildingObj.TopLeft
        BotRight = BuildingObj.BotRight

        for i in range (TopLeft[0],BotRight[0]+1):
            for j in range(TopLeft[1], BotRight[1]+1):
                if self.GameMap[i][j][1] == 'Grass':
                    self.GameMap[i][j][0] = BuildingObj.Symbol
                    self.GameMap[i][j][1] = BuildingObj

                else:
                    print('Error: Occupied')
                    return  # Error!! Building already exists there!


    def InitialiseTroop(self,TroopObj):
        # self.KingCoords = Coordinate
        # self.GameMap[self.KingCoords[0]][self.KingCoords[1]][0] = Symbol
        # self.GameMap[self.KingCoords[0]][self.KingCoords[1]][1] = Label
        self.GameMap[TroopObj.Coordinate[0]][TroopObj.Coordinate[1]][0] = TroopObj.Symbol
        self.GameMap[TroopObj.Coordinate[0]][TroopObj.Coordinate[1]][1] = TroopObj

    def isGrass(self, X, Y):
        if self.GameMap[X][Y][1] == "Grass":
            return True
        else: 
            return False

    # Currently, it only allows movement to empty spots. Hence, if there are many troops in a spot, they will all get erased!!
    # Need to implement an array or something. GameMap[][][0] should have an array of symbols, so if one troop moves out, another symbol is displayed.
    # GameMap[][][1] should have an array of objects.
    def UpdateTroopPosition(self, OldCoord, NewCoord, TroopObj):
        self.GameMap[OldCoord[0]][OldCoord[1]][0] = ' '
        self.GameMap[OldCoord[0]][OldCoord[1]][1] = 'Grass'

        self.GameMap[NewCoord[0]][NewCoord[1]][0] = TroopObj.Symbol
        self.GameMap[NewCoord[0]][NewCoord[1]][1] = TroopObj       

    def RemoveBuilding(self, TopLeft, BotRight):
        for i in range (TopLeft[0],BotRight[0]+1):
            for j in range(TopLeft[1], BotRight[1]+1):
                self.GameMap[i][j][0] = ' '
                self.GameMap[i][j][1] = 'Grass'            

    def KillTroop(self, Coordinate):
        self.GameMap[Coordinate[0]][Coordinate[1]][0] = ' '
        self.GameMap[Coordinate[0]][Coordinate[1]][1] = 'Grass'