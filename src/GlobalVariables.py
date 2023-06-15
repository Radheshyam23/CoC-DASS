MapNumRows = 20
# MapNumRows = 17
MapNumColumns = 60

KingSpeed = 0.2

CannonSpeed = 1
CannonRange = 7
CannonDamage = 100

WizardSpeed = 1
WizardRange = 7
WizardDamage = 100
WizardArea = 3

ArcherRange = 6

AutoTroops = ["Barbarian", "Archers"]

AutoTroopSpeed = {
    'Barbarian' : 0.6,
    'Archer' : 0.3
}

# returns distance between two points
def CalcDist(a,b):
    x1 = a[0]
    x2 = b[0]
    y1 = a[1]
    y2 = b[1]

    return ((x2-x1)**2 + (y2-y1)**2)**0.5

BarbSpawn = {
    'I':[3,8],
    'O':[12,15],
    'P':[13,47],
    'J':[3,8],
    'K':[12,15],
    'L':[13,47]
}