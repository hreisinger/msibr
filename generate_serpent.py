#!/usr/bin/python
#
# Generate Serpent
# A script that generates the Serpent input deck for our MSiBR
#
# Calls the deck_writing function for each case we want to run

import deck
import os
import numpy as np

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

# Job submission settings: currently not in use
FILENAME = "msibr_2.inp"
qsubtemplate = 'qsubtemplate.txt'
nperjob = 2  # num nodes per job
ncpu = 8  # cpu per job
queue = 'gen5'

'''#now the qsub text is constructed.
qtext=[]
with open(qsubtemplate, 'r') as temp:
    text=temp.read()
    for line in text:
       qtext.append(line.format(**locals())) 
'''
# From .108 cm to .327 cm. NOT ACTIVE
# 73 different slit widths are attempted. NOT ACTIVE
blankets = np.linspace(0.85, .85, 1)
temperatures = np.linspace(500, 700, 101)

dirName = "MSIBR_RUNS12/"
os.mkdir(dirName)
os.chdir(dirName)

i = 0

sigFig = 3

for BlanketFraction in blankets:
    # create the directory
    # go into the directory to run this lattice in

    bName = str(np.round(BlanketFraction, sigFig))
    bName = bName.ljust(sigFig+2, '0')
    slitName = 'blanketFraction_' + str(bName) + '/'
    os.mkdir(slitName)
    os.chdir(slitName)
    i += 1
    print(str(np.round(i / len(blankets) * 100, 2)) + "%", bName)
    for t in temperatures:
        hName = str(np.round(t, sigFig))
        hName = hName.ljust(sigFig + 2, '0')
        title = "MSiBR: bFrac = " + str(bName) + ', Temp =' + str(hName)

        # Make the deck
        serp_deck = deck.write_deck(fsf=FSF, relba=RELBA, pitch=PITCH, slit=0.108, temp=t,
                                    rfuel=RFUEL, rcore=RCORE, r2=R2, zcore=150, refl_ht=ZREFL,
                                    name=title, BlanketFraction=.85)

        FILENAME = "msibr_{bName}_{hName}.inp".format(**locals())

        # now write out the input file.
        with open(FILENAME, 'w') as f:
            f.write(serp_deck)

        # place a qsub script with a descriptive name here.
    #    with open('{}.sh'.format(dirname),'w') as f:
    #        f.write(qtext)

    # and finally, submit the job.
    # os.system('qsub {}'.format(FILENAME+'.sh'))

    # and now return to the original directory.
    os.chdir('..')
