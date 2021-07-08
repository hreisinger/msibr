




def write_init(temp):
    temp += 273
    init_rep = '''
%___________Reprocessing/depletion___________
%stockpile of extra Th
mat Th_stock -11.7 tmp {temp} burn 1 vol 1e6
90232.09c 1.0 % Th-232

%stockpile of extra U
mat U_stock -19.1 tmp {temp} burn 1 vol 1e6
92233.09c 1.0 % U-233

%bucket for Pr and U
mat dumptank 0.0 tmp {temp} burn 1 vol 1e6

%tanks for offgases
mat offgastankcore 0.0 tmp {temp} burn 1 vol 1e6
mat offgastankblanket 0.0 tmp {temp} burn 1 vol 1e6

%tanks for noblemetals
mat noblemetalcore 0.0 tmp {temp} burn 1 vol 1e6
mat noblemetalblanket 0.0 tmp {temp} burn 1 vol 1e6

%tanks for lanthanides
mat lanthtankcore 0.0 tmp {temp} burn 1 vol 1e6
mat lanthtankblanket 0.0 tmp {temp} burn 1 vol 1e6

%tanks for alkines and halogens
mat alkhaltankcore 0.0 tmp {temp} burn 1 vol 1e6
mat alkhaltankblanket 0.0 tmp {temp} burn 1 vol 1e6

%_______mass flow definitions______
mflow thor_in
Th-232 3.5e-10

mflow U_out
U-233 1e-2
Pr-233 1e-2
%this number will depend on the chemical process's rate.
%could possibly be modeled by a rate eqation: https://en.wikipedia.org/wiki/Rate_equation

mflow U_in
U-233 2.7e-10

mflow offgasratecore
Ne 1e-2
Ar 1e-2
He 1e-2
Kr 1e-2
Xe 1e-2
Rn 1e-2

mflow offgasrateblanket
Ne 1e-2
Ar 1e-2
He 1e-2
Kr 1e-2
Xe 1e-2
Rn 1e-2

mflow offnoblecore
Ru 1e-2
Rh 1e-2
Pd 1e-2
Ag 1e-2
Os 1e-2
Ir 1e-2
Pt 1e-2
Au 1e-2
Mo 1e-2 %Refractory metals
Nb 1e-2
Hf 1e-2

mflow offnobleblanket
Ru 1e-2
Rh 1e-2
Pd 1e-2
Ag 1e-2
Os 1e-2
Ir 1e-2
Pt 1e-2
Au 1e-2
Mo 1e-2 %Refractory metals
Nb 1e-2
Hf 1e-2

mflow offlanthcore
La 1e-4
Ce 1e-4
Pr 1e-4
Nd 1e-4
Pm 1e-4
Sm 1e-4
Eu 1e-4
Gd 1e-4
Tb 1e-4
Dy 1e-4
Ho 1e-4
Er 1e-4
Tm 1e-4
Yb 1e-4
Lu 1e-4

mflow offlanthblanket
La 1e-4
Ce 1e-4
Pr 1e-4
Nd 1e-4
Pm 1e-4
Sm 1e-4
Eu 1e-4
Gd 1e-4
Tb 1e-4
Dy 1e-4
Ho 1e-4
Er 1e-4
Tm 1e-4
Yb 1e-4
Lu 1e-4

mflow offalkhalcore
Rb 1e-4
Cs 1e-4
Sr 1e-4
Ba 1e-4
Br 1e-4
I  1e-4

mflow offalkhalblanket
Rb 1e-4
Cs 1e-4
Sr 1e-4
Ba 1e-4
Br 1e-4
I  1e-4

set pcc 0 %predictor-corrector must be turned off to use depletion
set gcu -1 %turning off group constant generation hastens the calculation
set depmtx 1 %dumps depletion matrices if needed. should be one per burnt material.
    '''
    init_rep = init_rep.format(**locals())
    return init_rep

def write_scheme(rep_order):
    scheme = '''
rep the_reprocessing_scheme
rc Th_stock blanket thor_in {rep_order[0]}
%the number one indicates that a removal term appears in the bateman equations for thoriu$
% and a corresponding addition term in the batemans for the blanket salt.
rc U_stock fuel U_in {rep_order[1]}
rc blanket offgastankblanket offgasrateblanket {rep_order[2]}
rc fuel offgastankcore offgasratecore {rep_order[3]}
rc blanket noblemetalblanket offnobleblanket {rep_order[4]}
rc fuel noblemetalcore offnoblecore {rep_order[5]}
rc blanket lanthtankblanket offlanthblanket {rep_order[6]}
rc fuel lanthtankcore offlanthcore {rep_order[7]}
rc blanket alkhaltankblanket offalkhalblanket {rep_order[8]}
rc fuel alkhaltankcore offalkhalcore {rep_order[9]}
rc blanket U_stock U_out {rep_order[10]}
    '''

    scheme = scheme.format(**locals())
    return scheme

def write_daySteps(days=9, interval=18):
    dayStep = '''
dep
pro the_reprocessing_scheme
daystep
'''
    step = days/interval
    placement = 0
    dayStepLine = ''''''
    for i in range(0,interval+1):
        dayStepLine += '''{step} '''
        if len(dayStepLine) > 80:
            dayStepLine += '''
            '''
            dayStep += dayStepLine
            dayStepLine = ''''''
    dayStep += '''
    '''

    dayStep = dayStep.format(**locals())
    return dayStep
