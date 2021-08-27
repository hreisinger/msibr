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
ZCORE = 140
ZREFL = 100
TEMP = 700  # temp in C nominal 700C

cwdStart = os.getcwd()

dirName = "MSIBR_NominalPlots"  # Name of the main folder everything will be put into
os.mkdir(dirName)
os.chdir(dirName)

sigFig = 3

'''
This is the start of input parameter examples
'''

# Arrays where each element is a new run | deck.write_deck(VariableName)
blankets = np.linspace(0.7, 0.9, 11)  # Blanket to Fuel Fraction  | BlanketFraction
heights = np.linspace(140, 140, 1)  # Height of central core | zcore
temperatures = np.linspace(500, 700, 101)  # Temperature (default control) | temp

# Reprocessing where each True relates to a new reprocessing step. The elements of the np array should be fed in as a
# new run, where the list dictates which reprocessing steps are taking place
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

# Temperature perturbation(augmentation) in specific materials. Changing only the temperature from above
# would be as if changing all of these materials at once
Augs = np.array(['Graphite', 'Fuel', 'Blanket'])  # These are the materials which are affected by the augmentation.
tempRange = np.linspace(-100, 100, 5)  # This is the array which tells by how the temperature changes for each run
# Each element in previous two arrays are related to an independent run or set of runs
# This sets the default temperature of each material in the reactor
tempAugTemplate = {
    'Graphite': TEMP,
    'Fuel': TEMP,
    'Blanket': TEMP,
    'Helium': TEMP,
    'Control Rod': TEMP,
    'Hastelloy': TEMP
}
tempAug = tempAugTemplate  # This variable is the one which gets adjusted when ['material'] from Augs
# is chosen and is then added by the current temperature change defined by the element in tempRange
# Inputting tempAug into deck.write_deck() only requires the one variable each run changes that variable

# Defines the names of the locations of the the control rods
# X  X  X  X  X
# X NW  X  NE X
# X  X  C  X  X
# X SW  X  SE X
# X  X  X  X  X
rodLocations = [
    'Center', 'NE', 'SE', 'SW', 'NW'
]

# Sets the default template out position for the central control rods
centralRods = {
    'Center': False,
    'NE': False,
    'SE': False,
    'SW': False,
    'NW': False
}

# Sets the default template out position for the cluster control rods
outerRods = {
    'Center': False,
    'NE': False,
    'SE': False,
    'SW': False,
    'NW': False
}

# creates a copy not a pointer of the template
outerChange = [outerRods.copy()]
centralChange = [centralRods.copy()]

# Appends sequential dictionaries in the order rodLocation where that element changes to True (rod insertion) and
# stays true
for i in range(0, len(rodLocations)):
    location = rodLocations[i]
    centralRods[location] = True
    outerRods[location] = True
    centralChange.append(centralRods.copy())
    outerChange.append(outerRods.copy())


# This is the place where you hard code the input template. Variable 1 relates to the first set of folders and
# Variable 2 relates to the second set of folders. These should be iterable.
variable1 = [1]
variable2 = [1]

for i in range(0, len(variable1)):
    print(str(np.round(i / len(variable1) * 100, 2)) + "%")
    # v1 is the current element in variable 1
    v1 = variable1[i]
    # This is where the name for current folder is made
    if False:
        v1 = v1
        print(v1)
        # in instances where the input is a list (reprocessing and Control Rods) it is useful just to count the
        # number of Trues as the label for the folder
        v1Name = 'CR_' + str(np.count_nonzero(list(v1.values())))
        pass
    else:
        v1Name = 'h_' + str(v1)
    os.mkdir(v1Name)
    os.chdir(v1Name)

    for j in range(0, len(variable2)):
        # v2 is the current element in variable 2
        v2 = variable2[j]
        print(v2)
        # tempAug[v1] += v2
        print(tempAug)
        if False:
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
                                    repro=False, controlRods=False, tempAug=False)

        # tempAug[v1] -= v2

        FILENAME = 'MSiBR.inp'
        with open(FILENAME, 'w') as f:
            f.write(serp_deck)

        os.chdir('..')  # moves back to the main variable 2 directory
    os.chdir('..')  # moves back to the main variable 1 directory
os.chdir(cwdStart)  # moves back to the main directory

# copies a useful run script to the main directory
shutil.copy('{}\{}'.format(cwdStart, 'runAll.py'), '{}\{}'.format(cwdStart, dirName))

