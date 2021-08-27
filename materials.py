#!/usr/bin/env python3
#
# Materials: Writes the material cards for the Serpent input deck.


def libraries(temp):
	lib = None
	scat_lib = None

	if 300 <= temp < 600:
		lib = '03c'
	elif 600 <= temp < 900:
		lib = '06c'
	elif 900 <= temp < 1200:
		lib = '09c'
	elif 1200 <= temp < 1500:
		lib = '12c'

	# set thermal scattering libraries
	if temp == 400:
		scat_lib = 'gre7.14t'
	elif 400 < temp < 600:
		scat_lib = 'gre7.14t gre7.16t'
	elif temp == 600:
		scat_lib = 'gre7.16t'
	elif 600 < temp < 800:
		scat_lib = 'gre7.16t gre7.18t'
	elif temp == 800:
		scat_lib = 'gre7.18t'
	elif 800 < temp < 1000:
		scat_lib = 'gre7.18t gre7.20t'
	elif temp == 1000:
		scat_lib = 'gre7.20t'
	elif 1000 < temp < 1200:
		scat_lib = 'gre7.20t gre7.22t'
	elif temp == 1200:
		scat_lib = 'gre7.22t'
	elif 1200 < temp < 1500:
		scat_lib = 'gre7.22t gre7.24t'

	return lib, scat_lib


