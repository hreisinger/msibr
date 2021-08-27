import os
import matplotlib.pyplot as plt
import numpy as np
import serpentTools as st

exceptions = ['runAll.py', 'readAllRepro.py', 'keff.png', 'conversion.png']

cwdStart = os.getcwd()
folders1 = os.listdir(cwdStart)
folders1 = [x for x in folders1 if x not in exceptions]
v1Order = np.array([])

os.chdir('{}/{}'.format(cwdStart, folders1[0]))
cwd = os.getcwd()
folders2 = os.listdir(cwd)
folders2 = [x for x in folders2 if x not in exceptions]

f1Len = len(folders1)
f2Len = len(folders2)

os.chdir(cwdStart)

keffArray = np.zeros((37, f2Len))
kErrorArray = np.zeros((37, f2Len))
conversionArray = np.zeros((37, f2Len))

for i in range(0, len(folders1)):
    f1 = folders1[i]
    v1Order = np.append(v1Order, f1)
    pDone = '{} {} %'.format(f1, np.round(i / f1Len * 100, 1))
    print("\u0332".join(pDone))

    dest1 = '{}/{}'.format(cwdStart, f1)
    os.chdir(dest1)

    cwd = os.getcwd()
    folders2 = os.listdir(cwd)
    folders2 = [x for x in folders2 if x not in exceptions]
    folders2 = []
    numRange = np.arange(0, 12)
    for i in range(0, len(numRange)):
        folders2.append('r_{}'.format(numRange[i]))
    v2Order = np.array([])

    for j in range(0, len(folders2)):
        f2 = folders2[j]
        v2Order = np.append(v2Order, f2)
        print(' ➞ {}'.format(f2))

        dest2 = '{}/{}'.format(dest1, f2)
        os.chdir(dest2)

        cwd = os.getcwd()
        files = os.listdir(cwd)

        for file in files:
            if file.endswith('res.m'):
                res = st.read(file)
                keff = np.array(res.resdata['anaKeff'])[:, 0]
                keffError = np.array(res.resdata['anaKeff'])[:, 1]
                conversion = np.array(res.resdata['conversionRatio'])[:, 0]

                keffArray[:, j] = keff
                kErrorArray[:, j] = keffError
                conversionArray[:, j] = conversion

print(keffArray)

os.chdir(cwdStart)
deltas =[
.05, .05, .1, .2, .2, .2, .2,
.2,.2, .2, .2, .2,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
.5, .5,
]

xSpace = np.zeros(len(deltas)+1)
for i in range(0, len(deltas)):
    xSpace[i+1] = sum(deltas[0:i+1])

print(xSpace)

labelsList = [
    [' 0: No Reprocessing', 'black'],
    ['1: Th -> Blanket', 'saddlebrown'],
    ['2: Fuel -> U', 'forestgreen'],
    ['3: Rem Blanket Gasses', 'steelblue'],
    ['4: Rem Fuel Gasses', 'indigo'],
    ['5: Rem Blanket Noble Metals', 'darkorange'],
    ['6: Rem Fuel Noble Metals', 'gold'],
    ['7: Rem Blanket Lanth', 'lime'],
    ['8: Rem Fuel Lanth', 'aqua'],
    ['9: Rem Blanket Alk & Hal', 'blue'],
    ['10: Rem Fuel Alk & Hal', 'hotpink'],
    ['11: All', 'red']
]
f = plt.figure()

for i in range(0, len(keffArray[0])):
    lbl = str(labelsList[i][0])
    clr = labelsList[i][1]
    print(lbl)
    print(keffArray[:,i])
    plt.plot(xSpace, keffArray[:, i], label=lbl, color=clr)
plt.legend( bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid()
# plt.title('k-eff')
plt.xlim([0, 14])
plt.xlabel('Time [Days]')
plt.ylabel(r'k$_{eff}$')
f.savefig('keff.png', bbox_inches='tight')
f.show()


f = plt.figure()
f.set_figwidth(7)
for i in range(0, len(keffArray[0])):
    lbl = str(labelsList[i][0])
    clr = labelsList[i][1]
    print(lbl)
    plt.plot(xSpace, conversionArray[:, i], label=lbl, color=clr)
plt.legend( bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid()
# plt.title('k-eff')
plt.xlim([0, 14])
plt.xlabel('Time [Days]')
plt.ylabel('Conversion Ratio')
plt.savefig('conversion.png', bbox_inches='tight')
plt.show()
