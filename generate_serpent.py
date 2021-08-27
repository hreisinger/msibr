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
SLIT = 0.108
RELBA = 0.72  # relative blanket fraction (same as in lattice analysis)
RFUEL = 152.4  # radius of fuel portion of the core
RCORE = 213.36  # outer radius of core vessel
ZCORE = 140
ZREFL = 100
TEMP = 700  # temp in C nominal 700C
BLANKETFRAC = 0.8  # Fraction of blanket to fuel can be converted to slit width with calculateSlit.py

cwdStart = os.getcwd()

dirName = "MSIBR_NominalPlots"  # Name of the main folder everything will be put into
os.mkdir(dirName)  # Creates new run directory
os.chdir(dirName)  # Enters new run directory

'''
Start of input parameter examples
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

# Creates a copy not a pointer of the template
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

'''
End of input parameter examples
Start of main loop
'''

# Begins looping through variable1
for i in range(0, len(variable1)):
    print(str(np.round(i / len(variable1) * 100, 2)) + "%")  # User feedback for current %

    v1 = variable1[i]  # Current element in variable 1
    #  Name for current folder is made. A new prefix or a custom denoter can replace this
    v1Name = 'h_' + str(v1)
    # v1Name = 'CR_' + str(np.count_nonzero(list(v1.values())))
    # This second definition is useful if v1 is a list or dict (Reprocessing or Control Rods)

    os.mkdir(v1Name)  # Makes the directory v1Name
    os.chdir(v1Name)  # Enters the directory v1Name

    #  Begin looping through variable2
    for j in range(0, len(variable2)):
        v2 = variable2[j]  # Current element in variable 2

        # tempAug[v1] += v2
        # Example of temperature augmentation from variable1=Augs and variable2=tempRange

        #  Name for current folder is made. A new prefix or a custom denoter can replace this
        v2Name = 'b_' + str(np.round(v2, 2))
        #  v2Name = 'OR_' + str(np.count_nonzero(list(v2.values())))
        # This second definition is useful if v1 is a list or dict (Reprocessing or Control Rods)

        os.mkdir(v2Name)  # Makes the directory v2Name
        os.chdir(v2Name)  # Enters the directory v2Name

        title = 'MSiBR: {} {}'.format(v1Name, v2Name)  # title of MSiBR.inp file

        '''
        This function creates a DOS based input deck as a string. With this current setup of this file only 2 variables
        can be run through the function.
            1. Define variable1 and variable2 with your desired parameters
            2. Change the appropriate base nominal parameter(s) with v1 or v2 
        '''
        serp_deck = deck.write_deck(fsf=FSF,                        # Fuel salt fraction
                                    relba=RELBA,                    # Relative blanket fraction
                                    pitch=PITCH,                    # Lattice pitch
                                    slit=SLIT,                      # Slit
                                    temp=TEMP,                      # Current default temperature
                                                                    # ↳ variable=temperatures
                                    rfuel=RFUEL,                    # Radius of fuel portion of the core
                                    rcore=RCORE,                    # Outer radius of core vessel
                                    r2=R2,                          # R2
                                    zcore=ZCORE,                    # Height of the central core
                                                                    # ↳ variable=heights
                                    refl_ht=ZREFL,                  # Height of the reflector
                                    name=title,                     # title of MSiBR.inp file
                                    BlanketFraction=BLANKETFRAC,    # Blanket to Fuel Fraction
                                                                    # ↳ variable=blankets
                                    repro=False,                    # Reprocessing conditions
                                                                    # ↳ variable=repros
                                    controlRods=False,              # Control rod conditions
                                                                    # ↳ variable=False,True,[centralRods,outerRods]
                                    tempAug=False)                  # Temperature augmentation conditions
                                                                    # ↳ variable=False,True,tempAug

        # tempAug[v1] -= v2
        # If tempAug Example is done, this is necessary to bring tempAug back to template temperatures

        FILENAME = 'MSiBR.inp'  # Defining the input file name of all the input files
        # Writes input files
        with open(FILENAME, 'w') as f:
            f.write(serp_deck)

        os.chdir('..')  # moves back to the main variable 2 directory
    os.chdir('..')  # moves back to the main variable 1 directory
os.chdir(cwdStart)  # moves back to the main directory

# copies a useful run script to the main directory. runAll.py works in a Linux environment
shutil.copy('{}\{}'.format(cwdStart, 'runAll.py'), '{}\{}'.format(cwdStart, dirName))

