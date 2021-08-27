"""
This file converts the variable BLANKETFRAC to the slit width between graphite hexagons
"""

import numpy as np
import math

bfArray = np.array([0.8])  # Define input blanket fractions
temp = 700  # define current temperature
hpitch = 14/2  # define half-pitch
hexarea = 2.0 * math.sqrt(3.0) * hpitch ** 2  # define hexagonal area
fsf = .165  # defines fuel salt fraction
r1 = math.sqrt(hexarea * fsf / (2.0 * math.pi))
relba = 0.72  # defines relative blanket fraction
gr_exp = 4.14 * 10 ** (-6)
for i in range(0, len(bfArray)):
    hexs = hpitch  # radius of cell, outside slit
    blanketfraction = bfArray[i]
    blanketA0 = blanketfraction * r1 ** 2 * math.pi
    blanketarea = blanketA0 * relba
    l2 = math.sqrt(hpitch ** 2 - blanketarea / (2.0 * math.sqrt(3.0)))
    hexg = l2 + (temp - 700.0) * gr_exp * l2  # radius of graphite, inside slit with thermal expansion 700C nominal temp

    print(2*(hexs - hexg))  # prints output slit width
