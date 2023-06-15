# import time
from time import time
from src.GameMap import GameMap
from src.building import Building, Cannon, TownHall, Wall, Hut, WizardTower
from src.troop import Archers, King, ArcherQueen, Barbarians
import os
from src.input import input_to
from src import GlobalVariables
import copy

cocMap = GameMap()

AllBuildings = []

Walls = []
for i in range(25,54):
    Walls.append(Wall((1,i),cocMap))
    Walls.append(Wall((11,i),cocMap))

for i in range(2,11):
    Walls.append(Wall((i,25),cocMap))
    Walls.append(Wall((i,53),cocMap))

Huts = [Hut((3,35),(3,36),cocMap), Hut((2,40),(2,41),cocMap), Hut((4,48),(4,49),cocMap), Hut((7,33),(7,34),cocMap), Hut((9,48),(9,49),cocMap)]

Towns = [TownHall((4,40),(7,42), cocMap)]

Cannons = [Cannon((2,29),(3,30),cocMap),Cannon((9,36),(10,37),cocMap), Cannon((6,45),(7,46),cocMap)]
# Cannons = []
WizardTowers = [WizardTower((6,26),(7,27),cocMap), WizardTower((3,43),(4,44),cocMap)]

AllBuildings.extend(Walls)
AllBuildings.extend(Towns)
AllBuildings.extend(Huts)
AllBuildings.extend(Cannons)
AllBuildings.extend(WizardTowers)

print("Choose your role: (enter number): \n")
print("1. King")
print("2. Archer Queen")

role = int(input())

if role == 1:
    LeadRole = King(cocMap)
elif role == 2:
    LeadRole = ArcherQueen(cocMap)
else:
    print("Invalid input. Exiting...")
    exit()

BarbList = []
ArcherList = []
AllTroops = []
AllTroops.append(LeadRole)

# prevKingTime = time()
# prevCannonTime = time()

prevRunTime = time()

while 1:
    i = input_to()
    while time() - prevRunTime < 0.1:
        retVal = input_to()
        if retVal != None:
            i = retVal
    prevRunTime = time()

    # Attack of Cannons:
    for cannon in list(Cannons):
        '''
            Cannon attacks.
            Check if there is already a troop being targeted.
            If yes, check if that troop is still in range. If yes, attack troop and reduce health of troop.
            If no, search for nearest troop and set as target. Attack target and reduce health.
        '''


        '''
            Check if there is a target.
                If yes, check if it is in range.
                    If yes, attack
                    If no, check for new target (it will be in range)
                        if yes, attack
                        If none, continue
                If no, check for new target (it will be in range)
                    if yes, attack
                    if none, continue
        '''

        if cannon.Alive == False:
            Cannons.remove(cannon)
            continue

        prevCannonTime = cannon.CannonPrevTime

        if (time() - prevCannonTime) >= GlobalVariables.CannonSpeed:
            if cannon.Target == "":
                #Find a target
                cannon.FindTarget(AllTroops)

            else:
                if cannon.InCannonRange(cannon.Target.Coordinate) == False or cannon.Target.Alive == False:
                    cannon.Target = ""
                    cannon.FindTarget(AllTroops)
            
            TargetObj = cannon.Target               # Troop object

            if TargetObj == "":
                # No troops in the range
                continue

            else:
                # attack troop
                cannon.AttackTarget(TargetObj, cocMap)
                cannon.CannonPrevTime = time()


    # Attack of Wizard Tower:
    for tower in list(WizardTowers):
        if tower.Alive == False:
            WizardTowers.remove(tower)
            continue

        prevWizardTime = tower.WizardPrevTime

        if (time() - prevWizardTime) >= GlobalVariables.CannonSpeed:
            if tower.Target == "":
                #Find a target
                tower.FindTarget(AllTroops)

            else:
                if tower.InWizardRange(tower.Target.Coordinate) == False or tower.Target.Alive == False:
                    tower.Target = ""
                    tower.FindTarget(AllTroops)
            
            TargetObj = tower.Target               # Troop object

            if TargetObj == "":
                # No troops in the range
                continue

            else:
                # attack troop
                tower.AreaAttackTarget(TargetObj, cocMap, AllTroops)
                tower.WizardPrevTime = time()      

    # Automated Troops (Barbarians, Archers) Turn:
    for troop in AllTroops:
        if troop.Type not in GlobalVariables.AutoTroops or troop.Alive == False:
            continue

        PrevTime = troop.PrevTime

        if (time() - PrevTime) >= GlobalVariables.AutoTroopSpeed[troop.Type]:
            # Move
            troop.Move(AllBuildings,AllTroops, cocMap)
            troop.PrevTime = time()

    if i == 'q':
        break

    elif i == ' ' and LeadRole.Alive == True:
        if (time() - LeadRole.PrevMoveTime) >= LeadRole.Speed:
            if LeadRole.Type == "King":
                LeadRole.Attack(cocMap)
            else:
                LeadRole.Attack(cocMap,AllBuildings)
            LeadRole.PrevMoveTime = time()
    elif i in {'a','s','d','w','A','S','D','W'} and LeadRole.Alive == True:
        if (time() - LeadRole.PrevMoveTime) >= LeadRole.Speed:
            LeadRole.Move(i,cocMap)
            LeadRole.PrevMoveTime = time()

    elif i in {'i','o','p','I','O','P'}:
        # Initialise the barbarian
        BarbList.append(Barbarians(cocMap,copy.deepcopy(GlobalVariables.BarbSpawn[i.upper()])))
        AllTroops.append(BarbList[-1])

    elif i in {'j', 'k', 'l', 'J', 'K', 'L'}:
        ArcherList.append(Archers(cocMap,copy.deepcopy(GlobalVariables.BarbSpawn[i.upper()])))
        AllTroops.append(ArcherList[-1])

    if os.name == 'nt':     # for windows
        os.system('cls')
    elif os.name == 'posix':    #for linux/mac
        os.system('clear')

    
    cocMap.DispMap()
    
    if Building.TotCount == 0:
        if os.name == 'nt':     # for windows
            os.system('cls')
        elif os.name == 'posix':    #for linux/mac
            os.system('clear')
        print("VICTORY!!! \nYou have looted the village!")
        break
    
    for troop in list(AllTroops):
        if troop.Alive == False:
            AllTroops.remove(troop)
    
    if len(AllTroops) == 0:
        if os.name == 'nt':     # for windows
            os.system('cls')
        elif os.name == 'posix':    #for linux/mac
            os.system('clear')
        print("DEFEAT!!! \nAll troops have been killed :(")
        break