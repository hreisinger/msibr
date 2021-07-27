#!/usr/bin/python
#
# Generate Serpent
# A script that generates the Serpent input deck for our MSiBR
#
# Calls the deck_writing function for each case we want to run

import deck
import os
import numpy as np
import shutil

# Parameters from the infinite lattice optimization
FSF = .165  # fuel salt fraction
PITCH = 14  # l * 2 from the lattice optimization script
R2 = 4.5
SLIT = 0.323  # TODO: Calculate from relba (only effects to center cell)
RELBA = 0.72  # relative blanket fraction (same as in lattice analysis)
RFUEL = 152.4  # radius of fuel portion of the core
RCORE = 213.36  # outer radius of core vessel
ZCORE = 404
ZREFL = 100
TEMP = 700  # temp in C nominal 700C

cwdStart = os.getcwd()


dirName = "MSIBR_ControlRods"

os.mkdir(dirName)
os.chdir(dirName)

sigFig = 3


blankets = np.linspace(0.7, 0.9, 11)

heights = np.linspace(140, 140, 1)
temperatures = np.linspace(500, 700, 101)
repros = np.array([[False, False, False, False, False, False, False, False, False, False, False],
                   [True, False, False, False, False, False, False, False, False, False, False],
                   [True, True, False, False, False, False, False, False, False, False, False],
                   [True, True, True, False, False, False, False, False, False, False, False],
                   [True, True, True, True, False, False, False, False, False, False, False],
                   [True, True, True, True, True, False, False, False, False, False, False],
                   [True, True, True, True, True, True, False, False, False, False, False],
                   [True, True, True, True, True, True, True, False, False, False, False],
                   [True, True, True, True, True, True, True, True, False, False, False],
                   [True, True, True, True, True, True, True, True, True, False, False],
                   [True, True, True, True, True, True, True, True, True, True, False],
                   [True, True, True, True, True, True, True, True, True, True, True]])


Augs = ['Graphite', 'Fuel', 'Blanket']
tempRange = np.linspace(-100, 100, 5)

tempAugTemplate = {
    'Graphite': TEMP,
    'Fuel': TEMP,
    'Blanket': TEMP,
    'Helium': TEMP,
    'Control Rod': TEMP,
    'Hastelloy': TEMP
}

tempAug = tempAugTemplate

rodLocations = [
    'Center', 'NE', 'SE', 'SW', 'NW'
]
centralRods = {
    'Center': False,
    'NE': False,
    'SE': False,
    'SW': False,
    'NW': False
}
outerRods = {
    'Center': False,
    'NE': False,
    'SE': False,
    'SW': False,
    'NW': False
}


outerChange = [outerRods.copy()]
centralChange= [centralRods.copy()]

for i in range(0, len(rodLocations)):
    location = rodLocations[i]
    centralRods[location] = True
    outerRods[location] = True
    centralChange.append(centralRods.copy())
    outerChange.append(outerRods.copy())



print(centralChange)
print(outerChange)


variable1 = centralChange
variable2 = outerChange


for i in range(0, len(variable1)):
    print(str(np.round(i / len(variable1) * 100, 2)) + "%")
    v1 = variable1[i]

    if True:
        v1 = v1
        print(v1)
        v1Name = 'CR_' + str(np.count_nonzero(list(v1.values())))

        pass
    else:
        v1Name = 'h_' + str(v1)
    os.mkdir(v1Name)
    os.chdir(v1Name)

    for j in range(0, len(variable2)):

        v2 = variable2[j]

        print(v2)
        # tempAug[v1] += v2
        print(tempAug)
        if True:
            v2 = v2
            v2Name = 'OR_' + str(np.count_nonzero(list(v2.values())))
            pass
        else:
            v2Name = 'b_' + str(np.round(v2, 2))

        os.mkdir(v2Name)
        os.chdir(v2Name)

        title = 'MSiBR: {} {}'.format(v1Name, v2Name)

        serp_deck = deck.write_deck(fsf=FSF, relba=RELBA, pitch=PITCH, slit=0.108, temp=700,
                                    rfuel=RFUEL, rcore=RCORE, r2=R2, zcore=140, refl_ht=ZREFL,
                                    name=title, BlanketFraction=0.8,
                                    repro=False, controlRods=[v1, v2])


        # tempAug[v1] -= v2

        FILENAME = 'MSiBR.inp'
        with open(FILENAME, 'w') as f:
            f.write(serp_deck)

        os.chdir('..')
    os.chdir('..')
os.chdir(cwdStart)
shutil.copy('{}\{}'.format(cwdStart, 'runAll.py'), '{}\{}'.format(cwdStart, dirName))
