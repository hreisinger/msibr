#!/usr/bin/env python3
#
# Cells: Write the cell cards and universes for the Serpent input deck


def write_cells(universes=range(1, 1 + 12), lattices=range(33, 33 + 7),
                surffuel=30, surfcore=31, surfgref=32, surfhast=29):
    '''Function to write cell cards for Serpent input deck.
	Inputs: these are old
		universes:		Tuple(12) containing the following.
		 ub, uf, uc:	 Universe number of blanket, fuel, central cells
		 uup, ul#:		 Universe number of upper/lower plenum assembly
		 uuc, ulc:		 Universe number of upper/lower control cells
		lattices:		Tuple(7) containing the following:
		 latmid:	 	 Lattice number of the middle fuel cells
		 lattop:		 Lattice number of the top fuel cells
		 latbot#: 		 Lattice number of the bottom fuel cells
		surffuel:		Surface no. of inner core (fuel cells)
		surfcore:		Surface no. of entire core, fuel+blanket
		surfgref:		Surface no. of graphite reflector
	Outputs:
		cells:		String containing cell cards'''

    # Unpack the universe tuple
    ub, uf, uc, uup, \
    ul1, ul2, ul3, ul4, \
    ulp, uuc, ulc, uh, \
    ucNone, ucCentral, ucOuter, ucCentralOuter = universes
    # Unpack the lattice tuple
    latmid, lattop, latbot1, latbot2, latbot3, \
    latbot4, latplen = lattices


    # New cell definitions
    cells = '''
%------define cells--------------------
% Universe {ub}: BLANKET CELL U1
cell 15 {ub} graphite   -101
cell 16 {ub} blanket     101 


% Universe {uf}: FUEL CELL U2
cell 10 {uf} graphite -201 203 205
cell 13 {uf} graphite 203 -204
cell 11 {uf} blanket  -202 201  
cell 12 {uf} void  202 
cell  7 {uf} fuel -203 
cell  1 {uf} fuel 204 -205 
    
    '''

    cells += '''
% Universe {ucNone}: CONTROL ROD U3 
% Similar to fuel cell, but with helium in channels
cell 30 {ucNone} graphite -301 303 316 317 318 319 320 321  
cell 31 {ucNone} blanket  -302 301 
cell 32 {ucNone} blanket -303 331
cell 33 {ucNone} void   302 
cell  34 {ucNone} he -304 
cell  35 {ucNone} he -305 
cell  36 {ucNone} he -306 
cell  37 {ucNone} he -307 
cell  38 {ucNone} he -308 
cell  39 {ucNone} he -309 

cell  40 {ucNone} he 304 -310
cell  41 {ucNone} he 305 -311
cell  42 {ucNone} he 306 -312
cell  43 {ucNone} he 307 -313
cell  44 {ucNone} he 308 -314
cell  45 {ucNone} he 309 -315

cell  46 {ucNone} he 310 -316
cell  47 {ucNone} he 311 -317
cell  48 {ucNone} he 312 -318
cell  49 {ucNone} he 313 -319
cell  50 {ucNone} he 314 -320
cell  51 {ucNone} he 315 -321

cell  52 {ucNone} blanket -330
cell  53 {ucNone} blanket -331 330
'''
    cells += '''
% Universe {ucCentral}: CONTROL ROD U3 
% Similar to fuel cell, but with helium in channels
cell  400 {ucCentral} graphite -301 303 316 317 318 319 320 321  
cell  401 {ucCentral} blanket  -302 301 
cell  402 {ucCentral} blanket -303 331
cell  403 {ucCentral} void   302 
cell  404 {ucCentral} he -304 
cell  405 {ucCentral} he -305 
cell  406 {ucCentral} he -306 
cell  407 {ucCentral} he -307 
cell  408 {ucCentral} he -308 
cell  409 {ucCentral} he -309 

cell  410 {ucCentral} he 304 -310
cell  411 {ucCentral} he 305 -311
cell  412 {ucCentral} he 306 -312
cell  413 {ucCentral} he 307 -313
cell  414 {ucCentral} he 308 -314
cell  415 {ucCentral} he 309 -315

cell  416 {ucCentral} he 310 -316
cell  417 {ucCentral} he 311 -317
cell  418 {ucCentral} he 312 -318
cell  419 {ucCentral} he 313 -319
cell  420 {ucCentral} he 314 -320
cell  421 {ucCentral} he 315 -321

cell  422 {ucCentral} absorber -330
cell  423 {ucCentral} hastelloy -331 330
    '''
    cells += '''
% Universe {ucOuter}: CONTROL ROD U3 
% Similar to fuel cell, but with helium in channels
cell  430 {ucOuter} graphite -301 303 316 317 318 319 320 321  
cell  431 {ucOuter} blanket  -302 301 
cell  432 {ucOuter} blanket -303 331
cell  433 {ucOuter} void   302 
cell  434 {ucOuter} absorber -304 
cell  435 {ucOuter} absorber -305 
cell  436 {ucOuter} absorber -306 
cell  437 {ucOuter} absorber -307 
cell  438 {ucOuter} absorber -308 
cell  439 {ucOuter} absorber -309 

cell  440 {ucOuter} hastelloy 304 -310
cell  441 {ucOuter} hastelloy 305 -311
cell  442 {ucOuter} hastelloy 306 -312
cell  443 {ucOuter} hastelloy 307 -313
cell  444 {ucOuter} hastelloy 308 -314
cell  445 {ucOuter} hastelloy 309 -315

cell  446 {ucOuter} he 310 -316
cell  447 {ucOuter} he 311 -317
cell  448 {ucOuter} he 312 -318
cell  449 {ucOuter} he 313 -319
cell  450 {ucOuter} he 314 -320
cell  451 {ucOuter} he 315 -321

cell  452 {ucOuter} blanket -330
cell  453 {ucOuter} blanket -331 330
    '''
    cells += '''
% Universe {ucCentralOuter}: CONTROL ROD U3 
% Similar to fuel cell, but with helium in channels
cell  460 {ucCentralOuter} graphite -301 303 316 317 318 319 320 321  
cell  461 {ucCentralOuter} blanket  -302 301 
cell  462 {ucCentralOuter} blanket -303 331
cell  463 {ucCentralOuter} void   302 
cell  464 {ucCentralOuter} absorber -304 
cell  465 {ucCentralOuter} absorber -305 
cell  466 {ucCentralOuter} absorber -306 
cell  467 {ucCentralOuter} absorber -307 
cell  468 {ucCentralOuter} absorber -308 
cell  469 {ucCentralOuter} absorber -309 

cell  470 {ucCentralOuter} hastelloy 304 -310
cell  471 {ucCentralOuter} hastelloy 305 -311
cell  472 {ucCentralOuter} hastelloy 306 -312
cell  473 {ucCentralOuter} hastelloy 307 -313
cell  474 {ucCentralOuter} hastelloy 308 -314
cell  475 {ucCentralOuter} hastelloy 309 -315

cell  476 {ucCentralOuter} he 310 -316
cell  477 {ucCentralOuter} he 311 -317
cell  478 {ucCentralOuter} he 312 -318
cell  479 {ucCentralOuter} he 313 -319
cell  480 {ucCentralOuter} he 314 -320
cell  481 {ucCentralOuter} he 315 -321

cell  482 {ucCentralOuter} absorber -330
cell  483 {ucCentralOuter} hastelloy -331 330
    '''
    cells += '''
% Universe {uup}: UPPER CHANNEL U4
cell 503 {uup} fuel     -403  404 -405	    % fuel cap
cell 504 {uup} graphite  403 -401  404 -405	% graphite,level1
cell 505 {uup} graphite -401  405 -406	    % graphite cap,level2
cell 506 {uup} blanket  -402  401  404 -406  % slit all the way through
cell 507 {uup} void      406
cell 508 {uup} void     -404
cell 509 {uup} void      402  404 -406


% Universe {uuc}: UPPER CONTROL U5
cell 61 {uuc} he       -503  504 -505	    % helium gap
cell 62 {uuc} graphite  503 -501  504 -506	% graphite,level1
cell 63 {uuc} graphite -503  505 -506	    % graphite cap,level2
cell 64 {uuc} blanket  -502  501  504 -506  % slit all the way through
cell 65 {uuc} void      506
cell 66 {uuc} void     -504
cell 67 {uuc} void      502  504 -506


% Universe {ulc}: LOWER CONTROL U6
cell 71 {ulc} graphite -602       % Central channel - was he
cell 72 {ulc} graphite -603  602  % Hast. pipe - was hastelelloy
cell 73 {ulc} graphite -604  603  % outer fuel channel - was he
cell 74 {ulc} graphite -605  604  % graphite hex
cell 75 {ulc} blanket  -601  605  % blanket reflector
cell 79 {ulc} void      601 


% Universe 7: Blank Blanket Cell U7
cell 701 7 blanket -701
cell 702 7 blanket 701


% Universe 8: Holding Shafts on top of plate U8
cell 801 8 graphite -801
cell 802 8 blanket  801


% Universe 9: Holding Shafts under plate U9
cell 901 9 graphite -901
cell 902 9 blanket 901


% Universe {ulp}: LOWER PLENUM BOTTOM U10
cell 250 {ulp} fuel -1001
cell 260 {ulp} void  1001


% Universe {uh}: HASTELLOY HEX U11
cell 18 {uh} hastelloy -1101
cell 19 {uh} void       1101


% Universe 12: Holding Plate U12
cell 1201 12 graphite -1201
cell 1202 12 hastelloy 1201

% Universe {ul1}: LOWER CHANNEL 1 U25
cell 351 {ul1} blanket   -2501  2507 
cell 352 {ul1} fuel      -2502        % Central channel
cell 353 {ul1} hastelloy -2503  2502  % Hast. pipe
cell 358 {ul1} graphite  -2505  2503
cell 354 {ul1} fuel      -2506  2505  % outer fuel channel
cell 355 {ul1} graphite  -2507  2506  % graphite hex
cell 359 {ul1} void       2501

% Universe {ul2}: LOWER CHANNEL 2  U26
cell 251 {ul2} blanket   -2601  2605 
cell 252 {ul2} fuel      -2602        % Central channel
cell 253 {ul2} hastelloy -2603  2602  % Hast. pipe
cell 254 {ul2} fuel      -2604  2603  % outer fuel channel
cell 257 {ul2} hastelloy -2605  2604  % outer pipe
cell 259 {ul2} void       2601



% Universe {ul3}: PENENETRATION TO INLET PLENUM U27
cell 261 {ul3} hastelloy -2701  2703
cell 262 {ul3} fuel      -2702        % Central channel
cell 263 {ul3} hastelloy -2704  2702  % Inner pipe
cell 264 {ul3} fuel      -2703  2704  % outer fuel channel
cell 265 {ul3} void       2701


% Universe {ul4}: PENETRATION TO OUTLET PLENUM U28
cell 266 {ul4} hastelloy -2801  2802
cell 267 {ul4} fuel      -2802
cell 268 {ul4} void       2801


% Universe 1111: LOWER PLENUM TOP U1111
cell 2611 1111 fuel      -111101  111103
cell 2621 1111 fuel      -111102          % Central channel
cell 2631 1111 hastelloy -111103  111102  % Inner pipe
cell 2651 1111 void       111101


% The main universe
cell 100 0 fill       {latmid}   -{surfgref} 8 -9
cell 104 0 fill       {lattop}   -{surfgref} 9 -10
cell 105 0 fill       {latbot1}  -{surfgref} 7 -8
cell 106 0 fill       {latbot2}  -{surfgref} 6 -7
cell 107 0 fill       {latbot3}  -{surfgref} 5 -6
cell 108 0 fill   43 -{surffuel}  4 -5
cell 109 0 fill       {latbot4}  -{surffuel} 3 -4
cell 110 0 fill       {latplen}  -{surffuel} 2 -3
cell 111 0 hastelloy -{surfgref}		1 -2
cell 112 0 hastelloy  {surffuel} -{surfgref} 2 -5
cell 113 0 hastelloy  {surfgref} -{surfhast} 1 -15
cell 122 0 hastelloy -{surfhast} 15 -16
cell 123 0 fill   41 -{surfgref} 11 -12 % holding shaft below plate
cell 124 0 fill   42 -{surfgref} 12 -13 % top holding plate
cell 125 0 fill   40 -{surfgref} 13 -14
cell 126 0 blanket -17 14 -15


cell 999 0 outside {surfhast} 1 -16
cell 998 0 outside -1
cell 997 0 outside  16
	'''

    cells = cells.format(**locals())
    return cells


if __name__ == '__main__':
    print("This is a module to write cells for the MSR core.")
    input("Press Ctrl+C to quit, or enter else to test it. ")
    print(write_cells())
