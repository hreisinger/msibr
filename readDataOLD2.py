import os
import numpy as np
import serpentTools as st

import matplotlib.pyplot as plt



st.verbosity = 'critical'


variableNames = []

cwdStart = os.getcwd()
folders = os.listdir(cwdStart)

print(cwdStart)



fractionOrder = np.array([])

exceptions = ['readData.py', 'run_all.py', 'keffArray.png', 'convArray.png']
folderLength = 0
for j in range(0, len(folders)):
    folderName = folders[j]
    if folderName in exceptions:
        print('pass', folderName)
        pass
    else:
        folderLength += 1
        os.chdir('{}\{}'.format(cwdStart, folderName))
        cwd = os.getcwd()
        files = os.listdir(cwd)
        fileLength = 0
        for i in range(0, len(files)):
            fileName = files[i]
            if fileName[-1] != 'm':
                pass
            else:
                fileLength += 1
        break

os.chdir(cwdStart)

keffArray = np.zeros((len(folders), fileLength))

conversionArray = np.zeros((len(folders), fileLength))


for j in range(0, len(folders)):
    folderName = folders[j]
    if folderName in exceptions:
        print('pass', folderName)
        pass
    else:
        heightOrder = np.array([])
        fractionOrder = np.append(fractionOrder, folderName)
        os.chdir('{}\{}'.format(cwdStart, folderName))
        cwd = os.getcwd()
        files = os.listdir(cwd)
        step = 0
        for i in range(0, len(files)):
            fileName = files[i]
            if fileName[-1] != 'm':
                pass
            else:
                heightOrder = np.append(heightOrder, fileName)
                res = st.readDataFile(fileName)
                keffArray[j,step] = res.resdata['absKeff'][0]
                conversionArray[j,step] = res.resdata['conversionRatio'][0]

                step += 1
        print(j / len(folders) * 100)

print(fractionOrder)
"""
for i in range(0, len(fractionOrder)):
    fractionOrder[i] = fractionOrder[i][5:-1]
"""
print(heightOrder)
for i in range(0, len(heightOrder)):
    heightOrder[i] = heightOrder[i][12:15]



os.chdir(cwdStart)



fractionOrder = fractionOrder.astype(np.float)
heightOrder = heightOrder.astype(np.float)

print(fractionOrder)
print(heightOrder)

X, Y = np.meshgrid(heightOrder, fractionOrder)
Z1 = keffArray[~np.all(keffArray == 0, axis=1)]
Z2 = conversionArray[~np.all(conversionArray == 0, axis=1)]

plt.contourf(X, Y, Z1, 100, cmap='CMRmap')
plt.title('k-eff')
plt.xlabel('height')
plt.ylabel('slit')
plt.colorbar()
plt.savefig('keffArray.png')
plt.show()

plt.contourf(X, Y, Z2, 100, cmap='CMRmap')
plt.title('conversion ratio')
plt.xlabel('height')
plt.ylabel('slit')
plt.colorbar()
plt.savefig('convArray.png')
plt.show()


print(keffArray)
print(conversionArray)