def write_materials(temp, repro=False, tempAug=None):
	'''Function to write material cards for Serpent input deck.
Inputs: these are old
	temp: core temperature
	lib:    String containing the neutron cross section library to use.
	scat_lib : thermal scattering library
Outputs:
	mats:    String containing the material cards'''

	if tempAug is None or tempAug is False:
		tempA = temp

		tempG = tempA + 273
		tempF = tempA + 273
		tempB = tempA + 273
		tempHe = tempA + 273
		tempCr = tempA + 273
		tempHa = tempA + 273

	else:
		tempG = tempAug['Graphite'] + 273
		tempF = tempAug['Fuel'] + 273
		tempB = tempAug['Blanket'] + 273
		tempHe = tempAug['Helium'] + 273
		tempCr = tempAug['Control Rod'] + 273
		tempHa = tempAug['Hastelloy'] + 273

	# change density of major components to match temperature (reference DMSR project) 973K nominal
	gr_dens = 1.82 / ((1. + (tempG - 973) * 4.14 * 10 ** (-6)) ** 3)
	fuel_dens = 2.03434 - (tempF - 973) * 1 * 10 ** (-3)
	blanket_dens = 4.43711 - (tempB - 973) * 1 * 10 ** (-3)
	# he_dens = (0.0000000000076562 * tempHe ** 6 + 0.0000000082650156 * tempHe ** 5 + 0.0000037029146623 * tempHe ** 4 + 0.0008803961010451 * tempHe ** 3 + 0.117098764605052 * tempHe ** 2 + 8.2559972443504 * tempHe + 241.217497540577) / 1000


	### TODO Add other 3 dens

	# set neutron cross section library
	libG, scat_libG = libraries(tempG)
	libF, scat_libF = libraries(tempF)
	libB, scat_libB = libraries(tempB)
	libHe, scat_libHe = libraries(tempHe)
	libCr, scat_libCr = libraries(tempCr)
	libHa, scat_libHa = libraries(tempHa)

	if repro is not False:
		burnVol = '''burn 1 vol 1e6'''
	else:
		burnVol = ''''''

	mats = f'''
%-------material definition--------------
%NOTE: VOLUMES OR MASS OF EACH MAY NEED TO 
%BE CALCULATED FOR BURNUP CALCULATIONS

%  FUEL SALT: 68.5-31.3-0.2 LiF-BeF2-UF4 at 900K 
%  DENSITY: 2.03434 g/cc
%  MELT TEMP: 450C or 742.15K
%  MATERIAL INFO FROM ONRL-4528 TALBE 3.1.
%  MAY NEED VOLUME OR MASS FOR BURNUP CALCULATIONS
mat fuel -{fuel_dens}  tmp {tempF} {burnVol}
rgb 130 32 144
3006.{libF}   -0.000725     %  Li6
3007.{libF}  -14.495960     %  Li7
4009.{libF}  -8.508748     %  Be9
9019.{libF}  -75.588074     %  F19
92233.{libF}  -1.265844     %  U233
92234.{libF}  -0.140649     %  U234

%  BLANKET SALT: 71-27-2 LiF-ThF4-BeF2 at 900K
%  DENSITY: 4.43711 g/cc
%  MELT TEMP: 560C or 833.15K
%  MATERIAL INFO FROM ONRL-4528 TALBE 3.1.
%  MAY NEED VOLUME OR MASS FOR BURNUP CALCULATIONS
mat blanket -{blanket_dens} tmp {tempB} {burnVol}
rgb 0 157 254 
3006.{libB}   -0.000243     %  Li6
3007.{libB}   -4.855845     %  Li7
4009.{libB}  -0.175712     %  Be9
9019.{libB}  -33.892970     %  F19
90232.{libB} -61.052512     %  Th232
91233.{libB}  -0.022718     %  Pa233

%  NUCLEAR GRAPHITE: Natural concentration of carbon
%  DENSITY: 1.82 G/CC
mat graphite -{gr_dens} moder graph 6000 tmp {tempG}
rgb 130 130 130
6000.{libG} 1
%  THERMAL SCATTERING LIBRARY FOR GRAPHITE
therm graph {tempG} {scat_libG}

%  HELIUM: gas due to alpha particles
%  DENSITY: 54.19 E-6 g/cc
mat he -54.19E-6 tmp {tempHe}
rgb 255 0 0
2004.{libHe} 1

% CONTROL ROD: NATURAL BORON at 900K
% DENSITY: 2.3 g/cc
% MELT TEMP: 2076C or 2349.15K
% 19.9 B10 and 80.1 B11
mat absorber -2.3 tmp {tempCr}
rgb 74 74 74
5010.{libCr} -0.199
5011.{libCr} -0.801

%  TODO: Hastelloy
mat hastelloy -8.86 tmp {tempHa}
rgb 139 69 19
28058.{libHa}  -0.472120   %  Ni
 28060.{libHa}  -0.181860   %  Ni
 28061.{libHa}  -0.007905   %  Ni
 28062.{libHa}  -0.025206   %  Ni
 28064.{libHa}  -0.006419   %  Ni
 42100.{libHa}  -0.015408   %  Mo
 42092.{libHa}  -0.023744   %  Mo
 42094.{libHa}  -0.014800   %  Mo
 42095.{libHa}  -0.025472   %  Mo
 42096.{libHa}  -0.026688   %  Mo
 42097.{libHa}  -0.015280   %  Mo
 42098.{libHa}  -0.038608   %  Mo
 24050.{libHa}  -0.003041   %  Cr
 24052.{libHa}  -0.058652   %  Cr
 24053.{libHa}  -0.006651   %  Cr
 24054.{libHa}  -0.001656   %  Cr
 26054.{libHa}  -0.002923   %  Fe
 26056.{libHa}  -0.045877   %  Fe
 26057.{libHa}  -0.001059   %  Fe
 26058.{libHa}  -0.000141   %  Fe
 14028.{libHa}  -0.009223   %  Si
 14029.{libHa}  -0.000468   %  Si
 14030.{libHa}  -0.000309   %  Si
 25055.{libHa}  -0.008000   %  Mn
 74182.{libHa}  -0.001325   %  W
 74183.{libHa}  -0.000715   %  W
 74184.{libHa}  -0.001532   %  W
 74186.{libHa}  -0.001422   %  W
 29063.{libHa}  -0.002421   %  Cu
 29065.{libHa}  -0.001079   %  Cu
'''
	mats = mats.format(**locals())

	return mats


if __name__ == '__main__':
	print("This is a module to write materials for the MSR core.")
	input("Press Ctrl+C to quit, or enter else to test it. ")
	print(write_materials())
